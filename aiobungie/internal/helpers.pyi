# Using these since mypy cry when
# using the builtins list[...] and dict[...]

from __future__ import annotations

import asyncio
from typing import Any as __Any
from typing import Callable as __Callable
from typing import Dict as __Dict
from typing import Final as __Final
from typing import List as __List
from typing import Literal as __Literal
from typing import TypeVar as __TypeVar
from typing import Union as __Union

T = __TypeVar("T", covariant=True)

JsonObject = __Dict[str, __Any]
JsonArray = __List[__Dict[str, __Any]]
NoneOr = __Union[T, None]

Unknown: __Final[str]

def just(lst: list[dict[str, __Any]], lookup: str) -> list[__Any]: ...
def deprecated(func: __Callable[..., __Any]) -> __Callable[..., None]: ...
def get_or_make_loop() -> asyncio.AbstractEventLoop: ...

class UndefinedType:
    def __bool__(self) -> __Literal[False]: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __new__(cls) -> UndefinedType: ...


Undefined: __Final[UndefinedType]

UndefinedOr = __Union[UndefinedType, T]
