# MIT License
#
# Copyright (c) 2020 - Present nxtlo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""A helper module for useful decorators, functions and types."""


from __future__ import annotations

__all__: tuple[str, ...] = (
    "deprecated",
    "JsonDict",
    "JsonList",
    "Undefined",
    "Unknown",
    "just",
    "NoneOr",
)

import typing
import warnings
from functools import wraps

JsonDict = typing.Dict[str, typing.Any]
JsonList = typing.List[typing.Dict[str, typing.Any]]

Undefined: str = "Undefined"
"""A helper that checks if stuff are unknown / empty string and Undefine them if they're."""

Unknown: str = ""
"""Stuff that are empty strings."""

T = typing.TypeVar("T", covariant=True)
"""A type var thats associated with NoneOr[T]"""

NoneOr = typing.Union[None, T]
"""A Union type thats similar to to Optional[T]"""


def just(lst: list[dict[str, typing.Any]], lookup: str) -> list[typing.Any]:
    """A helper function that takes a list of dicts and return a list of
    all keys found inside the dict
    """
    return list(map(lambda dct: dct[lookup], lst))


def deprecated(func):
    """
    functions with this decorator will not work or is not implemented yet.
    """

    @wraps(func)
    def wrapper(*args: typing.Any, **kwargs: typing.Any) -> None:
        warnings.warn(
            f"function {func.__name__!r} deprecated until further notice.",
            stacklevel=2,
            category=DeprecationWarning,
        )
        func.__doc__ += " DEPRECATED FUNCTION."
        print(func.__doc__)
        coro = func(*args, **kwargs)
        return coro

    return wrapper
