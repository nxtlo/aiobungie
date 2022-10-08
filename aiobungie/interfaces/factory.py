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

from aiobungie.internal import iterators

__all__: tuple[str, ...] = ("FactoryInterface",)

import abc
import typing

if typing.TYPE_CHECKING:
    import collections.abc as collections

    from aiobungie import traits
    from aiobungie import typedefs
    from aiobungie.crates import activity
    from aiobungie.crates import application
    from aiobungie.crates import character
    from aiobungie.crates import clans
    from aiobungie.crates import components
    from aiobungie.crates import entity
    from aiobungie.crates import fireteams
    from aiobungie.crates import friends
    from aiobungie.crates import items
    from aiobungie.crates import milestones
    from aiobungie.crates import profile
    from aiobungie.crates import progressions
    from aiobungie.crates import records
    from aiobungie.crates import season
    from aiobungie.crates import user


class FactoryInterface(abc.ABC):
    """An API interface that documents and describes the implementation of the marshaller factory."""

    __slots__ = ()

    if typing.TYPE_CHECKING:
        _net: traits.Netrunner

    # Users, Memberships.

    @abc.abstractmethod
    def deserialize_user(self, data: typedefs.JSONObject) -> user.User:
        """Deserialize a raw JSON results of fetched user memberships and Bungie.net user its their id.

        Parameters
        ----------
        data : `aiobungie.typedefs.JSONObject`
            The JSON data/payload.

        Returns
        -------
        `aiobungie.crates.User`
            A user object.
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
        `aiobungie.crates.BungieUser`
            A Bungie user.
        """

    @abc.abstractmethod
    def deserialize_searched_user(
        self, payload: typedefs.JSONObject
    ) -> user.SearchableDestinyUser:
        """Deserialize the results of user search details.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crates.SearchableDestinyUser`
            The searched for Destiny 2 membership.
        """

    @abc.abstractmethod
    def deserialize_partial_bungie_user(
        self, payload: typedefs.JSONObject
    ) -> user.PartialBungieUser:
        """Deserialize a raw JSON of a partial `bungieNetUserInfo`.

        A partial user is a bungie.net user payload with missing information from
        the main `BungieUser` object.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crates.PartialBungieUser`
            A partial bungie user.
        """

    @abc.abstractmethod
    def deserialize_destiny_membership(
        self, payload: typedefs.JSONObject
    ) -> user.DestinyMembership:
        """Deserialize a raw JSON of `destinyUserInfo` destiny membership information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crates.user.DestinyMembership`
            A Destiny 2 membership.
        """

    @abc.abstractmethod
    def deserialize_destiny_memberships(
        self, data: typedefs.JSONArray
    ) -> collections.Sequence[user.DestinyMembership]:
        """Deserialize a raw JSON payload/array of `destinyUserInfo`.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONArray`
            The JSON payload.

        Returns
        -------
        `collections.Sequence[aiobungie.crates.user.DestinyMembership]`
            A sequence of Destiny 2 memberships.
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
        `collections.Sequence[aiobungie.crates.user.UserThemes]`
            A sequence of bungie user themes.
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
        `collections.Sequence[aiobungie.crates.UserCredentials]`
            A sequence of user's credentials.
        """

    # Clans, Groups.

    @abc.abstractmethod
    def deserialize_clan(self, payload: typedefs.JSONObject) -> clans.Clan:
        """Deserialize a raw JSON payload of Bungie clan information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crates.Clan`
            A clan owner.
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
        `aiobungie.typedefs.NoneOr[aiobungie.crates.GroupMember]`
            A group member. This can return `None` if nothing was found.
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
        `aiobungie.crates.ClanMember`
            A clan member.
        """

    @abc.abstractmethod
    def deserialize_clan_members(
        self, data: typedefs.JSONObject, /
    ) -> iterators.Iterator[clans.ClanMember]:
        """Deserialize a JSON payload of a clan members information.

        Parameters
        ----------
        data : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.iterators.Iterator[aiobungie.crates.ClanMember]`
            An iterator of clan members of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_clan_conversations(
        self, payload: typedefs.JSONArray
    ) -> collections.Sequence[clans.ClanConversation]:
        """Deserialize a JSON array of a clan conversations information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONArray`
            The JSON payload.

        Returns
        -------
        `collections.Sequence[aiobungie.crates.ClanConversation]`
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
        `collections.Sequence[aiobungie.crates.ClanBanner]`
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
        `aiobungie.crates.application.ApplicationOwner`
            An application owner.
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
        `aiobungie.crates.application.Application`
            An application.
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
        `aiobungie.crates.CharacterComponent`
            A character component.
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
        `aiobungie.crates.RenderedData`
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
        `aiobungie.crates.character.MinimalEquipments`
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
        `aiobungie.crates.character.Dye`
            Information about a character dye object.
        """

    @abc.abstractmethod
    def deserialize_character_customization(
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
        `aiobungie.crates.character.CustomizationOptions`
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
    def deserialize_character_equipments(
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
    ) -> progressions.Progression:
        ...

    @abc.abstractmethod
    def deserialize_character_progressions(
        self, payload: typedefs.JSONObject
    ) -> character.CharacterProgression:
        ...

    @abc.abstractmethod
    def deserialize_character_progressions_mapping(
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
        `aiobungie.crates.ProfileProgression`
            A profile progression component.
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
        `typing.Optional[aiobungie.crates.Profile]`
            A profile.
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
        `typing.Optional[collections.Sequence[aiobungie.crates.ProfileItemImpl]]`
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
        `aiobungie.crates.LinkedProfile`
            A hard linked profile.
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
        `aiobungie.crates.ProfileItemImpl`
            Implementation of a Destiny 2 profile component item.
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
        `aiobungie.crates.Component`
            A component implementation that includes all other components
            of the deserialized payload.
        """

    @abc.abstractmethod
    def deserialize_items_component(
        self, payload: typedefs.JSONObject
    ) -> components.ItemsComponent:
        """Deserialize a JSON objects within the `itemComponents` key.`"""

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
            This exists only to keep the signature of `aiobungie.crates.CharacterRecord` with the record object.
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
    ) -> records.CharacterRecord:
        """Deserialize a JSON object of a profile character record component.

        This almost does the same this as `deserialize_records` but
        has more fields which can only be found in a character record.

        Parameters
        ----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON object payload

        Returns
        -------
        `aiobungie.records.CharacterRecord`
            A standard implementation of a profile character record component.
        """

    @abc.abstractmethod
    def deserialize_characters_records(
        self,
        payload: typedefs.JSONObject,
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
        `aiobungie.crates.records.Objective`
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
        `aiobungie.crates.InventoryEntity`
            An entity item.
        """

    @abc.abstractmethod
    def deserialize_inventory_results(
        self, payload: typedefs.JSONObject
    ) -> iterators.Iterator[entity.SearchableEntity]:
        """Deserialize results of searched Destiny2 entities.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.iterators.Iterator[aiobungie.crates.SearchableEntity]`
            An iterator over the found searched entities.
        """

    @abc.abstractmethod
    def deserialize_objective_entity(
        self, payload: typedefs.JSONObject, /
    ) -> entity.ObjectiveEntity:
        """Deserialize a JSON payload of an objective entity information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crates.ObjectiveEntity`
            An objective entity.
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
        `aiobungie.crates.Activity`
            An activity.
        """

    @abc.abstractmethod
    def deserialize_activities(
        self, payload: typedefs.JSONObject, /
    ) -> iterators.Iterator[activity.Activity]:
        """Deserialize a JSON payload of an array of activity history information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.iterators.Iterator[aiobungie.crates.Activity]`
            Am iterator over activity objects of the deserialized payload.
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
        `aiobungie.crates.PostActivity`
            A post activity object.
        """

    @abc.abstractmethod
    def deserialize_available_activity(
        self, payload: typedefs.JSONObject
    ) -> activity.AvailableActivity:
        """Deserialize a JSON payload of an available activities.

        This method is used to deserialize an array of `aiobungie.crates.CharacterActivity.available_activities`.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crates.AvailableActivity`
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
        `aiobungie.crates.CharacterActivity`
            A character activities component object.
        """

    @abc.abstractmethod
    def deserialize_aggregated_activity(
        self, payload: typedefs.JSONObject
    ) -> activity.AggregatedActivity:
        """Deserialize a JSON payload of an aggregated activity.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crates.AggregatedActivity`
            An aggregated activity object.
        """

    @abc.abstractmethod
    def deserialize_aggregated_activities(
        self, payload: typedefs.JSONObject
    ) -> iterators.Iterator[activity.AggregatedActivity]:
        """Deserialize a JSON payload of an array of aggregated activities.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.iterators.Iterator[aiobungie.crates.AggregatedActivity]`
            An iterator over aggregated activities objects.
        """

    @abc.abstractmethod
    def deserialize_extended_weapon_values(
        self, payload: typedefs.JSONObject
    ) -> activity.ExtendedWeaponValues:
        """Deserialize values of extended weapons JSON object.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crates.ExtendedWeaponValues`
            Information about an extended weapon values.
        """

    @abc.abstractmethod
    def deserialize_post_activity_player(
        self, payload: typedefs.JSONObject, /
    ) -> activity.PostActivityPlayer:
        """Deserialize a JSON payload of a post activity player information.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crates.PostActivityPlayer`
            A post activity player object.
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
        `aiobungie.crates.MilestoneContent`
            A milestone content.
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
        `aiobungie.crates.Friend`
            A friend.
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
        `collections.Sequence[aiobungie.crates.Friend]`
            A sequence of friends.
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
        `collections.Sequence[aiobungie.crates.FriendRequestView]`
            A sequence of incoming and outgoing friends.
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
        `collections.Sequence[aiobungie.crates.Fireteam]`
            A sequence of fireteam.
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
        `aiobungie.crates.FireteamUser`
            A fireteam user.
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
        `typing.Optional[collections.Sequence[aiobungie.crates.FireteamUser]]`
            An optional sequence of the fireteam members.
        """

    @abc.abstractmethod
    def deserialize_available_fireteams(
        self, data: typedefs.JSONObject, *, no_results: bool = False
    ) -> typing.Union[
        fireteams.AvailableFireteam, collections.Sequence[fireteams.AvailableFireteam]
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
        `typing.Union[aiobungie.crates.fireteams.AvailableFireteam, collections.Sequence[aiobungie.crates.fireteams.AvailableFireteam]]` # noqa: E501
            An available fireteam or a sequence of available fireteam.
        """

    @abc.abstractmethod
    def deserialize_fireteam_party(
        self, payload: typedefs.JSONObject
    ) -> fireteams.FireteamParty:
        """Deserialize a JSON payload of `profileTransitory` component response.

        Parameters
        ----------
        payload : `aiobungie.typedefs.JSONObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crates.FireteamParty`
            A fireteam party object of the current fireteam.
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
        `aiobungie.crates.Artifact`
            A seasonal artifact.
        """

    # Items

    @abc.abstractmethod
    def deserialize_instanced_item(
        self, payload: typedefs.JSONObject
    ) -> items.ItemInstance:
        """Deserialize a JSON object into an instanced item.

        Parameters
        -----------
        payload : `aiobungie.internal.helpers.JsonObject`
            The JSON payload.

        Returns
        -------
        `aiobungie.crates.ItemInstance`
            An instanced item object.
        """

    # No docs for this.
    @abc.abstractmethod
    def deserialize_item_energy(self, payload: typedefs.JSONObject) -> items.ItemEnergy:
        ...

    @abc.abstractmethod
    def deserialize_item_perk(self, payload: typedefs.JSONObject) -> items.ItemPerk:
        ...

    @abc.abstractmethod
    def deserialize_item_socket(self, payload: typedefs.JSONObject) -> items.ItemSocket:
        ...

    @abc.abstractmethod
    def deserialize_item_stats_view(
        self, payload: typedefs.JSONObject
    ) -> items.ItemStatsView:
        ...

    @abc.abstractmethod
    def deserialize_plug_item_state(
        self, payload: typedefs.JSONObject
    ) -> items.PlugItemState:
        ...
