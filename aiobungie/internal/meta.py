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

"""A very basic implementation of a bungie Manifest."""


from __future__ import annotations

__all__: t.Sequence[str] = ("Manifest",)

import json
import logging
import os
import os.path
import time
import typing as t
import zipfile

import aiohttp
import aiosqlite

from aiobungie import url

from ..http import HTTPClient
from .assets import Image
from .enums import Raid

log: t.Final[logging.Logger] = logging.getLogger(__name__)


class Manifest:
    def __init__(self, token: str, path: t.Dict[str, t.Any]) -> None:
        self.path = url.BASE + path["mobileWorldContentPaths"]["en"]
        self.token = token
        self.db = Database("./.cache/destiny.sqlite3")

    async def get_raid_image(self, raid: Raid) -> Image:
        image = await self.db.execute(
            "SELECT json FROM DestinyActivityDefinition WHERE id = ?",
            (int(raid),),
            "pgcrImage",
        )
        return Image(path=str(image))

    async def download(self, *, force: bool = False) -> None:
        _time = time.time()

        if os.path.isfile("./.cache/destiny.sqlite3"):
            if not force:
                log.info("Database already exists, returning.")
                return
            else:
                os.remove("./.cache/destiny.sqlite3")

        if os.path.isfile("./.cache/file.zip"):
            os.remove("./.cache/file.zip")
        try:
            log.debug("Downloading manifest...")
            token = {"X-API-KEY": self.token}
            async with aiohttp.ClientSession() as s:
                async with s.get(self.path, headers=token) as r:
                    if not os.path.exists("./.cache"):
                        os.mkdir("./.cache")
                    with open("./.cache/file.zip", "wb") as afile:
                        afile.write(await r.read())
                        with zipfile.ZipFile("./.cache/file.zip") as zipped:
                            name = zipped.namelist()
                            zipped.extractall()
                        os.rename(name[0], "./.cache/destiny.sqlite3")
                        print(f"Finished downloading file in: {_time - time.time()}")
        except Exception:
            raise


class Database:
    def __init__(self, path: str) -> None:
        self.path = path

    async def execute(self, sql: str, params: tuple = None, item: str = None) -> None:
        async with aiosqlite.connect(self.path) as db:
            try:
                cur = await db.execute(sql, params)
                async for row in cur:
                    return json.loads(*row)[item]
            except Exception:
                raise
