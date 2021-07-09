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
from . import error
from typing import (
    Any, 
    Optional, 
    Sequence, 
    Union, 
    # TYPE_CHECKING
    )

#if TYPE_CHECKING:
from .http import HTTPClient
from .objects import ( 
    Activity
    , AppInfo
    , Clan
    , Manifest
    , Player
    , Character
)
from .utils.enums import (
    MembershipType
    , DestinyCharecter
    , Component
    , GameMode
    , Vendor
)
from .utils.helpers import deprecated


__all__: Sequence[str] = (
    'Client',
)
class Client:
    """Represents a client that connects to the Bungie API

    Attributes
    -----------
    key: :class:`str`:
        Your Bungie's API key or Token from the developer's portal.
    loop: :class:`asyncio.AbstractEventLoop`:
        asyncio event loop.
    """
    def __init__(
        self, 
        key: str, 
        *, 
        loop: asyncio.AbstractEventLoop = None
        ) -> None:
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop() if not loop else loop
        self.key: str = key

        if not self.key:
            raise ValueError("Missing the API key!")
        self.http: HTTPClient = HTTPClient(key=key)
        super().__init__()

    async def from_path(self, path: str) -> Any:
        return await self.http.static_search(path)

    @deprecated
    async def fetch_manifest(self) -> Optional[Manifest]:
        resp = await self.http.fetch_manifest()
        return Manifest(resp)


    async def fetch_player(self, name: str, type: Union[MembershipType, int], /) -> Player:
        """
        Parameters
        -----------
        name: :class:`str`
            The Player's Name
        type: Union[:class:`.MembershipType`, :class:`int`]:
            The player's membership type, e,g. XBOX, STEAM, PSN

        Returns
        --------
        :class:`.Player`
            a Destiny Player object
        """
        resp = await self.http.fetch_player(name, type)
        return Player(data=resp)


    async def fetch_charecter(self, memberid: int, type: MembershipType, character: DestinyCharecter) -> Character:
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
        :class:`.Character`:
            a Bungie character object.

        Raises
        -------
            :exc:`.CharacterNotFound` 
                raised if the Character was not found.
        """
        resp = await self.http.fetch_character(memberid=memberid, type=type, character=character)
        return Character(char=character, data=resp)


    @deprecated
    async def fetch_vendor_sales(self, 
        vendor: Optional[Union[Vendor, int]], 
        memberid: int, 
        charid: int, 
        type: MembershipType
        ) -> Any:
        return await self.http.fetch('GET',
            f'Destiny2/{type}/Profile/{memberid}/Character/{charid}/Vendors/{vendor}/?components={Component.VENDOR_SALES}'
            )

    async def fetch_activity(
        self,
        userid: int,
        charid: int,
        mode: Union[GameMode, int], *,
        memtype: Optional[Union[int, MembershipType]] = MembershipType.ALL,
        page: Optional[int] = 1,
        limit: Optional[int] = 1
        ) -> Activity:
        '''
        Paramaters
        ----------
        userid: :class:`int`
            The user id that starts with `4611`.
        charaid: :class:`int`
            The id of the character to retrieve.
        mode: :class:`.GameMode`
            This paramater filters the game mode, Nightfall, Strike, Iron Banner, etc.
        memtype: Optional[Union[:class:`int`, :class:`.MembershipType`]]
            The Member ship type, if nothing was passed than it will return all.
        page: Optional[:class:`int`]
            The page number
        limit: Optional[:class:`int`]
            Limits the returned result.

        Returns
        --------
        :class:`.Activity`:
            A bungie Activity object.

        Raises
        ------
        `AttributeError`
            Using :meth:`Activity.hash()` for non raid activies.
        `ActivityNotFound`
            Any other errors occures during the response.

        '''
        resp = await self.http.fetch_activity(userid, charid, mode, memtype=memtype, page=page, limit=limit)
        try:
            return Activity(data=resp)

        except AttributeError:
            raise error.HashError(
                ".hash method is only used for raids, please remove it and use .raw_hash() instead"
                )
        except TypeError:
            raise error.ActivityNotFound(
                "Error has been occurred during getting your data, maybe the page is out of index or not found?\n")

    async def fetch_app(self, appid: int, /) -> AppInfo:
        """
        Returns
        --------
        :class:`.AppInfo`:
            a Bungie application object.

        Parameters
        -----------
        appid: :class:`int`
            The application id.
        """
        resp = await self.http.fetch_app(appid)
        return AppInfo(resp)


    async def fetch_clan(self, clanid: int, /) -> Clan:
        """
        Returns
        --------
        :class:`.Clan`:
            A Bungie clan object

        Parameters
        -----------
        clanid: :class:`int`:
            The clan id.
        """
        resp = Clan(data=(await self.http.fetch_clan(clanid)))
        return resp