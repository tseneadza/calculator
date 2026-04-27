from calculator.engine import CalculatorEngine


def test_basic_eval() -> None:
    engine = CalculatorEngine()
    assert engine.evaluate("2+2") == 4
    assert engine.evaluate("5/2") == 2.5


def test_scientific_eval() -> None:
    engine = CalculatorEngine()
    assert round(engine.evaluate("sin(pi/2)"), 6) == 1.0
    assert engine.evaluate("fact(5)") == 120.0


def test_tetration() -> None:
    engine = CalculatorEngine()
    assert engine.evaluate("tetration(2,3)") == 16.0


def test_rpn_binary() -> None:
    engine = CalculatorEngine()
    engine.rpn_push(2)
    engine.rpn_push(3)
    assert engine.rpn_binary("+")[-1] == 5.0
