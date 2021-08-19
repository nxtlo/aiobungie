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


__all__: t.Sequence[str] = ("Manifest",)

import logging
import os
import os.path
import typing as t
import zipfile

from aiobungie.http import HTTPClient
from aiobungie.internal import Image
from aiobungie.internal.db import Database
from aiobungie.internal.enums import Raid

log: t.Final[logging.Logger] = logging.getLogger(__name__)


class Manifest:
    __slots__: t.Sequence[str] = ("db", "_http", "_path", "version")

    def __init__(self, token: str, path: t.Dict[str, t.Any]) -> None:
        self._path = path
        self.version: str = path["version"]
        self._http = HTTPClient(token)

    def __dbinit__(self) -> None:
        self.db = Database("./.cache/destiny.sqlite3")

    async def download(self, *, force: bool = False) -> None:
        if os.path.isfile("./.cache/destiny.sqlite3"):
            if not force:
                if self.db.version != self.version:  # type: ignore[has-type]
                    log.warning("A newer Manifest version is available.")
                    force = True
                    await self.download(force=force)
                return
            elif force:
                os.remove("./.cache/destiny.sqlite3")

        if os.path.isfile("./.cache/file.zip"):
            os.remove("./.cache/file.zip")
        try:
            log.debug("Downloading manifest...")
            req = await self._http.fetch(
                method="GET",
                route=self._path["mobileWorldContentPaths"]["en"],
                base=True,
                type="read",
            )

            if not os.path.exists("./.cache"):
                os.mkdir("./.cache")

            with open("./.cache/file.zip", "wb") as afile:  # Manifest bytes.
                afile.write(req)
                with zipfile.ZipFile("./.cache/file.zip") as zipped:
                    name = zipped.namelist()
                    zipped.extractall()
                os.rename(name[0], "./.cache/destiny.sqlite3")

                # The only reason we're doing the db stuff here
                # Because we don't want to declare `self.db` in the `__init__()`
                self.__dbinit__()
                self.db.create_table("versions", "version", "TEXT")
                self.db.insert_version(self.version)

                log.info("Database finished downloading.")
        except Exception:
            raise

    def get_raid_image(self, raid: Raid) -> Image:
        image = self.db.fetch(
            "SELECT json FROM DestinyActivityDefinition WHERE id = ?",
            (int(raid),),
            "pgcrImage",
        )
        return Image(path=str(image))

    def fetch(
        self, definition: str, id: int, item: t.Optional[str] = None
    ) -> t.Optional[t.Dict[t.Any, t.Any]]:
        """Fetch something from the manifest databse.
        This returns a `typing.Dict[typing.Any, typing.Any]`

        Parameters
        ----------
        definition: `builtins.str`
            The definition you want to fetch from.
        id: `builtins.int`
            The id of the entity.
        item: `typing.Optional[builsint.str]`
            An item to get from the dict.

        Returns
        -------
        `typing.Optional[typing.Dict[typing.Any, typing.Any]]`
        """
        return self.db.fetch(
            "SELECT json FROM {} WHERE id = ?".format(definition), (id,), item
        )
