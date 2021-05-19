'''
This file is for testing only with DestinyManifest path.
'''
import typing as t
import httpx
from aiobungie import error
import aiosqlite
import zipfile
import time
import os
import aiofiles
import json

class Manifest:
    BASE: str = 'https://bungie.net'
    def __init__(self, data) -> None:
        self.data: t.Dict[str, t.Any] = data.get('Response', None)
        self.db = db = Database('./destiny.sqlite3')

    async def from_db(self):
        await self.update_man()
        return await self.db.execute('SELECT json FROM DestinyClassDefinition WHERE id = -639573535;')

    async def download(self) -> None:
        _time = time.time()
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

    async def execute(self, sql: str, params = None) -> t.Dict[str, t.Any]:
        async with aiosqlite.connect(self.path) as db:
            try:
                cur = await db.execute(sql, params)
                async for row in cur:
                    for x in row:
                       return json.loads(x).get('displayProperties')
            except Exception:
                raise