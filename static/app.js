const display = document.getElementById("display");
const basicLayout = document.getElementById("basicLayout");
const scientificLayout = document.getElementById("scientificLayout");
const basicNumbers = document.getElementById("basicNumbers");
const basicFunctions = document.getElementById("basicFunctions");
const scientificNumbers = document.getElementById("scientificNumbers");
const scientificOps = document.getElementById("scientificOps");
const scientificFunctions = document.getElementById("scientificFunctions");
const rpnPanel = document.getElementById("rpnPanel");
const rpnStackEl = document.getElementById("rpnStack");
const programmablePanel = document.getElementById("programmablePanel");
const conversionsPanel = document.getElementById("conversionsPanel");

const radBtn = document.getElementById("radBtn");
const degBtn = document.getElementById("degBtn");

let expression = "";
let memory = 0;
let angleUnit = "RAD";

const basicNumberButtons = ["7", "8", "9", "4", "5", "6", "1", "2", "3", "0", ".", "="];
const basicFunctionButtons = ["+", "-", "*", "/", "%", "(", ")", "pi", "e", "Rand", "C", "⌫"];
const scientificNumberButtons = ["7", "8", "9", "4", "5", "6", "1", "2", "3", "0", ".", "="];
const scientificOpsButtons = ["+", "-", "*", "/", "%", "(", ")", "pi", "e", "Rand", "C", "⌫"];
const scientificFunctionButtons = [
  "mc",
  "m+",
  "m-",
  "mr",
  "x^2",
  "x^3",
  "x^y",
  "e^x",
  "10^x",
  "1/x",
  "2√x",
  "3√x",
  "y√x",
  "ln",
  "log10",
  "x!",
  "sin",
  "cos",
  "tan",
  "sinh",
  "cosh",
  "tanh",
  "EE",
  "TET",
];

function updateDisplay(text) {
  display.textContent = text || "0";
}

function createButtons(container, labels, onClick) {
  container.innerHTML = "";
  labels.forEach((label) => {
    const button = document.createElement("button");
    button.textContent = label;
    button.addEventListener("click", () => onClick(label));
    container.appendChild(button);
  });
}

function appendToken(token) {
  expression += token;
  updateDisplay(expression);
}

function wrapFn(fnName) {
  expression = `${fnName}(${expression || 0})`;
  updateDisplay(expression);
}

async function evaluate() {
  if (!expression) return;
  const response = await fetch("/api/evaluate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ expression, angle_unit: angleUnit }),
  });
  const data = await response.json();
  if (!response.ok) {
    updateDisplay(`Error: ${data.detail}`);
    return;
  }
  expression = String(data.result);
  updateDisplay(expression);
}

function handleBasic(label) {
  if (label === "C") {
    expression = "";
    updateDisplay("");
    return;
  }
  if (label === "⌫") {
    expression = expression.slice(0, -1);
    updateDisplay(expression);
    return;
  }
  if (label === "=") {
    evaluate();
    return;
  }
  if (label === "pi") return appendToken("pi");
  if (label === "e") return appendToken("e");
  if (label === "Rand") return appendToken("rand()");
  appendToken(label);
}

function handleScientific(label) {
  if (/^[0-9]$/.test(label) || [".", "+", "-", "*", "/", "%", "(", ")"].includes(label)) {
    appendToken(label);
    return;
  }
  if (label === "C") {
    expression = "";
    updateDisplay("");
    return;
  }
  if (label === "⌫") {
    expression = expression.slice(0, -1);
    updateDisplay(expression);
    return;
  }
  if (label === "=") {
    evaluate();
    return;
  }
  if (label === "pi") {
    appendToken("pi");
    return;
  }
  if (label === "e") {
    appendToken("e");
    return;
  }
  if (label === "Rand") {
    appendToken("rand()");
    return;
  }

  const transforms = {
    "x^2": () => (expression = `(${expression || 0})**2`),
    "x^3": () => (expression = `(${expression || 0})**3`),
    "x^y": () => appendToken("**"),
    "e^x": () => (expression = `e**(${expression || 0})`),
    "10^x": () => (expression = `10**(${expression || 0})`),
    "1/x": () => (expression = `1/(${expression || 0})`),
    "2√x": () => (expression = `sqrt(${expression || 0})`),
    "3√x": () => (expression = `cbrt(${expression || 0})`),
    "y√x": () => (expression = `root(${expression || 0},2)`),
    ln: () => wrapFn("ln"),
    log10: () => wrapFn("log10"),
    "x!": () => wrapFn("fact"),
    sin: () => wrapFn("sin"),
    cos: () => wrapFn("cos"),
    tan: () => wrapFn("tan"),
    sinh: () => wrapFn("sinh"),
    cosh: () => wrapFn("cosh"),
    tanh: () => wrapFn("tanh"),
    EE: () => (expression = `ee(${expression || 0},0)`),
    TET: () => (expression = `tetration(${expression || 2},2)`),
    mc: () => {
      memory = 0;
    },
    "m+": () => {
      memory += Number(expression || 0);
    },
    "m-": () => {
      memory -= Number(expression || 0);
    },
    mr: () => appendToken(String(memory)),
  };

  if (transforms[label]) {
    transforms[label]();
    updateDisplay(expression);
  }
}

async function rpnRequest(payload) {
  const response = await fetch("/api/rpn", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) {
    updateDisplay(`Error: ${data.detail}`);
    return;
  }
  renderStack(data.stack);
}

function renderStack(stack) {
  rpnStackEl.innerHTML = "";
  stack.forEach((item) => {
    const row = document.createElement("div");
    row.textContent = item;
    rpnStackEl.appendChild(row);
  });
}

function isScientificModeActive() {
  const scientificTab = document.querySelector('.mode-btn[data-mode="scientific"]');
  return scientificTab?.classList.contains("active");
}

function pushCurrentValueToStack() {
  const value = Number(expression || 0);
  rpnRequest({ action: "push", value });
  expression = "";
  updateDisplay("0");
}

document.querySelectorAll(".mode-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".mode-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    const mode = btn.dataset.mode;

    const isCalc = mode === "basic" || mode === "scientific";
    document.querySelector(".calc-panel").classList.toggle("hidden", !isCalc);
    programmablePanel.classList.toggle("hidden", mode !== "programmable");
    conversionsPanel.classList.toggle("hidden", mode !== "conversions");
    basicLayout.classList.toggle("hidden", mode !== "basic");
    scientificLayout.classList.toggle("hidden", mode !== "scientific");
    rpnPanel.classList.toggle("hidden", mode !== "scientific");
  });
});

radBtn.addEventListener("click", () => {
  angleUnit = "RAD";
  radBtn.classList.add("active");
  degBtn.classList.remove("active");
});

degBtn.addEventListener("click", () => {
  angleUnit = "DEG";
  degBtn.classList.add("active");
  radBtn.classList.remove("active");
});

document.querySelectorAll("[data-rpn]").forEach((btn) => {
  btn.addEventListener("click", () => {
    const action = btn.dataset.rpn;
    if (action === "push") {
      pushCurrentValueToStack();
      return;
    }
    rpnRequest({ action });
  });
});

document.querySelectorAll("[data-rpn-binary]").forEach((btn) => {
  btn.addEventListener("click", () => {
    rpnRequest({ action: "binary", op: btn.dataset.rpnBinary });
  });
});

document.querySelectorAll("[data-rpn-unary]").forEach((btn) => {
  btn.addEventListener("click", () => {
    rpnRequest({ action: "unary", op: btn.dataset.rpnUnary, angle_unit: angleUnit });
  });
});

document.addEventListener("keydown", (event) => {
  const key = event.key;
  const inputKeys = ["+", "-", "*", "/", "%", "(", ")", "."];
  const isDigit = /^[0-9]$/.test(key);

  if (isDigit || inputKeys.includes(key)) {
    event.preventDefault();
    appendToken(key);
    return;
  }

  if (key === "Backspace") {
    event.preventDefault();
    expression = expression.slice(0, -1);
    updateDisplay(expression);
    return;
  }

  if (key === "Escape") {
    event.preventDefault();
    expression = "";
    updateDisplay("0");
    return;
  }

  if (key === "Enter") {
    event.preventDefault();
    if (isScientificModeActive()) {
      pushCurrentValueToStack();
      return;
    }
    evaluate();
  }
});

createButtons(basicNumbers, basicNumberButtons, handleBasic);
createButtons(basicFunctions, basicFunctionButtons, handleBasic);
createButtons(scientificNumbers, scientificNumberButtons, handleScientific);
createButtons(scientificOps, scientificOpsButtons, handleScientific);
createButtons(scientificFunctions, scientificFunctionButtons, handleScientific);
updateDisplay("0");
