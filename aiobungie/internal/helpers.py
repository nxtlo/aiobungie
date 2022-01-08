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
    "awaits",
    "get_or_make_loop",
    "collect",
)

import asyncio
import collections.abc as collections
import inspect
import typing
import warnings

AT = typing.TypeVar("AT", covariant=True)
JT = typing.TypeVar("JT")

ConsumerSigT = typing.TypeVar("ConsumerSigT", bound=typing.Callable[..., typing.Any])


def just(lst: list[dict[str, JT]], lookup: str) -> list[JT]:
    """A helper function that takes a list of dicts and return a list of
    all keys found inside the dict
    """
    return list(map(lambda dct: dct[lookup], lst))


def collect(
    *args: typing.Any, consume: ConsumerSigT = str, separator: str = ", "  # type: ignore[assignment]
) -> typing.Union[ConsumerSigT, str]:
    """Consume passed argumnts and return them joining ', ' for each argument.

    If only one argument was passed it will just return that argumnt.
    """
    if len(args) > 1:
        if consume:
            return separator.join(consume(arg) for arg in args)
        return separator.join(arg for arg in args)
    return args[0]  # type: ignore[no-any-return]


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


async def awaits(
    *aws: collections.Awaitable[JT],
    timeout: typing.Optional[float] = None,
    with_exception: bool = True,
) -> typing.Union[collections.Collection[JT], collections.Sequence[JT]]:
    """Await all given awaitables concurrently.

    Parameters
    ----------
    aws : `collections.Awaitable[JT]`
        Multiple awaitables to await.
    timeout : `typing.Optional[float]`
        An optional timeout.
    with_exceptions : `bool`
        If `True` then exceptions will be returned.

    Returns
    -------
    `typing.Union[collections.Collection[JT], collections.Collection[JT]]`
        A collection or sequence of the awaited coros objects.
    """

    if not aws:
        raise RuntimeError("No awaiables passed.", aws)

    pending: list[asyncio.Future[JT]] = []

    for future in aws:
        pending.append(asyncio.create_task(future))
    try:
        gatherer = asyncio.gather(*pending, return_exceptions=with_exception)
        return await asyncio.wait_for(gatherer, timeout=timeout)

    except asyncio.CancelledError:
        raise asyncio.CancelledError("Gathered Futures were cancelled.") from None

    finally:
        for fs in pending:
            if not fs.done() and not fs.cancelled():
                fs.cancel()


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
