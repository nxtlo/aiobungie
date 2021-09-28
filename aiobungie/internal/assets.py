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

from aiobungie import url
from aiobungie.internal import helpers


class Image:
    def __init__(self, path: typing.Optional[str] = None) -> None:
        self.path = path

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return url.BASE + self.path if self.path is not None else self.partial()

    @property
    def url(self) -> str:
        return str(self)

    @property
    def is_jpg(self) -> bool:
        """Checks if the given path for the image is a JPEG type."""
        if self.path is not None and self.path.endswith(".jpg"):
            return True
        return False

    @staticmethod
    def partial() -> str:
        """A partial image that just returns undefined."""
        return f"Image <{helpers.Undefined}>"


MaybeImage = typing.Union[Image, str, None]
"""A type hint for images that may or may not exists in the api.
Images returned from the api as None will be replaced with `Image.partial`.
"""
