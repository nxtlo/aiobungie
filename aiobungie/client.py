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

import asyncio
import httpx
from .objects import *
from .utils.enums import MembershipType, DestinyCharecter, Component, GameMode, Vendor
from . import error
from .http import HTTPClient
from typing import Any, Optional, List, Sequence, Union, Dict

__all__: Sequence[str] = (
    'Client',
)
class Client(object):
    """The base class the all Clients must inherit from."""

    __slots__: Sequence[str] = ('_client', 'key', 'loop')
    API_URL: str = 'https://www.bungie.net/Platform'

    def __init__(self, key = None, *, session: httpx.AsyncClient = None, loop = None) -> None:
        self.loop = asyncio.get_event_loop() if not loop else loop
        self.key: str = key
        if not self.key:
            raise ValueError("Missing the API key!")
        self._client = HTTPClient(session=session, key=key)
        super().__init__()

    async def from_path(self, path: str):
        return await self._client.fetch(f'{self.API_URL}/{path}')

    async def get_manifest(self) -> Optional[Manifest]:
        resp = await self._client.fetch(f'{self.API_URL}/Destiny2/Manifest')
        return Manifest(resp)

    async def get_player(self, name: str, type: MembershipType = MembershipType.ALL) -> Optional[Player]:
        """
        Parameters
        -----------
        name: :class:`str`
            The Player's Name

        Returns
        --------
        :class:`list`
            A list of Destiny memberships if given a full GamerTag.
        """
        resp = await self._client.fetch(f'{self.API_URL}/Destiny2/SearchDestinyPlayer/{type}/{name}')
        return Player(resp)


    async def get_charecter(self, memberid: int, type: MembershipType, character: DestinyCharecter) -> Character:
        """
        Fetches a destiny character and returns its data.

        Paramaters
        -----------
            memberid: :class:`int`
                A valid bungie member id.

            character: :class:`.DestinyCharacter`
                a Destiny character -> .WARLOCK, .TITAN, .HUNTER
            
            type: :class:`.MembershipType`
                The membership type -> .STEAM, .XBOX, .PSN

        Returns
        -------
            Character: A Destiny character.

        Raises
        -------
            :exc:`.PlayerNotFound` 
                raised if the Character was not found.
        """
        resp = await self._client.fetch(f'{self.API_URL}/Destiny2/{type}/Profile/{memberid}/?components={Component.CHARECTERS}')
        return Character(char=character, data=resp)

    async def get_vendor_sales(self, 
                                    vendor: Optional[Union[Vendor, int]], 
                                    memberid: int, 
                                    charid: int, 
                                    type: MembershipType
                                    ):
        return await self._client.fetch(
            f'{self.API_URL}/Destiny2/{type}/Profile/{memberid}/Character/{charid}/Vendors/{vendor}/?components={Component.VENDOR_SALES}'
            )

    async def get_activity_stats(
        self,
        userid: int,
        character: int,
        type: Optional[Union[MembershipType, None]] = MembershipType.ALL,
        mode: Optional[GameMode] = None,
        page: Optional[int] = 0,
        limit: int = 1
        ) -> Activity:
        '''
        Returns
        --------
        Optional[:class:`list`]

        Paramaters
        ----------
        userid: :class:`int`
            The user id that starts with `4611`.

        character: :class:`int`
            The id of the character to retrieve.
        
        type: Optional[:class:`.MembershipType`]
            The Member ship type, if nothing was passed than it will return all.
        
        mode: Optional[:class:`.GameMode`]
            This paramater filters the game mode, Nightfall, Strike, Iron Banner, etc.

        page: Optional[:class:`int`]
            The page number

        limit: Optional[:class:`int`]
            Limits the returned result.
        '''
        resp = await self._client.fetch(
            f"{self.API_URL}/Destiny2/{type}/Account/{userid}/Character/{character}/Stats/Activities/?page={page}&count={limit}&mode={mode}"
            )
        try:
            return Activity(data=resp)

        except AttributeError:
            raise error.HashError(
                ".hash method is only used for raids, please remove it and use .raw_hash() instead"
                )
        except TypeError:
            raise error.ActivityNotFound(
                "Error has been occurred during getting your data, maybe the page is out of index or not found?\n"
                f"Actual response: {resp!r}"
                )

    async def get_clan_admins(self, clanid: int) -> Optional[Dict[str, Any]]:
        resp = await self._client.fetch(f'{self.API_URL}/GroupV2/{clanid}/AdminsAndFounder/')
        return ClanAdmins(**resp)


    async def get_careers(self) -> None:
        """
        Returns
        --------
        :class:`list`
            Returns all available Careers at bungie.net.
        """
        resp = await self._client.fetch(f"{self.API_URL}/Content/Careers")
        return Careers(resp)


    async def get_app(self, appid: int) -> List[Any]:
        """
        Returns
        --------
        :class:`list`
            Returns all available application data.

        Parameters
        -----------
        appid: :class:`int`
            The application id.
        """
        resp = await self._client.fetch(f"{self.API_URL}/App/Application/{appid}")
        return AppInfo(resp)


    async def get_clan(self, clanid: int) -> List[Clans]:
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
