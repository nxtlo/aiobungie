# Using these since mypy cry when
# using the builtins list[...] and dict[...]

from __future__ import annotations

import asyncio
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
    def __aiter__(self) -> AsyncIterator: ...
    async def __anext__(self) -> T: ...

class UndefinedType:
    def __bool__(self) -> __Literal[False]: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __new__(cls) -> UndefinedType: ...

Undefined: __Final[UndefinedType]

UndefinedOr = __Union[UndefinedType, T]
