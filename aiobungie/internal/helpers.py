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

"""A module for helper functions and types."""


from __future__ import annotations

__all__ = (
    "deprecated",
    "JsonDict",
    "JsonList",
    "Undefined",
    "UndefinedOr",
    "UndefinedType",
    "Unknown",
    "just",
    "NoneOr",
    "get_or_make_loop",
)

import asyncio
import inspect
import typing
import warnings

JsonDict = typing.Dict[str, typing.Any]
"""A json like dict of string key and any value.

i.e., {"Key": 1, "Key2": "Value"}
"""

JsonList = typing.List[typing.Dict[str, typing.Any]]
"""A json like list of dicts of string key and any value

i.e., [{"Key": 1}, {"Key2": "Value"}]
"""

Unknown: str = ""
"""Stuff that are empty strings."""

T = typing.TypeVar("T", covariant=True)

NoneOr = typing.Union[None, T]
"""A Union type that's similar to to `Optional[T]`"""


def just(lst: list[dict[str, typing.Any]], lookup: str) -> list[typing.Any]:
    """A helper function that takes a list of dicts and return a list of
    all keys found inside the dict
    """
    return list(map(lambda dct: dct[lookup], lst))


def deprecated(func: typing.Callable[..., typing.Any]) -> typing.Callable[..., None]:
    """
    functions with this decorator will not work or is not implemented yet.
    """
    if inspect.isfunction(func):
        warnings.warn(
            f"function {func.__name__!r} is deprecated.",
            stacklevel=2,
            category=DeprecationWarning,
        )
        func.__doc__ += """.. warning::
        This function is a DEPRECATED.
        """  # type: ignore # Pyright bug
    return lambda *args, **kwargs: func(*args, **kwargs)


# Source [https://github.com/hikari-py/hikari/blob/master/hikari/internal/aio.py]
def get_or_make_loop() -> asyncio.AbstractEventLoop:
    """Get the current usable event loop or create a new one.
    Returns
    -------
    asyncio.AbstractEventLoop
    """
    # get_event_loop will error under oddly specific cases such as if set_event_loop has been called before even
    # if it was just called with None or if it's called on a thread which isn't the main Thread.
    try:
        loop = asyncio.get_event_loop_policy().get_event_loop()

        # Closed loops cannot be re-used.
        if not loop.is_closed():
            return loop

    except RuntimeError:
        pass

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop


class UndefinedType:
    """An `UNDEFINED` type."""

    __instance__: typing.ClassVar[UndefinedType]

    def __bool__(self) -> typing.Literal[False]:
        return False

    def __repr__(self) -> str:
        return "UNDEFINED"

    def __str__(self) -> str:
        return "UNDEFINED"

    def __new__(cls) -> UndefinedType:
        try:
            return cls.__instance__
        except AttributeError:
            o = super().__new__(cls)
            cls.__instance__ = o
            return cls.__instance__


Undefined: typing.Final[UndefinedType] = UndefinedType()
"""An undefined type for attribs that may be undefined and not None."""

UndefinedOr = typing.Union[UndefinedType, T]
"""A union version of the Undefined type which can be undefined or any other type."""
