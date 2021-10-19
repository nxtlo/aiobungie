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

"""Basic implementation of a client that interacts with the API,
Deserialize the REST payloads and returns `aiobungie.crate` implementations of these objects.
"""

from __future__ import annotations

import logging

__all__: list[str] = ["Client"]

import asyncio
import typing

from aiobungie import rest as rest_
from aiobungie.crate import user
from aiobungie.ext import meta
from aiobungie.internal import enums
from aiobungie.internal import factory
from aiobungie.internal import helpers
from aiobungie.internal import traits

if typing.TYPE_CHECKING:
    from aiobungie import interfaces
    from aiobungie.crate import activity
    from aiobungie.crate import application
    from aiobungie.crate import character
    from aiobungie.crate import clans
    from aiobungie.crate import entity
    from aiobungie.crate import friends
    from aiobungie.crate import milestones
    from aiobungie.crate import profile

_LOG: typing.Final[logging.Logger] = logging.getLogger("aiobungie.client")


class Client(traits.ClientBase):
    """Basic implementation for a client that interacts with Bungie's API.

    Attributes
    -----------
    token: `builtins.str`
        Your Bungie's API key or Token from the developer's portal.
    max_retries : `builtins.int`
        The max retries number to retry if the request hit a `5xx` status code.
    """

    __slots__ = ("_rest", "_serialize", "_token", "_loop")

    def __init__(self, token: str, /, max_retries: int = 4) -> None:
        self._loop: asyncio.AbstractEventLoop = helpers.get_or_make_loop()

        if token is None:
            raise ValueError("Missing the API key!")

        self._rest = rest_.RESTClient(token, max_retries=max_retries)
        self._serialize = factory.Factory(self)
        self._token = token  # We need the token For Manifest.

    @property
    def serialize(self) -> factory.Factory:
        return self._serialize

    @property
    def rest(self) -> interfaces.RESTInterface:
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
        except KeyboardInterrupt:
            _LOG.warn("Unexpected Keyboard interrupt. Exiting.")
            raise SystemExit(None)
        finally:
            # Session management.
            self._loop.run_until_complete(self.rest.close())
            _LOG.info("Client closed normally.")

    # * Unspecified methods. *#

    async def fetch_manifest(self) -> meta.Manifest:
        """Access The bungie Manifest.

        Returns
        -------
        `aiobungie.ext.Manifest`
            A Manifest crate.
        """
        return meta.Manifest(self._token)

    # * User methods.

    async def fetch_own_bungie_user(self, *, access_token: str) -> user.User:
        """Fetch and return a user object of the bungie net user associated with account.

        .. warning::
            This method requires OAuth2 scope and a Bearer access token.
            This token should be stored somewhere safe and just passed as a parameter. e.g., A database.

        Parameters
        ----------
        access_token : `builtins.str`
            A valid Bearer access token for the authorization.

        Returns
        -------
        `aiobungie.crate.user.User`
            A user object includes the Destiny memberships and Bungie.net user.
        """
        resp = await self.rest.fetch_own_bungie_user(access_token)
        assert isinstance(resp, dict)
        return self.serialize.deserialize_user(resp)

    async def fetch_user(self, id: int) -> user.BungieUser:
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

    async def search_users(self, name: str, /) -> typing.Sequence[user.DestinyUser]:
        """Search for players and return all players that matches the same name.

        Parameters
        ----------
        name : `buildins.str`
            The user name.

        Returns
        -------
        `typing.Sequence[aiobungie.crate.DestinyUser]`
            A sequence of destiny memberships.
        """
        payload = await self.rest.search_users(name)
        assert isinstance(payload, dict)
        return self.serialize.deseialize_found_users(payload)

    async def fetch_user_themes(self) -> typing.Sequence[user.UserThemes]:
        """Fetch all available user themes.

        Returns
        -------
        `typing.Sequence[aiobungie.crate.user.UserThemes]`
            A sequence of user themes.
        """
        data = await self.rest.fetch_user_themes()
        assert isinstance(data, list)
        return self.serialize.deserialize_user_themes(data)

    async def fetch_hard_types(
        self,
        credential: int,
        type: helpers.IntAnd[enums.CredentialType] = enums.CredentialType.STEAMID,
        /,
    ) -> user.HardLinkedMembership:
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

        return user.HardLinkedMembership(
            id=int(payload["membershipId"]),
            type=enums.MembershipType(payload["membershipType"]),
            cross_save_type=enums.MembershipType(payload["CrossSaveOverriddenType"]),
        )

    async def fetch_membership_from_id(
        self,
        id: int,
        type: helpers.IntAnd[enums.MembershipType] = enums.MembershipType.NONE,
        /,
    ) -> user.User:
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
        type: helpers.IntAnd[enums.MembershipType],
        /,
    ) -> profile.Profile:
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

    async def fetch_linked_profiles(
        self,
        member_id: int,
        member_type: helpers.IntAnd[enums.MembershipType],
        /,
        *,
        all: bool = False,
    ) -> profile.LinkedProfile:
        """Returns a summary information about all profiles linked to the requested member.

        The passed membership id/type maybe a Bungie.Net membership or a Destiny memberships.

        .. note::
            It will only return linked accounts whose linkages you are allowed to view.

        Parameters
        ----------
        member_id : `builtins.int`
            The ID of the membership. This must be a valid Bungie.Net or PSN or Xbox ID.
        member_type : `aiobungie.MembershipType`
            The type for the membership whose linked Destiny account you want to return.

        Other Parameters
        ----------------
        all : `builtins.bool`
            If provided and set to `True`, All memberships regardless
            of whether thry're obscured by overrides will be returned,

            If provided and set to `False`, Only available memberships will be returned.
            The default for this is `False`.

        Returns
        -------
        `aiobungie.crate.profile.LinkedProfile`
            A linked profile object.
        """
        resp = await self.rest.fetch_linked_profiles(member_id, member_type, all=all)
        assert isinstance(resp, dict)
        return self.serialize.deserialize_linked_profiles(resp)

    async def fetch_player(
        self,
        name: str,
        type: helpers.IntAnd[enums.MembershipType] = enums.MembershipType.ALL,
        /,
    ) -> typing.Sequence[user.DestinyUser]:
        """Fetch a Destiny 2 Player.

        .. note::
            You must also pass the player's unique code.
            A full name parameter should look like this `Fate怒#4275`.

        Parameters
        -----------
        name: `builtins.str`
            The Player's Name.
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
        self,
        memberid: int,
        type: helpers.IntAnd[enums.MembershipType],
        character: enums.Class,
    ) -> character.Character:
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
        return self.serialize.deserialize_character(resp, chartype=character)

    # * Destiny 2 Activities.

    async def fetch_activity(
        self,
        member_id: int,
        character_id: int,
        mode: helpers.IntAnd[enums.GameMode],
        membership_type: helpers.IntAnd[enums.MembershipType],
        *,
        page: int = 1,
        limit: int = 1,
    ) -> activity.Activity:
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
        page: builtins.int
            The page number. Default is `1`
        limit: builtins.int
            Limit the returned result. Default is `1`

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

    async def fetch_post_activity(self, instance: int, /) -> activity.PostActivity:
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

    async def fetch_clan_from_id(self, id: int, /) -> clans.Clan:
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
        return self.serialize.deserialize_clan(resp)

    async def fetch_clan(
        self, name: str, /, type: helpers.IntAnd[enums.GroupType] = enums.GroupType.CLAN
    ) -> clans.Clan:
        """Fetch a Clan by its name.
        This method will return the first clan found with given name.

        Parameters
        ----------
        name: `builtins.str`
            The clan name
        type `aiobungie.GroupType`
            The group type, Default is aiobungie.GroupType.CLAN.

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
        return self.serialize.deserialize_clan(resp)

    async def fetch_clan_conversations(
        self, clan_id: int, /
    ) -> typing.Sequence[clans.ClanConversation]:
        """Fetch the conversations/chat channels of the given clan id.

        Parameters
        ----------
        clan_id : `int`
            The clan id.

        Returns
        `typing.Sequence[aiobungie.crate.ClanConversation]`
            A sequence of the clan chat channels.
        """
        resp = await self.rest.fetch_clan_conversations(clan_id)
        assert isinstance(resp, list)
        return self.serialize.deserialize_clan_convos(resp)

    async def fetch_clan_admins(
        self, clan_id: int, /
    ) -> typing.Sequence[clans.ClanAdmin]:
        """Fetch the clan founder and admins.

        Parameters
        ----------
        clan_id : `builtins.int`
            The clan id.

        Returns
        -------
        `typing.Sequence[aiobungie.crate.ClanAdmin]`
            A sequence of the found clan admins and founder.

        Raises
        ------
        `aiobungie.ClanNotFound`
            The requested clan was not found.
        """
        resp = await self.rest.fetch_clan_admins(clan_id)
        assert isinstance(resp, dict)
        return self.serialize.deserialize_clan_admins(resp)

    async def fetch_groups_for_member(
        self,
        member_id: int,
        member_type: helpers.IntAnd[enums.MembershipType],
        /,
        *,
        filter: int = 0,
        group_type: enums.GroupType = enums.GroupType.CLAN,
    ) -> typing.Optional[clans.GroupMember]:
        """Fetch information about the groups that a given member has joined.

        Parameters
        ----------
        member_id : `builtins.int`
            The member's id
        member_type : `aiobungie.MembershipType`
            The member's membership type.

        Other Parameters
        ----------------
        filter : `builsins.int`
            Filter apply to list of joined groups. This Default to `0`
        group_type : `aiobungie.GroupType`
            The group's type.
            This is always set to `aiobungie.GroupType.CLAN` and should not be changed.

        Returns
        -------
        `typing.Optional[aiobungie.crate.clans.GroupMember]`
            The member if found and `None` if not.
        """
        resp = await self.rest.fetch_groups_for_member(
            member_id, member_type, filter=filter, group_type=group_type
        )
        assert isinstance(resp, dict)
        return self.serialize.deserialize_group_member(resp)

    async def fetch_potential_groups_for_member(
        self,
        member_id: int,
        member_type: helpers.IntAnd[enums.MembershipType],
        /,
        *,
        filter: int = 0,
        group_type: helpers.IntAnd[enums.GroupType] = enums.GroupType.CLAN,
    ) -> typing.Optional[clans.GroupMember]:
        """Fetch the potentional groups for a clan member.

        Parameters
        ----------
        member_id : `builtins.int`
            The member's id
        member_type : `aiobungie.internal.helpers.IntAnd[aiobungie.MembershipType]`
            The member's membership type.

        Other Parameters
        ----------------
        filter : `builsins.int`
            Filter apply to list of joined groups. This Default to `0`
        group_type : `aiobungie.internal.helpers.IntAnd[aiobungie.GroupType]`
            The group's type.
            This is always set to `aiobungie.GroupType.CLAN` and should not be changed.

        Returns
        -------
        `typing.Optional[aiobungie.crate.GroupMember]`
            An optional information about the group member.
        """
        resp = await self.rest.fetch_potential_groups_for_member(
            member_id, member_type, filter=filter, group_type=group_type
        )
        assert isinstance(resp, dict)
        return self.serialize.deserialize_group_member(resp)

    async def fetch_clan_member(
        self,
        clan_id: int,
        name: typing.Optional[str] = None,
        type: helpers.IntAnd[enums.MembershipType] = enums.MembershipType.NONE,
        /,
    ) -> clans.ClanMember:
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
        self,
        clan_id: int,
        type: helpers.IntAnd[enums.MembershipType] = enums.MembershipType.NONE,
        /,
    ) -> typing.Sequence[clans.ClanMember]:
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

    async def fetch_clan_banners(self) -> typing.Sequence[clans.ClanBanner]:
        """Fetch the clan banners.

        Returns
        -------
        `typing.Sequence[aiobungie.crate.ClanBanner]`
            A sequence of the clan banners.
        """
        resp = await self.rest.fetch_clan_banners()
        assert isinstance(resp, dict)
        return self.serialize.deserialize_clan_banners(resp)

    # This method is required to be here since it deserialize the clan.
    async def kick_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: helpers.IntAnd[enums.MembershipType],
    ) -> clans.Clan:
        """Kick a member from the clan.

        .. note::
            This request requires OAuth2: oauth2: `AdminGroups` scope.

        Parameters
        ----------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.
        group_id: `int`
            The group id.
        membership_id : `int`
            The member id to kick.
        membership_type : `aiobungie.internal.helpers.IntAnd[aiobungie.MembershipType]`
            The member's membership type.

        Returns
        -------
        `aiobungie.crate.clan.Clan`
            The clan that represents the kicked member.
        """
        resp = await self.rest.kick_clan_member(
            access_token,
            group_id=group_id,
            membership_id=membership_id,
            membership_type=membership_type,
        )
        assert isinstance(resp, dict)
        return self.serialize.deserialize_clan(resp, bound=True)

    # * Destiny 2 Definitions. Entities.

    async def fetch_inventory_item(self, hash: int, /) -> entity.InventoryEntity:
        """Fetch a static inventory item entity given a its hash.

        Parameters
        ----------
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

    async def fetch_friends(
        self, access_token: str, /
    ) -> typing.Sequence[friends.Friend]:
        """Fetch bungie friend list.

        .. note::
            This requests OAuth2: ReadUserData scope.

        Parameters
        -----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Returns
        -------
        `typing.Sequence[aiobungie.crate.Friend]`
            A sequence of the found friends.
        """

        resp = await self.rest.fetch_friends(access_token)
        assert isinstance(resp, dict)
        return self.serialize.deserialize_friends(resp)

    async def fetch_friend_requests(
        self, access_token: str, /
    ) -> friends.FriendRequestView:
        """Fetch pending bungie friend requests queue.

        .. note::
            This requests OAuth2: ReadUserData scope.

        Parameters
        -----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Returns
        -------
        `aiobungie.crate.FriendRequestView`
            A friend requests view object includes a sequence of incoming and outgoing requests.
        """

        resp = await self.rest.fetch_friend_requests(access_token)
        assert isinstance(resp, dict)
        return self.serialize.deserialize_friend_requests(resp)

    async def fetch_app(self, appid: int, /) -> application.Application:
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

    async def fetch_public_milestone_content(
        self, milestone_hash: int, /
    ) -> milestones.Milestone:
        """Fetch the milestone content given its hash.

        Parameters
        ----------
        milestone_hash : `builtins.int`
            The milestone hash.

        Returns
        -------
        `aiobungie.crate.milestones.Milestone`
            A milestone object.
        """
        resp = await self.rest.fetch_public_milestone_content(milestone_hash)
        assert isinstance(resp, dict)
        return self.serialize.deserialize_public_milestone_content(resp)
