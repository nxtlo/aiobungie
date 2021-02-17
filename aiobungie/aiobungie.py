import sys
from .clans import Clans
from .bungie import *
from .player import Player
from .appinfo import AppInfo
import httpx
import asyncio

class Client:
    __slots__ = ('session', 'key', 'loop')
    API_URL = 'https://www.bungie.net/Platform'

    def __init__(self, *, key = None, session: httpx.AsyncClient = None, loop = None):
        self.loop = asyncio.get_event_loop() if not loop else loop
        self.key = {'X-API-KEY': key}
        self.session = session


    def get_key(self, key):
        """Returns the cached api key"""
        return self.key.get(key)


    async def create_session(self):
        """:class: `Aiobungie`: Creates a new session."""
        self.session = httpx.AsyncClient()

    async def fetch(self ,url):
        if not self.session:
            await self.create_session()

        async with self.session as client:
            data = await client.get(url, headers=self.get_key("X-API-KEY"))
            if data.status_code == 200:
                try:
                    return data.json()
                except httpx.HTTPError as e:
                    print(f"HTTP error due to {e.with_traceback}")
                    sys.exit(1)


    async def get_player(self, name = None):
        """:class: `Aiobungie`: Returns the aviliable player data."""
        resp = await self.fetch(f'{self.API_URL}/Destiny2/SearchDestinyPlayer/All/{name}')
        if resp is None:
            print("Player not found,")
            return
        return Player(resp)

    async def get_careers(self):
        """Returns the aviliable careers at Bungie"""
        resp = await self.fetch(f"{self.API_URL}/Content/Careers")
        return Careers(resp)

    async def get_app(self, appid = None):
        """Returns info about the application"""
        resp = await self.fetch(f"{self.API_URL}/App/Application/{appid}")
        return AppInfo(resp)

    async def get_clan(self, clanid: int = None):
        """
        :class: `Aiobungie`: Returns the clan information.
        """
        resp = await self.fetch(f'{self.API_URL}/Group/{clanid}/ClanMembers')
        return Clans(resp)
