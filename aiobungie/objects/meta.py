'''
This file is for testing only with DestinyManifest path.
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
from ..utils import Raid, ImageProtocol

__all__: t.Sequence[str] = (
    'Manifest',
    'Database'
)
class Manifest:
    BASE: str = 'https://bungie.net'
    def __init__(self, data) -> None:
        self.data: t.Dict[str, t.Any] = data.get('Response', None)
        self.db = Database('./destiny.sqlite3')

    async def _dbinit(self):
        if not os.path.exists('./destiny.sqlite3'):
            await self.download()
        return
    
    async def get_raid_image(self, raid: Raid) -> None:
        image = await self.db.execute("SELECT json FROM DestinyActivityDefinition WHERE id = ?", (raid,), 'pgcrImage')
        return ImageProtocol(image)

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

    async def execute(self, sql: str, params = None, item = None) -> None:
        async with aiosqlite.connect(self.path) as db:
            try:
                cur = await db.execute(sql, params)
                async for row in cur:
                    return json.loads(*row)[item]
            except Exception:
                raise
