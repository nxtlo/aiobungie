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

"""Type definitions used globally in aiobungie."""

from __future__ import annotations

__all__ = (
    "JSONObject",
    "JSONArray",
    "Loads",
    "Dumps",
    "unknown",
)

import collections.abc as collections
import typing

JSONObject = collections.Mapping[str, typing.Any]
"""A JSON like dict of string key and any value.

i.e., `{"Key": 1, "Key2": "Value"}`
"""

JSONArray = collections.Sequence[JSONObject]
"""A JSON like list of any data type.

i.e., `[{"Key": 1}, {"Key2": "Value"}]`
"""

JSONIsh = JSONObject | JSONArray | bytes | str | int | bool | None
"""A type that any valid REST response from Bungie."""

Loads = collections.Callable[[str | bytes], JSONArray | JSONObject]
"""A function that takes a `str | bytes` JSON object and decode it into a Python object."""

Dumps = collections.Callable[[JSONObject | JSONArray], bytes]
"""A function that dump a Python JSON object and encode it into bytes."""


def unknown(string: str) -> str | None:
    """Returns `None` if `string` is empty, otherwise `string`."""
    if not string:
        return None
    return string
