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

"""A module that has type definitions used globally in aiobungie."""

from __future__ import annotations

__all__: tuple[str, ...] = (
    "JSONObject",
    "JSONArray",
    "Unknown",
    "NoneOr",
    "EnumSig",
    "IntAnd",
    "is_unknown",
)

import typing

from aiobungie.internal import enums

JSONObject = dict[str, typing.Any]  # type: ignore[misc]
"""A JSON like dict of string key and any value.

i.e., `{"Key": 1, "Key2": "Value"}`
"""

JSONArray = list[typing.Any]  # type: ignore[misc]
"""A JSON like list of any data type.

i.e., `[{"Key": 1}, {"Key2": "Value"}]`
"""

Unknown: typing.Final[typing.Literal[""]] = ""
"""Some Bungie strings return empty so we undefine them if so."""

T = typing.TypeVar("T", covariant=True)

NoneOr = typing.Union[None, T]
"""A Union type that's similar to to `typing.Optional[T]`"""

EnumSig = typing.TypeVar(
    "EnumSig", covariant=True, bound=typing.Union[enums.Enum, enums.Flag]
)
"""A type hint bound to `aiobungie.internal.enums.Enum` and `aiobungie.internal.enums.Flag`"""

IntAnd = typing.Union[int, EnumSig]
"""A type hint for parameters that may receives an enum or an int."""


def is_unknown(string: str) -> bool:
    return string == Unknown
