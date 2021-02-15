import httpx
from .player import Player

class Aiobungie:
    __slots__ = ('session', 'key')
    API_URL = 'https://www.bungie.net/platform/'

    def __init__(self, session = None, key = None):
        self.session = session
        self.key = {"X-API-KEY": key}

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
                except Exception:
                    raise

    async def get_player(self, name = None):
        resp = await self.get(self.API_URL + name)
        return Player(resp)

    async def get_clan(self, clanid = None):
        """
        :class: `Aiobungie`: Returns the clan information.
        """
        if not clanid:
            raise ValueError
        else:
            resp = await self.get(self.API_URL + clanid)
            return resp

    async def get_weapon(self, name = None):
        """
        :class: `Aiobungie`: Returns the avilibale information about a weapon.
        """
        if not name:
            raise NameError
        else:
            resp = await self.get(self.API_URL + name)
            #return Weapons(resp)

    async def close(self):
        if self.session.is_closed:
            return
        await self.session.aclose()
