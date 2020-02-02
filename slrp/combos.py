"""
Combinators.
"""
import re
from abc import ABC, abstractmethod
from typing import Any, Callable, Text, Tuple, Union, TypeVar


class Matcher(ABC):
    """An abstract class that is extended by classes that implement
    the `build` method. This includes any *expression* matchers and
    `Combinable`
    """

    T = TypeVar("T")

    @abstractmethod
    def match(self, expr: T) -> T:
        raise NotImplementedError()


class Combinable(Matcher):
    """
    An abstract class extended by concrete combinator classes and
    expression parsers. This class implements the operator methods,
    all of which return combinators
    """

    def __mul__(self, other) -> "Then":
        """Combine `self` with another matcher to create a matcher for `self`'s
        expression followed *by `other`'s expression.

        :param other: A matcher following `self`
        :type other: `Matcher`
        :return: matcher for `self` *then* `other`
        :rtype: `Then`
        """
        return Then(self, other)

    def __sub__(self, other) -> "Then":
        """Combine `self` with another matcher to create a matcher for `self`'s
        expression followed **optionally** by `other`'s expression.

        :param other: A matcher following `self`
        :type other: `Matcher`
        :return: matcher for `self` *then* *maybe* `other`
        :rtype: `Then`
        """
        return Then(self, Maybe(other))

    def __neg__(self) -> "Maybe":
        """Create a matcher that optionally matches `self`'s expression.

        :return: matcher for *maybe* `self`
        :rtype: `Maybe`
        """
        return Maybe(self)

    def __add__(self, other) -> "Then":
        """Create a matcher that matches `self`'s expression followed by repetitions
        of `other`'s expression.

        :param other: A matcher following `self`
        :type other: `Matcher`
        :return: matcher for `self` then *repeated* `other`
        :rtype: `Many`
        """
        return Then(self, Many(other))

    def __pos__(self) -> "Many":
        """Create a matcher that matches repetitions of `self`'s expression.

        :return: matcher for *repeated* `self`
        :rtype: `Many`
        """
        return Many(self)

    def __or__(self, other) -> "Either":
        """Create a matcher that matches *either* `self`'s expression or `other`'s.

        :param other: A matcher `self`
        :type other: `Matcher`
        :return: matcher for either `self` or `other`
        :rtype: `Either`
        """
        return Either(self, other)

    def __mod__(self, applicable) -> "Either":
        """
        """
        return Apply(self, applicable)


class Then(Combinable):
    """Match some expression, followed by another expression.
    """

    def __init__(self, first: Combinable, then: Combinable):
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
    """Match some expression, or not.
    """

    def __init__(self, matcher):
        self.matcher = matcher

    def match(self, expr):
        matched = self.matcher.match(expr)
        if matched:
            args, tail = matched
            return args, tail
        else:
            return (), expr


class Many(Combinable):
    """Match an expression repeatedly.
    """
    def __init__(self, extractor: Combinable):
        self.extr = extractor

    def match(self, expr):
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

class Either(Combinable):
    """Match on of two expressions.
    """

    def __init__(self, left: Combinable, right: Combinable):
        self._left = left
        self._right = right

    def match(self, expr):
        parsed = self._left.match(expr)
        if parsed:
            return parsed
        else:
            return self._right.match(expr)

class Apply(Combinable):
    def __init__(self, matcher, callable: Callable):
        self._matcher = matcher
        self._callable = callable

    def match(self, expr):
        matched, tail = self.matcher.match(expr)
        return self._callable(*matched)

class Lazy(Combinable):
    """
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
