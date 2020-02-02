from examples.arithmetic import *
import pytest


@pytest.mark.parametrize(
    "input_expression,expected_parsed",
    [("+", ("+",)), ("-", ("-",)), ("*", ("*",)), ("/", ("/",)),],
)
def test_operator(input_expression, expected_parsed):
    parsed, remaining = OPERATOR.match(input_expression)
    assert parsed == expected_parsed
    assert remaining == ""


@pytest.mark.parametrize(
    "input_expression,expected_parsed",
    [("+2", ("+", 2)), ("-2", ("-", 2)), ("*2", ("*", 2)), ("/2", ("/", 2))],
)
def test_applied_operator(input_expression, expected_parsed):
    parsed, remaining = APPLIED_OPERATOR_EXPR.match(input_expression)
    assert parsed == expected_parsed
    assert remaining == ""


@pytest.mark.parametrize(
    "input_expression,expected_parsed",
    [
        ("1+2", (1, "+", 2)),
        ("1 + 2", (1, "+", 2)),
        ("1+2 + 3", (1, "+", 2, "+", 3)),
        ("1", (1, )),
    ],
)
def test_binary_operation_expr(input_expression, expected_parsed):
    parsed, remaining = BINARY_OPERATION_EXPR.match(input_expression)
    assert parsed == expected_parsed
    assert remaining == ""


@pytest.mark.parametrize(
    "input_expression",
    [
        "1+2",
        "1 + 2",
        "1+2 + 3",
        "1",
    ],
)
def test_binary_operation(input_expression):
    parsed, remaining = BINARY_OPERATION.match(input_expression)
    print(parsed)
