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

__all__ = (
    "deprecated",
    "awaits",
    "get_or_make_loop",
    "unimplemented",
    "loads",
    "dumps",
    "unstable",
)

import asyncio
import collections.abc as collections
import functools
import inspect
import json as _json
import typing
import warnings

if typing.TYPE_CHECKING:
    from aiobungie import typedefs

    T_co = typing.TypeVar("T_co", covariant=True)
    T = typing.TypeVar("T", bound=collections.Callable[..., typing.Any])


class UnimplementedWarning(RuntimeWarning):
    """A warning that is raised when a function or class is not implemented."""


def deprecated(
    since: str,
    removed_in: str | None = None,
    use_instead: str | None = None,
) -> collections.Callable[[T], T]:
    """A decorator that marks a function as deprecated.

    Parameters
    ----------
    since : `str`
        The version that the function was deprecated.
    use_instead : `str | None`
        If provided, This should be the alternaviate object name that should be used instead.
    """

    def decorator(func: T) -> T:
        @functools.wraps(func)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            obj_type = "class" if inspect.isclass(func) else "function"
            msg = f"Warning! {obj_type} {func.__module__}.{func.__name__} is deprecated since {since}."

            if removed_in:
                msg += f" Will be removed in {removed_in}."

            if use_instead:
                msg += f" Use {use_instead} instead."

            warnings.warn(
                msg,
                stacklevel=2,
                category=DeprecationWarning,
            )
            return func(*args, **kwargs)

        return typing.cast("T", wrapper)

    return decorator


def unimplemented(
    message: str | None = None, available_in: str | None = None
) -> collections.Callable[[T], T]:
    """A decorator that marks a function or classes as unimplemented.

    Parameters
    ----------
    message : `str | None`
        An optional message to be displayed when the function is called. Otherwise default message will be used.
    available_in : `str | None`
        If provided, This will be shown as what release this object be implemented.
    """

    def decorator(obj: T) -> T:
        @functools.wraps(obj)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            obj_type = "class" if inspect.isclass(obj) else "function"
            msg = (
                message
                or f"Warning! {obj_type} {obj.__module__}.{obj.__name__} is not implemented yet."  # noqa: W503
            )

            if available_in:
                msg += f" Will be implemented in {available_in}."

            warnings.warn(
                msg,
                stacklevel=2,
                category=UnimplementedWarning,
            )
            return obj(*args, **kwargs)

        return typing.cast("T", wrapper)

    return decorator


def unstable(obj: T) -> collections.Callable[[T], typing.NoReturn]:
    """A decorator that marks a function or classes as unimplemented.

    .. warn::
        Calling an object decorated with this will raise a runtime error.

    Raises
    ------
    `RuntimeError`
        If the object has been called while marked `unstable`.
    """

    @functools.wraps(obj)
    def decorator(_: T) -> typing.NoReturn:
        raise RuntimeError(f"Object {obj!s} is currently unstable.")

    return decorator


# Source [https://github.com/hikari-py/hikari/blob/master/hikari/internal/aio.py]
async def awaits(
    *aws: collections.Awaitable[T_co],
    timeout: float | None = None,
) -> collections.Sequence[T_co]:
    """Await all given awaitables concurrently.

    Parameters
    ----------
    *aws : `collections.Awaitable[JT]`
        Multiple awaitables to await.
    timeout : `float | None`
        An optional timeout.
    with_exceptions : `bool`
        If `True` then exceptions will be returned.

    Returns
    -------
    `collections.Sequence[T_co]`
        A sequence of the results of the awaited coros.
    """

    if not aws:
        # Just pass if nothing was passed.
        pass

    tasks: list[asyncio.Task[T_co]] = []

    for future in aws:
        tasks.append(asyncio.ensure_future(future))
    try:
        gatherer = asyncio.gather(*tasks)
        return await asyncio.wait_for(gatherer, timeout=timeout)

    except asyncio.CancelledError:
        raise asyncio.CancelledError("Gathered Futures were cancelled.") from None

    finally:
        for task in tasks:
            if not task.done() and not task.cancelled():
                task.cancel()
        gatherer.cancel()


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


def dumps(
    obj: typedefs.JSONArray | typedefs.JSONObject,
) -> bytes:
    def default_dumps(x: typedefs.JSONArray | typedefs.JSONObject) -> bytes:
        return _json.dumps(x).encode("UTF-8")

    try:
        import orjson

        default_dumps = orjson.dumps  # noqa: F811
    except ModuleNotFoundError:
        try:
            import ujson

            default_dumps = lambda x: ujson.dumps(x).encode("UTF-8")  # noqa: E731
        except ModuleNotFoundError:
            pass

    return default_dumps(obj)  # type: ignore[no-any-return]


def loads(obj: str | bytes) -> typedefs.JSONArray | typedefs.JSONObject:
    default_loads = _json.loads
    try:
        import orjson

        default_loads = orjson.loads

    except ModuleNotFoundError:
        try:
            import ujson

            default_loads = ujson.loads
        except ModuleNotFoundError:
            pass

    return default_loads(obj)  # type: ignore[no-any-return]
