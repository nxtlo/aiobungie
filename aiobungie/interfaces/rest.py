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

__all__: list[str] = ["RESTInterface"]

import abc
import typing

from aiobungie.internal import enums
from aiobungie.internal import helpers

ResponseSigT = typing.TypeVar("ResponseSigT")
"""The type of the response signature."""

ResponseSig = typing.Coroutine[typing.Any, typing.Any, ResponseSigT]
"""A type hint for a general coro method that returns a type
that's mostly going to be on of `aiobungie.internal.helpers.JsonObject` or `aiobungie.internal.helpers.JsonArray`
"""


class RESTInterface(abc.ABC):
    """An interface for a rest only client implementation."""

    __slots__: typing.Sequence[str] = ()

    @abc.abstractmethod
    def static_search(self, path: str, **kwargs: typing.Any) -> ResponseSig[typing.Any]:
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
    def search_users(self, name: str, /) -> ResponseSig[helpers.JsonArray]:
        """Search for users by their global name and return all users who share this name.

        Parameters
        ----------
        name : `str`
            The user name.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonArray]`
            A JSON array of the found users.

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
        type: enums.CredentialType = enums.CredentialType.STEAMID,
        /,
    ) -> ResponseSig[helpers.JsonObject]:
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
        `ResponseSig[aiobungie.internal.helpers.JsonObject]`
            A JSON object of the found user hard linked types.
        """

    @abc.abstractmethod
    def fetch_membership_from_id(
        self, id: int, type: enums.MembershipType = enums.MembershipType.NONE, /
    ) -> ResponseSig[helpers.JsonObject]:
        """Fetch Bungie user's memberships from their id.

        Parameters
        ----------
        id : `builtins.int`
            The user's id.
        type : `aiobungie.MembershipType`
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
        type: enums.MembershipType,
        /,
    ) -> ResponseSig[helpers.JsonObject]:
        """
        Fetche a bungie profile.

        Parameters
        ----------
        memberid: `builtins.int`
            The member's id.
        type: `aiobungie.MembershipType`
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
        self, name: str, type: enums.MembershipType = enums.MembershipType.ALL, /
    ) -> ResponseSig[helpers.JsonArray]:
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
        self, memberid: int, type: enums.MembershipType, /
    ) -> ResponseSig[helpers.JsonObject]:
        """Fetch a Destiny 2 player's characters.

        Parameters
        ----------
        memberid: `builtins.int`
            A valid bungie member id.
        type: `aiobungie.internal.enums.MembershipType`
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
        mode: enums.GameMode,
        membership_type: enums.MembershipType,
        *,
        page: typing.Optional[int] = 1,
        limit: typing.Optional[int] = 1,
    ) -> ResponseSig[helpers.JsonObject]:
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
        self, name: str, /, type: enums.GroupType = enums.GroupType.CLAN
    ) -> ResponseSig[helpers.JsonObject]:
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
    def fetch_clan_members(
        self,
        clan_id: int,
        type: enums.MembershipType = enums.MembershipType.NONE,
        name: typing.Optional[str] = None,
        /,
    ) -> ResponseSig[helpers.JsonArray]:
        """Fetch all Bungie Clan members.

        Parameters
        ----------
        clan_id : `builsins.int`
            The clans id
        type : `aiobungie.MembershipType`
            An optional clan member's membership type.
            Default is set to `aiobungie.MembershipType.NONE`
            Which returns the first matched clan member by their name.
        name : `builtins.str`
            This parameter is only provided here to keep the signature with
            the main client implementation, Which only works with the non-rest clients.
            It returns a specific clan member by their name.

        Returns
        -------
        `ResponseSig[aiobungie.internal.helpers.JsonArray]`
            A JSON array of clan members.

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
