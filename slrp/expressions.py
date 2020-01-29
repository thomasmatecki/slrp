"""
Expression for matching.
"""
import re
from abc import ABC
from typing import Callable, Text, Tuple

from slrp.combos import Combinable


class RegExpr(Combinable):
    """
    Regular expression matcher.
    """

    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, expr):
        _match = re.match(self.pattern, expr)
        if _match:
            fr, to = _match.span()
            return _match.groups(), expr[to:]


class StringExpr(Combinable):
    """
    String Expression Matcher.
    """
    def __init__(self, string: str, capture=False):
        self.string = string
        self.capture = capture

    def match(self, expr):
        if expr.startswith(self.string):
            remaining = expr[len(self.string) :]
            return ((self.string,), remaining) if self.capture else (tuple(), remaining)
