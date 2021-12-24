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

"""An API interface for the rest client."""

from __future__ import annotations

__all__: list[str] = ["RESTInterface"]

import abc
import typing

from aiobungie import traits
from aiobungie import undefined
from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    import collections.abc as collections
    import pathlib
    import sqlite3

    from aiobungie import rest as _rest
    from aiobungie import typedefs
    from aiobungie.crate import fireteams

    ResponseSigT = typing.TypeVar(
        "ResponseSigT",
        covariant=True,
        bound=typing.Union[
            typedefs.JSONArray,
            typedefs.JSONObject,
            int,
            None,
        ],
    )
    ResponseSig = typing.Coroutine[None, None, ResponseSigT]


class RESTInterface(traits.RESTful, abc.ABC):
    """An API interface for the rest only client implementation."""

    __slots__ = ()

    @abc.abstractmethod
    async def read_manifest_bytes(self) -> bytes:
        """Read Bungie's manifest sqlite bytes respond.

        This method can be used to write the bytes to zipped file
        and then extract it to get the manifest content.

        Returns
        -------
        `bytes`
            The bytes to read and write the manifest database.
        """

    @abc.abstractmethod
    async def fetch_manifest_path(self) -> str:
        """Return a string of the Bungie sqlite manifest `.content` url.

        Returns
        -------
        `str`
            A url for the Bungie manifest content.
        """

    @abc.abstractmethod
    async def download_manifest(
        self, language: str = "en", name: str = "manifest.sqlite3"
    ) -> None:
        """A helper method to download the manifest.

        Note
        ----
        This method downloads the sqlite database and not JSON.

        Parameters
        ----------
        language : `str`
            The manifest language to download, Default is english.
        name : `str`
            The manifest database file name. Default is `manifest.sqlite3`

        Returns
        --------
        `None`
        """

    @staticmethod
    @abc.abstractmethod
    def connect_manifest(
        path: typing.Optional[pathlib.Path] = None,
    ) -> sqlite3.Connection:
        """A friendly method to connect to the manifest database.

        Parameters
        ----------
        path : `typing.Optional[pathlib.Path]`
            An optional path to pass, The assumed path to connect to is './manifest.sqlite3'

        Returns
        -------
        `sqlite3.Connection`
            An sqlite database connection.
        """

    @abc.abstractmethod
    def fetch_user(self, id: int) -> ResponseSig[typedefs.JSONObject]:
        """Fetch a Bungie user by their id.

        Parameters
        ----------
        id: `builtins.int`
            The user id.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of users objects.

        Raises
        ------
        `aiobungie.error.NotFound`
            The user was not found.
        """

    @abc.abstractmethod
    def search_users(self, name: str, /) -> ResponseSig[typedefs.JSONObject]:
        """Search for users by their global name and return all users who share this name.

        Parameters
        ----------
        name : `str`
            The user name.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of an array of the found users.

        Raises
        ------
        `aiobungie.NotFound`
            The user(s) was not found.

        """

    @abc.abstractmethod
    def fetch_user_themes(self) -> ResponseSig[typedefs.JSONArray]:
        """Fetch all available user themes.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONArray]`
            A JSON array of user themes.
        """

    @abc.abstractmethod
    def fetch_hard_linked(
        self,
        credential: int,
        type: typedefs.IntAnd[enums.CredentialType] = enums.CredentialType.STEAMID,
        /,
    ) -> ResponseSig[typedefs.JSONObject]:
        """Gets any hard linked membership given a credential.
        Only works for credentials that are public just `aiobungie.CredentialType.STEAMID` right now.
        Cross Save aware.

        Parameters
        ----------
        credential: `builtins.int`
            A valid SteamID64
        type: `aiobungie.typedefs.IntAnd[aiobungie.CredentialType]`
            The crededntial type. This must not be changed
            Since its only credential that works "currently"

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the found user hard linked types.
        """

    @abc.abstractmethod
    def fetch_membership_from_id(
        self,
        id: int,
        type: typedefs.IntAnd[enums.MembershipType] = enums.MembershipType.NONE,
        /,
    ) -> ResponseSig[typedefs.JSONObject]:
        """Fetch Bungie user's memberships from their id.

        Parameters
        ----------
        id : `builtins.int`
            The user's id.
        type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The user's membership type.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the found user.

        Raises
        ------
        aiobungie.NotFound
            The requested user was not found.
        """

    @abc.abstractmethod
    def fetch_profile(
        self,
        memberid: int,
        type: typedefs.IntAnd[enums.MembershipType],
        *components: enums.ComponentType,
        **options: str,
    ) -> ResponseSig[typedefs.JSONObject]:
        """
        Fetche a bungie profile.

        Parameters
        ----------
        memberid: `builtins.int`
            The member's id.
        type: `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            A valid membership type.
        *components : `aiobungie.ComponentType`
            Multiple arguments of profile components to collect and return.

        Other Parameters
        ----------------
        auth : `typing.Optional[str]`
            A passed kwarg Bearer access_token to make the request with.
            This is optional and limited to components that only requires an Authorization token.
        **options : `str`
            Other keyword arguments for the request to expect.
            This is only here for the `auth` option which's a kwarg.

        Returns
        --------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
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
        code: int,
        type: typedefs.IntAnd[enums.MembershipType] = enums.MembershipType.ALL,
        /,
    ) -> ResponseSig[typedefs.JSONArray]:
        """Fetch a Destiny 2 Player.

        Parameters
        -----------
        name: `builtins.str`
            The unique Bungie player name.
        code : `int`
            The unique Bungie display name code.
        type: `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The player's membership type, e,g. XBOX, STEAM, PSN

        Returns
        --------
        `ResponseSig[aiobungie.typedefs.JSONArray]`
            A JSON array of the found player's memberships.

        Raises
        ------
        `aiobungie.NotFound`
            The player was not found.

        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """

    @abc.abstractmethod
    def fetch_character(
        self,
        member_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
        character_id: int,
        *components: enums.ComponentType,
        **options: str,
    ) -> ResponseSig[typedefs.JSONObject]:
        """Fetch a Destiny 2 player's characters.

        Parameters
        ----------
        member_id: `builtins.int`
            A valid bungie member id.
        membership_type: `aiobungie.typedefs.IntAnd[aiobungie.internal.enums.MembershipType]`
            The member's membership type.
        character_id : `int`
            The character id to return.
        *components: `aiobungie.ComponentType`
            Multiple arguments of character components to collect and return.

        Other Parameters
        ----------------
        auth : `typing.Optional[str]`
            A passed kwarg Bearer access_token to make the request with.
            This is optional and limited to components that only requires an Authorization token.
        **options : `str`
            Other keyword arguments for the request to expect.
            This is only here for the `auth` option which's a kwarg.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the requested character.

        Raises
        ------
        `aiobungie.error.CharacterError`
            raised if the Character was not found.

        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """

    @abc.abstractmethod
    def fetch_activities(
        self,
        member_id: int,
        character_id: int,
        mode: typedefs.IntAnd[enums.GameMode],
        membership_type: typedefs.IntAnd[
            enums.MembershipType
        ] = enums.MembershipType.ALL,
        *,
        page: int = 1,
        limit: int = 1,
    ) -> ResponseSig[typedefs.JSONObject]:
        """Fetch a Destiny 2 activity for the specified user id and character.

        Parameters
        ----------
        member_id: `builtins.int`
            The user id that starts with `4611`.
        character_id: `builtins.int`
            The id of the character to retrieve.
        mode: `aiobungie.typedefs.IntAnd[aiobungie.GameMode]`
            This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc.

        Other Parameters
        ----------------
        membership_type: `aiobungie.typedefs.IntAnd[aiobungie.internal.enums.MembershipType]`
            The Member ship type, if nothing was passed than it will return all.
        page: `builtins.int`
            The page number. Default to `1`
        limit: `builtins.int`
            Limit the returned result. Default to `1`

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the player's activities.

        Raises
        ------
        `aiobungie.error.NotFound`
            The activity was not found.

        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """

    @abc.abstractmethod
    def fetch_post_activity(
        self, instance_id: int, /
    ) -> ResponseSig[typedefs.JSONObject]:
        """Fetch a post activity details.

        Parameters
        ----------
        instance_id: `int`
            The activity instance id.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the post activity.
        """

    @abc.abstractmethod
    def fetch_clan_from_id(self, id: int, /) -> ResponseSig[typedefs.JSONObject]:
        """Fetch a Bungie Clan by its id.

        Parameters
        -----------
        id: `builtins.int`
            The clan id.

        Returns
        --------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the clan.

        Raises
        ------
        `aiobungie.NotFound`
            The clan was not found.
        """

    @abc.abstractmethod
    def fetch_clan(
        self,
        name: str,
        /,
        type: typedefs.IntAnd[enums.GroupType] = enums.GroupType.CLAN,
    ) -> ResponseSig[typedefs.JSONObject]:
        """Fetch a Clan by its name.
        This method will return the first clan found with given name name.

        Parameters
        ----------
        name: `builtins.str`
            The clan name
        type `aiobungie.typedefs.IntAnd[aiobungie.GroupType]`
            The group type, Default is one.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the clan.

        Raises
        ------
        `aiobungie.NotFound`
            The clan was not found.
        """

    @abc.abstractmethod
    def fetch_clan_conversations(
        self, clan_id: int, /
    ) -> ResponseSig[typedefs.JSONArray]:
        """Fetch a clan's conversations.

        Parameters
        ----------
        clan_id : `builtins.int`
            The clan's id.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONArray]`
            A JSON array of the conversations.
        """

    @abc.abstractmethod
    def fetch_clan_admins(self, clan_id: int, /) -> ResponseSig[typedefs.JSONObject]:
        """Fetch the admins and founder members of the clan.

        Parameters
        ----------
        clan_id : `builtins.int`
            The clan id.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the clan admins and founder members.

        Raises
        ------
        `aiobungie.NotFound`
            The clan was not found.
        """

    @abc.abstractmethod
    def fetch_groups_for_member(
        self,
        member_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
        /,
        *,
        filter: int = 0,
        group_type: typedefs.IntAnd[enums.GroupType] = enums.GroupType.CLAN,
    ) -> ResponseSig[typedefs.JSONObject]:
        """Fetch the information about the groups for a member.

        Parameters
        ----------
        member_id : `builtins.int`
            The member's id
        member_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The member's membership type.

        Other Parameters
        ----------------
        filter : `builsins.int`
            Filter apply to list of joined groups. This Default to `0`
        group_type : `aiobungie.typedefs.IntAnd[aiobungie.GroupType]`
            The group's type.
            This is always set to `aiobungie.GroupType.CLAN` and should not be changed.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of an array of the member's membership data and groups data.
        """

    @abc.abstractmethod
    def fetch_potential_groups_for_member(
        self,
        member_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
        /,
        *,
        filter: int = 0,
        group_type: typedefs.IntAnd[enums.GroupType] = enums.GroupType.CLAN,
    ) -> ResponseSig[typedefs.JSONObject]:
        """Get information about the groups that a given member has applied to or been invited to.

        Parameters
        ----------
        member_id : `builtins.int`
            The member's id
        member_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The member's membership type.

        Other Parameters
        ----------------
        filter : `builsins.int`
            Filter apply to list of joined groups. This Default to `0`
        group_type : `aiobungie.typedefs.IntAnd[aiobungie.GroupType]`
            The group's type.
            This is always set to `aiobungie.GroupType.CLAN` and should not be changed.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of an array of the member's membership data and groups data.
        """

    @abc.abstractmethod
    def fetch_clan_members(
        self,
        clan_id: int,
        type: typedefs.IntAnd[enums.MembershipType] = enums.MembershipType.NONE,
        name: typing.Optional[str] = None,
        /,
    ) -> ResponseSig[typedefs.JSONObject]:
        """Fetch all Bungie Clan members.

        Parameters
        ----------
        clan_id : `builsins.int`
            The clans id
        type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            An optional clan member's membership type.
            Default is set to `aiobungie.MembershipType.NONE`
            Which returns the first matched clan member by their name.
        name : `builtins.str`
            This parameter is only provided here to keep the signature with
            the main client implementation, Which only works with the non-rest clients.
            It returns a specific clan member by their name.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of an array of clan members.

        Raises
        ------
        `aiobungie.NotFound`
            The clan was not found.
        """

    @abc.abstractmethod
    def fetch_entity(self, type: str, hash: int) -> ResponseSig[typedefs.JSONObject]:
        """Fetch a Destiny definition item given its type and hash.

        Parameters
        ----------
        type: `builtins.str`
            Entity's type definition.
        hash: `builtins.int`
            Entity's hash.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the definition data.
        """

    @abc.abstractmethod
    def fetch_inventory_item(self, hash: int, /) -> ResponseSig[typedefs.JSONObject]:
        """Fetch a Destiny inventory item entity given a its hash.

        Parameters
        ----------
        hash: `builtins.int`
            Entity's hash.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the inventory item.
        """

    @abc.abstractmethod
    def fetch_objective_entity(self, hash: int, /) -> ResponseSig[typedefs.JSONObject]:
        """Fetch a Destiny objective entity given a its hash.

        Parameters
        ----------
        hash: `builtins.int`
            objective's hash.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the objetive data.
        """

    @abc.abstractmethod
    def fetch_app(self, appid: int, /) -> ResponseSig[typedefs.JSONObject]:
        """Fetch a Bungie Application.

        Parameters
        -----------
        appid: `builtins.int`
            The application id.

        Returns
        --------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the application.
        """

    @abc.abstractmethod
    def fetch_linked_profiles(
        self,
        member_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
        /,
        *,
        all: bool = False,
    ) -> ResponseSig[typedefs.JSONObject]:
        """Returns a summary information about all profiles linked to the requested member.

        The passed membership id/type maybe a Bungie.Net membership or a Destiny memberships.

        .. note::
            It will only return linked accounts whose linkages you are allowed to view.

        Parameters
        ----------
        member_id : `builtins.int`
            The ID of the membership. This must be a valid Bungie.Net or PSN or Xbox ID.
        member_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
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
        `ResponseSig[aiobungie.typedefs.JSONObject]`
        A JSON object which contains an Array of profiles, an Array of profiles with errors and Bungie.Net membership
        """

    @abc.abstractmethod
    def fetch_clan_banners(self) -> ResponseSig[typedefs.JSONObject]:
        """Fetch the values of the clan banners.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the clan banners.
        """

    @abc.abstractmethod
    def fetch_public_milestones(self) -> ResponseSig[typedefs.JSONObject]:
        """Fetch the available milestones.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of information about the milestones.
        """

    @abc.abstractmethod
    def fetch_public_milestone_content(
        self, milestone_hash: int, /
    ) -> ResponseSig[typedefs.JSONObject]:
        """Fetch the milestone content given its hash.

        Parameters
        ----------
        milestone_hash : `builtins.int`
            The milestone hash.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of information related to the fetched milestone.
        """

    @abc.abstractmethod
    def fetch_own_bungie_user(
        self, access_token: str, /
    ) -> ResponseSig[typedefs.JSONObject]:
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
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the bungie net user and destiny memberships of this account.
        """

    @abc.abstractmethod
    def equip_item(
        self,
        access_token: str,
        /,
        item_id: int,
        character_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[None]:
        """Equip an item to a character.

        .. note::
            This requires the OAuth2: MoveEquipDestinyItems scope.
            Also You must have a valid Destiny account, and either be
            in a social space, in orbit or offline.

        Parameters
        ----------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.
        item_id : `builtins.int`
            The item id.
        character_id : `builtins.int`
            The character's id to equip the item to.
        membership_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The membership type assocaiated with this player.
        """

    @abc.abstractmethod
    def equip_items(
        self,
        access_token: str,
        /,
        item_ids: list[int],
        character_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[None]:
        """Equip multiple items to a character.

        .. note::
            This requires the OAuth2: MoveEquipDestinyItems scope.
            Also You must have a valid Destiny account, and either be
            in a social space, in orbit or offline.

        Parameters
        ----------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.
        item_ids : `list[builtins.int]`
            A list of item ids.
        character_id : `builtins.int`
            The character's id to equip the item to.
        membership_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The membership type assocaiated with this player.
        """

    @abc.abstractmethod
    def ban_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
        *,
        length: int = 0,
        comment: undefined.UndefinedOr[str] = undefined.Undefined,
    ) -> ResponseSig[None]:
        """Bans a member from the clan.

        .. note::
            This request requires OAuth2: oauth2: `AdminGroups` scope.

        Parameters
        ----------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.
        group_id: `int`
            The group id.
        membership_id : `int`
            The member id to ban.
        membership_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The member's membership type.

        Other Parameters
        ----------------
        length: `int`
            An optional ban length.
        comment: `aiobungie.UndefinedOr[str]`
            An optional comment to this ban. Default is `UNDEFINED`
        """

    @abc.abstractmethod
    def unban_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[None]:
        """Unbans a member from the clan.

        .. note::
            This request requires OAuth2: oauth2: `AdminGroups` scope.

        Parameters
        ----------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.
        group_id: `int`
            The group id.
        membership_id : `int`
            The member id to unban.
        membership_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The member's membership type.
        """

    @abc.abstractmethod
    def kick_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[typedefs.JSONObject]:
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
        membership_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The member's membership type.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the group that the member has been kicked from.
        """

    @abc.abstractmethod
    def edit_clan_options(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        invite_permissions_override: typedefs.NoneOr[bool] = None,
        update_culture_permissionOverride: typedefs.NoneOr[bool] = None,
        host_guided_game_permission_override: typedefs.NoneOr[
            typing.Literal[0, 1, 2]
        ] = None,
        update_banner_permission_override: typedefs.NoneOr[bool] = None,
        join_level: typedefs.NoneOr[typedefs.IntAnd[enums.ClanMemberType]] = None,
    ) -> ResponseSig[None]:
        """Edit the clan options.

        Notes
        -----
        * This request requires OAuth2: oauth2: `AdminGroups` scope.
        * All arguments will default to `None` if not provided. This does not include `access_token` and `group_id`

        Parameters
        ----------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.
        group_id: `int`
            The group id.

        Other Parameters
        ----------------
        invite_permissions_override : `aiobungie.typedefs.NoneOr[bool]`
            Minimum Member Level allowed to invite new members to group
            Always Allowed: Founder, Acting Founder
            True means admins have this power, false means they don't
            Default is False for clans, True for groups.
        update_culture_permissionOverride : `aiobungie.typedefs.NoneOr[bool]`
            Minimum Member Level allowed to update group culture
            Always Allowed: Founder, Acting Founder
            True means admins have this power, false means they don't
            Default is False for clans, True for groups.
        host_guided_game_permission_override : `aiobungie.typedefs.NoneOr[typing.Literal[0, 1, 2]]`
            Minimum Member Level allowed to host guided games
            Always Allowed: Founder, Acting Founder, Admin
            Allowed Overrides: `0` -> None, `1` -> Beginner `2` -> Member.
            Default is Member for clans, None for groups, although this means nothing for groups.
        update_banner_permission_override : `aiobungie.typedefs.NoneOr[bool]`
            Minimum Member Level allowed to update banner
            Always Allowed: Founder, Acting Founder
            True means admins have this power, false means they don't
            Default is False for clans, True for groups.
        join_level : `aiobungie.ClanMemberType`
            Level to join a member at when accepting an invite, application, or joining an open clan.
            Default is `aiobungie.ClanMemberType.BEGINNER`
        """

    @abc.abstractmethod
    def edit_clan(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        name: typedefs.NoneOr[str] = None,
        about: typedefs.NoneOr[str] = None,
        motto: typedefs.NoneOr[str] = None,
        theme: typedefs.NoneOr[str] = None,
        tags: typedefs.NoneOr[collections.Sequence[str]] = None,
        is_public: typedefs.NoneOr[bool] = None,
        locale: typedefs.NoneOr[str] = None,
        avatar_image_index: typedefs.NoneOr[int] = None,
        membership_option: typedefs.NoneOr[
            typedefs.IntAnd[enums.MembershipOption]
        ] = None,
        allow_chat: typedefs.NoneOr[bool] = None,
        chat_security: typedefs.NoneOr[typing.Literal[0, 1]] = None,
        call_sign: typedefs.NoneOr[str] = None,
        homepage: typedefs.NoneOr[typing.Literal[0, 1, 2]] = None,
        enable_invite_messaging_for_admins: typedefs.NoneOr[bool] = None,
        default_publicity: typedefs.NoneOr[typing.Literal[0, 1, 2]] = None,
        is_public_topic_admin: typedefs.NoneOr[bool] = None,
    ) -> ResponseSig[None]:
        """Edit a clan.

        Notes
        -----
        * This request requires OAuth2: oauth2: `AdminGroups` scope.
        * All arguments will default to `None` if not provided. This does not include `access_token` and `group_id`

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        group_id: `int`
            The group id to edit.

        Other Parameters
        ----------------
        name : `aiobungie.typedefs.NoneOr[str]`
            The name to edit the clan with.
        about : `aiobungie.typedefs.NoneOr[str]`
            The about section to edit the clan with.
        motto : `aiobungie.typedefs.NoneOr[str]`
            The motto section to edit the clan with.
        theme : `aiobungie.typedefs.NoneOr[str]`
            The theme name to edit the clan with.
        tags : `aiobungie.typedefs.NoneOr[collections.Sequence[str]]`
            A sequence of strings to replace the clan tags with.
        is_public : `aiobungie.typedefs.NoneOr[bool]`
            If provided and set to `True`, The clan will set to private.
            If provided and set to `False`, The clan will set to public whether it was or not.
        locale : `aiobungie.typedefs.NoneOr[str]`
            The locale section to edit the clan with.
        avatar_image_index : `aiobungie.typedefs.NoneOr[int]`
            The clan avatar image index to edit the clan with.
        membership_option : `aiobungie.typedefs.NoneOr[aiobungie.typedefs.IntAnd[aiobungie.MembershipOption]]` # noqa: E501 # Line too long
            The clan membership option to edit it with.
        allow_chat : `aiobungie.typedefs.NoneOr[bool]`
            If provided and set to `True`, The clan members will be allowed to chat.
            If provided and set to `False`, The clan members will not be allowed to chat.
        chat_security : `aiobungie.typedefs.NoneOr[typing.Literal[0, 1]]`
            If provided and set to `0`, The clan chat security will be edited to `Group` only.
            If provided and set to `1`, The clan chat security will be edited to `Admin` only.
        call_sign : `aiobungie.typedefs.NoneOr[str]`
            The clan call sign to edit it with.
        homepage : `aiobungie.typedefs.NoneOr[typing.Literal[0, 1, 2]]`
            If provided and set to `0`, The clan chat homepage will be edited to `Wall`.
            If provided and set to `1`, The clan chat homepage will be edited to `Forum`.
            If provided and set to `0`, The clan chat homepage will be edited to `AllianceForum`.
        enable_invite_messaging_for_admins : `aiobungie.typedefs.NoneOr[bool]`
            ???
        default_publicity : `aiobungie.typedefs.NoneOr[typing.Literal[0, 1, 2]]`
            If provided and set to `0`, The clan chat publicity will be edited to `Public`.
            If provided and set to `1`, The clan chat publicity will be edited to `Alliance`.
            If provided and set to `2`, The clan chat publicity will be edited to `Private`.
        is_public_topic_admin : `aiobungie.typedefs.NoneOr[bool]`
            ???
        """

    @abc.abstractmethod
    def fetch_friends(self, access_token: str, /) -> ResponseSig[typedefs.JSONObject]:
        """Fetch bungie friend list.

        .. note::
            This requests OAuth2: ReadUserData scope.

        Parameters
        -----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of an array of the bungie friends's data.
        """

    @abc.abstractmethod
    def fetch_friend_requests(
        self, access_token: str, /
    ) -> ResponseSig[typedefs.JSONObject]:
        """Fetch pending bungie friend requests queue.

        .. note::
            This requests OAuth2: ReadUserData scope.

        Parameters
        -----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of incoming requests and outgoing requests.
        """

    @abc.abstractmethod
    def accept_friend_request(
        self, access_token: str, /, member_id: int
    ) -> ResponseSig[None]:
        """Accepts a friend relationship with the target user. The user must be on your incoming friend request list.

        .. note::
            This request requires OAuth2: BnetWrite scope.

        Parameters
        -----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        member_id : `int`
            The member's id to accept.
        """

    @abc.abstractmethod
    def send_friend_request(
        self, access_token: str, /, member_id: int
    ) -> ResponseSig[None]:
        """Requests a friend relationship with the target user.

        .. note::
            This request requires OAuth2: BnetWrite scope.

        Parameters
        -----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        member_id: `int`
            The member's id to send the request to.
        """

    @abc.abstractmethod
    def decline_friend_request(
        self, access_token: str, /, member_id: int
    ) -> ResponseSig[None]:
        """Decline a friend request with the target user. The user must be in your incoming friend request list.

        .. note::
            This request requires OAuth2: BnetWrite scope.

        Parameters
        -----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        member_id : `int`
            The member's id to decline.
        """

    @abc.abstractmethod
    def remove_friend(self, access_token: str, /, member_id: int) -> ResponseSig[None]:
        """Removes a friend from your friend list. The user must be in your friend list.

        .. note::
            This request requires OAuth2: BnetWrite scope.

        Parameters
        -----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        member_id : `int`
            The member's id to remove.
        """

    @abc.abstractmethod
    def remove_friend_request(
        self, access_token: str, /, member_id: int
    ) -> ResponseSig[None]:
        """Removes a friend from your friend list requests. The user must be in your outgoing request list.

        .. note :
            This request requires OAuth2: BnetWrite scope.

        Parameters
        -----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        member_id: `int`
            The member's id to remove from the requested friend list.
        """

    @abc.abstractmethod
    def approve_all_pending_group_users(
        self,
        access_token: str,
        /,
        group_id: int,
        message: undefined.UndefinedOr[str] = undefined.Undefined,
    ) -> ResponseSig[None]:
        """Apporve all pending users for the given group id.

        .. note::
            This request requires OAuth2: AdminGroups scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        group_id: `int`
            The given group id.

        Other Parameters
        ----------------
        message: `aiobungie.UndefinedOr[str]`
            An optional message to send with the request. Default is `UNDEFINED`.
        """

    @abc.abstractmethod
    def deny_all_pending_group_users(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        message: undefined.UndefinedOr[str] = undefined.Undefined,
    ) -> ResponseSig[None]:
        """Deny all pending users for the given group id.

        .. note::
            This request requires OAuth2: AdminGroups scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        group_id: `int`
            The given group id.

        Other Parameters
        ----------------
        message: `aiobungie.UndefinedOr[str]`
            An optional message to send with the request. Default is `UNDEFINED`.
        """

    @abc.abstractmethod
    def add_optional_conversation(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        name: undefined.UndefinedOr[str] = undefined.Undefined,
        security: typing.Literal[0, 1] = 0,
    ) -> ResponseSig[None]:
        """Add a new chat channel to a group.

        .. note::
            This request requires OAuth2: AdminGroups scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        group_id: `int`
            The given group id.

        Other parameters
        ----------------
        name: `aiobungie.UndefinedOr[str]`
            The chat name. Default to `UNDEFINED`
        security: `typing.Literal[0, 1]`
            The security level of the chat.

            If provided and set to 0, It will be to `Group` only.
            If provided and set to 1, It will be `Admins` only.
            Default is `0`
        """

    @abc.abstractmethod
    def edit_optional_conversation(
        self,
        access_token: str,
        /,
        group_id: int,
        conversation_id: int,
        *,
        name: undefined.UndefinedOr[str] = undefined.Undefined,
        security: typing.Literal[0, 1] = 0,
        enable_chat: bool = False,
    ) -> ResponseSig[None]:
        """Edit the settings of this chat channel.

        .. note::
            This request requires OAuth2: AdminGroups scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        group_id : `int`
            The given group id.
        conversation_id : `int`
            The conversation/chat id.

        Other parameters
        ----------------
        name: `aiobungie.UndefinedOr[str]`
            The new chat name. Default to `UNDEFINED`
        security: `typing.Literal[0, 1]`
            The new security level of the chat.

            If provided and set to 0, It will be to `Group` only.
            If provided and set to 1, It will be `Admins` only.
            Default is `0`
        enable_chat : `bool`
            Whether to enable chatting or not.
            If set to `True` then chatting will be enabled. Otherwise it will be disabled.
        """

    @abc.abstractmethod
    def transfer_item(
        self,
        access_token: str,
        /,
        item_id: int,
        item_hash: int,
        character_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
        *,
        stack_size: int = 1,
        vault: bool = False,
    ) -> ResponseSig[None]:
        """Transfer an item from / to your vault.

        Notes
        -----
        * This method requires OAuth2: MoveEquipDestinyItems scope.
        * This method requires both item id and hash.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        item_id: `int`
            The item instance id you to transfer.
        item_hash : `int`
            The item hash.
        character_id : `int`
            The character id to transfer the item from/to.
        member_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The user membership type.

        Other Parameters
        ----------------
        stack_size : `int`
            The item stack size.
        valut : `bool`
            Whether to trasnfer this item to your valut or not. Defaults to `False`.
        """

    @abc.abstractmethod
    def pull_item(
        self,
        access_token: str,
        /,
        item_id: int,
        item_hash: int,
        character_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
        *,
        stack_size: int = 1,
        vault: bool = False,
    ) -> ResponseSig[None]:
        """pull an item from the postmaster.

        Notes
        -----
        * This method requires OAuth2: MoveEquipDestinyItems scope.
        * This method requires both item id and hash.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        item_id : `int`
            The item instance id to pull.
        item_hash : `int`
            The item hash.
        character_id : `int`
            The character id to pull the item to.
        member_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The user membership type.

        Other Parameters
        ----------------
        stack_size : `int`
            The item stack size.
        valut : `bool`
            Whether to pill this item to your valut or not. Defaults to `False`.
        """

    @abc.abstractmethod
    def fetch_fireteams(
        self,
        activity_type: typedefs.IntAnd[fireteams.FireteamActivity],
        *,
        platform: typedefs.IntAnd[fireteams.FireteamPlatform],
        language: typing.Union[fireteams.FireteamLanguage, str],
        date_range: typedefs.IntAnd[fireteams.FireteamDate] = 0,
        page: int = 0,
        slots_filter: int = 0,
    ) -> ResponseSig[typedefs.JSONObject]:
        """Fetch public Bungie fireteams with open slots.

        Parameters
        ----------
        activity_type : `aiobungie.typedefs.IntAnd[aiobungie.crate.FireteamActivity]`
            The fireteam activity type.

        Other Parameters
        ----------------
        platform : `aiobungie.typedefs.IntAnd[aiobungie.crate.fireteams.FireteamPlatform]`
            If this is provided. Then the results will be filtered with the given platform.
            Defaults to `aiobungie.crate.FireteamPlatform.ANY` which returns all platforms.
        language : `typing.Union[aiobungie.crate.fireteams.FireteamLanguage, str]`
            A locale language to filter the used language in that fireteam.
            Defaults to `aiobungie.crate.FireteamLanguage.ALL`
        date_range : `aiobungie.typedefs.IntAnd[aiobungie.FireteamDate]`
            An integer to filter the date range of the returned fireteams. Defaults to `aiobungie.FireteamDate.ALL`.
        page : `int`
            The page number. By default its `0` which returns all available activities.
        slots_filter : `int`
            Filter the returned fireteams based on available slots. Default is `0`

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the fireteam details.
        """

    @abc.abstractmethod
    def fetch_avaliable_clan_fireteams(
        self,
        access_token: str,
        group_id: int,
        activity_type: typedefs.IntAnd[fireteams.FireteamActivity],
        *,
        platform: typedefs.IntAnd[fireteams.FireteamPlatform],
        language: typing.Union[fireteams.FireteamLanguage, str],
        date_range: typedefs.IntAnd[fireteams.FireteamDate] = 0,
        page: int = 0,
        public_only: bool = False,
        slots_filter: int = 0,
    ) -> ResponseSig[typedefs.JSONObject]:
        """Fetch a clan's fireteams with open slots.

        .. note::
            This method requires OAuth2: ReadGroups scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        group_id : `int`
            The group/clan id of the fireteam.
        activity_type : `aiobungie.typedefs.IntAnd[aiobungie.crate.FireteamActivity]`
            The fireteam activity type.

        Other Parameters
        ----------------
        platform : `aiobungie.typedefs.IntAnd[aiobungie.crate.fireteams.FireteamPlatform]`
            If this is provided. Then the results will be filtered with the given platform.
            Defaults to `aiobungie.crate.FireteamPlatform.ANY` which returns all platforms.
        language : `typing.Union[aiobungie.crate.fireteams.FireteamLanguage, str]`
            A locale language to filter the used language in that fireteam.
            Defaults to `aiobungie.crate.FireteamLanguage.ALL`
        date_range : `aiobungie.typedefs.IntAnd[aiobungie.FireteamDate]`
            An integer to filter the date range of the returned fireteams. Defaults to `aiobungie.FireteamDate.ALL`.
        page : `int`
            The page number. By default its `0` which returns all available activities.
        public_only: `bool`
            If set to True, Then only public fireteams will be returned.
        slots_filter : `int`
            Filter the returned fireteams based on available slots. Default is `0`

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the fireteams detail.
        """

    @abc.abstractmethod
    def fetch_clan_fireteam(
        self, access_token: str, fireteam_id: int, group_id: int
    ) -> ResponseSig[typedefs.JSONObject]:
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
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the fireteam details.
        """

    @abc.abstractmethod
    def fetch_my_clan_fireteams(
        self,
        access_token: str,
        group_id: int,
        *,
        include_closed: bool = True,
        platform: typedefs.IntAnd[fireteams.FireteamPlatform],
        language: typing.Union[fireteams.FireteamLanguage, str],
        filtered: bool = True,
        page: int = 0,
    ) -> ResponseSig[typedefs.JSONObject]:
        """Fetch a clan's fireteams with open slots.

        .. note::
            This method requires OAuth2: ReadGroups scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        group_id : `int`
            The group/clan id to fetch.

        Other Parameters
        ----------------
        include_closed : `bool`
            If provided and set to `True`, It will also return closed fireteams.
            If provided and set to `False`, It will only return public fireteams.
            Default is `True`.
        platform : `aiobungie.typedefs.IntAnd[aiobungie.crate.fireteams.FireteamPlatform]`
            If this is provided. Then the results will be filtered with the given platform.
            Defaults to `aiobungie.crate.FireteamPlatform.ANY` which returns all platforms.
        language : `typing.Union[aiobungie.crate.fireteams.FireteamLanguage, str]`
            A locale language to filter the used language in that fireteam.
            Defaults to `aiobungie.crate.FireteamLanguage.ALL`
        filtered : `bool`
            If set to `True`, it will filter by clan. Otherwise not. Default is `True`.
        page : `int`
            The page number. By default its `0` which returns all available activities.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object of the fireteams detail.
        """

    @abc.abstractmethod
    def fetch_private_clan_fireteams(
        self, access_token: str, group_id: int, /
    ) -> ResponseSig[int]:
        """Fetch the active count of the clan fireteams that are only private.

        .. note::
            This method requires OAuth2: ReadGroups scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        group_id : `int`
            The group/clan id.

        Returns
        -------
        `ResponseSig[int]`
            The active fireteams count. Max value returned is 25.
        """

    @abc.abstractmethod
    async def fetch_oauth2_tokens(self, code: str, /) -> _rest.OAuth2Response:
        """Makes a POST request and fetch the OAuth2 access_token and refresh token.

        Parameters
        -----------
        code : `str`
            The Authorization code received from the authorization endpoint found in the URL parameters.

        Returns
        -------
        `aiobungie.rest.OAuth2Response`
            An OAuth2 deserialized response.

        Raises
        ------
        `aiobungie.error.Unauthorized`
            The passed code was invalid.
        """

    @abc.abstractmethod
    async def refresh_access_token(self, refresh_token: str, /) -> _rest.OAuth2Response:
        """Refresh OAuth2 access token given its refresh token.

        Parameters
        ----------
        refresh_token : `str`
            The refresh token.

        Returns
        -------
        `aiobungie.rest.OAuth2Response`
            An OAuth2 deserialized response.
        """

    @abc.abstractmethod
    def fetch_user_credentials(
        self, access_token: str, membership_id: int, /
    ) -> ResponseSig[typedefs.JSONArray]:
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
        `ResponseSig[aiobungie.typedefs.JSONArray]`
            A JSON array of the returned credentials.

        Raises
        ------
        `aiobungie.Unauthorized`
            The access token was wrong or no access token passed.
        """

    @abc.abstractmethod
    def insert_socket_plug(
        self,
        action_token: str,
        /,
        instance_id: int,
        plug: typing.Union[_rest.PlugSocketBuilder, dict[str, int]],
        character_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[typedefs.JSONObject]:
        """Insert a plug into a socketed item.

        .. note::
            OAuth2: AdvancedWriteActions scope is required

        Parameters
        ----------
        action_token : `str`
            Action token provided by the AwaGetActionToken API call.
        instance_id : `int`
            The item instance id that's plug inserted.
        plug : `typing.Union[aiobungie.PlugSocketbuilder, dict[str, int]]`
            Either a PlugSocketBuilder object or a raw dict contains key, value for the plug entries.

        Example
        -------
        ```py
        plug = (
            aiobungie.PlugSocketBuilder()
            .set_socket_array(0)
            .set_socket_index(0)
            .set_plug_item(3023847)
            .collect()
        )
        await insert_socket_plug_free(..., plug=plug)
        ```
        character_id : `int`
            The character's id.
        membership_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The membership type.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object contains the changed item details.

        Raises
        ------
        `aiobungie.Unauthorized`
            The access token was wrong or no access token passed.
        """

    @abc.abstractmethod
    def insert_socket_plug_free(
        self,
        access_token: str,
        /,
        instance_id: int,
        plug: typing.Union[_rest.PlugSocketBuilder, dict[str, int]],
        character_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[typedefs.JSONObject]:
        """Insert a plug into a socketed item. This doesn't require an Action token.

        .. note::
            OAuth2: MoveEquipDestinyItems scope is required

        Parameters
        ----------
        instance_id : `int`
            The item instance id that's plug inserted.
        plug : `typing.Union[aiobungie.PlugSocketbuilder, dict[str, int]]`
            Either a PlugSocketBuilder object or a raw dict contains key, value for the plug entries.

        Example
        -------
        ```py
        plug = (
            aiobungie.PlugSocketBuilder()
            .set_socket_array(0)
            .set_socket_index(0)
            .set_plug_item(3023847)
            .collect()
        )
        await insert_socket_plug_free(..., plug=plug)
        ```
        character_id : `int`
            The character's id.
        membership_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The membership type.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object contains the changed item details.

        Raises
        ------
        `aiobungie.Unauthorized`
            The access token was wrong or no access token passed.
        """

    @abc.abstractmethod
    def set_item_lock_state(
        self,
        access_token: str,
        state: bool,
        /,
        item_id: int,
        character_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[int]:
        """Set the Lock State for an instanced item.

        .. note::
            OAuth2: MoveEquipDestinyItems scope is required

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        state : `bool`
            If `True`, The item will be locked, If `False`, The item will be unlocked.
        item_id : `int`
            The item id.
        character_id : `int`
            The character id.
        membership_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The membership type for the associated account.

        Returns
        -------
        `ResponseSig[int]`
            An integer represents whether the request was successful or failed.

        Raises
        ------
        `aiobungie.Unauthorized`
            - The access token was wrong
            - No access token passed.
            - Other authorization causes.
        """

    @abc.abstractmethod
    def set_quest_track_state(
        self,
        access_token: str,
        state: bool,
        /,
        item_id: int,
        character_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[int]:
        """Set the Tracking State for an instanced Quest or Bounty.

        .. note::
            OAuth2: MoveEquipDestinyItems scope is required

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        state : `bool`
            If `True`, The item will be locked, If `False`, The item will be unlocked.
        item_id : `int`
            The item id.
        character_id : `int`
            The character id.
        membership_type : `aiobungie.typedefs.IntAnd[aiobungie.MembershipType]`
            The membership type for the associated account.

        Returns
        -------
        `ResponseSig[int]`
            An integer represents whether the request was successful or failed.

        Raises
        ------
        `aiobungie.Unauthorized`
            - The access token was wrong
            - No access token passed.
            - Other authorization causes.
        """

    @abc.abstractmethod
    def search_entities(
        self, name: str, entity_type: str, *, page: int = 0
    ) -> ResponseSig[typedefs.JSONObject]:
        """Search for Destiny2 entities given a name and its type.

        Parameters
        ----------
        name : `str`
            The name of the entity, i.e., Thunderlord, One thousand voices.
        entity_type : `str`
            The type of the entity, AKA Definition, For an example `DestinyInventoryItemDefinition`

        Other Parameters
        ----------------
        page : `int`
            An optional page to return. Default to 0.

        Returns
        -------
        `ResponseSig[aiobungie.typedefs.JSONObject]`
            A JSON object contains details about the searched term.
        """

    @abc.abstractmethod
    def fetch_item(
        self, member_id: int, item_id: int, /
    ) -> ResponseSig[typedefs.JSONObject]:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_clan_weekly_rewards(
        self, clan_id: int, /
    ) -> ResponseSig[typedefs.JSONObject]:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_weapon_history(
        self,
        character_id: int,
        member_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[typedefs.JSONObject]:
        raise NotImplementedError
