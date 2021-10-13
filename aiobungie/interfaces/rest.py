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

"""An interface for the rest client."""

from __future__ import annotations

from aiobungie.internal.helpers import JsonObject

__all__: list[str] = ["RESTInterface"]

import abc
import typing

from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    from aiobungie.internal import helpers

    ResponseSigT = typing.TypeVar(
        "ResponseSigT",
        covariant=True,
        bound=typing.Union[helpers.JsonArray, helpers.JsonObject, None],
    )
    ResponseSig = typing.Coroutine[typing.Any, typing.Any, ResponseSigT]


class RESTInterface(abc.ABC):
    """An interface for a rest only client implementation."""

    __slots__: typing.Sequence[str] = ()

    @abc.abstractmethod
    async def close(self) -> None:
        """Close the rest client."""

    @abc.abstractmethod
    def static_request(
        self, method: str, path: str, **kwargs: typing.Any
    ) -> ResponseSig[typing.Any]:
        """Raw http request given a valid bungie endpoint.

        Parameters
        ----------
        method : `builtins.str`
            The request method, This may be `GET`, `POST`, `PUT`, etc.
        path: `builtins.str`
            The bungie endpoint or path.
            A path must look something like this
            `Destiny2/3/Profile/46111239123/...`
        **kwargs: `typing.Any`
            Any other key words you'd like to pass through.

        Returns
        -------
        `typing.Any`
            Any object.
        """

    @abc.abstractmethod
    async def fetch_manifest(self) -> bytes:
        """Access The bungie Manifest.

        Returns
        -------
        `builtins.bytes`
            The bytes to read and write the manifest database.
        """

    @abc.abstractmethod
    async def fetch_manifest_path(self) -> str:
        """Return a string of the bungie manifest database url.

        Returns
        -------
        `builtins.str`
            A downloadable url for the bungie manifest database.
        """

    @abc.abstractmethod
    def fetch_user(self, id: int) -> ResponseSig[helpers.JsonObject]:
        """Fetch a Bungie user by their id.

        Parameters
        ----------
        id: `builtins.int`
            The user id.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of users objects.

        Raises
        ------
        `aiobungie.error.UserNotFound`
            The user was not found.
        """

    @abc.abstractmethod
    def search_users(self, name: str, /) -> ResponseSig[helpers.JsonObject]:
        """Search for users by their global name and return all users who share this name.

        Parameters
        ----------
        name : `str`
            The user name.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of an array of the found users.

        Raises
        ------
        `aiobungie.NotFound`
            The user(s) was not found.

        """

    @abc.abstractmethod
    def fetch_user_themes(self) -> ResponseSig[helpers.JsonArray]:
        """Fetch all available user themes.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonArray]`
            A JSON array of user themes.
        """

    @abc.abstractmethod
    def fetch_hard_linked(
        self,
        credential: int,
        type: helpers.IntAnd[enums.CredentialType] = enums.CredentialType.STEAMID,
        /,
    ) -> ResponseSig[helpers.JsonObject]:
        """Gets any hard linked membership given a credential.
        Only works for credentials that are public just `aiobungie.CredentialType.STEAMID` right now.
        Cross Save aware.

        Parameters
        ----------
        credential: `builtins.int`
            A valid SteamID64
        type: `aiobungie.internal.helpers.IntAnd[aiobungie.CredentialType]`
            The crededntial type. This must not be changed
            Since its only credential that works "currently"

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of the found user hard linked types.
        """

    @abc.abstractmethod
    def fetch_membership_from_id(
        self,
        id: int,
        type: helpers.IntAnd[enums.MembershipType] = enums.MembershipType.NONE,
        /,
    ) -> ResponseSig[helpers.JsonObject]:
        """Fetch Bungie user's memberships from their id.

        Parameters
        ----------
        id : `builtins.int`
            The user's id.
        type : `aiobungie.internal.helpers.IntAnd[aiobungie.MembershipType]`
            The user's membership type.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of the found user.

        Raises
        ------
        aiobungie.UserNotFound
            The requested user was not found.
        """

    @abc.abstractmethod
    def fetch_profile(
        self,
        memberid: int,
        type: helpers.IntAnd[enums.MembershipType],
        /,
    ) -> ResponseSig[helpers.JsonObject]:
        """
        Fetche a bungie profile.

        Parameters
        ----------
        memberid: `builtins.int`
            The member's id.
        type: `aiobungie.internal.helpers.IntAnd[aiobungie.MembershipType]`
            A valid membership type.

        Returns
        --------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of the found profile.

        Raises
        ------
        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """

    @abc.abstractmethod
    def fetch_player(
        self,
        name: str,
        type: helpers.IntAnd[enums.MembershipType] = enums.MembershipType.ALL,
        /,
    ) -> ResponseSig[helpers.JsonArray]:
        """Fetch a Destiny 2 Player.

        .. note::
            You must also pass the player's unique code.
            A full name parameter should look like this
            `Fate怒#4275`

        Parameters
        -----------
        name: `builtins.str`
            The Player's Name.
        type: `aiobungie.internal.helpers.IntAnd[aiobungie.MembershipType]`
            The player's membership type, e,g. XBOX, STEAM, PSN

        Returns
        --------
        `ResponseSig[aiobungie.internal.helpers.JsonArray]`
            A JSON array of the found players.

        Raises
        ------
        `aiobungie.PlayerNotFound`
            The player was not found.

        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """

    @abc.abstractmethod
    def fetch_character(
        self, memberid: int, type: helpers.IntAnd[enums.MembershipType], /
    ) -> ResponseSig[helpers.JsonObject]:
        """Fetch a Destiny 2 player's characters.

        Parameters
        ----------
        memberid: `builtins.int`
            A valid bungie member id.
        type: `aiobungie.internal.helpers.IntAnd[aiobungie.internal.enums.MembershipType]`
            The member's membership type.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of the requested character.

        Raises
        ------
        `aiobungie.error.CharacterError`
            raised if the Character was not found.

        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """

    @abc.abstractmethod
    def fetch_activity(
        self,
        member_id: int,
        character_id: int,
        mode: helpers.IntAnd[enums.GameMode],
        membership_type: helpers.IntAnd[
            enums.MembershipType
        ] = enums.MembershipType.ALL,
        *,
        page: int = 1,
        limit: int = 1,
    ) -> ResponseSig[helpers.JsonObject]:
        """Fetch a Destiny 2 activity for the specified user id and character.

        Parameters
        ----------
        member_id: `builtins.int`
            The user id that starts with `4611`.
        character_id: `builtins.int`
            The id of the character to retrieve.
        mode: `aiobungie.internal.helpers.IntAnd[aiobungie.GameMode]`
            This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc.
        membership_type: `aiobungie.internal.helpers.IntAnd[aiobungie.internal.enums.MembershipType]`
            The Member ship type, if nothing was passed than it will return all.

        Other Parameters
        ----------------
        page: `builtins.int`
            The page number. Default to `1`
        limit: `builtins.int`
            Limit the returned result. Default to `1`

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of the player's activities.

        Raises
        ------
        `aiobungie.error.ActivityNotFound`
            The activity was not found.

        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """

    @abc.abstractmethod
    def fetch_post_activity(self, instance: int, /) -> ResponseSig[helpers.JsonObject]:
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
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of the post activity.
        """

    @abc.abstractmethod
    def fetch_clan_from_id(self, id: int, /) -> ResponseSig[helpers.JsonObject]:
        """Fetch a Bungie Clan by its id.

        Parameters
        -----------
        id: `builtins.int`
            The clan id.

        Returns
        --------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of the clan.

        Raises
        ------
        `aiobungie.ClanNotFound`
            The clan was not found.
        """

    @abc.abstractmethod
    def fetch_clan(
        self, name: str, /, type: helpers.IntAnd[enums.GroupType] = enums.GroupType.CLAN
    ) -> ResponseSig[helpers.JsonObject]:
        """Fetch a Clan by its name.
        This method will return the first clan found with given name name.

        Parameters
        ----------
        name: `builtins.str`
            The clan name
        type `aiobungie.internal.helpers.IntAnd[aiobungie.GroupType]`
            The group type, Default is one.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of the clan.

        Raises
        ------
        `aiobungie.ClanNotFound`
            The clan was not found.
        """

    @abc.abstractmethod
    def fetch_clan_conversations(
        self, clan_id: int, /
    ) -> ResponseSig[helpers.JsonArray]:
        """Fetch a clan's conversations.

        Parameters
        ----------
        clan_id : `builtins.int`
            The clan's id.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonArray]`
            A JSON array of the conversations.
        """

    @abc.abstractmethod
    def fetch_clan_admins(self, clan_id: int, /) -> ResponseSig[helpers.JsonObject]:
        """Fetch the admins and founder members of the clan.

        Parameters
        ----------
        clan_id : `builtins.int`
            The clan id.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of the clan admins and founder members.

        Raises
        ------
        `aiobungie.ClanNotFound`
            The clan was not found.
        """

    @abc.abstractmethod
    def fetch_groups_for_member(
        self,
        member_id: int,
        member_type: helpers.IntAnd[enums.MembershipType],
        /,
        *,
        filter: int = 0,
        group_type: helpers.IntAnd[enums.GroupType] = enums.GroupType.CLAN,
    ) -> ResponseSig[helpers.JsonObject]:
        """Fetch the information about the groups for a member.

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
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of an array of the member's membership data and groups data.
        """

    @abc.abstractmethod
    def fetch_potential_groups_for_member(
        self,
        member_id: int,
        member_type: helpers.IntAnd[enums.MembershipType],
        /,
        *,
        filter: int = 0,
        group_type: enums.GroupType = enums.GroupType.CLAN,
    ) -> ResponseSig[helpers.JsonObject]:
        """Get information about the groups that a given member has applied to or been invited to.

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
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of an array of the member's membership data and groups data.
        """

    @abc.abstractmethod
    def fetch_clan_members(
        self,
        clan_id: int,
        type: helpers.IntAnd[enums.MembershipType] = enums.MembershipType.NONE,
        name: typing.Optional[str] = None,
        /,
    ) -> ResponseSig[helpers.JsonObject]:
        """Fetch all Bungie Clan members.

        Parameters
        ----------
        clan_id : `builsins.int`
            The clans id
        type : `aiobungie.internal.helpers.IntAnd[aiobungie.MembershipType]`
            An optional clan member's membership type.
            Default is set to `aiobungie.MembershipType.NONE`
            Which returns the first matched clan member by their name.
        name : `builtins.str`
            This parameter is only provided here to keep the signature with
            the main client implementation, Which only works with the non-rest clients.
            It returns a specific clan member by their name.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of an array of clan members.

        Raises
        ------
        `aiobungie.ClanNotFound`
            The clan was not found.
        """

    @abc.abstractmethod
    def fetch_inventory_item(self, hash: int, /) -> ResponseSig[helpers.JsonObject]:
        """Fetch a static inventory item entity given a its hash.

        Parameters
        ----------
        type: `builtins.str`
            Entity's type definition.
        hash: `builtins.int`
            Entity's hash.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON array object of the inventory item.
        """

    @abc.abstractmethod
    def fetch_app(self, appid: int, /) -> ResponseSig[helpers.JsonObject]:
        """Fetch a Bungie Application.

        Parameters
        -----------
        appid: `builtins.int`
            The application id.

        Returns
        --------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of the application.
        """

    @abc.abstractmethod
    def fetch_linked_profiles(
        self,
        member_id: int,
        member_type: helpers.IntAnd[enums.MembershipType],
        /,
        *,
        all: bool = False,
    ) -> ResponseSig[helpers.JsonObject]:
        """Returns a summary information about all profiles linked to the requested member.

        The passed membership id/type maybe a Bungie.Net membership or a Destiny memberships.

        .. note::
            It will only return linked accounts whose linkages you are allowed to view.

        Parameters
        ----------
        member_id : `builtins.int`
            The ID of the membership. This must be a valid Bungie.Net or PSN or Xbox ID.
        member_type : `aiobungie.internal.helpers.IntAnd[aiobungie.MembershipType]`
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
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
        A JSON object which contains an Array of profiles, an Array of profiles with errors and Bungie.Net membership
        """

    @abc.abstractmethod
    def fetch_clan_banners(self) -> ResponseSig[helpers.JsonObject]:
        """Fetch the values of the clan banners.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of the clan banners.
        """

    @abc.abstractmethod
    def fetch_public_milestones(self) -> ResponseSig[helpers.JsonObject]:
        """Fetch the available milestones.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of information about the milestones.
        """

    @abc.abstractmethod
    def fetch_public_milestone_content(
        self, milestone_hash: int, /
    ) -> ResponseSig[helpers.JsonObject]:
        """Fetch the milestone content given its hash.

        Parameters
        ----------
        milestone_hash : `builtins.int`
            The milestone hash.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of information related to the fetched milestone.
        """

    @abc.abstractmethod
    def fetch_own_bungie_user(
        self, access_token: str, /
    ) -> ResponseSig[helpers.JsonObject]:
        """Fetch a bungie user's accounts with the signed in user.
        This GET method  requires a Bearer access token for the authorization.

        .. note::
            This requires OAuth2 scope enabled and the valid Bearer `access_token`.
            This token should be stored somewhere safe and just passed as a parameter. e.g., A database.

        Parameters
        ----------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of the bungie net user and destiny memberships of this account.
        """

    @abc.abstractmethod
    def equip_item(
        self,
        access_token: str,
        /,
        *,
        item_id: int,
        character_id: int,
        membership_type: helpers.IntAnd[enums.MembershipType],
    ) -> ResponseSig[None]:
        """Equip an item to a character.

        .. note::
            This requires the OAuth2: MoveEquipDestinyItems scope.
            Also You must have a valid Destiny account, and either be
            in a social space, in orbit or offline.

        Positional arguments
        --------------------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.

        Parameters
        ----------
        item_id : `builtins.int`
            The item id.
        character_id : `builtins.int`
            The character's id to equip the item to.
        membership_type : `aiobungie.internal.helpers.IntAnd[aiobungie.MembershipType]`
            The membership type assocaiated with this player.

        Returns
        -------
        `ResponseSig[None]`
            None
        """

    @abc.abstractmethod
    def equip_items(
        self,
        access_token: str,
        /,
        *,
        item_ids: list[int],
        character_id: int,
        membership_type: helpers.IntAnd[enums.MembershipType],
    ) -> ResponseSig[None]:
        """Equip multiple items to a character.

        .. note::
            This requires the OAuth2: MoveEquipDestinyItems scope.
            Also You must have a valid Destiny account, and either be
            in a social space, in orbit or offline.

        Positional arguments
        --------------------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.

        Parameters
        ----------
        item_ids : `list[builtins.int]`
            A list of item ids.
        character_id : `builtins.int`
            The character's id to equip the item to.
        membership_type : `aiobungie.internal.helpers.IntAnd[aiobungie.MembershipType]`
            The membership type assocaiated with this player.

        Returns
        -------
        `ResponseSig[None]`
            None
        """

    @abc.abstractmethod
    def ban_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: helpers.IntAnd[enums.MembershipType],
        *,
        length: int = 0,
        comment: typing.Optional[str] = None,
    ) -> ResponseSig[None]:
        """Bans a member from the clan.

        .. note::
            This request requires OAuth2: oauth2: `AdminGroups` scope.

        Positional arguments
        --------------------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.

        Parameters
        ----------
        group_id: `int`
            The group id.
        membership_id : `int`
            The member id to ban.
        membership_type : `aiobungie.internal.helpers.IntAnd[aiobungie.MembershipType]`
            The member's membership type.

        Other Parameters
        ----------------
        length: `int`
            An optional ban length.
        comment: `typing.Optional[str]`
            An optional comment to this ban.

        Returns
        -------
        `ResponseSig[None]`
            None
        """

    @abc.abstractmethod
    def unban_clan_member(
        self,
        access_token: str,
        /,
        *,
        group_id: int,
        membership_id: int,
        membership_type: helpers.IntAnd[enums.MembershipType],
    ) -> ResponseSig[None]:
        """Unbans a member from the clan.

        .. note::
            This request requires OAuth2: oauth2: `AdminGroups` scope.

        Positional arguments
        --------------------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.

        Parameters
        ----------
        group_id: `int`
            The group id.
        membership_id : `int`
            The member id to unban.
        membership_type : `aiobungie.internal.helpers.IntAnd[aiobungie.MembershipType]`
            The member's membership type.

        Returns
        -------
        `ResponseSig[None]`
            None
        """

    @abc.abstractmethod
    def kick_clan_member(
        self,
        access_token: str,
        /,
        *,
        group_id: int,
        membership_id: int,
        membership_type: helpers.IntAnd[enums.MembershipType],
    ) -> ResponseSig[JsonObject]:
        """Kick a member from the clan.

        .. note::
            This request requires OAuth2: oauth2: `AdminGroups` scope.

        Positional arguments
        --------------------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.

        Parameters
        ----------
        group_id: `int`
            The group id.
        membership_id : `int`
            The member id to kick.
        membership_type : `aiobungie.internal.helpers.IntAnd[aiobungie.MembershipType]`
            The member's membership type.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of the group that the member has been kicked from.
        """

    @abc.abstractmethod
    def fetch_item(
        self, member_id: int, item_id: int, /
    ) -> ResponseSig[helpers.JsonObject]:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_clan_weekly_rewards(
        self, clan_id: int, /
    ) -> ResponseSig[helpers.JsonObject]:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_weapon_history(
        self,
        character_id: int,
        member_id: int,
        member_type: helpers.IntAnd[enums.MembershipType],
    ) -> ResponseSig[helpers.JsonObject]:
        raise NotImplementedError
