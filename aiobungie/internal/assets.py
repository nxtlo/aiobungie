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

"""aiobungie assets module for API Image hash and path linking."""


from __future__ import annotations

__all__: list[str] = ["Image", "MaybeImage"]

import typing

from aiobungie import undefined
from aiobungie import url


class Image:
    def __init__(self, path: typing.Optional[str] = None) -> None:
        self.path = path

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{url.BASE}/{self.path if self.path else self.missing_path()}"

    @staticmethod
    def missing_path() -> str:
        return "img/misc/missing_icon_d2.png"

    @staticmethod
    def partial() -> str:
        return f"<Image {undefined.Undefined}>"

    def is_missing(self) -> bool:
        return not self.path

    @property
    def url(self) -> str:
        return str(self)

    def typeof(self, mimtype: typing.Literal[".jpg", ".png", ".gif"]) -> bool:
        if self.path is not None and self.path.endswith(mimtype):
            return True
        return False


MaybeImage = typing.Union[Image, str, None]
"""A type hint for images that may or may not exists in the api.
Images returned from the api as None will be replaced with `Image.partial`.
"""
