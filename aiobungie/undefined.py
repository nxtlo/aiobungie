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

"""An undefined type object."""

from __future__ import annotations

import typing

_T = typing.TypeVar("_T", covariant=True)


class UndefinedType:
    """An `UNDEFINED` type."""

    __instance: typing.Optional[UndefinedType] = None

    def __bool__(self) -> typing.Literal[False]:
        return False

    def __int__(self) -> typing.Literal[0]:
        return 0

    def __repr__(self) -> str:
        return "UNDEFINED"

    def __str__(self) -> str:
        return "UNDEFINED"

    def __new__(cls) -> UndefinedType:
        if cls.__instance is None:
            o = super().__new__(cls)
            cls.__instance = o
        return cls.__instance


Undefined: typing.Final[UndefinedType] = UndefinedType()
"""An undefined type for attribs that may be undefined and not None."""

UndefinedOr = typing.Union[UndefinedType, _T]
"""A union version of the Undefined type which can be undefined or any other type."""
