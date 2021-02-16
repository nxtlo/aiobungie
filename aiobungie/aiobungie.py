import sys
from .player import Player
import httpx
import asyncio

class Client:

    __slots__ = ('session', 'key', 'loop')
    API_URL = 'https://www.bungie.net/Platform'

    def __init__(self, key = None, session: httpx.AsyncClient = None, loop = None):
        self.loop = asyncio.get_event_loop() if not loop else loop
        self.key = {'X-API-KEY': key}
        self.session = session

    @property
    def get_key(self):
        """Returns the cached api key"""
        return self.key.get("X-API-KEY")

    async def create_session(self):
        """:class: `Aiobungie`: Creates a new session."""
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

    async def get_player(self, name = None):
        """:class: `Aiobungie`: Returns the aviliable player data."""
        resp = await self.get(self.API_URL + '/Destiny2/SearchDestinyPlayer/All/' + name)
        if resp is None:
            print("Player not found,")
            return
        return Player(resp)

    async def get_clan(self, clanid = None):
        """
        :class: `Aiobungie`: Returns the clan information.
        """
        if not clanid:
            raise ValueError
        resp = await self.get(self.API_URL + '' + clanid)
        return resp

    async def get_weapon(self, name = None):
        """
        :class: `Aiobungie`: Returns the avilibale information about a weapon.
        """
        if not name:
            raise NameError
        resp = await self.get(self.API_URL + name)
        #return Weapons(resp)
