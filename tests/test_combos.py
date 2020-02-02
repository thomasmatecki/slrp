from slrp import RE, S

import pytest

integer_literal = RE(r"(\d+)")
single_space = RE(r"\s")
string_literal = RE(r"(\w+)")


def test_simple_expression():

    parsed, remaining = integer_literal.match("31 muffins")
    assert parsed == ("31",)
    assert remaining == " muffins"


@pytest.mark.parametrize(
    "input_expression,expected_parsed,expected_remaining",
    [
        ("31 muffins", ("31",), " muffins"),
        ("thirty-one muffins", ("thirty",), "-one muffins"),
    ],
)
def test_or_operator(input_expression, expected_parsed, expected_remaining):
    muffin_count = integer_literal | string_literal

    parsed, remaining = muffin_count.match(input_expression)
    assert parsed == expected_parsed
    assert remaining == expected_remaining


def test_then_operator():

    muffin_count = integer_literal * single_space * string_literal
    parsed, remaining = muffin_count.match("31 muffins")

    assert parsed == ("31", "muffins")
    assert remaining == ""


@pytest.mark.parametrize(
    "grammar,input_expression,expected_parsed,expected_remaining",
    [
        (
            integer_literal - single_space * string_literal,
            "31 muffins",
            ("31", "muffins"),
            "",
        ),
        (integer_literal - single_space * string_literal, "31 ", ("31",), " ",),
        (
            (integer_literal - single_space) * string_literal,
            "31muffins",
            ("31", "muffins"),
            "",
        ),
        (
            (integer_literal - single_space) * string_literal,
            "31 muffins",
            ("31", "muffins"),
            "",
        ),
        (
            integer_literal - single_space - string_literal,
            "31muffins",
            ("31", "muffins"),
            "",
        ),
        (
            integer_literal - single_space - string_literal,
            "31 muffins",
            ("31", "muffins"),
            "",
        ),
        (integer_literal - single_space - string_literal, "31", ("31",), ""),
    ],
)
def test_maybe_operator(grammar, input_expression, expected_parsed, expected_remaining):

    parsed, remaining = grammar.match(input_expression)
    assert parsed == expected_parsed
    assert remaining == expected_remaining


def test_maybe_unary_operator():

    muffin_count = -integer_literal - single_space - string_literal

    parsed, remaining = muffin_count.match("muffins")
    assert parsed == ("muffins",)
    assert remaining == ""


def test_many_unary_operator():

    baked_goods_counts = +(integer_literal * single_space * string_literal * RE(","))
    parsed, remaining = baked_goods_counts.match("31 muffins,29 scones,7 cookies,")
    expected = (
        "31",
        "muffins",
        "29",
        "scones",
        "7",
        "cookies",
    )
    assert parsed == expected
    assert remaining == ""


def test_many_operator():

    baked_goods_counts = S("There are: ") + (
        integer_literal * single_space * string_literal * RE(",")
    )
    parsed, remaining = baked_goods_counts.match(
        "There are: 31 muffins,29 scones,7 cookies,"
    )
    expected = (
        "31",
        "muffins",
        "29",
        "scones",
        "7",
        "cookies",
    )
    assert parsed == expected
    assert remaining == ""


def test_apply_operator():

    muffin_count = integer_literal % int * single_space * string_literal
    parsed, remaining = muffin_count.match("31 muffins")

    assert parsed == (31, "muffins")
