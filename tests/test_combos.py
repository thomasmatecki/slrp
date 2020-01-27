from slrp import RE, S

integer_literal = RE(r"(\d+)")
single_space = RE(r"\s")
string_literal = RE(r"(\w+)")


def test_simple_expression():

    parsed, remaining = integer_literal.match("31 muffins")
    assert parsed == ("31",)
    assert remaining == " muffins"


def test_or_operator():
    muffin_count = integer_literal | string_literal

    parsed, remaining = muffin_count.match("31 muffins")
    assert parsed == ("31",)
    assert remaining == " muffins"

    parsed, remaining = muffin_count.match("thirty-one muffins")
    assert parsed == ("thirty",)
    assert remaining == "-one muffins"


def test_then_operator():

    muffin_count = integer_literal * single_space * string_literal
    parsed, remaining = muffin_count.match("31 muffins")

    assert parsed == ("31", "muffins")
    assert remaining == ""


def test_maybe_operator():

    muffin_count = integer_literal - single_space * string_literal

    parsed, remaining = muffin_count.match("31 muffins")
    assert parsed == ("31", "muffins")
    assert remaining == ""

    parsed, remaining = muffin_count.match("31 ")
    assert parsed == ("31",)
    assert remaining == " "

    muffin_count = (integer_literal - single_space) * string_literal

    parsed, remaining = muffin_count.match("31muffins")
    assert parsed == ("31", "muffins")
    assert remaining == ""

    parsed, remaining = muffin_count.match("31 muffins")
    assert parsed == ("31", "muffins")
    assert remaining == ""

    muffin_count = integer_literal - single_space - string_literal
    parsed, remaining = muffin_count.match("31muffins")
    assert parsed == ("31", "muffins")
    assert remaining == ""

    parsed, remaining = muffin_count.match("31 muffins")
    assert parsed == ("31", "muffins")
    assert remaining == ""

    parsed, remaining = muffin_count.match("31")
    assert parsed == ("31",)
    assert remaining == ""


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
