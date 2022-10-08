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

"""Standard aiobungie API client implementation."""

from __future__ import annotations

__all__: tuple[str, ...] = ("Client",)

import copy
import logging
import typing

from aiobungie import rest as rest_
from aiobungie import traits
from aiobungie.crates import fireteams
from aiobungie.crates import user
from aiobungie.internal import enums
from aiobungie.internal import factory as factory_
from aiobungie.internal import helpers
from aiobungie.internal import iterators

if typing.TYPE_CHECKING:
    import asyncio
    import collections.abc as collections

    from aiobungie import interfaces
    from aiobungie import typedefs
    from aiobungie.crates import activity
    from aiobungie.crates import application
    from aiobungie.crates import clans
    from aiobungie.crates import components
    from aiobungie.crates import entity
    from aiobungie.crates import friends
    from aiobungie.crates import milestones
    from aiobungie.crates import profile

_LOG: typing.Final[logging.Logger] = logging.getLogger("aiobungie.client")


class Client(traits.ClientApp):
    """Standard Bungie API client application.

    This client deserialize the REST JSON responses using `aiobungie.internal.factory.Factory`
    and returns `aiobungie.crates` Python object implementations of the responses.

    A `aiobungie.RESTClient` REST client can also be used alone for low-level concepts.

    Example
    -------
    ```py
    import aiobungie

    client = aiobungie.Client('...')

    async def main():
        async with client.rest:
            user = await client.fetch_current_user_memberships('...')
            print(user)
    ```

    Parameters
    -----------
    token: `str`
        Your Bungie's API key or Token from the developer's portal.

    Other Parameters
    ----------------
    rest_client: `aiobungie.interfaces.RESTInterface | None`
        An optional rest client instance you can pass.
        If set to `None` then the client will use the default instance.

    max_retries : `int`
        The max retries number to retry if the request hit a `5xx` status code.
    max_ratelimit_retries : `int`
        The max retries number to retry if the request hit a `429` status code. Defaults to `3`.
    client_secret : `str | None`
        An optional application client secret,
        This is only needed if you're fetching OAuth2 tokens with this client.
    client_id : `int | None`
        An optional application client id,
        This is only needed if you're fetching OAuth2 tokens with this client.
    """

    __slots__ = ("_rest", "_factory", "_client_secret", "_client_id")

    def __init__(
        self,
        token: str,
        /,
        client_secret: typing.Optional[str] = None,
        client_id: typing.Optional[int] = None,
        *,
        rest_client: typing.Optional[interfaces.RESTInterface] = None,
        max_retries: int = 4,
        max_ratelimit_retries: int = 3,
    ) -> None:

        self._client_secret = client_secret
        self._client_id = client_id

        self._rest = (
            rest_client
            if rest_client is not None
            else rest_.RESTClient(
                token,
                client_secret,
                client_id,
                max_retries=max_retries,
                max_ratelimit_retries=max_ratelimit_retries,
            )
        )

        self._factory = factory_.Factory(self)

    @property
    def factory(self) -> factory_.Factory:
        return self._factory

    @property
    def rest(self) -> interfaces.RESTInterface:
        return self._rest

    @property
    def request(self) -> Client:
        return copy.copy(self)

    @property
    def metadata(self) -> collections.MutableMapping[typing.Any, typing.Any]:
        return self._rest.metadata

    def run(
        self, future: collections.Coroutine[typing.Any, None, None], debug: bool = False
    ) -> None:
        loop: typing.Final[asyncio.AbstractEventLoop] = helpers.get_or_make_loop()
        try:
            if not loop.is_running():
                loop.set_debug(debug)
                loop.run_until_complete(future)

        except Exception as exc:
            raise RuntimeError(f"Failed to run {future.__qualname__}") from exc

        except KeyboardInterrupt:
            _LOG.warn("Unexpected Keyboard interrupt. Exiting.")
            return

    # * User methods.

    async def fetch_current_user_memberships(self, access_token: str, /) -> user.User:
        """Fetch and return a user object of the bungie net user associated with account.

        .. warning::
            This method requires OAuth2 scope and a Bearer access token.

        Parameters
        ----------
        access_token : `str`
            A valid Bearer access token for the authorization.

        Returns
        -------
        `aiobungie.crates.user.User`
            A user object includes the Destiny memberships and Bungie.net user.
        """
        resp = await self.rest.fetch_current_user_memberships(access_token)

        return self.factory.deserialize_user(resp)

    async def fetch_bungie_user(self, id: int, /) -> user.BungieUser:
        """Fetch a Bungie user by their BungieNet id.

        .. note::
            This returns a Bungie user membership only. Take a look at `Client.fetch_membership_from_id`
            for other memberships.

        Parameters
        ----------
        id: `int`
            The user id.

        Returns
        -------
        `aiobungie.crates.user.BungieUser`
            A Bungie user.

        Raises
        ------
        `aiobungie.error.NotFound`
            The user was not found.
        """
        payload = await self.rest.fetch_bungie_user(id)

        return self.factory.deserialize_bungie_user(payload)

    async def search_users(
        self, name: str, /
    ) -> iterators.Iterator[user.SearchableDestinyUser]:
        """Search for players and return all players that matches the same name.

        Parameters
        ----------
        name : `buildins.str`
            The user name.

        Returns
        -------
        `aiobungie.iterators.Iterator[aiobungie.crates.DestinyMembership]`
            A sequence of destiny memberships.
        """
        payload = await self.rest.search_users(name)

        return iterators.Iterator(
            [
                self.factory.deserialize_searched_user(user)
                for user in payload["searchResults"]
            ]
        )

    async def fetch_user_themes(self) -> collections.Sequence[user.UserThemes]:
        """Fetch all available user themes.

        Returns
        -------
        `collections.Sequence[aiobungie.crates.user.UserThemes]`
            A sequence of user themes.
        """
        data = await self.rest.fetch_user_themes()

        return self.factory.deserialize_user_themes(data)

    async def fetch_hard_types(
        self,
        credential: int,
        type: typedefs.IntAnd[enums.CredentialType] = enums.CredentialType.STEAMID,
        /,
    ) -> user.HardLinkedMembership:
        """Gets any hard linked membership given a credential.
        Only works for credentials that are public just `aiobungie.CredentialType.STEAMID` right now.
        Cross Save aware.

        Parameters
        ----------
        credential: `int`
            A valid SteamID64
        type: `aiobungie.CredentialType`
            The credential type. This must not be changed
            Since its only credential that works "currently"

        Returns
        -------
        `aiobungie.crates.user.HardLinkedMembership`
            Information about the hard linked data.
        """

        payload = await self.rest.fetch_hardlinked_credentials(credential, type)

        return user.HardLinkedMembership(
            id=int(payload["membershipId"]),
            type=enums.MembershipType(payload["membershipType"]),
            cross_save_type=enums.MembershipType(payload["CrossSaveOverriddenType"]),
        )

    async def fetch_membership_from_id(
        self,
        id: int,
        /,
        type: typedefs.IntAnd[enums.MembershipType] = enums.MembershipType.NONE,
    ) -> user.User:
        """Fetch Bungie user's memberships from their id.

        Notes
        -----
        * This returns both BungieNet membership and a sequence of the player's DestinyMemberships
        Which includes Stadia, Xbox, Steam and PSN memberships if the player has them,
        see `aiobungie.crates.user.DestinyMembership` for more details.
        * If you only want the bungie user. Consider using `Client.fetch_user` method.

        Parameters
        ----------
        id : `int`
            The user's id.
        type : `aiobungie.MembershipType`
            The user's membership type.

        Returns
        -------
        `aiobungie.crates.User`
            A Bungie user with their membership types.

        Raises
        ------
        aiobungie.NotFound
            The requested user was not found.
        """
        payload = await self.rest.fetch_membership_from_id(id, type)

        return self.factory.deserialize_user(payload)

    async def fetch_user_credentials(
        self, access_token: str, membership_id: int, /
    ) -> collections.Sequence[user.UserCredentials]:
        """Fetch an array of credential types attached to the requested account.

        .. note::
            This method require OAuth2 Bearer access token.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        membership_id : `int`
            The id of the membership to return.

        Returns
        -------
        `collections.Sequence[aiobungie.crates.UserCredentials]`
            A sequence of the attached user credentials.

        Raises
        ------
        `aiobungie.Unauthorized`
            The access token was wrong or no access token passed.
        """
        resp = await self.rest.fetch_user_credentials(access_token, membership_id)

        return self.factory.deserialize_user_credentials(resp)

    # * Destiny 2.

    async def fetch_profile(
        self,
        member_id: int,
        type: typedefs.IntAnd[enums.MembershipType],
        components: list[enums.ComponentType],
        auth: typing.Optional[str] = None,
    ) -> components.Component:
        """
        Fetch a bungie profile passing components to the request.

        Parameters
        ----------
        member_id: `int`
            The member's id.
        type: `aiobungie.MembershipType`
            A valid membership type.
        components : `list[aiobungie.ComponentType]`
            List of profile components to collect and return.

        Other Parameters
        ----------------
        auth : `typing.Optional[str]`
            A Bearer access_token to make the request with.
            This is optional and limited to components that only requires an Authorization token.

        Returns
        --------
        `aiobungie.crates.Component`
            A Destiny 2 player profile with its components.
            Only passed components will be available if they exists. Otherwise they will be `None`

        Raises
        ------
        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """
        data = await self.rest.fetch_profile(member_id, type, components, auth)
        return self.factory.deserialize_components(data)

    async def fetch_linked_profiles(
        self,
        member_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
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
        member_id : `int`
            The ID of the membership. This must be a valid Bungie.Net or PSN or Xbox ID.
        member_type : `aiobungie.MembershipType`
            The type for the membership whose linked Destiny account you want to return.

        Other Parameters
        ----------------
        all : `bool`
            If provided and set to `True`, All memberships regardless
            of whether they're obscured by overrides will be returned,

            If provided and set to `False`, Only available memberships will be returned.
            The default for this is `False`.

        Returns
        -------
        `aiobungie.crates.profile.LinkedProfile`
            A linked profile object.
        """
        resp = await self.rest.fetch_linked_profiles(member_id, member_type, all=all)

        return self.factory.deserialize_linked_profiles(resp)

    async def fetch_player(
        self,
        name: str,
        code: int,
        /,
        type: typedefs.IntAnd[enums.MembershipType] = enums.MembershipType.ALL,
    ) -> collections.Sequence[user.DestinyMembership]:
        """Fetch a Destiny 2 player's memberships.

        Parameters
        -----------
        name: `str`
            The unique Bungie player name.
        code : `int`
            The unique Bungie display name code.
        type: `aiobungie.internal.enums.MembershipType`
            The player's membership type, e,g. XBOX, STEAM, PSN

        Returns
        --------
        `collections.Sequence[aiobungie.crates.DestinyMembership]`
            A sequence of the found Destiny 2 player memberships.
            An empty sequence will be returned if no one found.

        Raises
        ------
        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """
        resp = await self.rest.fetch_player(name, code, type)

        return self.factory.deserialize_destiny_memberships(resp)

    async def fetch_character(
        self,
        member_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
        character_id: int,
        components: list[enums.ComponentType],
        auth: typing.Optional[str] = None,
    ) -> components.CharacterComponent:
        """Fetch a Destiny 2 character.

        Parameters
        ----------
        member_id: `int`
            A valid bungie member id.
        character_id: `int`
            The Destiny character id to retrieve.
        membership_type: `aiobungie.internal.enums.MembershipType`
            The member's membership type.
        components: `list[aiobungie.ComponentType]`
            Multiple arguments of character components to collect and return.

        Other Parameters
        ----------------
        auth : `typing.Optional[str]`
            A Bearer access_token to make the request with.
            This is optional and limited to components that only requires an Authorization token.

        Returns
        -------
        `aiobungie.crates.CharacterComponent`
            A Bungie character component.

        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """
        resp = await self.rest.fetch_character(
            member_id, membership_type, character_id, components, auth
        )

        return self.factory.deserialize_character_component(resp)

    async def fetch_unique_weapon_history(
        self,
        membership_id: int,
        character_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> collections.Sequence[activity.ExtendedWeaponValues]:
        """Fetch details about unique weapon usage for a character. Includes all exotics.

        Parameters
        ----------
        membership_id : `int`
            The Destiny user membership id.
        character_id : `int`
            The character id to retrieve.
        membership_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The Destiny user's membership type.

        Returns
        -------
        `collections.Sequence[aiobungie.crates.ExtendedWeaponValues]`
            A sequence of the weapon's extended values.
        """
        resp = await self._rest.fetch_unique_weapon_history(
            membership_id, character_id, membership_type
        )

        return [
            self._factory.deserialize_extended_weapon_values(weapon)
            for weapon in resp["weapons"]
        ]

    # * Destiny 2 Activities.

    async def fetch_activities(
        self,
        member_id: int,
        character_id: int,
        mode: typedefs.IntAnd[enums.GameMode],
        *,
        membership_type: typedefs.IntAnd[
            enums.MembershipType
        ] = enums.MembershipType.ALL,
        page: int = 0,
        limit: int = 250,
    ) -> iterators.Iterator[activity.Activity]:
        """Fetch a Destiny 2 activity for the specified character id.

        Parameters
        ----------
        member_id: `int`
            The user id that starts with `4611`.
        character_id: `int`
            The id of the character to retrieve the activities for.
        mode: `aiobungie.typedefs.IntAnd[aiobungie.internal.enums.GameMode]`
            This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc.

        Other Parameters
        ----------------
        membership_type: `aiobungie.internal.enums.MembershipType`
            The Member ship type, if nothing was passed than it will return all.
        page: int
            The page number. Default is `0`
        limit: int
            Limit the returned result. Default is `250`.

        Returns
        -------
        `aiobungie.iterators.Iterator[aiobungie.crates.Activity]`
            An iterator of the player's activities.

        Raises
        ------
        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """
        resp = await self.rest.fetch_activities(
            member_id,
            character_id,
            mode,
            membership_type=membership_type,
            page=page,
            limit=limit,
        )

        return self.factory.deserialize_activities(resp)

    async def fetch_post_activity(self, instance_id: int, /) -> activity.PostActivity:
        """Fetch a post activity details.

        Parameters
        ----------
        instance_id: `int`
            The activity instance id.

        Returns
        -------
        `aiobungie.crates.PostActivity`
           A post activity object.
        """
        resp = await self.rest.fetch_post_activity(instance_id)

        return self.factory.deserialize_post_activity(resp)

    async def fetch_aggregated_activity_stats(
        self,
        character_id: int,
        membership_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> iterators.Iterator[activity.AggregatedActivity]:
        """Fetch aggregated activity stats for a character.

        Parameters
        ----------
        character_id: `int`
            The id of the character to retrieve the activities for.
        membership_id: `int`
            The id of the user that started with `4611`.
        membership_type: `aiobungie.internal.enums.MembershipType`
            The Member ship type.

        Returns
        -------
        `aiobungie.iterators.Iterator[aiobungie.crates.AggregatedActivity]`
            An iterator of the player's activities.

        Raises
        ------
        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """
        resp = await self.rest.fetch_aggregated_activity_stats(
            character_id, membership_id, membership_type
        )

        return self.factory.deserialize_aggregated_activities(resp)

    # * Destiny 2 Clans or GroupsV2.

    async def fetch_clan_from_id(
        self,
        id: int,
        /,
        access_token: typing.Optional[str] = None,
    ) -> clans.Clan:
        """Fetch a Bungie Clan by its id.

        Parameters
        -----------
        id: `int`
            The clan id.

        Returns
        --------
        `aiobungie.crates.Clan`
            An Bungie clan.

        Raises
        ------
        `aiobungie.NotFound`
            The clan was not found.
        """
        resp = await self.rest.fetch_clan_from_id(id, access_token)

        return self.factory.deserialize_clan(resp)

    async def fetch_clan(
        self,
        name: str,
        /,
        access_token: typing.Optional[str] = None,
        *,
        type: typedefs.IntAnd[enums.GroupType] = enums.GroupType.CLAN,
    ) -> clans.Clan:
        """Fetch a Clan by its name.
        This method will return the first clan found with given name.

        Parameters
        ----------
        name: `str`
            The clan name

        Other Parameters
        ----------------
        access_token : `typing.Optional[str]`
            An optional access token to make the request with.

            If the token was bound to a member of the clan,
            This field `aiobungie.crates.Clan.current_user_membership` will be available
            and will return the membership of the user who made this request.
        type : `aiobungie.GroupType`
            The group type, Default is aiobungie.GroupType.CLAN.

        Returns
        -------
        `aiobungie.crates.Clan`
            A Bungie clan.

        Raises
        ------
        `aiobungie.NotFound`
            The clan was not found.
        """
        resp = await self.rest.fetch_clan(name, access_token, type=type)

        return self.factory.deserialize_clan(resp)

    async def fetch_clan_conversations(
        self, clan_id: int, /
    ) -> collections.Sequence[clans.ClanConversation]:
        """Fetch the conversations/chat channels of the given clan id.

        Parameters
        ----------
        clan_id : `int`
            The clan id.

        Returns
        `collections.Sequence[aiobungie.crates.ClanConversation]`
            A sequence of the clan chat channels.
        """
        resp = await self.rest.fetch_clan_conversations(clan_id)

        return self.factory.deserialize_clan_conversations(resp)

    async def fetch_clan_admins(
        self, clan_id: int, /
    ) -> iterators.Iterator[clans.ClanMember]:
        """Fetch the clan founder and admins.

        Parameters
        ----------
        clan_id : `int`
            The clan id.

        Returns
        -------
        `aiobungie.iterators.Iterator[aiobungie.crates.ClanMember]`
            An iterator over the found clan admins and founder.

        Raises
        ------
        `aiobungie.NotFound`
            The requested clan was not found.
        """
        resp = await self.rest.fetch_clan_admins(clan_id)

        return self.factory.deserialize_clan_members(resp)

    async def fetch_groups_for_member(
        self,
        member_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
        /,
        *,
        filter: int = 0,
        group_type: enums.GroupType = enums.GroupType.CLAN,
    ) -> collections.Sequence[clans.GroupMember]:
        """Fetch information about the groups that a given member has joined.

        Parameters
        ----------
        member_id : `int`
            The member's id
        member_type : `aiobungie.MembershipType`
            The member's membership type.

        Other Parameters
        ----------------
        filter : `int`
            Filter apply to list of joined groups. This Default to `0`
        group_type : `aiobungie.GroupType`
            The group's type.
            This is always set to `aiobungie.GroupType.CLAN` and should not be changed.

        Returns
        -------
        `collections.Sequence[aiobungie.crates.GroupMember]`
            A sequence of joined groups for the fetched member.
        """
        resp = await self.rest.fetch_groups_for_member(
            member_id, member_type, filter=filter, group_type=group_type
        )

        return [
            self.factory.deserialize_group_member(group) for group in resp["results"]
        ]

    async def fetch_potential_groups_for_member(
        self,
        member_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
        /,
        *,
        filter: int = 0,
        group_type: typedefs.IntAnd[enums.GroupType] = enums.GroupType.CLAN,
    ) -> collections.Sequence[clans.GroupMember]:
        """Fetch the potential groups for a clan member.

        Parameters
        ----------
        member_id : `int`
            The member's id
        member_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The member's membership type.

        Other Parameters
        ----------------
        filter : `int`
            Filter apply to list of joined groups. This Default to `0`
        group_type : `aiobungie.typedefs.IntAnd[aiobungie.GroupType]`
            The group's type.
            This is always set to `aiobungie.GroupType.CLAN` and should not be changed.

        Returns
        -------
        `collections.Sequence[aiobungie.crates.GroupMember]`
            A sequence of joined potential groups for the fetched member.
        """
        resp = await self.rest.fetch_potential_groups_for_member(
            member_id, member_type, filter=filter, group_type=group_type
        )

        return [
            self.factory.deserialize_group_member(group) for group in resp["results"]
        ]

    async def fetch_clan_members(
        self,
        clan_id: int,
        /,
        *,
        name: typing.Optional[str] = None,
        type: typedefs.IntAnd[enums.MembershipType] = enums.MembershipType.NONE,
    ) -> iterators.Iterator[clans.ClanMember]:
        """Fetch Bungie clan members.

        Parameters
        ----------
        clan_id : `int`
            The clans id

        Other Parameters
        ----------------
        name : `typing.Optional[str]`
            If provided, Only players matching this name will be returned.
        type : `aiobungie.MembershipType`
            An optional clan member's membership type.
            This parameter is used to filter the returned results
            by the provided membership, For an example XBox memberships only,
            Otherwise will return all memberships.

        Returns
        -------
        `aiobungie.iterators.Iterator[aiobungie.crates.ClanMember]`
            An iterator over the bungie clan members.

        Raises
        ------
        `aiobungie.NotFound`
            The clan was not found.
        """
        resp = await self.rest.fetch_clan_members(clan_id, type=type, name=name)

        return self.factory.deserialize_clan_members(resp)

    async def fetch_clan_banners(self) -> collections.Sequence[clans.ClanBanner]:
        """Fetch the clan banners.

        Returns
        -------
        `collections.Sequence[aiobungie.crates.ClanBanner]`
            A sequence of the clan banners.
        """
        resp = await self.rest.fetch_clan_banners()

        return self.factory.deserialize_clan_banners(resp)

    # This method is required to be here since it deserialize the clan.
    async def kick_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> clans.Clan:
        """Kick a member from the clan.

        .. note::
            This request requires OAuth2: oauth2: `AdminGroups` scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        group_id: `int`
            The group id.
        membership_id : `int`
            The member id to kick.
        membership_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The member's membership type.

        Returns
        -------
        `aiobungie.crates.clan.Clan`
            The clan that the member was kicked from.
        """
        resp = await self.rest.kick_clan_member(
            access_token,
            group_id=group_id,
            membership_id=membership_id,
            membership_type=membership_type,
        )

        return self.factory.deserialize_clan(resp)

    async def fetch_clan_weekly_rewards(self, clan_id: int) -> milestones.Milestone:
        """Fetch a Bungie clan's weekly reward state.

        Parameters
        ----------
        clan_id : `int`
            The clan's id.

        Returns
        -------
        `aiobungie.crates.Milestone`
            A runtime status of the clan's milestone data.
        """

        resp = await self.rest.fetch_clan_weekly_rewards(clan_id)

        return self.factory.deserialize_milestone(resp)

    # * Destiny 2 Entities aka Definitions.

    async def fetch_inventory_item(self, hash: int, /) -> entity.InventoryEntity:
        """Fetch a static inventory item entity given a its hash.

        Parameters
        ----------
        hash: `int`
            Inventory item's hash.

        Returns
        -------
        `aiobungie.crates.InventoryEntity`
            A bungie inventory item.
        """
        resp = await self.rest.fetch_inventory_item(hash)

        return self.factory.deserialize_inventory_entity(resp)

    async def fetch_objective_entity(self, hash: int, /) -> entity.ObjectiveEntity:
        """Fetch a Destiny objective entity given a its hash.

        Parameters
        ----------
        hash: `int`
            objective's hash.

        Returns
        -------
        `aiobungie.crates.ObjectiveEntity`
            An objective entity item.
        """
        resp = await self.rest.fetch_objective_entity(hash)

        return self.factory.deserialize_objective_entity(resp)

    async def search_entities(
        self, name: str, entity_type: str, *, page: int = 0
    ) -> iterators.Iterator[entity.SearchableEntity]:
        """Search for Destiny2 entities given a name and its type.

        Parameters
        ----------
        name : `str`
            The name of the entity, i.e., Thunderlord, One thousand voices.
        entity_type : `str`
            The type of the entity, AKA Definition,
            For an example `DestinyInventoryItemDefinition` for emblems, weapons, and other inventory items.

        Other Parameters
        ----------------
        page : `int`
            An optional page to return. Default to 0.

        Returns
        -------
        `aiobungie.iterators.Iterator[aiobungie.crates.SearchableEntity]`
            An iterator over the found results matching the provided name.
        """
        resp = await self.rest.search_entities(name, entity_type, page=page)

        return self.factory.deserialize_inventory_results(resp)

    # Fireteams

    async def fetch_fireteams(
        self,
        activity_type: typedefs.IntAnd[fireteams.FireteamActivity],
        *,
        platform: typedefs.IntAnd[
            fireteams.FireteamPlatform
        ] = fireteams.FireteamPlatform.ANY,
        language: typing.Union[
            fireteams.FireteamLanguage, str
        ] = fireteams.FireteamLanguage.ALL,
        date_range: int = 0,
        page: int = 0,
        slots_filter: int = 0,
    ) -> typing.Optional[collections.Sequence[fireteams.Fireteam]]:
        """Fetch public Bungie fireteams with open slots.

        Parameters
        ----------
        activity_type : `aiobungie.typedefs.IntAnd[aiobungie.crates.FireteamActivity]`
            The fireteam activity type.

        Other Parameters
        ----------------
        platform : `aiobungie.typedefs.IntAnd[aiobungie.crates.fireteams.FireteamPlatform]`
            If this is provided. Then the results will be filtered with the given platform.
            Defaults to `aiobungie.crates.FireteamPlatform.ANY` which returns all platforms.
        language : `typing.Union[aiobungie.crates.fireteams.FireteamLanguage, str]`
            A locale language to filter the used language in that fireteam.
            Defaults to `aiobungie.crates.FireteamLanguage.ALL`
        date_range : `int`
            An integer to filter the date range of the returned fireteams. Defaults to `aiobungie.FireteamDate.ALL`.
        page : `int`
            The page number. By default its `0` which returns all available activities.
        slots_filter : `int`
            Filter the returned fireteams based on available slots. Default is `0`

        Returns
        -------
        `typing.Optional[collections.Sequence[fireteams.Fireteam]]`
            A sequence of `aiobungie.crates.Fireteam` or `None`.
        """

        resp = await self.rest.fetch_fireteams(
            activity_type,
            platform=platform,
            language=language,
            date_range=date_range,
            page=page,
            slots_filter=slots_filter,
        )

        return self.factory.deserialize_fireteams(resp)

    async def fetch_avaliable_clan_fireteams(
        self,
        access_token: str,
        group_id: int,
        activity_type: typedefs.IntAnd[fireteams.FireteamActivity],
        *,
        platform: typedefs.IntAnd[fireteams.FireteamPlatform],
        language: typing.Union[fireteams.FireteamLanguage, str],
        date_range: int = 0,
        page: int = 0,
        public_only: bool = False,
        slots_filter: int = 0,
    ) -> typing.Optional[collections.Sequence[fireteams.Fireteam]]:
        """Fetch a clan's fireteams with open slots.

        .. note::
            This method requires OAuth2: ReadGroups scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        group_id : `int`
            The group/clan id of the fireteam.
        activity_type : `aiobungie.typedefs.IntAnd[aiobungie.crates.FireteamActivity]`
            The fireteam activity type.

        Other Parameters
        ----------------
        platform : `aiobungie.typedefs.IntAnd[aiobungie.crates.fireteams.FireteamPlatform]`
            If this is provided. Then the results will be filtered with the given platform.
            Defaults to `aiobungie.crates.FireteamPlatform.ANY` which returns all platforms.
        language : `typing.Union[aiobungie.crates.fireteams.FireteamLanguage, str]`
            A locale language to filter the used language in that fireteam.
            Defaults to `aiobungie.crates.FireteamLanguage.ALL`
        date_range : `int`
            An integer to filter the date range of the returned fireteams. Defaults to `0`.
        page : `int`
            The page number. By default its `0` which returns all available activities.
        public_only: `bool`
            If set to True, Then only public fireteams will be returned.
        slots_filter : `int`
            Filter the returned fireteams based on available slots. Default is `0`

        Returns
        -------
        `typing.Optional[collections.Sequence[aiobungie.crates.Fireteam]]`
            A sequence of  fireteams found in the clan.
            `None` will be returned if nothing was found.
        """
        resp = await self.rest.fetch_avaliable_clan_fireteams(
            access_token,
            group_id,
            activity_type,
            platform=platform,
            language=language,
            date_range=date_range,
            page=page,
            public_only=public_only,
            slots_filter=slots_filter,
        )

        return self.factory.deserialize_fireteams(resp)

    async def fetch_clan_fireteam(
        self, access_token: str, fireteam_id: int, group_id: int
    ) -> fireteams.AvailableFireteam:
        """Fetch a specific clan fireteam.

        .. note::
            This method requires OAuth2: ReadGroups scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        group_id : `int`
            The group/clan id to fetch the fireteam from.
        fireteam_id : `int`
            The fireteam id to fetch.

        Returns
        -------
        `typing.Optional[aiobungie.crates.AvailableFireteam]`
            A sequence of available fireteams objects if exists. else `None` will be returned.
        """
        resp = await self.rest.fetch_clan_fireteam(access_token, fireteam_id, group_id)

        return self.factory.deserialize_available_fireteams(
            resp, no_results=True
        )  # type: ignore[return-value]

    async def fetch_my_clan_fireteams(
        self,
        access_token: str,
        group_id: int,
        *,
        include_closed: bool = True,
        platform: typedefs.IntAnd[fireteams.FireteamPlatform],
        language: typing.Union[fireteams.FireteamLanguage, str],
        filtered: bool = True,
        page: int = 0,
    ) -> collections.Sequence[fireteams.AvailableFireteam]:
        """A method that's similar to `fetch_fireteams` but requires OAuth2.

        .. note::
            This method requires OAuth2: ReadGroups scope.

        Parameters
        ----------
        access_token : str
            The bearer access token associated with the bungie account.
        group_id : int
            The group/clan id to fetch.

        Other Parameters
        ----------------
        include_closed : bool
            If provided and set to True, It will also return closed fireteams.
            If provided and set to False, It will only return public fireteams. Default is True.
        platform : aiobungie.typedefs.IntAnd[aiobungie.crates.fireteams.FireteamPlatform]
            If this is provided. Then the results will be filtered with the given platform.
            Defaults to aiobungie.crates.FireteamPlatform.ANY which returns all platforms.
        language : typing.Union[aiobungie.crates.fireteams.FireteamLanguage, str]
            A locale language to filter the used language in that fireteam.
            Defaults to aiobungie.crates.FireteamLanguage.ALL
        filtered : bool
            If set to True, it will filter by clan. Otherwise not. Default is True.
        page : int
            The page number. By default its 0 which returns all available activities.

        Returns
        -------
        `collections.Sequence[aiobungie.crates.AvailableFireteam]`
            A sequence of available fireteams objects if exists. else `None` will be returned.
        """
        resp = await self.rest.fetch_my_clan_fireteams(
            access_token,
            group_id,
            include_closed=include_closed,
            platform=platform,
            language=language,
            filtered=filtered,
            page=page,
        )

        return self.factory.deserialize_available_fireteams(resp)  # type: ignore[return-value]

    # Friends and social.

    async def fetch_friends(
        self, access_token: str, /
    ) -> collections.Sequence[friends.Friend]:
        """Fetch bungie friend list.

        .. note::
            This requests OAuth2: ReadUserData scope.

        Parameters
        -----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Returns
        -------
        `collections.Sequence[aiobungie.crates.Friend]`
            A sequence of the friends associated with that access token.
        """

        resp = await self.rest.fetch_friends(access_token)

        return self.factory.deserialize_friends(resp)

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
        `aiobungie.crates.FriendRequestView`
            A friend requests view of that associated access token.
        """

        resp = await self.rest.fetch_friend_requests(access_token)

        return self.factory.deserialize_friend_requests(resp)

    # Applications and Developer portal.

    async def fetch_application(self, appid: int, /) -> application.Application:
        """Fetch a Bungie application.

        Parameters
        -----------
        appid: `int`
            The application id.

        Returns
        --------
        `aiobungie.crates.Application`
            A Bungie application.
        """
        resp = await self.rest.fetch_application(appid)

        return self.factory.deserialize_app(resp)

    # Milestones

    async def fetch_public_milestone_content(
        self, milestone_hash: int, /
    ) -> milestones.MilestoneContent:
        """Fetch the milestone content given its hash.

        Parameters
        ----------
        milestone_hash : `int`
            The milestone hash.

        Returns
        -------
        `aiobungie.crates.milestones.MilestoneContent`
            A milestone content object.
        """
        resp = await self.rest.fetch_public_milestone_content(milestone_hash)

        return self.factory.deserialize_public_milestone_content(resp)
