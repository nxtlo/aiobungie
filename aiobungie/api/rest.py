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

import datetime
import pathlib

__all__ = ("RESTClient",)

import abc
import collections.abc as collections
import typing

from aiobungie import traits
from aiobungie.internal import enums, helpers

if typing.TYPE_CHECKING:
    import concurrent.futures
    import types

    from typing_extensions import Self

    from aiobungie import builders, typedefs
    from aiobungie.crates import clans, fireteams

    _ALLOWED_LANGS = typing.Literal[
        "en",
        "fr",
        "es",
        "es-mx",
        "de",
        "it",
        "ja",
        "pt-br",
        "ru",
        "pl",
        "ko",
        "zh-cht",
        "zh-chs",
    ]


class RESTClient(traits.RESTful, abc.ABC):
    """An API interface for functionality that a REST API implementation provides."""

    __slots__ = ()

    if typing.TYPE_CHECKING:

        async def __aenter__(self) -> Self: ...

        async def __aexit__(
            self,
            exception_type: type[BaseException] | None,
            exception: BaseException | None,
            exception_traceback: types.TracebackType | None,
        ) -> None: ...

    @abc.abstractmethod
    async def read_manifest_bytes(self, language: _ALLOWED_LANGS = "en", /) -> bytes:
        """Read raw manifest SQLite database bytes response.

        This method can be used to write the bytes to zipped file
        and then extract it to get the manifest content.

        Parameters
        ----------
        language : `str`
            The manifest database language bytes to get.

        Returns
        -------
        `bytes`
            The bytes to read and write the manifest database.
        """

    @abc.abstractmethod
    async def fetch_manifest_path(self) -> typedefs.JSONObject:
        """Fetch the manifest JSON paths.

        Returns
        -------
        `typedefs.JSONObject`
            The manifest JSON paths.
        """

    @abc.abstractmethod
    async def download_json_manifest(
        self,
        file_name: str = "manifest",
        path: str | pathlib.Path = ".",
        *,
        language: _ALLOWED_LANGS = "en",
        executor: concurrent.futures.Executor | None = None,
    ) -> pathlib.Path:
        """Download the Bungie manifest json file.

        Example
        -------
        ```py
        manifest = await rest.download_json_manifest()
        with open(manifest, "r") as f:
            to_dict = json.loads(f.read())
            item_definitions = to_dict['DestinyInventoryItemDefinition']
        ```

        Parameters
        ----------
        file_name: `str`
            The file name to save the manifest json file. Default is `manifest`.
        path: `str` | `pathlib.Path`
            The path to save the manifest json file. Default is the current directory. Example `"D:/"`
        language: `str`
            The manifest database language bytes to get. Default is English.
        executor: `concurrent.futures.Executor | None`
            An optional executor which will be used to write the bytes of the manifest.

        Returns
        -------
        `pathlib.Path`
            The path of this JSON manifest.
        """

    @abc.abstractmethod
    async def download_sqlite_manifest(
        self,
        language: _ALLOWED_LANGS = "en",
        name: str = "manifest",
        path: str | pathlib.Path = ".",
        *,
        force: bool = False,
        executor: concurrent.futures.Executor | None = None,
    ) -> pathlib.Path:
        """Downloads the SQLite version of Destiny2's Manifest.

        Example
        -------
        ```py
        manifest = await rest.download_sqlite_manifest()
        with sqlite3.connect(manifest) as conn:
            ...
        ```

        Parameters
        ----------
        language : `str`
            The manifest language to download, Default is English.
        path: `str` | `pathlib.Path`
            The path to download this manifest. Example `"/tmp/databases/"`, Default is the current directory.
        name : `str`
            The manifest database file name. Default is `manifest`
        force : `bool`
            Whether to force the download. Default is `False`. However if set to true the old
            file will get unlinked and a new one will begin to download.
        executor: `concurrent.futures.Executor | None`
            An optional executor which will be used to write the bytes of the manifest.

        Returns
        --------
        `pathlib.Path`
            A pathlib object of the `.sqlite` file.

        Raises
        ------
        `FileExistsError`
            If the manifest file exists and `force` is `False`.
        `ValueError`
            If the provided language was not recognized.
        """

    @abc.abstractmethod
    async def fetch_manifest_version(self) -> str:
        """Fetch the manifest version.

        Returns
        -------
        `str`
            The manifest version.
        """

    @abc.abstractmethod
    async def fetch_bungie_user(self, id: int) -> typedefs.JSONObject:
        """Fetch a Bungie user by their id.

        Parameters
        ----------
        id: `int`
            The user id.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of users objects.

        Raises
        ------
        `aiobungie.error.NotFound`
            The user was not found.
        """

    @abc.abstractmethod
    async def search_users(self, name: str, /) -> typedefs.JSONObject:
        """Search for users by their global name and return all users who share this name.

        Parameters
        ----------
        name : `str`
            The user name.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of an array of the found users.

        Raises
        ------
        `aiobungie.NotFound`
            The user(s) was not found.

        """

    @abc.abstractmethod
    async def fetch_user_themes(self) -> typedefs.JSONArray:
        """Fetch all available user themes.

        Returns
        -------
        `aiobungie.typedefs.JSONArray`
            A JSON array of user themes.
        """

    @abc.abstractmethod
    async def fetch_sanitized_membership(
        self, membership_id: int, /
    ) -> typedefs.JSONObject:
        """Fetch a list of all display names linked to `membership_id`, Which is profanity filtered.

        Parameters
        ----------
        membership_id: `int`
            The membership ID to fetch

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object contains all the available display names.
        """

    @abc.abstractmethod
    async def fetch_hardlinked_credentials(
        self,
        credential: int,
        type: enums.CredentialType | int = enums.CredentialType.STEAMID,
        /,
    ) -> typedefs.JSONObject:
        """Gets any hard linked membership given a credential.

        Only works for credentials that are public just `aiobungie.CredentialType.STEAMID` right now.
        Cross Save aware.

        Parameters
        ----------
        credential: `int`
            A valid SteamID64
        type: `aiobungie.aiobungie.CredentialType | int`
            The credential type. This must not be changed
            Since its only credential that works "currently"

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the found user hard linked types.
        """

    @abc.abstractmethod
    async def fetch_membership_from_id(
        self,
        id: int,
        type: enums.MembershipType | int = enums.MembershipType.NONE,
        /,
    ) -> typedefs.JSONObject:
        """Fetch Bungie user's memberships from their id.

        Parameters
        ----------
        id : `int`
            The user's id.
        type : `aiobungie.aiobungie.MembershipType | int`
            The user's membership type.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the found user.

        Raises
        ------
        aiobungie.NotFound
            The requested user was not found.
        """

    @abc.abstractmethod
    async def fetch_profile(
        self,
        membership_id: int,
        type: enums.MembershipType | int,
        components: collections.Sequence[enums.ComponentType],
        auth: str | None = None,
    ) -> typedefs.JSONObject:
        """
        Fetch a bungie profile.

        Parameters
        ----------
        membership_id: `int`
            The member's id.
        type: `aiobungie.aiobungie.MembershipType | int`
            A valid membership type.
        components : `collections.Sequence[aiobungie.ComponentType]`
            A sequence of profile components to collect and return.

        Other Parameters
        ----------------
        auth : `str | None`
            A bearer access_token to make the request with.
            This is optional and limited to components that only requires an Authorization token.

        Returns
        --------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the found profile.

        Raises
        ------
        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """

    @abc.abstractmethod
    async def fetch_membership(
        self,
        name: str,
        code: int,
        type: enums.MembershipType | int = enums.MembershipType.ALL,
        /,
    ) -> typedefs.JSONArray:
        """Fetch a Destiny 2 Player.

        Parameters
        -----------
        name: `str`
            The unique Bungie player name.
        code : `int`
            The unique Bungie display name code.
        type: `aiobungie.aiobungie.MembershipType | int`
            The player's membership type, e,g. XBOX, STEAM, PSN

        Returns
        --------
        `aiobungie.typedefs.JSONArray`
            A JSON array of the found player's memberships.

        Raises
        ------
        `aiobungie.NotFound`
            The player was not found.
        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """

    @abc.abstractmethod
    async def fetch_character(
        self,
        member_id: int,
        membership_type: enums.MembershipType | int,
        character_id: int,
        components: collections.Sequence[enums.ComponentType],
        auth: str | None = None,
    ) -> typedefs.JSONObject:
        """Fetch a Destiny 2 player's characters.

        Parameters
        ----------
        member_id: `int`
            A valid bungie member id.
        membership_type: `aiobungie.aiobungie.internal.enums.MembershipType | int`
            The member's membership type.
        character_id : `int`
            The character id to return.
        components: `collections.Sequence[aiobungie.ComponentType]`
            A list of character components to collect and return.

        Other Parameters
        ----------------
        auth : `str | None`
            A bearer access_token to make the request with.
            This is optional and limited to components that only requires an Authorization token.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the requested character.

        Raises
        ------
        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """

    @abc.abstractmethod
    async def fetch_activities(
        self,
        member_id: int,
        character_id: int,
        mode: enums.GameMode | int,
        membership_type: enums.MembershipType | int,
        *,
        page: int = 1,
        limit: int = 1,
    ) -> typedefs.JSONObject:
        """Fetch a Destiny 2 activity for the specified user id and character.

        Parameters
        ----------
        member_id: `int`
            The user id that starts with `4611`.
        character_id: `int`
            The id of the character to retrieve.
        mode: `aiobungie.aiobungie.GameMode | int`
            This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc.
        membership_type: `aiobungie.aiobungie.internal.enums.MembershipType | int`
            The Destiny 2 membership type.

        Other Parameters
        ----------------
        page: `int`
            The page number. Default to `1`
        limit: `int`
            Limit the returned result. Default to `1`

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the player's activities.

        Raises
        ------
        `aiobungie.error.NotFound`
            The activity was not found.
        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """

    @abc.abstractmethod
    async def fetch_post_activity(self, instance_id: int, /) -> typedefs.JSONObject:
        """Fetch a post activity details.

        Parameters
        ----------
        instance_id: `int`
            The activity instance id.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the post activity.
        """

    @abc.abstractmethod
    async def report_player(
        self,
        access_token: str,
        /,
        activity_id: int,
        character_id: int,
        reason_hashes: collections.Sequence[int],
        reason_category_hashes: collections.Sequence[int],
    ) -> None:
        """Report a player that you met in an activity that was engaging in ToS-violating activities.

        .. note::
            This method requires `BnetWrite` OAuth2 scope.

        Both you and the offending player must have played in the `activity_id` passed in.
        Please use this judiciously and only when you have strong suspicions of violation, pretty please.

        Parameters
        ----------
        access_token: `str`
            The bearer access token associated with the bungie account that
            will be used to make the request with.
        activity_id: `int`
            The activity where you ran into the person you're reporting.
        character_id: `int`
            The character ID of the person you're reporting.
        reason_hashes: `Sequence[int]`
            [See](https://bungie-net.github.io/multi/schema_Destiny-Reporting-Requests-DestinyReportOffensePgcrRequest.html#schema_Destiny-Reporting-Requests-DestinyReportOffensePgcrRequest)
        reason_category_hashes: `Sequence[int]`
            [See](https://bungie-net.github.io/multi/schema_Destiny-Reporting-Requests-DestinyReportOffensePgcrRequest.html#schema_Destiny-Reporting-Requests-DestinyReportOffensePgcrRequest)
        """

    @abc.abstractmethod
    async def fetch_clan_from_id(
        self, id: int, /, access_token: str | None = None
    ) -> typedefs.JSONObject:
        """Fetch a Bungie Clan by its id.

        Parameters
        -----------
        id : `int`
            The clan id.

        Other Parameters
        ----------------
        access_token : `str | None`
            An optional access token to make the request with.

            If the token was bound to a member of the clan,
            This field `aiobungie.crates.Clan.current_user_membership` will be available
            and will return the membership of the user who made this request.

        Returns
        --------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the clan.

        Raises
        ------
        `aiobungie.NotFound`
            The clan was not found.
        """

    @abc.abstractmethod
    async def fetch_clan(
        self,
        name: str,
        /,
        access_token: str | None = None,
        *,
        type: enums.GroupType | int = enums.GroupType.CLAN,
    ) -> typedefs.JSONObject:
        """Fetch a Clan by its name.
        This method will return the first clan found with given name name.

        Parameters
        ----------
        name : `str`
            The clan name.

        Other Parameters
        ----------------
        access_token : `str | None`
            An optional access token to make the request with.

            If the token was bound to a member of the clan,
            This field `aiobungie.crates.Clan.current_user_membership` will be available
            and will return the membership of the user who made this request.
        type : `aiobungie.aiobungie.GroupType | int`
            The group type, Default is one.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the clan.

        Raises
        ------
        `aiobungie.NotFound`
            The clan was not found.
        """

    @abc.abstractmethod
    async def fetch_clan_conversations(self, clan_id: int, /) -> typedefs.JSONArray:
        """Fetch a clan's conversations.

        Parameters
        ----------
        clan_id : `int`
            The clan's id.

        Returns
        -------
        `aiobungie.typedefs.JSONArray`
            A JSON array of the conversations.
        """

    @abc.abstractmethod
    async def fetch_clan_admins(self, clan_id: int, /) -> typedefs.JSONObject:
        """Fetch the admins and founder members of the clan.

        Parameters
        ----------
        clan_id : `int`
            The clan id.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the clan admins and founder members.

        Raises
        ------
        `aiobungie.NotFound`
            The clan was not found.
        """

    @abc.abstractmethod
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
    ) -> typedefs.JSONObject:
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
        `aiobungie.typedefs.JSONObject`
            A JSON object of the search results.

        Raises
        ------
        `ValueError`
            If the group type is `aiobungie.GroupType.CLAN` and `group_member_count_filter`,
            `locale_filter` and `tag_text` are not `None`.
        """

    @abc.abstractmethod
    async def fetch_groups_for_member(
        self,
        member_id: int,
        member_type: enums.MembershipType | int,
        /,
        *,
        filter: int = 0,
        group_type: enums.GroupType | int = enums.GroupType.CLAN,
    ) -> typedefs.JSONObject:
        """Fetch the information about the groups for a member.

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
        `aiobungie.typedefs.JSONObject`
            A JSON object of an array of the member's membership data and groups data.
        """

    @abc.abstractmethod
    async def fetch_potential_groups_for_member(
        self,
        member_id: int,
        member_type: enums.MembershipType | int,
        /,
        *,
        filter: int = 0,
        group_type: enums.GroupType | int = enums.GroupType.CLAN,
    ) -> typedefs.JSONObject:
        """Get information about the groups that a given member has applied to or been invited to.

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
        `aiobungie.typedefs.JSONObject`
            A JSON object of an array of the member's membership data and groups data.
        """

    @abc.abstractmethod
    async def fetch_clan_members(
        self,
        clan_id: int,
        /,
        *,
        name: str | None = None,
        type: enums.MembershipType | int = enums.MembershipType.NONE,
    ) -> typedefs.JSONObject:
        """Fetch all Bungie Clan members.

        Parameters
        ----------
        clan_id : `int`
            The clans id

        Other Parameters
        ----------------
        name : `str | None`
            If provided, Only players matching this name will be returned.
        type : `aiobungie.aiobungie.MembershipType | int`
            An optional clan member's membership type.
            Default is set to `aiobungie.MembershipType.NONE`
            Which returns the first matched clan member by their name.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of an array of clan members.

        Raises
        ------
        `aiobungie.NotFound`
            The clan was not found.
        """

    @abc.abstractmethod
    async def fetch_entity(self, type: str, hash: int) -> typedefs.JSONObject:
        """Fetch a Destiny definition item given its type and hash.

        Parameters
        ----------
        type: `str`
            Entity's type definition.
        hash: `int`
            Entity's hash.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the definition data.
        """

    @abc.abstractmethod
    async def fetch_inventory_item(self, hash: int, /) -> typedefs.JSONObject:
        """Fetch a Destiny inventory item entity given a its hash.

        Parameters
        ----------
        hash: `int`
            Entity's hash.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the inventory item.
        """

    @abc.abstractmethod
    async def fetch_objective_entity(self, hash: int, /) -> typedefs.JSONObject:
        """Fetch a Destiny objective entity given a its hash.

        Parameters
        ----------
        hash: `int`
            objective's hash.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the objective data.
        """

    @abc.abstractmethod
    async def fetch_application(self, appid: int, /) -> typedefs.JSONObject:
        """Fetch a Bungie Application.

        Parameters
        -----------
        appid: `int`
            The application id.

        Returns
        --------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the application.
        """

    @abc.abstractmethod
    async def fetch_linked_profiles(
        self,
        member_id: int,
        member_type: enums.MembershipType | int,
        /,
        *,
        all: bool = False,
    ) -> typedefs.JSONObject:
        """Returns a summary information about all profiles linked to the requested member.

        The passed membership id/type maybe a Bungie.Net membership or a Destiny memberships.

        .. note::
            It will only return linked accounts whose linkages you are allowed to view.

        Parameters
        ----------
        member_id : `int`
            The ID of the membership. This must be a valid Bungie.Net or PSN or Xbox ID.
        member_type : `aiobungie.aiobungie.MembershipType | int`
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
        `aiobungie.typedefs.JSONObject`
        A JSON object which contains an Array of profiles, an Array of profiles with errors and Bungie.Net membership
        """

    @abc.abstractmethod
    async def fetch_clan_banners(self) -> typedefs.JSONObject:
        """Fetch the values of the clan banners.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the clan banners.
        """

    @abc.abstractmethod
    async def fetch_public_milestones(self) -> typedefs.JSONObject:
        """Fetch the available milestones.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of information about the milestones.
        """

    @abc.abstractmethod
    async def fetch_public_milestone_content(
        self, milestone_hash: int, /
    ) -> typedefs.JSONObject:
        """Fetch the milestone content given its hash.

        Parameters
        ----------
        milestone_hash : `int`
            The milestone hash.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of information related to the fetched milestone.
        """

    @abc.abstractmethod
    async def fetch_current_user_memberships(
        self, access_token: str, /
    ) -> typedefs.JSONObject:
        """Fetch a bungie user's accounts with the signed in user.
        This GET method  requires a Bearer access token for the authorization.

        .. note::
            This requires OAuth2 scope enabled and the valid Bearer `access_token`.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the bungie net user and destiny memberships of this account.
        """

    @abc.abstractmethod
    async def equip_item(
        self,
        access_token: str,
        /,
        item_id: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> None:
        """Equip an item to a character.

        .. note::
            This requires the OAuth2: MoveEquipDestinyItems scope.
            Also You must have a valid Destiny account, and either be
            in a social space, in orbit or offline.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        item_id : `int`
            The item id.
        character_id : `int`
            The character's id to equip the item to.
        membership_type : `aiobungie.aiobungie.MembershipType | int`
            The membership type associated with this player.
        """

    @abc.abstractmethod
    async def equip_items(
        self,
        access_token: str,
        /,
        item_ids: collections.Sequence[int],
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> None:
        """Equip multiple items to a character.

        .. note::
            This requires the OAuth2: MoveEquipDestinyItems scope.
            Also You must have a valid Destiny account, and either be
            in a social space, in orbit or offline.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        item_ids : `Sequence[int]`
            A sequence of item ids.
        character_id : `int`
            The character's id to equip the item to.
        membership_type : `aiobungie.aiobungie.MembershipType | int`
            The membership type associated with this player.
        """

    @abc.abstractmethod
    async def ban_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
        *,
        length: int = 0,
        comment: str | None = None,
    ) -> None:
        """Bans a member from the clan.

        .. note::
            This request requires OAuth2: oauth2: `AdminGroups` scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        group_id: `int`
            The group id.
        membership_id : `int`
            The member id to ban.
        membership_type : `aiobungie.aiobungie.MembershipType | int`
            The member's membership type.

        Other Parameters
        ----------------
        length: `int`
            An optional ban length.
        comment: `aiobungie.UndefinedOr[str]`
            An optional comment to this ban. Default is `UNDEFINED`
        """

    @abc.abstractmethod
    async def unban_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
    ) -> None:
        """Unban a member from the clan.

        .. note::
            This request requires OAuth2: oauth2: `AdminGroups` scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        group_id: `int`
            The group id.
        membership_id : `int`
            The member id to unban.
        membership_type : `aiobungie.aiobungie.MembershipType | int`
            The member's membership type.
        """

    @abc.abstractmethod
    async def kick_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
    ) -> typedefs.JSONObject:
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
        `aiobungie.typedefs.JSONObject`
            A JSON object of the group that the member has been kicked from.
        """

    @abc.abstractmethod
    async def edit_clan_options(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        invite_permissions_override: bool | None = None,
        update_culture_permissionOverride: bool | None = None,
        host_guided_game_permission_override: typing.Literal[0, 1, 2] | None = None,
        update_banner_permission_override: bool | None = None,
        join_level: enums.ClanMemberType | int | None = None,
    ) -> None:
        """Edit the clan options.

        Notes
        -----
        * This request requires OAuth2: oauth2: `AdminGroups` scope.
        * All arguments will default to `None` if not provided. This does not include `access_token` and `group_id`

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        group_id: `int`
            The group id.

        Other Parameters
        ----------------
        invite_permissions_override : `bool | None`
            Minimum Member Level allowed to invite new members to group
            Always Allowed: Founder, Acting Founder
            True means admins have this power, false means they don't
            Default is False for clans, True for groups.
        update_culture_permissionOverride : `bool | None`
            Minimum Member Level allowed to update group culture
            Always Allowed: Founder, Acting Founder
            True means admins have this power, false means they don't
            Default is False for clans, True for groups.
        host_guided_game_permission_override : `aiobungie.typedefs.NoneOr[typing.Literal[0, 1, 2]]`
            Minimum Member Level allowed to host guided games
            Always Allowed: Founder, Acting Founder, Admin
            Allowed Overrides: `0` -> None, `1` -> Beginner `2` -> Member.
            Default is Member for clans, None for groups, although this means nothing for groups.
        update_banner_permission_override : `bool | None`
            Minimum Member Level allowed to update banner
            Always Allowed: Founder, Acting Founder
            True means admins have this power, false means they don't
            Default is False for clans, True for groups.
        join_level : `aiobungie.ClanMemberType`
            Level to join a member at when accepting an invite, application, or joining an open clan.
            Default is `aiobungie.ClanMemberType.BEGINNER`
        """

    @abc.abstractmethod
    async def edit_clan(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        name: str | None = None,
        about: str | None = None,
        motto: str | None = None,
        theme: str | None = None,
        tags: collections.Sequence[str] | None = None,
        is_public: bool | None = None,
        locale: str | None = None,
        avatar_image_index: int | None = None,
        membership_option: enums.MembershipOption | int | None = None,
        allow_chat: bool | None = None,
        chat_security: typing.Literal[0, 1] | None = None,
        call_sign: str | None = None,
        homepage: typing.Literal[0, 1, 2] | None = None,
        enable_invite_messaging_for_admins: bool | None = None,
        default_publicity: typing.Literal[0, 1, 2] | None = None,
        is_public_topic_admin: bool | None = None,
    ) -> None:
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
        name : `str | None`
            The name to edit the clan with.
        about : `str | None`
            The about section to edit the clan with.
        motto : `str | None`
            The motto section to edit the clan with.
        theme : `str | None`
            The theme name to edit the clan with.
        tags : `collections.Sequence[str] | None`
            A sequence of strings to replace the clan tags with.
        is_public : `bool | None`
            If provided and set to `True`, The clan will set to private.
            If provided and set to `False`, The clan will set to public whether it was or not.
        locale : `str | None`
            The locale section to edit the clan with.
        avatar_image_index : `int | None`
            The clan avatar image index to edit the clan with.
        membership_option : `aiobungie.typedefs.NoneOr[aiobungie.aiobungie.MembershipOption | int]` # noqa: E501 # Line too long
            The clan membership option to edit it with.
        allow_chat : `bool | None`
            If provided and set to `True`, The clan members will be allowed to chat.
            If provided and set to `False`, The clan members will not be allowed to chat.
        chat_security : `aiobungie.typedefs.NoneOr[typing.Literal[0, 1]]`
            If provided and set to `0`, The clan chat security will be edited to `Group` only.
            If provided and set to `1`, The clan chat security will be edited to `Admin` only.
        call_sign : `str | None`
            The clan call sign to edit it with.
        homepage : `aiobungie.typedefs.NoneOr[typing.Literal[0, 1, 2]]`
            If provided and set to `0`, The clan chat homepage will be edited to `Wall`.
            If provided and set to `1`, The clan chat homepage will be edited to `Forum`.
            If provided and set to `0`, The clan chat homepage will be edited to `AllianceForum`.
        enable_invite_messaging_for_admins : `bool | None`
            ???
        default_publicity : `aiobungie.typedefs.NoneOr[typing.Literal[0, 1, 2]]`
            If provided and set to `0`, The clan chat publicity will be edited to `Public`.
            If provided and set to `1`, The clan chat publicity will be edited to `Alliance`.
            If provided and set to `2`, The clan chat publicity will be edited to `Private`.
        is_public_topic_admin : `bool | None`
            ???
        """

    @abc.abstractmethod
    async def fetch_friends(self, access_token: str, /) -> typedefs.JSONObject:
        """Fetch bungie friend list.

        .. note::
            This requests OAuth2: ReadUserData scope.

        Parameters
        -----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of an array of the bungie friends's data.
        """

    @abc.abstractmethod
    async def fetch_friend_requests(self, access_token: str, /) -> typedefs.JSONObject:
        """Fetch pending bungie friend requests queue.

        .. note::
            This requests OAuth2: ReadUserData scope.

        Parameters
        -----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of incoming requests and outgoing requests.
        """

    @abc.abstractmethod
    async def accept_friend_request(self, access_token: str, /, member_id: int) -> None:
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
    async def send_friend_request(self, access_token: str, /, member_id: int) -> None:
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
    async def decline_friend_request(
        self, access_token: str, /, member_id: int
    ) -> None:
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
    async def remove_friend(self, access_token: str, /, member_id: int) -> None:
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
    async def remove_friend_request(self, access_token: str, /, member_id: int) -> None:
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
    async def approve_all_pending_group_users(
        self,
        access_token: str,
        /,
        group_id: int,
        message: str | None = None,
    ) -> None:
        """Approve all pending users for the given group id.

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
    async def deny_all_pending_group_users(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        message: str | None = None,
    ) -> None:
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
    async def add_optional_conversation(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        name: str | None = None,
        security: typing.Literal[0, 1] = 0,
    ) -> None:
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
    async def edit_optional_conversation(
        self,
        access_token: str,
        /,
        group_id: int,
        conversation_id: int,
        *,
        name: str | None = None,
        security: typing.Literal[0, 1] = 0,
        enable_chat: bool = False,
    ) -> None:
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
    async def transfer_item(
        self,
        access_token: str,
        /,
        item_id: int,
        item_hash: int,
        character_id: int,
        member_type: enums.MembershipType | int,
        *,
        stack_size: int = 1,
        vault: bool = False,
    ) -> None:
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
        member_type : `aiobungie.aiobungie.MembershipType | int`
            The user membership type.

        Other Parameters
        ----------------
        stack_size : `int`
            The item stack size.
        vault : `bool`
            Whether to transfer this item to your vault or not. Defaults to `False`.
        """

    @abc.abstractmethod
    async def pull_item(
        self,
        access_token: str,
        /,
        item_id: int,
        item_hash: int,
        character_id: int,
        member_type: enums.MembershipType | int,
        *,
        stack_size: int = 1,
        vault: bool = False,
    ) -> None:
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
        member_type : `aiobungie.aiobungie.MembershipType | int`
            The user membership type.

        Other Parameters
        ----------------
        stack_size : `int`
            The item stack size.
        vault : `bool`
            If `True`, an extra HTTP call will be performed to transfer this item to the vault, Defaults to `False`.
        """

    @abc.abstractmethod
    async def fetch_fireteams(
        self,
        activity_type: fireteams.FireteamActivity | int,
        *,
        platform: fireteams.FireteamPlatform | int,
        language: fireteams.FireteamLanguage | str,
        date_range: fireteams.FireteamDate | int = 0,
        page: int = 0,
        slots_filter: int = 0,
    ) -> typedefs.JSONObject:
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
        date_range : `aiobungie.aiobungie.FireteamDate | int`
            An integer to filter the date range of the returned fireteams. Defaults to `aiobungie.FireteamDate.ALL`.
        page : `int`
            The page number. By default its `0` which returns all available activities.
        slots_filter : `int`
            Filter the returned fireteams based on available slots. Default is `0`

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the fireteam details.
        """

    @abc.abstractmethod
    async def fetch_available_clan_fireteams(
        self,
        access_token: str,
        group_id: int,
        activity_type: fireteams.FireteamActivity | int,
        *,
        platform: fireteams.FireteamPlatform | int,
        language: fireteams.FireteamLanguage | str,
        date_range: fireteams.FireteamDate | int = 0,
        page: int = 0,
        public_only: bool = False,
        slots_filter: int = 0,
    ) -> typedefs.JSONObject:
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
        date_range : `aiobungie.aiobungie.FireteamDate | int`
            An integer to filter the date range of the returned fireteams. Defaults to `aiobungie.FireteamDate.ALL`.
        page : `int`
            The page number. By default its `0` which returns all available activities.
        public_only: `bool`
            If set to True, Then only public fireteams will be returned.
        slots_filter : `int`
            Filter the returned fireteams based on available slots. Default is `0`

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the fireteams detail.
        """

    @abc.abstractmethod
    async def fetch_clan_fireteam(
        self, access_token: str, fireteam_id: int, group_id: int
    ) -> typedefs.JSONObject:
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
        `aiobungie.typedefs.JSONObject`
            A JSON object of the fireteam details.
        """

    @abc.abstractmethod
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
    ) -> typedefs.JSONObject:
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
        platform : `aiobungie.aiobungie.crates.fireteams.FireteamPlatform | int`
            If this is provided. Then the results will be filtered with the given platform.
            Defaults to `aiobungie.crates.FireteamPlatform.ANY` which returns all platforms.
        language : `aiobungie.crates.fireteams.FireteamLanguage | str`
            A locale language to filter the used language in that fireteam.
            Defaults to `aiobungie.crates.FireteamLanguage.ALL`
        filtered : `bool`
            If set to `True`, it will filter by clan. Otherwise not. Default is `True`.
        page : `int`
            The page number. By default its `0` which returns all available activities.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the fireteams detail.
        """

    @abc.abstractmethod
    async def fetch_private_clan_fireteams(
        self, access_token: str, group_id: int, /
    ) -> int:
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
        `int`
            The active fireteams count. Max value returned is 25.
        """

    @abc.abstractmethod
    async def fetch_oauth2_tokens(self, code: str, /) -> builders.OAuth2Response:
        """Makes a POST request and fetch the OAuth2 access_token and refresh token.

        Parameters
        -----------
        code : `str`
            The Authorization code received from the authorization endpoint found in the URL parameters.

        Returns
        -------
        `aiobungie.builders.OAuth2Response`
            An OAuth2 deserialized response.

        Raises
        ------
        `aiobungie.error.Unauthorized`
            The passed code was invalid.
        """

    @abc.abstractmethod
    async def refresh_access_token(
        self, refresh_token: str, /
    ) -> builders.OAuth2Response:
        """Refresh OAuth2 access token given its refresh token.

        Parameters
        ----------
        refresh_token : `str`
            The refresh token.

        Returns
        -------
        `aiobungie.builders.OAuth2Response`
            An OAuth2 deserialized response.
        """

    @abc.abstractmethod
    async def fetch_user_credentials(
        self, access_token: str, membership_id: int, /
    ) -> typedefs.JSONArray:
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
        `aiobungie.typedefs.JSONArray`
            A JSON array of the returned credentials.

        Raises
        ------
        `aiobungie.Unauthorized`
            The access token was wrong or no access token passed.
        """

    @abc.abstractmethod
    async def insert_socket_plug(
        self,
        action_token: str,
        /,
        instance_id: int,
        plug: builders.PlugSocketBuilder | collections.Mapping[str, int],
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> typedefs.JSONObject:
        """Insert a plug into a socketed item.

        .. note::
            OAuth2: AdvancedWriteActions scope is required

        Parameters
        ----------
        action_token : `str`
            Action token provided by the AwaGetActionToken API call.
        instance_id : `int`
            The item instance id that's plug inserted.
        plug : `aiobungie.builders.PlugSocketBuilder | Mapping[str, int]`
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
        membership_type : `aiobungie.aiobungie.MembershipType | int`
            The membership type.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object contains the changed item details.

        Raises
        ------
        `aiobungie.Unauthorized`
            The access token was wrong or no access token passed.
        """

    @abc.abstractmethod
    async def insert_socket_plug_free(
        self,
        access_token: str,
        /,
        instance_id: int,
        plug: builders.PlugSocketBuilder | collections.Mapping[str, int],
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> typedefs.JSONObject:
        """Insert a plug into a socketed item. This doesn't require an Action token.

        .. note::
            OAuth2: MoveEquipDestinyItems scope is required

        Parameters
        ----------
        instance_id : `int`
            The item instance id that's plug inserted.
        plug : `aiobungie.builders.PlugSocketBuilder | Mapping[str, int]`
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
        membership_type : `aiobungie.aiobungie.MembershipType | int`
            The membership type.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object contains the changed item details.

        Raises
        ------
        `aiobungie.Unauthorized`
            The access token was wrong or no access token passed.
        """

    @abc.abstractmethod
    @helpers.unstable
    async def set_item_lock_state(
        self,
        access_token: str,
        state: bool,
        /,
        item_id: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> int:
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
        membership_type : `aiobungie.aiobungie.MembershipType | int`
            The membership type for the associated account.

        Returns
        -------
        `int`
            An integer represents whether the request was successful or failed.

        Raises
        ------
        `aiobungie.Unauthorized`
            - The access token was wrong
            - No access token passed.
            - Other authorization causes.
        """

    @abc.abstractmethod
    async def set_quest_track_state(
        self,
        access_token: str,
        state: bool,
        /,
        item_id: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> int:
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
        membership_type : `aiobungie.aiobungie.MembershipType | int`
            The membership type for the associated account.

        Returns
        -------
        `int`
            An integer represents whether the request was successful or failed.

        Raises
        ------
        `aiobungie.Unauthorized`
            - The access token was wrong
            - No access token passed.
            - Other authorization causes.
        """

    @abc.abstractmethod
    @helpers.unstable
    async def search_entities(
        self, name: str, entity_type: str, *, page: int = 0
    ) -> typedefs.JSONObject:
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
        `aiobungie.typedefs.JSONObject`
            A JSON object contains details about the searched term.
        """

    @abc.abstractmethod
    async def fetch_unique_weapon_history(
        self,
        membership_id: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> typedefs.JSONObject:
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
        `aiobungie.typedefs.JSONObject`
            A JSON object contains details about the returned weapons.
        """

    @abc.abstractmethod
    async def fetch_available_locales(self) -> typedefs.JSONObject:
        """Fetch available locales at Bungie.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object contains a list of all available localization cultures.
        """

    @abc.abstractmethod
    async def fetch_common_settings(self) -> typedefs.JSONObject:
        """Fetch the common settings used by Bungie's environment.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            The common settings JSON object.
        """

    @abc.abstractmethod
    async def fetch_user_systems_overrides(self) -> typedefs.JSONObject:
        """Fetch a user's specific system overrides.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            The system overrides JSON object.
        """

    @abc.abstractmethod
    async def fetch_global_alerts(
        self, *, include_streaming: bool = False
    ) -> typedefs.JSONArray:
        """Fetch any active global alerts.

        Parameters
        ----------
        include_streaming : `bool`
            If True, the returned results will include streaming alerts. Default is False.

        Returns
        -------
        `aiobungie.typedefs.JSONArray`
            A JSON array of the global alerts objects.
        """

    @abc.abstractmethod
    async def fetch_item(
        self,
        member_id: int,
        item_id: int,
        membership_type: enums.MembershipType | int,
        components: collections.Sequence[enums.ComponentType],
    ) -> typedefs.JSONObject:
        """Fetch an instanced Destiny 2 item's details.

        Parameters
        ----------
        member_id : `int`
            The membership id of the Destiny 2 player.
        item_id : `int`
            The instance id of the item.
        membership_type : `aiobungie.aiobungie.MembershipType | int`
            The membership type of the Destiny 2 player.
        components : `collections.Sequence[aiobungie.ComponentType]`
            A list of components to retrieve.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object response contains the fetched item with its components.
        """

    @abc.abstractmethod
    async def fetch_clan_weekly_rewards(self, clan_id: int, /) -> typedefs.JSONObject:
        """Fetch the weekly reward state for a clan.

        Parameters
        ----------
        clan_id : `int`
            The clan id.

        Returns
        ------
        `aiobungie.typedefs.JSONObject`
            A JSON response of the clan rewards state.
        """

    @abc.abstractmethod
    async def awainitialize_request(
        self,
        access_token: str,
        type: typing.Literal[0, 1],
        membership_type: enums.MembershipType | int,
        /,
        *,
        affected_item_id: int | None = None,
        character_id: int | None = None,
    ) -> typedefs.JSONObject:
        """Initialize a request to perform an advanced write action.

        .. warning::
            OAuth2: AdvancedWriteActions application scope is required to perform this request.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        type : `typing.Literal[0, 1]`
            Type of the advanced write action. Its either 0 or 1.
            If set to 0 that means it `None`. Otherwise if 1 that means its insert plugs.
        membership_type : `aiobungie.aiobungie.MembershipType | int`
            The Destiny membership type of the account to modify.

        Other Parameters
        ----------------
        affected_item_id : `int | None`
            Item instance ID the action shall be applied to.
            This is optional for all but a new AwaType values.
        character_id : `int | None`
            The Destiny character ID to perform this action on.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object response.
        """

    @abc.abstractmethod
    async def awaget_action_token(
        self, access_token: str, correlation_id: str, /
    ) -> typedefs.JSONObject:
        """Returns the action token if user approves the request.

        .. warning::
            OAuth2: AdvancedWriteActions application scope is required to perform this request.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        correlation_id : `str`
            The identifier for the advanced write action request.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object response.
        """

    @abc.abstractmethod
    async def awa_provide_authorization_result(
        self,
        access_token: str,
        selection: int,
        correlation_id: str,
        nonce: collections.MutableSequence[str | bytes],
    ) -> int:
        """Provide the result of the user interaction. Called by the Bungie Destiny App to approve or reject a request.

        .. warning::
            OAuth2: AdvancedWriteActions application scope is required to perform this request.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        selection : `int`
            Indication of the selection the user has made (Approving or rejecting the action)
        correlation_id : `str`
            Correlation ID of the request.
        nonce : `collections.MutableSequence[str | bytes]`
            Secret nonce received via the PUSH notification.

        Returns
        -------
        `int`
            ...
        """

    @abc.abstractmethod
    async def fetch_vendors(
        self,
        access_token: str,
        character_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
        /,
        components: collections.Sequence[enums.ComponentType],
        filter: int | None = None,
    ) -> typedefs.JSONObject:
        """Get currently available vendors from the list of vendors that can possibly have rotating inventory.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        character_id : `int`
            The character ID to return the vendor info for.
        membership_id : `int`
            The Destiny membership id to return the vendor info for.
        membership_type : `aiobungie.aiobungie.MembershipType | int`
            The Destiny membership type to return the vendor info for.
        components: `collections.Sequence[aiobungie.ComponentType]`
            A list of vendor components to collect and return.

        Other Parameters
        ----------------
        filter : `int`
           Filters the type of items returned from the vendor. This can be left to `None`.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the vendor response.
        """

    @abc.abstractmethod
    async def fetch_vendor(
        self,
        access_token: str,
        character_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
        vendor_hash: int,
        /,
        components: collections.Sequence[enums.ComponentType],
    ) -> typedefs.JSONObject:
        """Fetch details for a specific vendor.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        character_id : `int`
            The character ID to return the vendor info for.
        membership_id : `int`
            The Destiny membership id to return the vendor info for.
        membership_type : `aiobungie.aiobungie.MembershipType | int`
            The Destiny membership type to return the vendor info for.
        vendor_hash : `int`
            The vendor hash to return the details for.
        components: `collections.Sequence[aiobungie.ComponentType]`
            A list of vendor components to collect and return.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the vendor response.
        """

    @abc.abstractmethod
    async def fetch_bungie_applications(self) -> typedefs.JSONArray:
        """Fetch details for applications created by Bungie.

        Returns
        -------
        `aiobungie.typedefs.JSONArray`
            An array of Bungie created applications.
        """

    @abc.abstractmethod
    async def fetch_application_api_usage(
        self,
        access_token: str,
        application_id: int,
        /,
        *,
        start: datetime.datetime | None = None,
        end: datetime.datetime | None = None,
    ) -> typedefs.JSONObject:
        """Fetch a Bungie application's API usage.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        application_id : `int`
            The application id to get.

        Other Parameters
        ----------------
        start : `datetime.datetime | None`
            A datetime object can be used to collect the start of the application usage.
            This is limited and can go back to 30 days maximum.

            If this is left to `None`. It will return the last 24 hours.
        end : `datetime.datetime | None`
            A datetime object can be used to collect the end of the application usage.

            If this is left to `None`. It will return `now`.

        Example
        -------
        ```py
        import datetime

        # Fetch data from 2021 Dec 10th to 2021 Dec 20th
        await fetch_application_api_usage(
            start=datetime.datetime(2021, 12, 10),
            end=datetime.datetime(2021, 12, 20)
        )
        ```

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the application usage details.
        """

    @abc.abstractmethod
    async def fetch_historical_stats(
        self,
        character_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
        day_start: datetime.datetime,
        day_end: datetime.datetime,
        groups: collections.Sequence[enums.StatsGroupType | int],
        modes: collections.Sequence[enums.GameMode | int],
        *,
        period_type: enums.PeriodType = enums.PeriodType.ALL_TIME,
    ) -> typedefs.JSONObject:
        """Fetch historical stats for a specific membership character.

        Parameters
        ----------
        character_id : `int`
            The character ID to return the stats for.
        membership_id : `int`
            The Destiny membership id to return the stats for.
        membership_type : `aiobungie.MembershipType | int`
            The Destiny membership type to return the stats for.
        day_start : `datetime.datetime`
            The start of the day to return the stats for.
        day_end : `datetime.datetime`
            The end of the day to return the stats for.
        groups : `collections.Sequence[aiobungie.StatsGroupType]`
            A list of stats groups to return.
        modes : `collections.Sequence[aiobungie.GameMode | int]`
            A list of game modes to return.
        period_type : `aiobungie.enums.PeriodType`
            The period type to return the stats for.
            This will return `ALL_TIME` by default if not modified.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the historical stats.
        """

    @abc.abstractmethod
    async def fetch_historical_stats_for_account(
        self,
        membership_id: int,
        membership_type: enums.MembershipType | int,
        groups: collections.Sequence[enums.StatsGroupType | int],
    ) -> typedefs.JSONObject:
        """Fetch historical stats for an account's membership.

        Parameters
        ----------
        membership_id : `int`
            The Destiny membership id to return the stats for.
        membership_type : `aiobungie.MembershipType | int`
            The Destiny membership type to return the stats for.
        groups : `collections.Sequence[aiobungie.StatsGroupType]`
            A list of stats groups to return.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the historical stats for the account. This includes both the
            character and account stats.
        """

    @abc.abstractmethod
    async def fetch_aggregated_activity_stats(
        self,
        character_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
        /,
    ) -> typedefs.JSONObject:
        """Fetch aggregated activity stats for a specific membership character.

        Parameters
        ----------
        character_id : `int`
            The character ID to return the stats for.
        membership_id : `int`
            The Destiny membership id to return the stats for.
        membership_type : `aiobungie.MembershipType | int`
            The Destiny membership type to return the stats for.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the aggregated activity stats.
        """

    @abc.abstractmethod
    async def fetch_historical_definition(self) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def fetch_content_type(self, type: str, /) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def fetch_content_by_id(
        self, id: int, locale: str, /, *, head: bool = False
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def fetch_content_by_tag_and_type(
        self, locale: str, tag: str, type: str, *, head: bool = False
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def search_content_with_text(
        self,
        locale: str,
        /,
        content_type: str,
        search_text: str,
        tag: str,
        *,
        page: int | None = None,
        source: str | None = None,
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def search_content_by_tag_and_type(
        self,
        locale: str,
        tag: str,
        type: str,
        *,
        page: int | None = None,
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def search_help_articles(
        self, text: str, size: str, /
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def fetch_topics_page(
        self,
        category_filter: int,
        group: int,
        date_filter: int,
        sort: str | bytes,
        *,
        page: int | None = None,
        locales: collections.Iterable[str] | None = None,
        tag_filter: str | None = None,
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def fetch_core_topics_page(
        self,
        category_filter: int,
        date_filter: int,
        sort: str | bytes,
        *,
        page: int | None = None,
        locales: collections.Iterable[str] | None = None,
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def fetch_posts_threaded_page(
        self,
        parent_post: bool,
        page: int,
        page_size: int,
        parent_post_id: int,
        reply_size: int,
        root_thread_mode: bool,
        sort_mode: int,
        show_banned: str | None = None,
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def fetch_posts_threaded_page_from_child(
        self,
        child_id: bool,
        page: int,
        page_size: int,
        reply_size: int,
        root_thread_mode: bool,
        sort_mode: int,
        show_banned: str | None = None,
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def fetch_post_and_parent(
        self, child_id: int, /, *, show_banned: str | None = None
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def fetch_posts_and_parent_awaiting(
        self, child_id: int, /, *, show_banned: str | None = None
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def fetch_topic_for_content(self, content_id: int, /) -> int: ...

    @abc.abstractmethod
    async def fetch_forum_tag_suggestions(
        self, partial_tag: str, /
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def fetch_poll(self, topic_id: int, /) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def fetch_recruitment_thread_summaries(self) -> typedefs.JSONArray: ...

    @abc.abstractmethod
    async def fetch_recommended_groups(
        self,
        access_token: str,
        /,
        *,
        date_range: int = 0,
        group_type: enums.GroupType | int = enums.GroupType.CLAN,
    ) -> typedefs.JSONArray: ...

    @abc.abstractmethod
    async def fetch_available_avatars(self) -> collections.Mapping[str, int]: ...

    @abc.abstractmethod
    async def fetch_user_clan_invite_setting(
        self,
        access_token: str,
        /,
        membership_type: enums.MembershipType | int,
    ) -> bool: ...

    @abc.abstractmethod
    async def fetch_banned_group_members(
        self,
        access_token: str,
        group_id: int,
        /,
        *,
        page: int = 1,
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def fetch_pending_group_memberships(
        self, access_token: str, group_id: int, /, *, current_page: int = 1
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def fetch_invited_group_memberships(
        self, access_token: str, group_id: int, /, *, current_page: int = 1
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def invite_member_to_group(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
        *,
        message: str | None = None,
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def cancel_group_member_invite(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
    ) -> typedefs.JSONObject: ...

    @abc.abstractmethod
    async def equip_loadout(
        self,
        access_token: str,
        /,
        loadout_index: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> None:
        """Equip a loadout. Your character must be in a Social space, Orbit or Offline
        while performing this operation.

        .. note::
            This operation requires `MoveEquipDestinyItems` OAuth2 scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        loadout_index : `int`
            The index of the loadout to use.
        character_id : `int`
            The character ID to equip the loadout to.
        membership_type : `aiobungie.MembershipType | int`
            The membership type of the account.
        """

    @abc.abstractmethod
    async def snapshot_loadout(
        self,
        access_token: str,
        /,
        loadout_index: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
        *,
        color_hash: int | None = None,
        icon_hash: int | None = None,
        name_hash: int | None = None,
    ) -> None:
        """Snapshot a loadout with the currently equipped items.

        .. note::
            This operation requires `MoveEquipDestinyItems` OAuth2 scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        loadout_index : `int`
            The index of the loadout to use.
        character_id : `int`
            The character ID to equip the loadout to.
        membership_type : `aiobungie.MembershipType | int`
            The membership type of the account.

        Other Parameters
        ----------------
        color_hash : `int | None`
            ...
        icon_hash: `int | None`
            ...
        name_hash: `int | None`
            ...
        """

    @abc.abstractmethod
    async def update_loadout(
        self,
        access_token: str,
        /,
        loadout_index: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
        *,
        color_hash: int | None = None,
        icon_hash: int | None = None,
        name_hash: int | None = None,
    ) -> None:
        """Update the loadout. Color, Icon and Name.

        .. note::
            This operation requires `MoveEquipDestinyItems` OAuth2 scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        loadout_index : `int`
            The index of the loadout to use.
        character_id : `int`
            The character ID to equip the loadout to.
        membership_type : `aiobungie.MembershipType | int`
            The membership type of the account.

        Other Parameters
        ----------------
        color_hash : `int | None`
            The new color hash of the loadout to update.
        icon_hash: `int | None`
            The new icon hash of the loadout to update.
        name_hash: `int | None`
            The new name hash of the loadout to update.
        """

    @abc.abstractmethod
    async def clear_loadout(
        self,
        access_token: str,
        /,
        loadout_index: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> None:
        """Clear the identifiers and items of a loadout.

        .. note::
            This operation requires `MoveEquipDestinyItems` OAuth2 scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        loadout_index : `int`
            The index of the loadout to use.
        character_id : `int`
            The character ID to equip the loadout to.
        membership_type : `aiobungie.MembershipType | int`
            The membership type of the account.
        """

    @abc.abstractmethod
    async def force_drops_repair(self, access_token: str, /) -> bool:
        """Twitch Drops self-repair function - scans twitch for drops not marked as fulfilled and resyncs them.

        .. note::
            This operation requires `PartnerOfferGrant` OAuth2 scope.

        Parameters
        ----------
        access_token: `str`
            The bearer access token associated with the bungie account that
            will be used to make the request with.

        Returns
        -------
        `bool`
            The nature of this response is a `boolean`.
        """

    @abc.abstractmethod
    async def claim_partner_offer(
        self,
        access_token: str,
        /,
        *,
        offer_id: str,
        bungie_membership_id: int,
        transaction_id: str,
    ) -> bool:
        """Claim a partner offer as the authenticated user.

        .. note::
            This operation requires `PartnerOfferGrant` OAuth2 scope.

        Parameters
        ----------
        access_token: `str`
            The bearer access token associated with the bungie account that
            will be used to make the request with.
        offer_id: `str`
            The partner offer ID
        bungie_membership_id: `int`
            The associated Bungie.net membership ID
        transaction_id: `str`
            The transaction ID

        Returns
        -------
        `bool`
            The nature of this response is a `boolean`.
        """

    @abc.abstractmethod
    async def fetch_bungie_rewards_for_user(
        self, access_token: str, /, membership_id: int
    ) -> typedefs.JSONObject:
        """Returns the bungie rewards for the targeted user.

        .. note::
            This operation requires `ReadAndApplyTokens` OAuth2 scope.

        Parameters
        ----------
        access_token: `str`
            The bearer access token associated with the bungie account that
            will be used to make the request with.
        membership_id: `int`
            The associated membership ID to fetch the rewards for.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object contains a display of the rewards. [See](https://bungie-net.github.io/multi/schema_Tokens-BungieRewardDisplay.html#schema_Tokens-BungieRewardDisplay)
        """

    @abc.abstractmethod
    async def fetch_bungie_rewards_for_platform(
        self,
        access_token: str,
        /,
        membership_id: int,
        membership_type: enums.MembershipType | int,
    ) -> typedefs.JSONObject:
        """Returns the bungie rewards for the targeted user and membership.

        .. note::
            This operation requires `ReadAndApplyTokens` OAuth2 scope.

        Parameters
        ----------
        access_token: `str`
            The bearer access token associated with the bungie account that
            will be used to make the request with.
        membership_id: `int`
            The associated membership ID to fetch the rewards for.
        membership_type: `aiobungie.MembershipType | int`
            The associated membership type for the user.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object contains a display of the rewards. [See](https://bungie-net.github.io/multi/schema_Tokens-BungieRewardDisplay.html#schema_Tokens-BungieRewardDisplay)
        """

    @abc.abstractmethod
    async def fetch_bungie_rewards(self) -> typedefs.JSONObject:
        """Returns a list of the current bungie rewards.

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object contains a display of the rewards. [See](https://bungie-net.github.io/multi/schema_Tokens-BungieRewardDisplay.html#schema_Tokens-BungieRewardDisplay)
        """

    @abc.abstractmethod
    async def fetch_fireteam_listing(self, listing_id: int) -> typedefs.JSONObject: ...
