# Using these since mypy cry when
# using the builtins list[...] and dict[...]
from typing import Any as __Any
from typing import Dict as __Dict
from typing import List as __List
from typing import TypeVar as __TypeVar
from typing import Union as __Union

__all__: __Any

T__ = __TypeVar("T__", covariant=True)

JsonDict = __Dict[str, __Any]
JsonList = __List[__Dict[str, __Any]]
NoneOr = __Union[T__, None]

Undefined: str = "Undefined"
Unknown: str = ""

def just(lst: list[dict[str, __Any]], lookup: str) -> list[__Any]: ...
def deprecated(func): ...