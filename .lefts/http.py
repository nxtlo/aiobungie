import sys
import httpx
import asyncio

class HTTPClient:
    __slots__ = ('session', 'key')
    def __init__(self, session = None, key = None):
        self.key = {'X-API_KEY': key}
        self.session = session

    @property
    def get_key(self):
        """Returns the cached api key"""
        return self.key.get("X-API-KEY")

    async def create_session(self):
        self.session = httpx.AsyncClient()

    async def get(self ,url):
        if not self.session:
            await self.create_session()

        async with self.session as client:
            data = await client.get(url, headers=self.get_key)
            if data.status_code == 200:
                try:
                    return data.json()
                except httpx.HTTPError as e:
                    print(f"HTTP error due to {e.with_traceback}")
                    sys.exit(1)
