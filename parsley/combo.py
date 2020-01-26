import re
from abc import ABC
from typing import Any, Callable, Text, Tuple, Union


class Combinable(ABC):
    """

    """

    def __mul__(self, other):
        return Then(self, other)

    def __sub__(self, other):
        return Then(self, Maybe(other))

    def __neg__(self):
        return Maybe(self)

    def __add__(self, other):
        return Then(self, Many(other))

    def __pos__(self):
        return Many(self)

    def __or__(self, other):
        return Either(self, other)


class Either(Combinable):
    """
    """

    def __init__(self, left, right):
        self._left = left
        self._right = right

    def match(self, expr):
        parsed = self._left.match(expr)
        if parsed:
            return parsed
        else:
            return self._right.match(expr)


class Then(Combinable):
    """

    """

    def __init__(self, first, then: Combinable):
        self._first = first
        self._then = then

    def match(self, expr):
        matched = self._first.match(expr)
        if matched:
            args, tail = matched

            next_matched = self._then.match(tail)
            if next_matched:
                next_args, tail = next_matched

                args = args + next_args
                return args, tail


class Maybe(Combinable):
    """

    """

    def __init__(self, extractor):
        self.extr = extractor

    def match(self, expr):
        matched = self.extr.match(expr)
        if matched:
            args, tail = matched
            return args, tail
        else:
            return (), expr

class Many(Combinable):
    def __init__(self, extractor: Combinable):
        self.extr = extractor

    def match(self, expr):
        """
    Extract recursively WHILE extraction is successful AND the tail is consumed.

    Use with a `Maybe` builder to extract 0..N repeated expressions. Without a `Maybe`
    builder, extracts 1..N repeated expressions. `call` is not applied for each
    recursion, and therefore should accept a variable number of arguments.
    :param expr:
    :return:
    """
        extracted = self.extr.match(expr)

        if not extracted:
            return None

        args, tail = extracted

        if tail != expr:
            next_extracted = self.match(tail)

            if next_extracted:
                next_args, tail = next_extracted
                args = args + next_args

        return args, tail

class Lazy(Combinable):
    """

      .. code-block::
      Foo(*args0..., Foo(*args1..., Foo(...))) ).

    """

    def __init__(self, extr_call):
        assert callable(extr_call)
        self._extr_call = extr_call

    def build(self, expr):
        extractor = self._extr_call()

        extracted = extractor.extract(expr)

        if extracted:
            args, tail = extracted
            return args, tail
