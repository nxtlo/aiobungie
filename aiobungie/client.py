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

    async def get_avatar(self, avatar: int):
        resp = await self._client.fetch(f'{self.API_URL}/.../{avatar}')
        # return Emblem(resp)


    async def get_clan_admins(self, clanid: int):
        resp = await self._client.fetch(f'{self.API_URL}/GroupV2/{clanid}/AdminsAndFounder/')
        return ClanAdmins(**resp)


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
