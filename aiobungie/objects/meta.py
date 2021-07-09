'''
MIT License

Copyright (c) 2020 - Present nxtlo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import typing as t
import httpx
import aiosqlite
import zipfile
import time
import os
import aiofiles
import json
import os.path
from ..utils.enums import Raid
from ..utils import Image

__all__: t.Sequence[str] = (
    'Manifest',
)
class Manifest:
    BASE: str = 'https://bungie.net'
    def __init__(self, data) -> None:
        self.data: t.Any = data.get('Response', None)
        self.db = Database('./destiny.sqlite3')

    async def _dbinit(self):
        if not os.path.exists('./destiny.sqlite3'):
            await self.download()
        return
    
    async def get_raid_image(self, raid: Raid) -> Image:
        image = await self.db.execute("SELECT json FROM DestinyActivityDefinition WHERE id = ?", (raid,), 'pgcrImage')
        return Image(path=str(image))

    async def download(self) -> None:
        _time = time.time()
        if os.path.isfile('./file.zip'):
            os.remove('./destiny.sqlite3')
            os.remove('./file.zip')
        path = self.data.get('mobileWorldContentPaths').get('en')
        async with httpx.AsyncClient() as ses:
            try:
                file = await ses.get(self.BASE + path)
                async with aiofiles.open('./file.zip', 'wb') as afile:
                    await afile.write(file.content)
                    with zipfile.ZipFile('./file.zip') as zipped:
                        name = zipped.namelist()
                        zipped.extractall()
                    os.rename(name[0], 'destiny.sqlite3')
                    print(f"Finished downloading file in: {_time - time.time()}")
            except Exception:
                raise

class Database:
    def __init__(self, path: str) -> None:
        self.path = path

    async def execute(self, sql: str, params: tuple = None, item:str = None) -> None:
        async with aiosqlite.connect(self.path) as db:
            try:
                cur = await db.execute(sql, params)
                async for row in cur:
                    return json.loads(*row)[item]
            except Exception:
                raise
