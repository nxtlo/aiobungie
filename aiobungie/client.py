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

"""A higher-level single process client implementation."""

from __future__ import annotations

__all__ = ("Client",)

import typing

import sain

from aiobungie import framework
from aiobungie import rest as rest_
from aiobungie import traits
from aiobungie.crates import fireteams, user
from aiobungie.internal import enums, helpers

if typing.TYPE_CHECKING:
    import collections.abc as collections

    from aiobungie import api, builders
    from aiobungie.crates import (
        activity,
        application,
        clans,
        components,
        entity,
        friends,
        milestones,
        profile,
    )


class Client(traits.Compact):
    """Compact standard client implementation.

    This client is the way to be able to start sending requests over the REST API and receiving deserialized response objects.

    Refer to `aiobungie.RESTClient` if you prefer to use a more lower-level client.

    Example
    -------
    ```py
    import aiobungie
    import asyncio

    async def main():
        client = aiobungie.Client('token')
        async with client.rest:
            user = await client.fetch_bungie_user(20315338)
            print(user)

    asyncio.run(main())
    ```

    Parameters
    -----------
    token: `str`
        Your Bungie's API key or Token from the developer's portal.

    Other Parameters
    ----------------
    client_secret : `str | None`
        An optional application client secret,
        This is only needed if you're fetching OAuth2 tokens with this client.
    client_id : `int | None`
        An optional application client id,
        This is only needed if you're fetching OAuth2 tokens with this client.
    settings: `aiobungie.builders.Settings | None`
        The client settings to use, if `None` the default will be used.
    max_retries : `int`
        The max retries number to retry if the request hit a `5xx` status code.
    debug: `"TRACE" | bool | int`
        The level of logging to enable.
    """

    __slots__ = ("_rest", "_framework")

    def __init__(
        self,
        token: str,
        /,
        *,
        client_secret: str | None = None,
        client_id: int | None = None,
        settings: builders.Settings | None = None,
        max_retries: int = 4,
        debug: typing.Literal["TRACE"] | bool | int = False,
    ) -> None:
        self._rest = rest_.RESTClient(
            token,
            client_secret=client_secret,
            client_id=client_id,
            settings=settings,
            max_retries=max_retries,
            debug=debug,
        )

        self._framework = framework.Framework()

    @property
    def framework(self) -> api.Framework:
        return self._framework

    @property
    def rest(self) -> api.RESTClient:
        return self._rest

    @property
    def metadata(self) -> collections.MutableMapping[typing.Any, typing.Any]:
        return self._rest.metadata

    @property
    def settings(self) -> builders.Settings:
        return self._rest.settings

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
        resp = await self._rest.fetch_current_user_memberships(access_token)

        return self._framework.deserialize_user(resp)

    async def fetch_bungie_user(self, id: int, /) -> user.BungieUser:
        """Fetch a Bungie user by their BungieNet id.

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
        payload = await self._rest.fetch_bungie_user(id)
        return self._framework.deserialize_bungie_user(payload)

    async def search_users(
        self, name: str, /
    ) -> sain.Iterator[user.SearchableDestinyUser]:
        """Search for players and return all players that matches the same name.

        Parameters
        ----------
        name : `str`
            The user name.

        Returns
        -------
        `aiobungie.Iterator[aiobungie.crates.SearchableDestinyUser]`
            A sequence of the found users with this name.
        """
        payload = await self._rest.search_users(name)
        return sain.Iter(
            self._framework.deserialize_searched_user(user)
            for user in payload["searchResults"]
        )

    async def fetch_user_themes(self) -> collections.Sequence[user.UserThemes]:
        """Fetch all available user themes.

        Returns
        -------
        `collections.Sequence[aiobungie.crates.user.UserThemes]`
            A sequence of user themes.
        """
        data = await self._rest.fetch_user_themes()

        return self._framework.deserialize_user_themes(data)

    async def fetch_hard_types(
        self,
        credential: int,
        type: enums.CredentialType | int = enums.CredentialType.STEAMID,
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

        payload = await self._rest.fetch_hardlinked_credentials(credential, type)

        return user.HardLinkedMembership(
            id=int(payload["membershipId"]),
            type=enums.MembershipType(payload["membershipType"]),
            cross_save_type=enums.MembershipType(payload["CrossSaveOverriddenType"]),
        )

    async def fetch_membership_from_id(
        self,
        id: int,
        /,
        type: enums.MembershipType | int = enums.MembershipType.NONE,
    ) -> user.User:
        """Fetch a Bungie user's memberships from their Bungie ID.

        This method returns both Bungie user and its Destiny 2 memberships bound to it.

        Parameters
        ----------
        id : `int`
            A Bungie.net user's ID. It looks something like this `20315338`
        type : `aiobungie.MembershipType`
            The user's membership type. This is optional.

        Returns
        -------
        `aiobungie.crates.User`
            A Bungie user with their membership types.

        Raises
        ------
        `aiobungie.NotFound`
            The requested user was not found.
        """
        payload = await self._rest.fetch_membership_from_id(id, type)

        return self._framework.deserialize_user(payload)

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
        resp = await self._rest.fetch_user_credentials(access_token, membership_id)

        return self._framework.deserialize_user_credentials(resp)

    async def fetch_sanitized_membership(
        self, membership_id: int, /
    ) -> user.SanitizedMembership:
        """Fetch a list of all display names linked to `membership_id`, Which is profanity filtered.

        Parameters
        ----------
        membership_id: `int`
            The membership ID to fetch

        Returns
        -------
        `aiobungie.crates.SanitizedMembership`
            A JSON object contains all the available display names.
        """
        response = await self._rest.fetch_sanitized_membership(membership_id)
        return self._framework.deserialize_sanitized_membership(response)

    # * Destiny 2.

    async def fetch_profile(
        self,
        member_id: int,
        type: enums.MembershipType | int,
        components: collections.Sequence[enums.ComponentType],
        auth: str | None = None,
    ) -> components.Component:
        """Fetch a Bungie profile with the required components.

        Example
        -------
        ```py
        my_profile_id = 4611686018484639825
        my_profile = await client.fetch_profile(
            my_profile_id,
            MembershipType.STEAM,
            components=(ComponentType.CHARACTERS,)
        )
        characters = my_profile.characters
        if characters is not None:
            for character in characters.values():
                print(character.power_level)
        ```

        Parameters
        ----------
        member_id: `int`
            The profile membership's id.
        type: `aiobungie.MembershipType`
            The profile's membership type.
        components : `collections.Sequence[aiobungie.ComponentType]`
            A sequence of components to collect. If the sequence is empty, then all components will be `None`.

        Other Parameters
        ----------------
        auth : `str | None`
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
        data = await self._rest.fetch_profile(member_id, type, components, auth)
        return self._framework.deserialize_components(data)

    async def fetch_linked_profiles(
        self,
        member_id: int,
        member_type: enums.MembershipType | int,
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
        resp = await self._rest.fetch_linked_profiles(member_id, member_type, all=all)

        return self._framework.deserialize_linked_profiles(resp)

    async def fetch_membership(
        self,
        name: str,
        code: int,
        /,
        type: enums.MembershipType | int = enums.MembershipType.ALL,
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
        resp = await self._rest.fetch_membership(name, code, type)

        return self._framework.deserialize_destiny_memberships(resp)

    async def fetch_character(
        self,
        member_id: int,
        membership_type: enums.MembershipType | int,
        character_id: int,
        components: collections.Sequence[enums.ComponentType],
        auth: str | None = None,
    ) -> components.CharacterComponent:
        """Fetch a Destiny 2 character.

        Example
        -------
        ```py
        membership_id, titan_id = 0, 0
        my_character = await client.fetch_character(
            membership_id,
            MembershipType.STEAM,
            titan_id,
            components=(ComponentType.CHARACTER_INVENTORIES,)
        )
        inventory = my_character.inventory
        if inventory is not None:
            for item in inventory.values():
                print(item)
        ```

        Parameters
        ----------
        member_id: `int`
            A valid bungie member id.
        character_id: `int`
            The Destiny character id to retrieve.
        membership_type: `aiobungie.internal.enums.MembershipType`
            The member's membership type.
        components: `collections.Sequence[aiobungie.ComponentType]`
            Multiple arguments of character components to collect and return.

        Other Parameters
        ----------------
        auth : `str | None`
            A Bearer access_token to make the request with.
            This is optional and limited to components that only requires an Authorization token.

        Returns
        -------
        `aiobungie.crates.CharacterComponent`
            A Bungie character component.

        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """
        resp = await self._rest.fetch_character(
            member_id, membership_type, character_id, components, auth
        )

        return self._framework.deserialize_character_component(resp)

    async def fetch_unique_weapon_history(
        self,
        membership_id: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> collections.Sequence[activity.ExtendedWeaponValues]:
        """Fetch details about unique weapon usage for a character. Includes all exotics.

        Parameters
        ----------
        membership_id : `int`
            The Destiny user membership id.
        character_id : `int`
            The character id to retrieve.
        membership_type : `aiobungie.aiobungie.MembershipType | int`
            The Destiny user's membership type.

        Returns
        -------
        `collections.Sequence[aiobungie.crates.ExtendedWeaponValues]`
            A sequence of the weapon's extended values.
        """
        resp = await self._rest.fetch_unique_weapon_history(
            membership_id, character_id, membership_type
        )

        return tuple(
            self._framework.deserialize_extended_weapon_values(weapon)
            for weapon in resp["weapons"]
        )

    # * Destiny 2 Activities.

    async def fetch_activities(
        self,
        member_id: int,
        character_id: int,
        mode: enums.GameMode | int,
        membership_type: enums.MembershipType | int,
        *,
        page: int = 0,
        limit: int = 250,
    ) -> sain.Iterator[activity.Activity]:
        """Fetch a Destiny 2 activity for the specified character id.

        Parameters
        ----------
        member_id: `int`
            The user id that starts with `4611`.
        character_id: `int`
            The id of the character to retrieve the activities for.
        mode: `aiobungie.aiobungie.internal.enums.GameMode | int`
            This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc.
        membership_type: `aiobungie.internal.enums.MembershipType`
            The Destiny 2 membership type.

        Other Parameters
        ----------------
        page: int
            The page number. Default is `0`
        limit: int
            Limit the returned result. Default is `250`.

        Returns
        -------
        `Iterator[aiobungie.crates.Activity]`
            An iterator of the player's activities.

        Raises
        ------
        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """
        resp = await self._rest.fetch_activities(
            member_id,
            character_id,
            mode,
            membership_type=membership_type,
            page=page,
            limit=limit,
        )

        return self._framework.deserialize_activities(resp)

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
        resp = await self._rest.fetch_post_activity(instance_id)

        return self._framework.deserialize_post_activity(resp)

    async def fetch_aggregated_activity_stats(
        self,
        character_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
    ) -> sain.Iterator[activity.AggregatedActivity]:
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
        `Iterator[aiobungie.crates.AggregatedActivity]`
            An iterator of the player's activities.

        Raises
        ------
        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """
        resp = await self._rest.fetch_aggregated_activity_stats(
            character_id, membership_id, membership_type
        )

        return self._framework.deserialize_aggregated_activities(resp)

    # * Destiny 2 Clans or GroupsV2.

    async def fetch_clan_from_id(
        self,
        id: int,
        /,
        access_token: str | None = None,
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
        resp = await self._rest.fetch_clan_from_id(id, access_token)

        return self._framework.deserialize_clan(resp)

    async def fetch_clan(
        self,
        name: str,
        /,
        access_token: str | None = None,
        *,
        type: enums.GroupType | int = enums.GroupType.CLAN,
    ) -> clans.Clan:
        """Fetch a Clan by its name.
        This method will return the first clan found with given name.

        Parameters
        ----------
        name: `str`
            The clan name

        Other Parameters
        ----------------
        access_token : `str | None`
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
        resp = await self._rest.fetch_clan(name, access_token, type=type)

        return self._framework.deserialize_clan(resp)

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
        resp = await self._rest.fetch_clan_conversations(clan_id)

        return self._framework.deserialize_clan_conversations(resp)

    async def fetch_clan_admins(
        self, clan_id: int, /
    ) -> sain.Iterator[clans.ClanMember]:
        """Fetch the clan founder and admins.

        Parameters
        ----------
        clan_id : `int`
            The clan id.

        Returns
        -------
        `aiobungie.Iterator[aiobungie.crates.ClanMember]`
            An iterator over the found clan admins and founder.

        Raises
        ------
        `aiobungie.NotFound`
            The requested clan was not found.
        """
        resp = await self._rest.fetch_clan_admins(clan_id)

        return self._framework.deserialize_clan_members(resp)

    async def fetch_groups_for_member(
        self,
        member_id: int,
        member_type: enums.MembershipType | int,
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
        resp = await self._rest.fetch_groups_for_member(
            member_id, member_type, filter=filter, group_type=group_type
        )

        return tuple(
            self._framework.deserialize_group_member(group) for group in resp["results"]
        )

    async def fetch_potential_groups_for_member(
        self,
        member_id: int,
        member_type: enums.MembershipType | int,
        /,
        *,
        filter: int = 0,
        group_type: enums.GroupType | int = enums.GroupType.CLAN,
    ) -> collections.Sequence[clans.GroupMember]:
        """Fetch the potential groups for a clan member.

        Parameters
        ----------
        member_id : `int`
            The member's id
        member_type : `aiobungie.aiobungie.MembershipType | int`
            The member's membership type.

        Other Parameters
        ----------------
        filter : `int`
            Filter apply to list of joined groups. This Default to `0`
        group_type : `aiobungie.aiobungie.GroupType | int`
            The group's type.
            This is always set to `aiobungie.GroupType.CLAN` and should not be changed.

        Returns
        -------
        `collections.Sequence[aiobungie.crates.GroupMember]`
            A sequence of joined potential groups for the fetched member.
        """
        resp = await self._rest.fetch_potential_groups_for_member(
            member_id, member_type, filter=filter, group_type=group_type
        )

        return tuple(
            self._framework.deserialize_group_member(group) for group in resp["results"]
        )

    async def fetch_clan_members(
        self,
        clan_id: int,
        /,
        *,
        name: str | None = None,
        type: enums.MembershipType | int = enums.MembershipType.NONE,
    ) -> sain.Iterator[clans.ClanMember]:
        """Fetch Bungie clan members.

        Parameters
        ----------
        clan_id : `int`
            The clans id

        Other Parameters
        ----------------
        name : `str | None`
            If provided, Only players matching this name will be returned.
        type : `aiobungie.MembershipType`
            An optional clan member's membership type.
            This parameter is used to filter the returned results
            by the provided membership, For an example XBox memberships only,
            Otherwise will return all memberships.

        Returns
        -------
        `Iterator[aiobungie.crates.ClanMember]`
            An iterator over the bungie clan members.

        Raises
        ------
        `aiobungie.NotFound`
            The clan was not found.
        """
        resp = await self._rest.fetch_clan_members(clan_id, type=type, name=name)

        return self._framework.deserialize_clan_members(resp)

    async def fetch_clan_banners(self) -> collections.Sequence[clans.ClanBanner]:
        """Fetch the clan banners.

        Returns
        -------
        `collections.Sequence[aiobungie.crates.ClanBanner]`
            A sequence of the clan banners.
        """
        resp = await self._rest.fetch_clan_banners()

        return self._framework.deserialize_clan_banners(resp)

    # This method is required to be here since it deserialize the clan.
    async def kick_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
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
        membership_type : `aiobungie.aiobungie.MembershipType | int`
            The member's membership type.

        Returns
        -------
        `aiobungie.crates.clan.Clan`
            The clan that the member was kicked from.
        """
        resp = await self._rest.kick_clan_member(
            access_token,
            group_id=group_id,
            membership_id=membership_id,
            membership_type=membership_type,
        )

        return self._framework.deserialize_clan(resp)

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

        resp = await self._rest.fetch_clan_weekly_rewards(clan_id)

        return self._framework.deserialize_milestone(resp)

    async def search_group(
        self,
        name: str,
        group_type: enums.GroupType | int,
        *,
        creation_date: clans.GroupDate | int = 0,
        sort_by: int | None = None,
        group_member_count_filter: typing.Literal[0, 1, 2, 3] | None = None,
        locale_filter: str | None = None,
        tag_text: str | None = None,
        items_per_page: int | None = None,
        current_page: int | None = None,
        request_token: str | None = None,
    ) -> collections.Sequence[clans.Group]:
        """Search for groups.

        .. note::
            If the group type is set to `CLAN`, then parameters `group_member_count_filter`,
            `locale_filter` and `tag_text` must be `None`, otherwise `ValueError` will be raised.

        Parameters
        ----------
        name : `str`
            The group name.
        group_type : `aiobungie.GroupType | int`
            The group type that's being searched for.

        Other Parameters
        ----------------
        creation_date : `aiobungie.GroupDate | int`
            The creation date of the group. Defaults to `0` which is all time.
        sort_by : `int | None`
            ...
        group_member_count_filter : `int | None`
            ...
        locale_filter : `str | None`
            ...
        tag_text : `str | None`
            ...
        items_per_page : `int | None`
            ...
        current_page : `int | None`
            ...
        request_token : `str | None`
            ...

        Returns
        --------
        `collections.Sequence[aiobungie.crates.Group]`
            An array that contains the groups that match the search criteria.

        Raises
        ------
        `ValueError`
            If the group type is `aiobungie.GroupType.CLAN` and `group_member_count_filter`,
            `locale_filter` and `tag_text` are not `None`.
        """
        response = await self._rest.search_group(
            name,
            group_type,
            sort_by=sort_by,
            creation_date=creation_date,
            group_member_count_filter=group_member_count_filter,
            locale_filter=locale_filter,
            tag_text=tag_text,
            items_per_page=items_per_page,
            current_page=current_page,
            request_token=request_token,
        )
        return tuple(
            self._framework.deserialize_group(result) for result in response["results"]
        )

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
        resp = await self._rest.fetch_inventory_item(hash)

        return self._framework.deserialize_inventory_entity(resp)

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
        resp = await self._rest.fetch_objective_entity(hash)

        return self._framework.deserialize_objective_entity(resp)

    @helpers.unstable
    async def search_entities(
        self, name: str, entity_type: str, *, page: int = 0
    ) -> sain.Iterator[entity.SearchableEntity]:
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
        `Iterator[aiobungie.crates.SearchableEntity]`
            An iterator over the found results matching the provided name.
        """
        # resp = await self._rest.search_entities(name, entity_type, page=page)
        # calling this method will raise anyways.
        raise

    # Fireteams

    @helpers.unstable
    async def fetch_fireteams(
        self,
        activity_type: fireteams.FireteamActivity | int,
        *,
        platform: fireteams.FireteamPlatform | int = fireteams.FireteamPlatform.ANY,
        language: fireteams.FireteamLanguage | str = fireteams.FireteamLanguage.ALL,
        date_range: int = 0,
        page: int = 0,
        slots_filter: int = 0,
    ) -> collections.Sequence[fireteams.Fireteam]:
        """Fetch public Bungie fireteams with open slots.

        Parameters
        ----------
        activity_type : `aiobungie.aiobungie.crates.FireteamActivity | int`
            The fireteam activity type.

        Other Parameters
        ----------------
        platform : `aiobungie.aiobungie.crates.fireteams.FireteamPlatform | int`
            If this is provided. Then the results will be filtered with the given platform.
            Defaults to `aiobungie.crates.FireteamPlatform.ANY` which returns all platforms.
        language : `aiobungie.crates.fireteams.FireteamLanguage | str`
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
        `collections.Sequence[fireteams.Fireteam]`
            A sequence of `aiobungie.crates.Fireteam`.
        """

        # resp = await self._rest.fetch_fireteams(
        #     activity_type,
        #     platform=platform,
        #     language=language,
        #     date_range=date_range,
        #     page=page,
        #     slots_filter=slots_filter,
        # )

        # return self._framework.deserialize_fireteams(resp)
        # ! unreachable
        raise

    async def fetch_available_clan_fireteams(
        self,
        access_token: str,
        group_id: int,
        activity_type: fireteams.FireteamActivity | int,
        *,
        platform: fireteams.FireteamPlatform | int,
        language: fireteams.FireteamLanguage | str,
        date_range: int = 0,
        page: int = 0,
        public_only: bool = False,
        slots_filter: int = 0,
    ) -> collections.Sequence[fireteams.Fireteam]:
        """Fetch a clan's fireteams with open slots.

        .. note::
            This method requires OAuth2: ReadGroups scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        group_id : `int`
            The group/clan id of the fireteam.
        activity_type : `aiobungie.aiobungie.crates.FireteamActivity | int`
            The fireteam activity type.

        Other Parameters
        ----------------
        platform : `aiobungie.aiobungie.crates.fireteams.FireteamPlatform | int`
            If this is provided. Then the results will be filtered with the given platform.
            Defaults to `aiobungie.crates.FireteamPlatform.ANY` which returns all platforms.
        language : `aiobungie.crates.fireteams.FireteamLanguage | str`
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
        `collections.Sequence[aiobungie.crates.Fireteam]`
            A sequence of  fireteams found in the clan.
            `None` will be returned if nothing was found.
        """
        resp = await self._rest.fetch_available_clan_fireteams(
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

        return self._framework.deserialize_fireteams(resp)

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
        `aiobungie.crates.AvailableFireteam`
            A sequence of available fireteams objects.
        """
        resp = await self._rest.fetch_clan_fireteam(access_token, fireteam_id, group_id)

        return self._framework.deserialize_available_fireteam(resp)

    async def fetch_my_clan_fireteams(
        self,
        access_token: str,
        group_id: int,
        *,
        include_closed: bool = True,
        platform: fireteams.FireteamPlatform | int,
        language: fireteams.FireteamLanguage | str,
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
        include_closed : `bool`
            If provided and set to True, It will also return closed fireteams.
            If provided and set to False, It will only return public fireteams. Default is True.
        platform : aiobungie.aiobungie.crates.fireteams.FireteamPlatform | int
            If this is provided. Then the results will be filtered with the given platform.
            Defaults to aiobungie.crates.FireteamPlatform.ANY which returns all platforms.
        language : `aiobungie.crates.fireteams.FireteamLanguage | str`
            A locale language to filter the used language in that fireteam.
            Defaults to aiobungie.crates.FireteamLanguage.ALL
        filtered : `bool`
            If set to True, it will filter by clan. Otherwise not. Default is True.
        page : `int`
            The page number. By default its 0 which returns all available activities.

        Returns
        -------
        `collections.Sequence[aiobungie.crates.AvailableFireteam]`
            A sequence of available fireteams objects if exists. else `None` will be returned.
        """
        resp = await self._rest.fetch_my_clan_fireteams(
            access_token,
            group_id,
            include_closed=include_closed,
            platform=platform,
            language=language,
            filtered=filtered,
            page=page,
        )

        return self._framework.deserialize_available_fireteams(resp)

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

        resp = await self._rest.fetch_friends(access_token)

        return self._framework.deserialize_friends(resp)

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

        resp = await self._rest.fetch_friend_requests(access_token)

        return self._framework.deserialize_friend_requests(resp)

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
        resp = await self._rest.fetch_application(appid)

        return self._framework.deserialize_application(resp)

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
        ...
        resp = await self._rest.fetch_public_milestone_content(milestone_hash)
        return self._framework.deserialize_public_milestone_content(resp)
