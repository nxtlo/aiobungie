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

"""A very basic helper for the bungie Manifest."""


from __future__ import annotations

__all__ = ("Manifest",)

import logging
import os
import os.path
import typing as t
import zipfile

from aiobungie.rest import RESTClient

log: t.Final[logging.Logger] = logging.getLogger(__name__)


class Manifest:
    __slots__: t.Sequence[str] = ("_rest", "version")

    def __init__(self, token: str, /) -> None:
        self._rest = RESTClient(token)

    async def download(self, *, force: bool = False) -> None:
        if os.path.isfile("./.cache/destiny.sqlite3"):
            if not force:
                return
            os.remove("./.cache/destiny.sqlite3")

        if os.path.isfile("./.cache/file.zip"):
            os.remove("./.cache/file.zip")
        try:
            log.debug("Downloading manifest...")
            req = await self._rest.fetch_manifest()

            if not os.path.exists("./.cache"):
                os.mkdir("./.cache")

            with open("./.cache/file.zip", "wb") as afile:  # Manifest bytes.
                afile.write(req)
                with zipfile.ZipFile("./.cache/file.zip") as zipped:
                    name = zipped.namelist()
                    zipped.extractall()
                os.rename(name[0], "./.cache/destiny.sqlite3")

                log.info("Database finished downloading.")
        except Exception:
            raise
