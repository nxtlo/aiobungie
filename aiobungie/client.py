# MIT License
#
# Copyright (c) 2020 - Present nxtlo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""The base aiobungie Client that your should inherit from / use."""


from __future__ import annotations

__all__: typing.Sequence[str] = [
    "Client",
]

import asyncio
import typing

from aiobungie.ext import Manifest
from aiobungie.internal import cache as cache_
from aiobungie.internal import deprecated
from aiobungie.internal import impl
from aiobungie.internal import serialize as serialize_
from aiobungie.objects import activity

from . import objects
from .http import HTTPClient
from .internal.enums import Class
from .internal.enums import GameMode
from .internal.enums import MembershipType


class Client(impl.BaseClient):
    """Represents a client that connects to the Bungie API

    Attributes
    -----------
    token: `builtins.str`
        Your Bungie's API key or Token from the developer's portal.
    loop: `asyncio.AbstractEventLoop`
        asyncio event loop.
    """

    __slots__: typing.Sequence[str] = ("loop", "http", "_cache", "_serialize", "_token")

    def __init__(self, token: str, *, loop: asyncio.AbstractEventLoop = None) -> None:
        self.loop: asyncio.AbstractEventLoop = (  # asyncio loop.
            asyncio.get_event_loop() if not loop else loop
        )

        # Redis hash cache for testing purposes only.
        # This requires a redis server running for usage.
        self._cache = cache_.Cache(loop=self.loop)

        if not token:
            raise ValueError("Missing the API key!")

        # HTTP Client
        self.http: HTTPClient = HTTPClient(key=token, loop=self.loop)

        # DeSerilaizing payloads
        self._serialize = serialize_.Deserialize(self)

        self._token = token  # We need the token For Manifest.
        super().__init__()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    @property
    def cache(self) -> cache_.Cache:
        return self._cache

    @property
    def serialize(self) -> serialize_.Deserialize:
        return self._serialize

    @property
    def rest(self) -> "Client":
        return self

    def run(
        self, future: typing.Coroutine[typing.Any, None, None], debug: bool = False
    ) -> None:
        """Runs a Coro function until its complete.
        This is equivalent to asyncio.get_event_loop().run_until_complete(...)

        Parameters
        ----------
        future: `typing.Coroutine[typing.Any, typing.Any, typing.Any]`
            Your coro function.

        Example
        -------
        ```py
        async def main() -> None:
            player = await client.fetch_player("Fate")
            print(player.name)

        client.run(main())
        ```
        """
        try:
            if not self.loop.is_running():
                if debug:
                    self.loop.set_debug(True)
                self.loop.run_until_complete(future)
        except asyncio.CancelledError:
            raise

    async def from_path(self, path: str) -> typing.Any:
        """Raw http search given a valid bungie endpoint.

        Parameters
        ----------
        path: `builtins.str`
            The bungie endpoint or path.
            A path must look something like this
            "Destiny2/3/Profile/46111239123/..."

        Returns
        -------
        `typing.Any`
            Any object.
        """
        return await self.http.static_search(path)

    async def fetch_manifest(self) -> Manifest:
        """Access The bungie Manifest.

        Returns
        -------
        `aiobungie.ext.Manifest`
            A Manifest object.
        """
        resp = await self.http.fetch_manifest()
        return Manifest(self._token, resp)

    async def fetch_user(self, name: str, *, position: int = 0) -> objects.User:
        """Fetches a Bungie user by their name.

        Parameters
        ----------
        name: `builtins.str`
            The user name.
        position: `builtins.int`
            The user position/index in the list to return,
            Will returns the first one if not specified.

        Raises
        ------
        `aiobungie.error.UserNotFound`
            The user wasa not found.
        """
        data = await self.http.fetch_user(name=name)
        assert isinstance(data, list)
        user_mod = self._serialize.deserialize_user(data, position)
        return user_mod

    async def fetch_user_from_id(self, id: int) -> objects.User:
        """Fetches a Bungie user by their id.

        Parameters
        ----------
        id: `builtins.int`
            The user id.
        position: `builtins.int`
            The user position/index in the list to return,
            Will returns the first one if not specified.

        Raises
        ------
        `aiobungie.error.UserNotFound`
            The user wasa not found.
        """
        payload = await self.http.fetch_user_from_id(id)
        assert isinstance(payload, dict)
        # User and User from id has the same attrs but different return types so we have to ignore here.
        return self._serialize.deserialize_user(payload)  # type: ignore

    async def fetch_profile(
        self,
        memberid: int,
        type: MembershipType,
        /,
    ) -> objects.Profile:
        """
        Fetches a bungie profile.

        See `aiobungie.objects.Profile` to access other components.

        Paramaters
        ----------
        memberid: `builtins.int`
            The member's id.
        type: `aiobungie.MembershipType`
            A valid membership type.

        Returns
        --------
        `aiobungie.objects.Profile`
            An aiobungie member profile.
        """
        data = await self.http.fetch_profile(memberid, type)
        assert isinstance(data, dict)
        return self._serialize.deserialize_profile(data)

    async def fetch_player(
        self, name: str, type: MembershipType, *, position: int = 0
    ) -> objects.Player:
        """Fetches a Destiny2 Player.

        Parameters
        -----------
        name: `builtins.str`
            The Player's Name
        type: `aiobungie.internal.enums.MembershipType`
            The player's membership type, e,g. XBOX, STEAM, PSN
        position: `builtins.int`
            Which player position to return, first player will return if None.

        Returns
        --------
        `aiobungie.objects.Player`
            An aiobungie Destiny 2 Player object
        """
        resp = await self.http.fetch_player(name, type)
        assert isinstance(resp, list)
        return self._serialize.deserialize_player(payload=resp, position=position)

    async def fetch_character(
        self, memberid: int, type: MembershipType, character: Class
    ) -> objects.Character:
        """Fetches a Destiny 2 character.

        Parameters
        ----------
        memberid: `builtins.int`
            A valid bungie member id.
        character: `aiobungie.internal.enums.Class`
            The Destiny character to retrieve.
        type: `aiobungie.internal.enums.MembershipType`
            The member's membership type.

        Returns
        -------
        `aiobungie.objects.Character`
            An aiobungie character object.

        Raises
        ------
        `aiobungie.error.CharacterError`
            raised if the Character was not found.
        """
        resp = await self.http.fetch_character(
            memberid=memberid, type=type, character=character
        )
        assert isinstance(resp, dict)
        char_module = self.serialize.deserialize_character(resp, chartype=character)
        return char_module

    async def fetch_vendor_sales(
        self,
    ) -> typing.Any:
        """Fetch vendor sales."""
        return await self.http.fetch_vendor_sales()

    @deprecated
    async def fetch_activity(
        self,
        userid: int,
        charid: int,
        mode: GameMode,
        memtype: MembershipType,
        *,
        page: typing.Optional[int] = 1,
        limit: typing.Optional[int] = 1,
    ) -> None:
        """Fetches a Destiny 2 activity for the specified user id and character.

        Parameters
        ----------
        userid: `builtins.int`
            The user id that starts with `4611`.
        charaid: `builtins.int`
            The id of the character to retrieve.
        mode: `aiobungie.internal.enums.GameMode`
            This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc.
        memtype: `aiobungie.internal.enums.MembershipType`
            The Member ship type, if nothing was passed than it will return all.
        page: typing.Optional[builtins.int]
            The page number
        limit: typing.Optional[builtins.int]
            Limit the returned result.

        Returns
        -------
        `aiobungie.objects.Activity`
            An aiobungie Activity object.

        Raises
        ------
        `AttributeError`
            Using `aiobungie.objects.Activity.hash` for non raid activies.
        `aiobungie.error.ActivityNotFound`
            Any other errors occures during the response.
        """
        resp = await self.http.fetch_activity(
            userid, charid, mode, memtype=memtype, page=page, limit=limit
        )
        pass

    async def fetch_app(self, appid: int, /) -> objects.Application:
        """Fetches a Bungie Application.

        Parameters
        -----------
        appid: `builtins.int`
            The application id.

        Returns
        --------
        `aiobungie.objects.Application`
            An aiobungie application object.
        """
        resp = await self.http.fetch_app(appid)
        assert isinstance(resp, dict)
        return self._serialize.deserialize_app(resp)

    async def fetch_clan_from_id(self, id: int, /) -> objects.Clan:
        """Fetches a Bungie Clan by its id.

        Parameters
        -----------
        id: `builtins.int`
            The clan id.

        Returns
        --------
        `aiobungie.objects.Clan`
            An aioungie clan object
        """
        resp = await self.http.fetch_clan_from_id(id)
        assert isinstance(resp, dict)
        return self._serialize.deseialize_clan(resp)

    async def fetch_clan(self, name: str, /, type: int = 1) -> objects.Clan:
        """Fetches a Clan by its name and returns the first result.

        Parameters
        ----------
        name: `builtins.str`
            The clan name
        type `builtins.int`
            The group type, Default is one.

        Returns
        -------
        `aiobungie.objects.Clan`
            An aiobungie clan object.
        """
        resp = await self.http.fetch_clan(name, type)
        assert isinstance(resp, dict)
        return self._serialize.deseialize_clan(resp)

    # These are not documented for a reason.
    # See: `aiobungie.objects.Clan.fetch_member()`
    # and `aiobungie.objects.Clan.fetch_members()`

    async def fetch_clan_member(
        self,
        id: int,
        name: typing.Optional[str] = None,
        type: MembershipType = MembershipType.NONE,
        /,
    ) -> objects.clans.ClanMember:

        resp = await self.http.fetch_clan_members(id, type, name)
        assert isinstance(resp, dict)
        return self._serialize.deserialize_clan_member(resp)

    async def fetch_clan_members(
        self, id: int, type: MembershipType = MembershipType.NONE, /
    ) -> typing.Dict[str, int]:

        resp = await self.http.fetch_clan_members(id, type, page=1)
        assert isinstance(resp, dict)
        return self._serialize.deserialize_clan_members(resp)

    async def fetch_inventory_item(
        self, hash: int, /
    ) -> objects.entity.InventoryEntity:
        """Fetches a static inventory item entity given a its hash.

        Paramaters
        ----------
        type: `builtins.str`
            Entity's type definition.
        hash: `builtins.int`
            Entity's hash.

        Returns
        -------
        `aiobungie.objects.InventoryEntity`
            A bungie inventory item.
        """
        resp = await self.http.fetch_inventory_item(hash)
        assert isinstance(resp, dict)
        return self._serialize.deserialize_inventory_entity(resp)
