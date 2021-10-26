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

from __future__ import annotations

__all__: tuple[str, ...] = (
    "deprecated",
    "JsonObject",
    "JsonArray",
    "Undefined",
    "UndefinedOr",
    "UndefinedType",
    "Unknown",
    "just",
    "NoneOr",
    "get_or_make_loop",
    "AsyncIterator",
    "IntAnd",
)

import asyncio

# This is required to be imported like this otherwise mypy will throw an error.
from typing import Any as __Any
from typing import Callable as __Callable
from typing import Dict as __Dict
from typing import Final as __Final
from typing import Generic as __Generic
from typing import Iterable as __Iterable
from typing import List as __List
from typing import Literal as __Literal
from typing import TypeVar as __TypeVar
from typing import Union as __Union

from aiobungie.internal import enums as __enums

T = __TypeVar("T", covariant=True)

JsonObject = __Dict[str, __Any]
JsonArray = __List[__Any]
NoneOr = __Union[T, None]

Unknown: __Final[str]

EnumSig = __TypeVar(
    "EnumSig", covariant=True, bound=__Union[__enums.Enum, __enums.IntEnum]
)
IntAnd = __Union[int, EnumSig]

def just(lst: list[dict[str, __Any]], lookup: str) -> list[__Any]: ...
def deprecated(func: __Callable[..., __Any]) -> __Callable[..., None]: ...
def get_or_make_loop() -> asyncio.AbstractEventLoop: ...

class AsyncIterator(__Generic[T]):
    def __init__(self, sequence: __Iterable[T]) -> None: ...
    def __aiter__(self) -> AsyncIterator[T]: ...
    async def __anext__(self) -> T: ...

class UndefinedType:
    def __bool__(self) -> __Literal[False]: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __new__(cls) -> UndefinedType: ...

Undefined: __Final[UndefinedType]

UndefinedOr = __Union[UndefinedType, T]
