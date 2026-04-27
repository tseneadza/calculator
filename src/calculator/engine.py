import ast
import math
import random


class CalculatorEngine:
    def __init__(self) -> None:
        self.rpn_stack: list[float] = []

    @staticmethod
    def tetration(base: float, height: int) -> float:
        if height != int(height):
            raise ValueError("Tetration height must be an integer.")
        height = int(height)
        if height < 0 or height > 5:
            raise ValueError("Tetration height must be between 0 and 5.")
        if height == 0:
            return 1.0
        result = base
        for _ in range(1, height):
            result = base ** result
            if abs(result) > 1e100:
                raise ValueError("Tetration result too large.")
        return float(result)

    @staticmethod
    def factorial(value: float) -> float:
        if value != int(value) or value < 0:
            raise ValueError("Factorial only supports non-negative integers.")
        return float(math.factorial(int(value)))

    @staticmethod
    def nth_root(value: float, degree: float) -> float:
        if degree == 0:
            raise ValueError("Root degree cannot be zero.")
        return float(value ** (1.0 / degree))

    @staticmethod
    def ee(value: float, exponent: float) -> float:
        return float(value * (10 ** exponent))

    def _make_functions(self, angle_unit: str) -> dict[str, object]:
        unit = angle_unit.upper()

        def angle_input(v: float) -> float:
            return math.radians(v) if unit == "DEG" else v

        return {
            "sin": lambda x: math.sin(angle_input(x)),
            "cos": lambda x: math.cos(angle_input(x)),
            "tan": lambda x: math.tan(angle_input(x)),
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "ln": math.log,
            "log10": math.log10,
            "sqrt": math.sqrt,
            "cbrt": lambda x: math.copysign(abs(x) ** (1.0 / 3.0), x),
            "root": self.nth_root,
            "fact": self.factorial,
            "rand": lambda: random.random(),
            "tetration": self.tetration,
            "ee": self.ee,
            "abs": abs,
            "pow": pow,
        }

    def evaluate(self, expression: str, angle_unit: str = "RAD") -> float:
        functions = self._make_functions(angle_unit)
        constants = {"pi": math.pi, "e": math.e}

        allowed_bin_ops = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod)
        allowed_unary_ops = (ast.UAdd, ast.USub)

        def _eval(node: ast.AST) -> float:
            if isinstance(node, ast.Expression):
                return _eval(node.body)
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return float(node.value)
                raise ValueError("Unsupported constant type.")
            if isinstance(node, ast.BinOp):
                if not isinstance(node.op, allowed_bin_ops):
                    raise ValueError("Unsupported operator.")
                left = _eval(node.left)
                right = _eval(node.right)
                if isinstance(node.op, ast.Add):
                    return left + right
                if isinstance(node.op, ast.Sub):
                    return left - right
                if isinstance(node.op, ast.Mult):
                    return left * right
                if isinstance(node.op, ast.Div):
                    return left / right
                if isinstance(node.op, ast.Pow):
                    return left ** right
                if isinstance(node.op, ast.Mod):
                    return left % right
            if isinstance(node, ast.UnaryOp):
                if not isinstance(node.op, allowed_unary_ops):
                    raise ValueError("Unsupported unary operator.")
                operand = _eval(node.operand)
                return +operand if isinstance(node.op, ast.UAdd) else -operand
            if isinstance(node, ast.Name):
                if node.id in constants:
                    return float(constants[node.id])
                raise ValueError(f"Unknown identifier: {node.id}")
            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name):
                    raise ValueError("Invalid function call.")
                fn_name = node.func.id
                if fn_name not in functions:
                    raise ValueError(f"Unsupported function: {fn_name}")
                fn = functions[fn_name]
                args = [_eval(arg) for arg in node.args]
                return float(fn(*args))
            raise ValueError("Unsupported expression.")

        tree = ast.parse(expression, mode="eval")
        return float(_eval(tree))

    def rpn_push(self, value: float) -> list[float]:
        self.rpn_stack.append(float(value))
        return self.rpn_stack.copy()

    def rpn_clear(self) -> list[float]:
        self.rpn_stack.clear()
        return self.rpn_stack.copy()

    def rpn_drop(self) -> list[float]:
        if self.rpn_stack:
            self.rpn_stack.pop()
        return self.rpn_stack.copy()

    def rpn_swap(self) -> list[float]:
        if len(self.rpn_stack) < 2:
            raise ValueError("Need at least two values to swap.")
        self.rpn_stack[-1], self.rpn_stack[-2] = self.rpn_stack[-2], self.rpn_stack[-1]
        return self.rpn_stack.copy()

    def rpn_binary(self, op: str) -> list[float]:
        if len(self.rpn_stack) < 2:
            raise ValueError("Need at least two values on stack.")
        b = self.rpn_stack.pop()
        a = self.rpn_stack.pop()
        if op == "+":
            r = a + b
        elif op == "-":
            r = a - b
        elif op == "*":
            r = a * b
        elif op == "/":
            r = a / b
        elif op == "^":
            r = a ** b
        else:
            raise ValueError("Unsupported RPN binary operation.")
        self.rpn_stack.append(float(r))
        return self.rpn_stack.copy()

    def rpn_unary(self, op: str, angle_unit: str = "RAD") -> list[float]:
        if not self.rpn_stack:
            raise ValueError("Need at least one value on stack.")
        v = self.rpn_stack.pop()
        unit = angle_unit.upper()
        v_in = math.radians(v) if unit == "DEG" else v

        if op == "sin":
            r = math.sin(v_in)
        elif op == "cos":
            r = math.cos(v_in)
        elif op == "tan":
            r = math.tan(v_in)
        elif op == "sqrt":
            r = math.sqrt(v)
        elif op == "ln":
            r = math.log(v)
        elif op == "log10":
            r = math.log10(v)
        elif op == "fact":
            r = self.factorial(v)
        else:
            raise ValueError("Unsupported RPN unary operation.")

        self.rpn_stack.append(float(r))
        return self.rpn_stack.copy()
