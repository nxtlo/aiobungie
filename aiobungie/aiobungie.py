from .bungie import Careers
from .player import Player
from .appinfo import AppInfo
from .clans import Clans
from typing import Dict
import copy
import aiohttp
import asyncio

class Client(object):
    """The base class the all Clients must inherit from."""

    __slots__ = ('session', 'key', 'loop')
    API_URL = 'https://www.bungie.net/Platform'

    def __init__(self, *, key = None, session: aiohttp.ClientSession = None, loop = None):
        self.loop = asyncio.get_event_loop() if not loop else loop
        self.key: Dict = {'X-API-KEY': key}
        self.session = session
        super().__init__()


    def get_key(self, key):
        """an easier access to get the api key."""
        node = copy.copy(self.key.get(key))
        return node

    @classmethod
    def qual_name(cls):
        return cls.__qualname__

    def __repr__(self):
        return f"<{self.__class__}, key: {self.key}, session: {self.session}, loop: {self.loop}>"


    def __contains__(self, key):
        return key in self.key


    async def create_session(self):
        """Creates a new aiohttp Client Session"""
        self.session = aiohttp.ClientSession()


    async def close(self):
        await self.session.close()


    async def fetch(self ,url):
        if not self.session:
            await self.create_session()

        async with self.session as client:
            data = await client.get(url, headers=self.get_key("X-API-KEY"))
            if data.status == 200:
                try:
                    return await data.json()
                except Exception:
                    return await data.text()


    async def get_player(self, name: str):
        """
        Parameters
        -----------
        name: str
            The Player's Name

        Returns
        --------
        :class:`list`
            A list of Destiny memberships if given a full GamerTag.
        """
        resp = await self.fetch(f'{self.API_URL}/Destiny2/SearchDestinyPlayer/All/{name}')
        if resp is None:
            print("Player not found,")
            return
        return Player(resp)


    async def get_careers(self):
        """
        Returns
        --------
        :class:`list`
            Returns all available Careers at bungie.net.
        """
        resp = await self.fetch(f"{self.API_URL}/Content/Careers")
        return Careers(resp)


    async def get_app(self, appid: int):
        """
        Returns
        --------
        Returns all available application data.

        Parameters
        -----------
        appid: int
            The application id.
        """
        resp = await self.fetch(f"{self.API_URL}/App/Application/{appid}")
        return AppInfo(resp)


    async def get_clan(self, clanid: int):
        """
        Returns
        --------
        Returns information about a destiny2 clan

        Parameters
        -----------
        clanid: int
            The clan id.
        """
        resp = await self.fetch(f'{self.API_URL}/GroupV2/{clanid}')
        return Clans(resp)
