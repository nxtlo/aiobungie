from .objects import *
from .http import HTTPClient
import httpx
import asyncio

class Client(object):
    """The base class the all Clients must inherit from."""

    __slots__ = ('_client', 'key', 'loop')
    API_URL = 'https://www.bungie.net/Platform'

    def __init__(self, key = None, *, session: httpx.AsyncClient = None, loop = None):
        self.loop = asyncio.get_event_loop() if not loop else loop
        self.key = key
        self._client = HTTPClient(session=session, key=key)
        super().__init__()


    def __repr__(self):
        return f"<{self.__class__}, key: {self.key}, Client: {self._client}, loop: {self.loop}>"

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
        resp = await self._client.fetch(f'{self.API_URL}/Destiny2/SearchDestinyPlayer/All/{name}')
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
        resp = await self._client.fetch(f"{self.API_URL}/Content/Careers")
        return Careers(resp)


    async def get_app(self, appid: int):
        """
        Returns
        --------
        :class:`list`
            Returns all available application data.

        Parameters
        -----------
        appid: int
            The application id.
        """
        resp = await self._client.fetch(f"{self.API_URL}/App/Application/{appid}")
        return AppInfo(resp)


    async def get_clan(self, clanid: int):
        """
        Returns
        --------
        :class:`list`
            Returns information about a destiny2 clan

        Parameters
        -----------
        clanid: int
            The clan id.
        """
        resp = await self._client.fetch(f'{self.API_URL}/GroupV2/{clanid}')
        return Clans(resp)
