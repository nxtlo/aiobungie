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
    import collections.abc as collections

    from aiobungie import traits
    from aiobungie import typedefs
    from aiobungie.crate import activity
    from aiobungie.crate import application
    from aiobungie.crate import character
    from aiobungie.crate import clans
    from aiobungie.crate import components
    from aiobungie.crate import entity
    from aiobungie.crate import fireteams
    from aiobungie.crate import friends
    from aiobungie.crate import milestones
    from aiobungie.crate import profile
    from aiobungie.crate import records
    from aiobungie.crate import season
    from aiobungie.crate import user


class FactoryInterface(abc.ABC):
    """An API interface that documents and describes the implementation of the marshaller factory."""

    __slots__ = ()

    if typing.TYPE_CHECKING:
        _net: traits.Netrunner

    # Users, Memberships.

    @abc.abstractmethod
    def deserialize_user(self, data: typedefs.JSONObject) -> user.User:
        """Deserialize a raw JSON hard linked Bungie.net user payload into a user object.

        This implements both HardLinkedCredential and the Destiny memberships.

        Parameters
        ----------
        data : `aiobungie.typedefs.JSONObject`
            The JSON data/payload.

        Returns
        -------
        `aiobungie.crate.User`
            A user object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_bungie_user(self, data: typedefs.JSONObject) -> user.BungieUser:
        """Deserialize a raw JSON Bungie.net user only payload into a user object.

        .. note::
            This only returns the Bungie.net user and not the Destiny memberships.

        Parameters
        ----------
        data : `aiobungie.typedefs.JSONObject`
            The JSON data/payload.

        Returns
        -------
        `aiobungie.crate.BungieUser`
            A Bungie user object of the deserialized payload.
        """

    @abc.abstractmethod
    def deseialize_found_users(
        self, payload: typedefs.JSONObject
    ) -> collections.Sequence[user.DestinyUser]:
        """Deserialize a raw JSON of prefix searched users.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.DestinyUser`
            A Destiny user object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_partial_bungie_user(
        self, payload: typedefs.JSONObject, *, noeq: bool = False
    ) -> user.PartialBungieUser:
        """Deserialize a raw JSON of a partial `bungieNetUserInfo`.

        A partial user is a bungie.net user payload with missing information from
        the main `BungieUser` object.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
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

    @abc.abstractmethod
    def deserialize_destiny_user(
        self, payload: typedefs.JSONObject, *, noeq: bool = False
    ) -> user.DestinyUser:
        """Deserialize a raw JSON of `destinyUserInfo`.

        A destiny user is just destiny memberships, i.e., Xbox membershio, Steam membership. etc.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
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
    @abc.abstractmethod
    def deserialize_destiny_members(
        self,
        data: typing.Union[typedefs.JSONObject, typedefs.JSONArray],
        *,
        bound: bool = False,
    ) -> collections.Sequence[user.DestinyUser]:
        """Deserialize a raw JSON payload/array of `destinyUserInfo`.

        Parameters
        ----------
        payload : `typing.Union[aiobungie.typedefs.JSONObject, aiobungie.typedefs.JSONArray]`
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
        `collections.Sequence[aiobungie.crate.user.DestinyUser]`
            A sequence of destiny membership/user object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_user_themes(
        self, payload: typedefs.JSONArray
    ) -> collections.Sequence[user.UserThemes]:
        """Deserialize a raw JSON array of Bungie user themes.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONArray`
            The JSON payload.

        Returns
        -------
        `collections.Sequence[aiobungie.crate.user.UserThemes]`
            A sequence of bungie user themes object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_player(
        self, payload: typedefs.JSONArray, /
    ) -> collections.Sequence[user.DestinyUser]:
        """Deserialize a raw JSON sequence of players.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONArray`
            The JSON payload.

        Returns
        -------
        `collections.Sequence[aiobungie.crate.user.DestinyUser]`
            A sequence of players object of the deserialized payload.

            .. note::
                This typically returns just 1 element
                but keeping it a sequence to match the JSON array signature.
        """

    @abc.abstractmethod
    def deserialize_user_credentials(
        self, payload: typedefs.JSONArray
    ) -> collections.Sequence[user.UserCredentials]:
        """Deserialize a JSON array of Bungie user credentials.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONArray`
            The JSON payload.

        Returns
        -------
        `collections.Sequence[aiobungie.crate.UserCredentials]`
            A sequence of user's credentials.
        """

    # Clans, Groups.

    @abc.abstractmethod
    def deseialize_clan_owner(self, data: typedefs.JSONObject) -> clans.ClanMember:
        """Deserialize a raw JSON payload of clan founder information.

        Parameters
        ----------
        data : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.ClanMember`
            A clan owner object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_clan(
        self, payload: typedefs.JSONObject, *, bound: bool = False
    ) -> clans.Clan:
        # To bind this function between this and group for member.

        """Deserialize a raw JSON payload of Bungie clan information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
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

    @abc.abstractmethod
    def deserialize_group_member(
        self, payload: typedefs.JSONObject
    ) -> typedefs.NoneOr[clans.GroupMember]:
        """Deserialize a JSON payload of group information for a member.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.typedefs.NoneOr[aiobungie.crate.GroupMember]`
            A group member object of the deserialized payload. This can return `None` if nothing was found.
        """

    @abc.abstractmethod
    def deserialize_clan_admins(
        self, payload: typedefs.JSONObject
    ) -> collections.Sequence[clans.ClanAdmin]:
        """Deserialize a JSON payload of clan admins/owners information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `collections.Sequence[aiobungie.crate.ClanAdmin]`
            A sequence of clan admins object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_clan_member(self, data: typedefs.JSONObject, /) -> clans.ClanMember:
        """Deserialize a JSON payload of a clan member information.

        Parameters
        ----------
        data : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.ClanMember`
            A clan member object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_clan_members(
        self, data: typedefs.JSONObject, /
    ) -> collections.Sequence[clans.ClanMember]:
        """Deserialize a JSON payload of a clan members information.

        Parameters
        ----------
        data : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `collections.Sequence[aiobungie.crate.ClanMember]`
            A sequence of clan members of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_clan_convos(
        self, payload: typedefs.JSONArray
    ) -> collections.Sequence[clans.ClanConversation]:
        """Deserialize a JSON array of a clan conversations information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONArray`
            The JSON payload.

        Returns
        -------
        `collections.Sequence[aiobungie.crate.ClanConversation]`
            A sequence of clan conversations of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_clan_banners(
        self, payload: typedefs.JSONObject
    ) -> collections.Sequence[clans.ClanBanner]:
        """Deserialize a JSON array of a clan banners information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `collections.Sequence[aiobungie.crate.ClanBanner]`
            A sequence of clan banners of the deserialized payload.
        """

    # Application

    @abc.abstractmethod
    def deserialize_app_owner(
        self, payload: typedefs.JSONObject
    ) -> application.ApplicationOwner:
        """Deserialize a JSON payload of Bungie Developer portal application owner information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.application.ApplicationOwner`
            An application owner object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_app(self, payload: typedefs.JSONObject) -> application.Application:
        """Deserialize a JSON payload of Bungie Developer portal application information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.application.Application`
            An application object of the deserialized payload.
        """

    # Characters.

    @abc.abstractmethod
    def deserialize_character_component(
        self, payload: typedefs.JSONObject
    ) -> components.CharacterComponent:
        """Deserialize a JSON payload of Destiny 2 character component.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.CharacterComponent`
            A character component object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_character_render_data(
        self, payload: typedefs.JSONObject, /
    ) -> character.RenderedData:
        """Deserialize a JSON payload of a profile character render data component.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.RenderedData`
            A character rendered data profile component.
        """

    @abc.abstractmethod
    def deserialize_character_minimal_equipments(
        self, payload: typedefs.JSONObject
    ) -> character.MinimalEquipments:
        """Deserialize a singular JSON peer view of equipment found in character render data profile component.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.character.MinimalEquipments`
            A minimal equipment object.
        """

    @abc.abstractmethod
    def deserialize_character_dye(self, payload: typedefs.JSONObject) -> character.Dye:
        """Deserialize a JSON payload of a character's dye information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.character.Dye`
            Information about a character dye object.
        """

    @abc.abstractmethod
    def deserialize_character_customazition(
        self, payload: typedefs.JSONObject
    ) -> character.CustomizationOptions:
        """Deserialize a JSON payload of a character customization information found in character
        render data profile component.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.character.CustomizationOptions`
            Information about a character customs object.
        """

    @abc.abstractmethod
    def deserialize_characters(
        self, payload: typedefs.JSONObject
    ) -> collections.Mapping[int, character.Character]:
        ...

    @abc.abstractmethod
    def deserialize_character(
        self, payload: typedefs.JSONObject
    ) -> character.Character:
        ...

    @abc.abstractmethod
    def deserialize_character_equipmnets(
        self, payload: typedefs.JSONObject
    ) -> collections.Mapping[int, collections.Sequence[profile.ProfileItemImpl]]:
        ...

    @abc.abstractmethod
    def deserialize_characters_render_data(
        self, payload: typedefs.JSONObject
    ) -> collections.Mapping[int, character.RenderedData]:
        ...

    @abc.abstractmethod
    def deserialize_progressions(
        self, payload: typedefs.JSONObject
    ) -> character.CharacterProgression:
        ...

    @abc.abstractmethod
    def deserialize_character_progressions(
        self, payload: typedefs.JSONObject
    ) -> collections.Mapping[int, character.CharacterProgression]:
        ...

    # Profiles.

    @abc.abstractmethod
    def deserialize_profile_progression(
        self, payload: typedefs.JSONObject
    ) -> profile.ProfileProgression:
        """Deserialize a JSON payload of a profile progression component.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.ProfileProgression`
            A profile progression component object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_profile(
        self, payload: typedefs.JSONObject, /
    ) -> typing.Optional[profile.Profile]:
        """Deserialize a JSON payload of Bungie.net profile information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `typing.Optional[aiobungie.crate.Profile]`
            A profile object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_profile_items(
        self, payload: typedefs.JSONObject, /
    ) -> typing.Optional[collections.Sequence[profile.ProfileItemImpl]]:
        """Deserialize a JSON payload of profile items component information.

        This may deserialize `profileInventories` or `profileCurrencies` or any
        other alternatives.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `typing.Optional[collections.Sequence[aiobungie.crate.ProfileItemImpl]]`
            A profile component object that contains items of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_linked_profiles(
        self, payload: typedefs.JSONObject
    ) -> profile.LinkedProfile:
        """Deserialize a JSON payload of Bungie.net hard linked profile information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.LinkedProfile`
            A hard linked profile object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_profile_item(
        self, payload: typedefs.JSONObject
    ) -> profile.ProfileItemImpl:
        """Deserialize a JSON payload of a singular profile component item.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.ProfileItemImpl`
            A concerete implementation of a profile component item.
        """

    # Components

    @abc.abstractmethod
    def deserialize_components(
        self, payload: typedefs.JSONObject
    ) -> components.Component:
        """Deserialize a JSON payload of Bungie.net profile components information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.Component`
            A component implementation that includes all other components
            of the deserialized payload.
        """

    # Records

    @abc.abstractmethod
    def deserialize_records(
        self,
        payload: typedefs.JSONObject,
        scores: typing.Optional[records.RecordScores] = None,
        **nodes: int,
    ) -> records.Record:
        """Deserialize a JSON object of a profile record component.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON object payload
        scores: `typing.Optional[records.RecordScores]`
            The records scores object.
            This exists only to keep the signature of `aiobungie.crate.CharacterRecord` with the record object.
            As it will always be `None` in that object.
        **nodes: `int`
            An int kwargs use to grab the node hashes while deserializing components.

        Returns
        -------
        `aiobungie.records.Record`
            A standard implementation of a profile record component.
        """

    @abc.abstractmethod
    def deserialize_character_records(
        self,
        payload: typedefs.JSONObject,
        scores: typing.Optional[records.RecordScores] = None,
        record_hashes: typing.Optional[list[int]] = None,
    ) -> records.CharacterRecord:
        """Deserialize a JSON object of a profile character record component.

        This almost does the same this as `deserialize_records` but
        has more fields which can only be found in a character record.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON object payload
        scores: `typing.Optional[records.RecordScores]`
            The records scores object.
        record_hashes: `typing.Optional[list[int]]`
            A list of record hashes that's included during deserializing the component.

        Returns
        -------
        `aiobungie.records.CharacterRecord`
            A standard implementation of a profile character record component.
        """

    @abc.abstractmethod
    def deserialize_characters_records(
        self,
        payload: typedefs.JSONObject,
        scores: typing.Optional[records.RecordScores] = None,
        record_hashes: typing.Optional[list[int]] = None,
    ) -> collections.Mapping[int, records.CharacterRecord]:
        ...

    @abc.abstractmethod
    def deserialize_profile_records(
        self, payload: typedefs.JSONObject
    ) -> collections.Mapping[int, records.Record]:
        ...

    @abc.abstractmethod
    def deserialize_objectives(self, payload: typedefs.JSONObject) -> records.Objective:
        """Deserialize a JSON payload of an objective found in a record profile component.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.records.Objective`
            A record objective object.
        """

    # Inventory entities and Definitions.

    @abc.abstractmethod
    def deserialize_inventory_entity(
        self, payload: typedefs.JSONObject, /
    ) -> entity.InventoryEntity:
        """Deserialize a JSON payload of an inventory entity item information.

        This can be any item from `DestinyInventoryItemDefinition` definition.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.InventoryEntity`
            An entity item object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_inventory_results(
        self, payload: typedefs.JSONObject
    ) -> collections.Sequence[entity.SearchableEntity]:
        """Deserialize results of searched Destiny2 entities.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `collections.Sequence[aiobungie.crate.SearchableEntity]`
            A sequence of the found searched entities.
        """

    @abc.abstractmethod
    def deserialize_objective_entity(
        self, payload: typedefs.JSONObject, /
    ) -> entity.ObjectiveEntity:
        """Deserialize a JSON payload of an objetive entity information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.ObjectiveEntity`
            An objetive entity object of the deserialized payload.
        """

    # Activities.

    @abc.abstractmethod
    def deserialize_activity(
        self, payload: typedefs.JSONObject, /
    ) -> activity.Activity:
        """Deserialize a JSON payload of an activity history information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.Activity`
            An activity object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_activities(
        self, payload: typedefs.JSONObject, /
    ) -> collections.Sequence[activity.Activity]:
        """Deserialize a JSON payload of an array of activity history information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `collections.Sequence[aiobungie.crate.Activity]`
            A sequence of activity objects of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_post_activity(
        self, payload: typedefs.JSONObject
    ) -> activity.PostActivity:
        """Deserialize a JSON payload of a post activity information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.PostActivity`
            A post activity object.
        """

    @abc.abstractmethod
    def deserialize_available_activity(
        self, payload: typedefs.JSONObject
    ) -> activity.AvailableActivity:
        """Deserialize a JSON payload of an available activities.

        This method is used to deserialize an array of `aiobungie.crate.CharacterActivity.available_activities`.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.AvailableActivity`
            An available activity object.
        """

    @abc.abstractmethod
    def deserialize_character_activity(
        self, payload: typedefs.JSONObject
    ) -> activity.CharacterActivity:
        """Deserialize a JSON payload of character activity profile component.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.CharacterActivity`
            A character activities component object.
        """

    # Milestones.

    @abc.abstractmethod
    def deserialize_public_milestone_content(
        self, payload: typedefs.JSONObject
    ) -> milestones.MilestoneContent:
        """Deserialize a JSON payload of milestone content information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.MilestoneContent`
            A milestone content object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_milestone(
        self, payload: typedefs.JSONObject
    ) -> milestones.Milestone:
        ...

    # Social and friends.

    @abc.abstractmethod
    def deserialize_friend(self, payload: typedefs.JSONObject, /) -> friends.Friend:
        """Deserialize a JSON payload of a Bungie friend information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.Friend`
            A friend object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_friends(
        self, payload: typedefs.JSONObject
    ) -> collections.Sequence[friends.Friend]:
        """Deserialize a JSON sequence of Bungie friends information.

        This is usually used to deserialize the incoming/outgoing friend requests.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `collections.Sequence[aiobungie.crate.Friend]`
            A sequence of friends object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_friend_requests(
        self, payload: typedefs.JSONObject
    ) -> friends.FriendRequestView:
        """Deserialize a JSON sequence of Bungie friend requests information.

        This is used for incoming/outgoing friend requests.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `collections.Sequence[aiobungie.crate.FriendRequestView]`
            A sequence of incoming and outgoing friends object of the deserialized payload.
        """

    # Fireteams.

    @abc.abstractmethod
    def deserialize_fireteams(
        self, payload: typedefs.JSONObject
    ) -> typedefs.NoneOr[collections.Sequence[fireteams.Fireteam]]:
        """Deserialize a JSON sequence of Bungie fireteams information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `collections.Sequence[aiobungie.crate.Fireteam]`
            A sequence of fireteam object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_fireteam_destiny_users(
        self, payload: typedefs.JSONObject
    ) -> fireteams.FireteamUser:
        """Deserialize a JSON payload of Bungie fireteam destiny users information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.FireteamUser`
            A fireteam user object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_fireteam_members(
        self, payload: typedefs.JSONObject, *, alternatives: bool = False
    ) -> typing.Optional[collections.Sequence[fireteams.FireteamMember]]:
        """Deserialize a JSON sequence of Bungie fireteam members information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.
        alternatives : `bool`
            If set to `True`, Then it will deserialize the `alternatives` data in the payload.
            If not the it will just deserialize the `members` data.

        Returns
        -------
        `typing.Optional[collections.Sequence[aiobungie.crate.FireteamUser]]`
            An optional sequence of the fireteam members object of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_available_fireteams(
        self, data: typedefs.JSONObject, *, no_results: bool = False
    ) -> typing.Union[
        fireteams.AvalaibleFireteam, collections.Sequence[fireteams.AvalaibleFireteam]
    ]:
        """Deserialize a JSON payload of a sequence of/fireteam information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.
        no_results : `bool`
            Whether to deserialize the data from `results` in the payload or not.

        Returns
        -------
        `typing.Union[aiobungie.crate.fireteams.AvalaibleFireteam, collections.Sequence[aiobungie.crate.fireteams.AvalaibleFireteam]]` # noqa: E501
            An available fireteam or a sequence of available fireteam object of the deserialized payload.
        """

    # Seasonal content.

    @abc.abstractmethod
    def deserialize_seasonal_artifact(
        self, payload: typedefs.JSONObject
    ) -> season.Artifact:
        """Deserialize a JSON payload of a Destiny 2 seasonal artifact information.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crate.Artifact`
            A seasonal artifact object of the deserialized payload.
        """
