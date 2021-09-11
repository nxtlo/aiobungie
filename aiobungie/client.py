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
from aiobungie.internal import helpers
from aiobungie.internal import serialize as serialize_
from aiobungie.internal import traits

from . import crate
from . import rest as rest_
from .internal.enums import Class
from .internal.enums import CredentialType
from .internal.enums import GameMode
from .internal.enums import GroupType
from .internal.enums import MembershipType


class Client(traits.RESTful):
    """Basic implementation for a client that interacts with Bungie's API.

    Attributes
    -----------
    token: `builtins.str`
        Your Bungie's API key or Token from the developer's portal.
    """

    __slots__ = ("_rest", "_serialize", "_token", "_loop")

    def __init__(self, token: str, **kwargs: typing.Any) -> None:
        self._loop: asyncio.AbstractEventLoop = helpers.get_or_make_loop()

        if not token:
            raise ValueError("Missing the API key!")

        self._rest = rest_.RESTClient(token=token)
        self._serialize = serialize_.Deserialize(self)
        self._token = token  # We need the token For Manifest.

    @property
    def serialize(self) -> serialize_.Deserialize:
        return self._serialize

    @property
    def rest(self) -> rest_.RESTClient:
        return self._rest

    @property
    def request(self) -> Client:
        return self

    def run(
        self, future: typing.Coroutine[typing.Any, None, None], debug: bool = False
    ) -> None:
        try:
            if not self._loop.is_running():
                if debug:
                    self._loop.set_debug(True)
                self._loop.run_until_complete(future)
        except Exception as exc:
            raise RuntimeError(f"Failed to run {future.__name__}", exc)

    async def __aenter__(self):
        return self

    async def __aexit__(self, _, __, ___) -> None:
        return None

    # * Unspecified methods. *#

    async def from_path(self, path: str, **kwargs: typing.Any) -> typing.Any:
        """Raw http search given a valid bungie endpoint.

        Parameters
        ----------
        path: `builtins.str`
            The bungie endpoint or path.
            A path must look something like this
            "Destiny2/3/Profile/46111239123/..."
        kwargs: `typing.Any`
            Any other key words you'd like to pass through.

        Returns
        -------
        `typing.Any`
            Any object.
        """
        return await self.rest.static_search(path, **kwargs)

    async def fetch_manifest(self) -> Manifest:
        """Access The bungie Manifest.

        Returns
        -------
        `aiobungie.ext.Manifest`
            A Manifest crate.
        """
        return Manifest(self._token)

    # * User methods.

    async def fetch_user(self, id: int) -> crate.user.BungieUser:
        """Fetch a Bungie user by their id.

        .. note::
            This returns a Bungie user membership only. Take a look at `Client.fetch_membership_from_id`
            for other memberships.

        Parameters
        ----------
        id: `builtins.int`
            The user id.

        Returns
        -------
        `aiobungie.crate.user.BungieUser`
            A Bungie user.

        Raises
        ------
        `aiobungie.error.UserNotFound`
            The user was not found.
        """
        payload = await self.rest.fetch_user(id)
        assert isinstance(payload, dict)
        return self.serialize.deserialize_bungie_user(payload)

    async def fetch_user_themes(self) -> typing.Sequence[crate.user.UserThemes]:
        """Fetch all available user themes.

        Returns
        -------
        `typing.Sequence[aiobungie.crate.user.UserThemes]`
            A sequence of user themes.
        """
        data = await self.rest.fetch_user_themes()
        return self.serialize.deserialize_user_themes(data)

    async def fetch_hard_types(
        self, credential: int, type: CredentialType = CredentialType.STEAMID, /
    ) -> crate.user.HardLinkedMembership:
        """Gets any hard linked membership given a credential.
        Only works for credentials that are public just `aiobungie.CredentialType.STEAMID` right now.
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

        # This doesn't really needs to be serialized like other stuff
        # since the dict only contains 3 keys.
        payload = await self.rest.fetch_hard_linked(credential, type)
        assert isinstance(payload, dict)

        return crate.user.HardLinkedMembership(
            id=int(payload["membershipId"]),
            type=MembershipType(payload["membershipType"]),
            cross_save_type=MembershipType(payload["CrossSaveOverriddenType"]),
        )

    async def fetch_membership_from_id(
        self, id: int, type: MembershipType = MembershipType.NONE, /
    ) -> crate.User:
        """Fetch Bungie user's memberships from their id.

        Notes
        -----
        * This returns both BungieNet membership and a sequence of the player's DestinyMemberships
        Which includes Stadia, Xbox, Steam and PSN memberships if the player has them,
        see `aiobungie.crate.user.DestinyUser` for indetailed.
        * If you only want the bungie user. Consider using `Client.fetch_user` method.

        Parameters
        ----------
        id : `builtins.int`
            The user's id.
        type : `aiobungie.MembershipType`
            The user's membership type.

        Returns
        -------
        `aiobungie.crate.User`
            A Bungie user with their membership types.

        Raises
        ------
        aiobungie.UserNotFound
            The requested user was not found.
        """
        payload = await self.rest.fetch_membership_from_id(id, type)
        assert isinstance(payload, dict)
        return self.serialize.deserialize_user(payload)

    # * Destiny 2 methods.

    async def fetch_profile(
        self,
        memberid: int,
        type: MembershipType,
        /,
    ) -> crate.Profile:
        """
        Fetche a bungie profile.

        See `aiobungie.crate.Profile` to access other components.

        Parameters
        ----------
        memberid: `builtins.int`
            The member's id.
        type: `aiobungie.MembershipType`
            A valid membership type.

        Returns
        --------
        `aiobungie.crate.Profile`
            A Destiny 2 player profile.

        Raises
        ------
        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """
        data = await self.rest.fetch_profile(memberid, type)
        assert isinstance(data, dict)
        return self.serialize.deserialize_profile(data)

    async def fetch_player(
        self, name: str, type: MembershipType = MembershipType.ALL, /
    ) -> typing.Sequence[crate.user.DestinyUser | None]:
        """Fetch a Destiny 2 Player.

        Parameters
        -----------
        name: `builtins.str`
            The Player's Name.

        .. note::
            You must also pass the player's unique code.
            A full name parameter should look like this
            `Fate怒#4275`

        type: `aiobungie.internal.enums.MembershipType`
            The player's membership type, e,g. XBOX, STEAM, PSN

        Returns
        --------
        `typing.Sequence[aiobungie.crate.Player]`
            A sequence of the found Destiny 2 Player memberships.

        Raises
        ------
        `aiobungie.PlayerNotFound`
            The player was not found.

        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """
        resp = await self.rest.fetch_player(name, type)
        assert isinstance(resp, list)
        return self.serialize.deserialize_player(resp)

    async def fetch_character(
        self, memberid: int, type: MembershipType, character: Class
    ) -> crate.Character:
        """Fetch a Destiny 2 character.

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
            A Bungie character crate.

        Raises
        ------
        `aiobungie.error.CharacterError`
            raised if the Character was not found.

        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """
        resp = await self.rest.fetch_character(memberid, type)
        assert isinstance(resp, dict)
        char_module = self.serialize.deserialize_character(resp, chartype=character)
        return char_module

    @deprecated
    async def fetch_vendor_sales(self) -> typing.Any:
        """Fetch vendor sales."""
        return await self.rest.fetch_vendor_sales()

    # * Destiny 2 Activities.

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
        """Fetch a Destiny 2 activity for the specified user id and character.

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
            A Bungie activity.

        Raises
        ------
        `aiobungie.error.ActivityNotFound`
            The activity was not found.

        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """
        resp = await self.rest.fetch_activity(
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
        """Fetch a post activity details.

        .. warning::
            This http request is not implemented yet
            and it will raise `NotImplementedError`

        Parameters
        ----------
        instance: `builtins.int`
            The activity instance id.

        Returns
        -------
        `aiobungie.crate.activity.PostActivity`
           Information about the requested post activity.
        """
        # resp = await self.rest.fetch_post_activity(instance)
        # assert isinstance(resp, list)
        raise NotImplementedError

    # * Destiny 2 Clans or GroupsV2.

    async def fetch_clan_from_id(self, id: int, /) -> crate.Clan:
        """Fetch a Bungie Clan by its id.

        Parameters
        -----------
        id: `builtins.int`
            The clan id.

        Returns
        --------
        `aiobungie.crate.Clan`
            An Bungie clan.

        Raises
        ------
        `aiobungie.ClanNotFound`
            The clan was not found.
        """
        resp = await self.rest.fetch_clan_from_id(id)
        assert isinstance(resp, dict)
        return self.serialize.deseialize_clan(resp)

    async def fetch_clan(
        self, name: str, /, type: GroupType = GroupType.CLAN
    ) -> crate.Clan:
        """Fetch a Clan by its name.
        This method will return the first clan found with given name name.

        Parameters
        ----------
        name: `builtins.str`
            The clan name
        type `aiobungie.GroupType`
            The group type, Default is one.

        Returns
        -------
        `aiobungie.crate.Clan`
            A Bungie clan.

        Raises
        ------
        `aiobungie.ClanNotFound`
            The clan was not found.
        """
        resp = await self.rest.fetch_clan(name, type)
        assert isinstance(resp, dict)
        return self.serialize.deseialize_clan(resp)

    async def fetch_clan_member(
        self,
        clan_id: int,
        name: typing.Optional[str] = None,
        type: MembershipType = MembershipType.NONE,
        /,
    ) -> crate.clans.ClanMember:
        """Fetch a Bungie Clan member.

        .. note::
            This method also can be also accessed via
            `aiobungie.crate.Clan.fetch_member()`
            to fetch a member for the fetched clan.

        Parameters
        ----------
        clan_id : `builsins.int`
            The clans id
        name : `builtins.str`
            The clan member's name
        type : `aiobungie.MembershipType`
            An optional clan member's membership type.
            Default is set to `aiobungie.MembershipType.NONE`
            Which returns the first matched clan member by their name.

        Returns
        -------
        `aiobungie.crate.ClanMember`
            A Bungie Clan member.

        Raises
        ------
        `aiobungie.ClanNotFound`
            The clan was not found.

        `aiobungie.NotFound`
            The member was not found.
        """

        resp = await self.rest.fetch_clan_members(clan_id, type, name)
        assert isinstance(resp, dict)
        return self.serialize.deserialize_clan_member(resp)

    async def fetch_clan_members(
        self, clan_id: int, type: MembershipType = MembershipType.NONE, /
    ) -> typing.Sequence[crate.clans.ClanMember]:
        """Fetch a Bungie Clan member. if no members found in the clan
        you will get an empty sequence.

        .. note::
            This method also can be also accessed via
            `aiobungie.crate.Clan.fetch_members()`
            to fetch a member for the fetched clan.

        Parameters
        ----------
        clan_id : `builsins.int`
            The clans id
        type : `aiobungie.MembershipType`
            An optional clan member's membership type.
            Default is set to `aiobungie.MembershipType.NONE`
            Which returns the first matched clan member by their name.

        Returns
        -------
        `typing.Sequence[aiobungie.crate.ClanMember]`
            A sequence of bungie clan members.

        Raises
        ------
        `aiobungie.ClanNotFound`
            The clan was not found.
        """
        resp = await self.rest.fetch_clan_members(clan_id, type)
        assert isinstance(resp, dict)
        return self.serialize.deserialize_clan_members(resp)

    # * Destiny 2 Definitions. Entities.

    async def fetch_inventory_item(self, hash: int, /) -> crate.entity.InventoryEntity:
        """Fetch a static inventory item entity given a its hash.

        Parameters
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
        resp = await self.rest.fetch_inventory_item(hash)
        assert isinstance(resp, dict)
        return self.serialize.deserialize_inventory_entity(resp)

    # * These methods should be for Special bungie endpoints, i.e,
    # * Applications, Forums, Polls, Trending, etc.

    async def fetch_app(self, appid: int, /) -> crate.Application:
        """Fetch a Bungie Application.

        Parameters
        -----------
        appid: `builtins.int`
            The application id.

        Returns
        --------
        `aiobungie.crate.Application`
            A Bungie application.
        """
        resp = await self.rest.fetch_app(appid)
        assert isinstance(resp, dict)
        return self.serialize.deserialize_app(resp)
