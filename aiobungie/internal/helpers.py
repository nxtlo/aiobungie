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

"""A helper module the provides functions, classes for various of uses."""

from __future__ import annotations

__all__: tuple[str, ...] = (
    "deprecated",
    "just",
    "get_or_make_loop",
    "AsyncIterator",
)

import asyncio
import inspect
import typing
import warnings

AT = typing.TypeVar("AT", covariant=True)
JT = typing.TypeVar("JT")


def just(lst: list[dict[str, JT]], lookup: str) -> list[JT]:
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


class Ok(StopIteration):
    def __init__(self) -> None:
        self.__call__()

    def __call__(self) -> typing.NoReturn:
        raise StopIteration("Reached the maximum iterables.") from None


class AsyncIterator(typing.Generic[AT]):
    """A simple async iterator for iterating over sequences asynchronously.

    Attributes
    ----------
    sequence: `typing.Iterable[AT]`
        A sequence of the generic iterables type.
    """

    __slots__: typing.Sequence[str] = ("_seq",)

    def __init__(self, sequence: typing.Iterable[AT]) -> None:
        self._seq = iter(sequence)

    def __iter__(self) -> typing.NoReturn:
        raise TypeError("This class supports `async for` syntax only.")

    def __aiter__(self) -> AsyncIterator[AT]:
        return self

    def __next__(self) -> AT:
        return next(self._seq)

    async def __anext__(self) -> AT:
        try:
            return next(self._seq)
        except StopIteration:
            raise Ok()
