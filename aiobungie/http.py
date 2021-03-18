import httpx
import os
# from . import Client

class HTTPClient:
    __slots__ = ('session', 'key')

    def __init__(self, key, session = None):
        self.session = session
        self.key = key

    async def create_session(self):
        """Creates a new aiohttp Client Session"""
        self.session = httpx.AsyncClient()

    async def close(self):
        if not self.session.is_closed:
            await self.session.aclose()
            self.session = None

    async def fetch(self ,url):
        if not self.session:
            await self.create_session()

        async with self.session as client:
            data = await client.get(url, headers={'X-API-KEY': self.key})
            if data.status_code == 200:
                try:
                    return data.json()
                except httpx.DecodingError:
                    return data.text
