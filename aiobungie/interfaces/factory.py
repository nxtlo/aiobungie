# MIT License
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

"""An API interface for the factory marshaller."""

from __future__ import annotations

__all__: tuple[str, ...] = ("FactoryInterface",)

import abc
import typing

if typing.TYPE_CHECKING:
    from aiobungie.crate import activity
    from aiobungie.crate import application
    from aiobungie.crate import character
    from aiobungie.crate import clans
    from aiobungie.crate import entity
    from aiobungie.crate import fireteams
    from aiobungie.crate import friends
    from aiobungie.crate import milestones
    from aiobungie.crate import profile
    from aiobungie.crate import user
    from aiobungie.internal import enums
    from aiobungie.internal import helpers
    from aiobungie.internal import traits


class FactoryInterface(abc.ABC):
    """An API interface that documents and describes the implementation of the marshaller factory."""

    __slots__ = ()

    if typing.TYPE_CHECKING:
        _net: traits.Netrunner

    # Users, Memberships.

    def deserialize_user(self, data: helpers.JsonObject) -> user.User:
        """Deserialize a raw JSON hard linked Bungie.net user payload into a user object.

        This implements both HardLinkedCredential and the Destiny memberships.

        Parameters
        ----------
        data : `aiobungie.internal.helpers.JsonObject`
            The JSON data/payload.

        Returns
        -------
        `aiobungie.crate.User`
            A user object of the deserialized payload.
        """

    def deserialize_bungie_user(self, data: helpers.JsonObject) -> user.BungieUser:
        """Deserialize a raw JSON Bungie.net user only payload into a user object.

        .. note::
            This only returns the Bungie.net user and not the Destiny memberships.

        Parameters
        ----------
        data : `aiobungie.internal.helpers.JsonObject`
            The JSON data/payload.

        Returns
        -------
        `aiobungie.crate.BungieUser`
            A Bungie user object of the deserialized payload.
        """

    def deseialize_found_users(
        self, payload: helpers.JsonObject
    ) -> typing.Sequence[user.DestinyUser]:
        """Deserialize a raw JSON of prefix searched users.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.DestinyUser`
            A Destiny user object of the deserialized payload.
        """

    def deserialize_partial_bungie_user(
        self, payload: helpers.JsonObject, *, noeq: bool = False
    ) -> user.PartialBungieUser:
        """Deserialize a raw JSON of a partial `bungieNetUserInfo`.

        A partial user is a bungie.net user payload with missing information from
        the main `BungieUser` object.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.
        noeq : `bool`
            If set to True, Then the payload will be returned without the `bungieNetUserInfo` key.
            If set to False, The the payload will return the `bungieNetUserInfo` key.

            This is useful for binding the same method with other payloads that returns
            the same object but with different payload key name. This defaults to `False`

        Returns
        -------
        `aiobungie.crate.PartialBungieUser`
            A partial bungie user object of the deserialized payload.
        """

    def deserialize_destiny_user(
        self, payload: helpers.JsonObject, *, noeq: bool = False
    ) -> user.DestinyUser:
        """Deserialize a raw JSON of `destinyUserInfo`.

        A destiny user is just destiny memberships, i.e., Xbox membershio, Steam membership. etc.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Other Parameters
        ---------------
        noeq : `bool`
            If set to True, Then the payload will be returned without the `destinyUserInfo` key.
            If set to False, The the payload will return the `destinyUserInfo` key.

            This is useful for binding the same method with other payloads that returns
            the same object but with different payload key name. This defaults to `False`

        Returns
        -------
        `aiobungie.crate.user.DestinyUser`
            A destiny membership/user object of the deserialized payload.
        """

    # Deserialize a list of `destinyUserInfo`
    def deserialize_destiny_members(
        self,
        data: typing.Union[helpers.JsonObject, helpers.JsonArray],
        *,
        bound: bool = False,
    ) -> typing.Sequence[user.DestinyUser]:
        """Deserialize a raw JSON payload/array of `destinyUserInfo`.

        Parameters
        ----------
        payload : `typing.Union[aiobungie.internal.helpers.JsonObject, aiobungie.internal.helpers.JsonArray]`
            The JSON payload array or object.

        Other Parameters
        ----------------
        bound : `bool`
            If set to True, Then the payload will be returned without the `destinyUserInfo` key.
            If set to False, The the payload will return the `destinyUserInfo` key.

            This is useful for binding the same method with other payloads that returns
            the same object but with different payload key name. This defaults to `False`

        Returns
        -------
        `typing.Sequence[aiobungie.crate.user.DestinyUser]`
            A sequence of destiny membership/user object of the deserialized payload.
        """

    def deserialize_user_themes(
        self, payload: helpers.JsonArray
    ) -> typing.Sequence[user.UserThemes]:
        """Deserialize a raw JSON array of Bungie user themes.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonArray`
            The JSON payload.

        Returns
        -------
        `typing.Sequence[aiobungie.crate.user.UserThemes]`
            A sequence of bungie user themes object of the deserialized payload.
        """

    def deserialize_player(
        self, payload: helpers.JsonArray, /
    ) -> typing.Sequence[user.DestinyUser]:
        """Deserialize a raw JSON sequence of players.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonArray`
            The JSON payload.

        Returns
        -------
        `typing.Sequence[aiobungie.crate.user.DestinyUser]`
            A sequence of players object of the deserialized payload.

            .. note::
                This typically returns just 1 element
                but keeping it a sequence to match the JSON array signature.
        """

    # Clans, Groups.

    def deseialize_clan_owner(self, data: helpers.JsonObject) -> clans.ClanMember:
        """Deserialize a raw JSON payload of clan founder information.

        Parameters
        ----------
        data : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.ClanMember`
            A clan owner object of the deserialized payload.
        """

    def deserialize_clan(
        self, payload: helpers.JsonObject, *, bound: bool = False
    ) -> clans.Clan:
        # To bind this function between this and group for member.

        """Deserialize a raw JSON payload of Bungie clan information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Other Parameters
        ----------------
        bound : `bool`
            If set to True, Then the payload will be returned without the `detail` key.
            If set to False, The the payload will return the `detail` key.

            This is used to bind this method with `fetch_group_member` currently,
            and can be used with other methods that returns the same data.

        Returns
        -------
        `aiobungie.crate.Clan`
            A clan owner object of the deserialized payload.
        """

    def deserialize_group_member(
        self, payload: helpers.JsonObject
    ) -> helpers.NoneOr[clans.GroupMember]:
        """Deserialize a JSON payload of group information for a member.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.internal.helpers.NoneOr[aiobungie.crate.GroupMember]`
            A group member object of the deserialized payload. This can return `None` if nothing was found.
        """

    def deserialize_clan_admins(
        self, payload: helpers.JsonObject
    ) -> typing.Sequence[clans.ClanAdmin]:
        """Deserialize a JSON payload of clan admins/owners information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `typing.Sequence[aiobungie.crate.ClanAdmin]`
            A sequence of clan admins object of the deserialized payload.
        """

    def deserialize_clan_member(self, data: helpers.JsonObject, /) -> clans.ClanMember:
        """Deserialize a JSON payload of a clan member information.

        Parameters
        ----------
        data : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.ClanMember`
            A clan member object of the deserialized payload.
        """

    def deserialize_clan_members(
        self, data: helpers.JsonObject, /
    ) -> typing.Sequence[clans.ClanMember]:
        """Deserialize a JSON payload of a clan members information.

        Parameters
        ----------
        data : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `typing.Sequence[aiobungie.crate.ClanMember]`
            A sequence of clan members of the deserialized payload.
        """

    def deserialize_clan_convos(
        self, payload: helpers.JsonArray
    ) -> typing.Sequence[clans.ClanConversation]:
        """Deserialize a JSON array of a clan conversations information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonArray`
            The JSON payload.

        Returns
        -------
        `typing.Sequence[aiobungie.crate.ClanConversation]`
            A sequence of clan conversations of the deserialized payload.
        """

    def deserialize_clan_banners(
        self, payload: helpers.JsonObject
    ) -> typing.Sequence[clans.ClanBanner]:
        """Deserialize a JSON array of a clan banners information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `typing.Sequence[aiobungie.crate.ClanBanner]`
            A sequence of clan banners of the deserialized payload.
        """

    # Application

    def deserialize_app_owner(
        self, payload: helpers.JsonObject
    ) -> application.ApplicationOwner:
        """Deserialize a JSON payload of Bungie Developer portal application owner information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.application.ApplicationOwner`
            An application owner object of the deserialized payload.
        """

    def deserialize_app(self, payload: helpers.JsonObject) -> application.Application:
        """Deserialize a JSON payload of Bungie Developer portal application information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.application.Application`
            An application object of the deserialized payload.
        """

    # Characters.

    def deserialize_character(
        self, payload: helpers.JsonObject, *, chartype: enums.Class
    ) -> character.Character:
        """Deserialize a JSON payload of Destiny 2 character information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        TODO: make this not position arg?

        Other Parameters
        ----------------
        chartype : `aiobungie.Class`
            The character to deserialize and return.
            This parameter is not optional and must be passed to the client.

        Returns
        -------
        `aiobungie.crate.character`
            A character object of the deserialized payload.
        """

    # Profiles.

    def deserialize_profile(self, payload: helpers.JsonObject, /) -> profile.Profile:
        """Deserialize a JSON payload of Bungie.net profile information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.Profile`
            A profile object of the deserialized payload.
        """

    def deserialize_linked_profiles(
        self, payload: helpers.JsonObject
    ) -> profile.LinkedProfile:
        """Deserialize a JSON payload of Bungie.net hard linked profile information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.LinkedProfile`
            A hard linked profile object of the deserialized payload.
        """

    # Inventory entities and Definitions.

    def deserialize_inventory_entity(
        self, payload: helpers.JsonObject, /
    ) -> entity.InventoryEntity:
        """Deserialize a JSON payload of an inventory entity item information.

        This can be any item from `DestinyInventoryItemDefinition` definition.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.InventoryEntiry`
            A hard linked profile object of the deserialized payload.
        """

    # Activities.

    def deserialize_activity(self, payload: helpers.JsonObject, /) -> activity.Activity:
        """Deserialize a JSON payload of an occurred activity information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.Activity`
            An activity object of the deserialized payload.
        """

    # Milestones.

    def deserialize_public_milestone_content(
        self, payload: helpers.JsonObject
    ) -> milestones.Milestone:
        """Deserialize a JSON payload of milestone content information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.Milestone`
            A milestone object of the deserialized payload.
        """

    # Social and friends.

    def deserialize_friend(self, payload: helpers.JsonObject, /) -> friends.Friend:
        """Deserialize a JSON payload of a Bungie friend information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.Friend`
            A friend object of the deserialized payload.
        """

    def deserialize_friends(
        self, payload: helpers.JsonObject
    ) -> typing.Sequence[friends.Friend]:
        """Deserialize a JSON sequence of Bungie friends information.

        This is usually used to deserialize the incoming/outgoing friend requests.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `typing.Sequence[aiobungie.crate.Friend]`
            A sequence of friends object of the deserialized payload.
        """

    def deserialize_friend_requests(
        self, payload: helpers.JsonObject
    ) -> friends.FriendRequestView:
        """Deserialize a JSON sequence of Bungie friend requests information.

        This is used for incoming/outgoing friend requests.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `typing.Sequence[aiobungie.crate.FriendRequestView]`
            A sequence of incoming and outgoing friends object of the deserialized payload.
        """

    # Fireteams.

    def deserialize_fireteams(
        self, payload: helpers.JsonObject
    ) -> helpers.NoneOr[typing.Sequence[fireteams.Fireteam]]:
        """Deserialize a JSON sequence of Bungie fireteams information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `typing.Sequence[aiobungie.crate.Fireteam]`
            A sequence of fireteam object of the deserialized payload.
        """

    def deserialize_fireteam_destiny_users(
        self, payload: helpers.JsonObject
    ) -> fireteams.FireteamUser:
        """Deserialize a JSON payload of Bungie fireteam destiny users information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.FireteamUser`
            A fireteam user object of the deserialized payload.
        """

    def deserialize_fireteam_members(
        self, payload: helpers.JsonObject, *, alternatives: bool = False
    ) -> typing.Optional[typing.Sequence[fireteams.FireteamMember]]:
        """Deserialize a JSON sequence of Bungie fireteam members information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.
        alternatives : `bool`
            If set to `True`, Then it will deserialize the `alternatives` data in the payload.
            If not the it will just deserialize the `members` data.

        Returns
        -------
        `typing.Optional[typing.Sequence[aiobungie.crate.FireteamUser]]`
            An optional sequence of the fireteam members object of the deserialized payload.
        """

    def deserialize_available_fireteams(
        self, data: helpers.JsonObject, *, no_results: bool = False
    ) -> typing.Union[
        fireteams.AvalaibleFireteam, typing.Sequence[fireteams.AvalaibleFireteam]
    ]:
        """Deserialize a JSON payload of a sequence of/fireteam information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.
        no_results : `bool`
            Whether to deserialize the data from `results` in the payload or not.

        Returns
        -------
        `typing.Union[aiobungie.crate.fireteams.AvalaibleFireteam, typing.Sequence[aiobungie.crate.fireteams.AvalaibleFireteam]]` # noqa: E501
            An available fireteam or a sequence of available fireteam object of the deserialized payload.
        """
