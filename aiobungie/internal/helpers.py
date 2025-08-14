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
    "get_or_make_loop",
    "unimplemented",
    "loads",
    "dumps",
    "unstable",
)

import asyncio
import collections.abc as collections
import functools
import json as _json
import typing

if typing.TYPE_CHECKING:
    from aiobungie import typedefs

    T_co = typing.TypeVar("T_co", covariant=True)
    T = typing.TypeVar("T", bound=collections.Callable[..., typing.Any])


from sain import deprecated, unimplemented


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

        # Closed loops cannot be reused.
        if not loop.is_closed():
            return loop

    except RuntimeError:
        pass

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop


# The reason we're ignoring the types here because one of those modules will be
# available at runtime which we need to ignore, But json is guaranteed to be available
# if none of the others are.


def dumps(
    obj: typedefs.JSONArray | typedefs.JSONObject,
) -> bytes:
    def default_dumps(x: typedefs.JSONArray | typedefs.JSONObject) -> bytes:
        return _json.dumps(x).encode("UTF-8")

    try:
        import orjson  # pyright: ignore

        default_dumps = orjson.dumps  # type: ignore[UnknownMemberType]  # noqa: F811
    except ModuleNotFoundError:
        pass

    try:
        return default_dumps(obj)
    # This could get raised in some scenarios, Just to be safe.
    except TypeError:
        return _json.dumps(obj).encode("utf-8")


def loads(obj: str | bytes) -> typedefs.JSONArray | typedefs.JSONObject:
    try:
        import orjson  # pyright: ignore

        default_loads = orjson.loads  # pyright: ignore
    except ModuleNotFoundError:
        default_loads = _json.loads

    return default_loads(obj)
