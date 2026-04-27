from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn

from calculator.engine import CalculatorEngine


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Calculator API")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
engine = CalculatorEngine()


class EvaluateRequest(BaseModel):
    expression: str = Field(..., min_length=1)
    angle_unit: str = Field(default="RAD")


class RpnRequest(BaseModel):
    action: str
    value: float | None = None
    op: str | None = None
    angle_unit: str = Field(default="RAD")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/evaluate")
def evaluate(request: EvaluateRequest) -> dict[str, float]:
    try:
        result = engine.evaluate(request.expression, request.angle_unit)
        return {"result": result}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/rpn")
def rpn_action(request: RpnRequest) -> dict[str, list[float]]:
    try:
        action = request.action
        if action == "push":
            if request.value is None:
                raise ValueError("Missing value for push.")
            stack = engine.rpn_push(request.value)
        elif action == "clear":
            stack = engine.rpn_clear()
        elif action == "drop":
            stack = engine.rpn_drop()
        elif action == "swap":
            stack = engine.rpn_swap()
        elif action == "binary":
            if not request.op:
                raise ValueError("Missing op for binary action.")
            stack = engine.rpn_binary(request.op)
        elif action == "unary":
            if not request.op:
                raise ValueError("Missing op for unary action.")
            stack = engine.rpn_unary(request.op, request.angle_unit)
        else:
            raise ValueError("Unknown RPN action.")
        return {"stack": stack}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/rpn")
def get_rpn_stack() -> dict[str, list[float]]:
    return {"stack": engine.rpn_stack.copy()}


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8094, reload=False)
