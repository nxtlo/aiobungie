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

__all__: list[str] = ["Client"]

import asyncio
import typing

from aiobungie.ext import Manifest
from aiobungie.internal import deprecated
from aiobungie.internal import impl
from aiobungie.internal import serialize as serialize_

from . import crate
from .http import HTTPClient
from .internal.enums import Class
from .internal.enums import CredentialType
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

    __slots__: tuple[str, ...] = ("loop", "http", "_serialize", "_token")

    def __init__(self, token: str, *, loop: asyncio.AbstractEventLoop = None) -> None:
        self.loop: asyncio.AbstractEventLoop = (  # asyncio loop.
            asyncio.get_event_loop() if not loop else loop
        )

        # Redis hash cache for testing purposes only.
        # This requires a redis server running for usage.

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
    def serialize(self) -> serialize_.Deserialize:
        return self._serialize

    @property
    def request(self) -> Client:
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
            A Manifest crate.
        """
        resp = await self.http.fetch_manifest()
        return Manifest(self._token, resp)

    async def fetch_user(self, name: str, *, position: int = 0) -> crate.User:
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
        user_mod = self.serialize.deserialize_user(data, position)
        return user_mod

    async def fetch_user_from_id(self, id: int) -> crate.User:
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
        return self.serialize.deserialize_user(payload)  # type: ignore

    async def fetch_hard_types(
        self, credential: int, type: CredentialType = CredentialType.STEAMID, /
    ) -> crate.user.HardLinkedMembership:
        """Gets any hard linked membership given a credential.
        Only works for credentials that are public just STEAMID from `aiobungie.CredentialType` right now.
        Cross Save aware.

        Parameters
        ----------
        credential: `builtins.int`
            A valid SteamID64
        type: `aiobungie.CredentialType`
            The crededntial type. This must not be changed
            Since its only credential that works "currently"

        Returns
        -------
        `aiobungie.crate.user.HardLinkedMembership`
            Information about the hard linked data.
        """

        # This doens't really needs to be serialized like other stuff
        # since the dict only contains 3 keys.
        payload = await self.http.fetch_hard_linked(credential, type)
        assert isinstance(payload, dict)

        return crate.user.HardLinkedMembership(
            id=int(payload["membershipId"]),
            type=MembershipType(payload["membershipType"]),
            cross_save_type=MembershipType(payload["CrossSaveOverriddenType"]),
        )

    async def fetch_profile(
        self,
        memberid: int,
        type: MembershipType,
        /,
    ) -> crate.Profile:
        """
        Fetches a bungie profile.

        See `aiobungie.crate.Profile` to access other components.

        Paramaters
        ----------
        memberid: `builtins.int`
            The member's id.
        type: `aiobungie.MembershipType`
            A valid membership type.

        Returns
        --------
        `aiobungie.crate.Profile`
            An aiobungie member profile.
        """
        data = await self.http.fetch_profile(memberid, type)
        assert isinstance(data, dict)
        return self.serialize.deserialize_profile(data)

    async def fetch_player(
        self, name: str, type: MembershipType, *, position: int = 0
    ) -> crate.Player:
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
        `aiobungie.crate.Player`
            An aiobungie Destiny 2 Player crate
        """
        resp = await self.http.fetch_player(name, type)
        assert isinstance(resp, list)
        return self.serialize.deserialize_player(payload=resp, position=position)

    async def fetch_character(
        self, memberid: int, type: MembershipType, character: Class
    ) -> crate.Character:
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
        `aiobungie.crate.Character`
            An aiobungie character crate.

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

    @deprecated
    async def fetch_vendor_sales(self) -> typing.Any:
        """Fetch vendor sales."""
        return await self.http.fetch_vendor_sales()

    async def fetch_activity(
        self,
        member_id: int,
        character_id: int,
        mode: GameMode,
        membership_type: MembershipType,
        *,
        page: typing.Optional[int] = 1,
        limit: typing.Optional[int] = 1,
    ) -> crate.activity.Activity:
        """Fetches a Destiny 2 activity for the specified user id and character.

        Parameters
        ----------
        member_id: `builtins.int`
            The user id that starts with `4611`.
        character_id: `builtins.int`
            The id of the character to retrieve.
        mode: `aiobungie.internal.enums.GameMode`
            This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc.
        membership_type: `aiobungie.internal.enums.MembershipType`
            The Member ship type, if nothing was passed than it will return all.
        page: typing.Optional[builtins.int]
            The page number
        limit: typing.Optional[builtins.int]
            Limit the returned result.

        Returns
        -------
        `aiobungie.crate.Activity`
            An aiobungie Activity crate.

        Raises
        ------
        `aiobungie.error.ActivityNotFound`
            The activity was not found.
        """
        resp = await self.http.fetch_activity(
            member_id,
            character_id,
            mode,
            membership_type=membership_type,
            page=page,
            limit=limit,
        )
        assert isinstance(resp, dict)
        return self.serialize.deserialize_activity(resp)

    async def fetch_post_activity(
        self, instance: int, /
    ) -> crate.activity.PostActivity:
        """Fetchs a post activity details.

        Parameters
        ----------
        instance: `builtins.int`
            The activity instance id.

        Returns
        -------
        `aiobungie.crate.activity.PostActivity`
           Information about the requested post activity.
        """
        # resp = await self.http.fetch_post_activity(instance)
        # assert isinstance(resp, list)
        raise NotImplementedError

    async def fetch_app(self, appid: int, /) -> crate.Application:
        """Fetches a Bungie Application.

        Parameters
        -----------
        appid: `builtins.int`
            The application id.

        Returns
        --------
        `aiobungie.crate.Application`
            An aiobungie application crate.
        """
        resp = await self.http.fetch_app(appid)
        assert isinstance(resp, dict)
        return self.serialize.deserialize_app(resp)

    async def fetch_clan_from_id(self, id: int, /) -> crate.Clan:
        """Fetches a Bungie Clan by its id.

        Parameters
        -----------
        id: `builtins.int`
            The clan id.

        Returns
        --------
        `aiobungie.crate.Clan`
            An aioungie clan crate
        """
        resp = await self.http.fetch_clan_from_id(id)
        assert isinstance(resp, dict)
        return self.serialize.deseialize_clan(resp)

    async def fetch_clan(self, name: str, /, type: int = 1) -> crate.Clan:
        """Fetches a Clan by its name and returns the first result.

        Parameters
        ----------
        name: `builtins.str`
            The clan name
        type `builtins.int`
            The group type, Default is one.

        Returns
        -------
        `aiobungie.crate.Clan`
            An aiobungie clan crate.
        """
        resp = await self.http.fetch_clan(name, type)
        assert isinstance(resp, dict)
        return self.serialize.deseialize_clan(resp)

    # These are not documented for a reason.
    # See: `aiobungie.crate.Clan.fetch_member()`
    # and `aiobungie.crate.Clan.fetch_members()`

    async def fetch_clan_member(
        self,
        id: int,
        name: typing.Optional[str] = None,
        type: MembershipType = MembershipType.NONE,
        /,
    ) -> crate.clans.ClanMember:

        resp = await self.http.fetch_clan_members(id, type, name)
        assert isinstance(resp, dict)
        return self.serialize.deserialize_clan_member(resp)

    async def fetch_clan_members(
        self, id: int, type: MembershipType = MembershipType.NONE, /
    ) -> typing.Sequence[crate.clans.ClanMember]:

        resp = await self.http.fetch_clan_members(id, type, page=1)
        assert isinstance(resp, dict)
        return self.serialize.deserialize_clan_members(resp)

    async def fetch_inventory_item(self, hash: int, /) -> crate.entity.InventoryEntity:
        """Fetches a static inventory item entity given a its hash.

        Paramaters
        ----------
        type: `builtins.str`
            Entity's type definition.
        hash: `builtins.int`
            Entity's hash.

        Returns
        -------
        `aiobungie.crate.InventoryEntity`
            A bungie inventory item.
        """
        resp = await self.http.fetch_inventory_item(hash)
        assert isinstance(resp, dict)
        return self.serialize.deserialize_inventory_entity(resp)
