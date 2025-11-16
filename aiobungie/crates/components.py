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

"""Bungie profile components implementation.

Components are returned when fetching a profile. All components may or may not be available
since it depends on components passed to the request or due to privacy by the profile owner.
"""

from __future__ import annotations

__all__ = (
    "Component",
    "CharacterComponent",
    "ProfileComponent",
    "RecordsComponent",
    "ItemsComponent",
    "VendorsComponent",
    "RecordsComponent",
    "UninstancedItemsComponent",
    "StringVariableComponent",
    "CraftablesComponent",
)

import typing

import attrs

from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    import collections.abc as collections

    from aiobungie.crates import activity
    from aiobungie.crates import character as character_
    from aiobungie.crates import fireteams, items, profile
    from aiobungie.crates import records as records_


@typing.final
class ComponentPrivacy(int, enums.Enum):
    """An enum the provides privacy settings for profile components."""

    NONE = 0
    PUBLIC = 1
    PRIVATE = 2


# Main component cannot inherit from multiple classes that have `__slots__`
# Which's why some components have no slots.
@attrs.frozen(kw_only=True, slots=False)
class RecordsComponent:
    """Represents records-only Bungie component.

    This includes all components that falls under the records object.

    Notes
    -----
    * profile_records is for global profile records
    * character_records is for character-only records.

    Included Components
    -------------------
    - `ProfileRecords`
    - `CharacterRecords`
    """

    profile_records: collections.Mapping[int, records_.Record] | None
    """A mapping from the profile record id to a record component.

    Notes
    -----
    * This will be available when `aiobungie.ComponentType.RECORDS`
    is passed to the request components. otherwise will be `None`.
    * This will always be `None` if it's a character component.
    """

    character_records: collections.Mapping[int, records_.CharacterRecord] | None
    """A mapping from character record ids to a character record component.

    This will be available when `aiobungie.ComponentType.RECORDS`
    is passed to the request components. otherwise will be `None`.
    """


@attrs.frozen(kw_only=True)
class CraftablesComponent:
    """Represents craftables-only Bungie component."""

    craftables: collections.Mapping[int, items.CraftableItem | None]
    """A mapping from craftable item IDs to a craftable item component.

    Items may or may not be available but its hash will always be available.
    You can use the hash to fetch those items using `fetch_craftables` method.
    """

    crafting_root_node_hash: int
    """The hash for the root presentation node definition of craftable item categories."""


@attrs.frozen(kw_only=True)
class ProfileComponent:
    """Represents a profile-only Bungie component.

    This includes all components that falls under the profile object.

    Included Components
    -------------------
    - `Profiles`
    - `ProfileInventories`
    - `ProfileCurrencies`
    - `ProfileProgression`
    """

    profiles: profile.Profile | None
    """The profile component.

    This will be available when `aiobungie.ComponentType.PROFILE` is passed to the request components.
    otherwise will be `None`.
    """

    profile_progression: profile.ProfileProgression | None
    """The profile progression component.

    This will be available when `aiobungie.ComponentType.PROFILE_PROGRESSION`
    is passed to the request components.
    otherwise will be `None`.
    """

    profile_currencies: collections.Sequence[profile.ProfileItemImpl] | None
    """A sequence of profile currencies component.

    Notes
    -----
    * This will always be `None` unless `auth="access_token"` is passed to the request.
    * This will always be `None` unless `aiobungie.ComponentType.PROFILE_CURRENCIES`
    is passed to the request components.
    """

    profile_inventories: collections.Sequence[profile.ProfileItemImpl] | None
    """A sequence of profile inventories items component.

    Notes
    -----
    * This will always be `None` unless `auth="access_token"` is passed to the request.
    * This will always be `None` unless `aiobungie.ComponentType.PROFILE_INVENTORIES`
    is passed to the request components.
    """


@attrs.frozen(kw_only=True)
class UninstancedItemsComponent:
    """Represents Components belonging to the player's uninstanced items."""

    objectives: (
        collections.Mapping[int, collections.Sequence[records_.Objective]] | None
    )
    """A mapping from the objective id to a sequence of objectives component."""

    perks: collections.Mapping[int, collections.Collection[items.ItemPerk]] | None
    """A mapping for the item instance id to its perks."""


@attrs.frozen(kw_only=True, repr=False)
class ItemsComponent(UninstancedItemsComponent):
    """Represents items-only Bungie component.

    This component implements most of the `ItemX` components, i.e. ItemInstances, ItemStats, ItemSockets, etc.

    Note
    -----
    Some fields will always be `None` until either `aiobungie.ComponentType.CHARACTER_INVENTORY`
    or `aiobungie.ComponentType.CHARACTER_EQUIPMENT` is passed to the request.
    """

    instances: collections.Sequence[collections.Mapping[int, items.ItemInstance]] | None
    """A sequence from the item instance id to an item object bound to this instance.

    This will be available when `aiobungie.ComponentType.ITEM_INSTANCES` is passed to the request.
    otherwise will be `None`.
    """

    render_data: collections.Mapping[int, tuple[bool, dict[int, int]]] | None
    """A mapping from the item instance id to tuple that holds two values.

    * First one is a bool that determines whether this item uses custom dyes or not.
    * Second one is dict that holds int key that maps to int value of the art regions.

    This will be available when `aiobungie.ComponentType.ITEM_RENDER_DATA` is passed to the request.
    otherwise will be `None`.
    """

    stats: collections.Mapping[int, items.ItemStatsView] | None
    """A mapping of the item instance id to a view of its stats.

    This will be available when `aiobungie.ComponentType.ITEM_STATS` is passed to the request.
    otherwise will be `None`.
    """

    sockets: collections.Mapping[int, collections.Sequence[items.ItemSocket]] | None
    """A mapping from the item instance id to a sequence of inserted sockets into it.

    This will be available when `aiobungie.ComponentType.ITEM_SOCKETS` is passed to the request.
    otherwise will be `None`.
    """

    reusable_plugs: (
        collections.Mapping[int, collections.Sequence[items.PlugItemState]] | None
    )
    """If the item supports reusable plugs,
    this is the mapping from the item instance id to a sequence of plugs that are allowed to be used for the socket.

    This will be available when `aiobungie.ComponentType.ITEM_SOCKETS` is passed to the request.
    otherwise will be `None`.
    """

    plug_objectives: (
        collections.Mapping[
            int, collections.Mapping[int, collections.Collection[records_.Objective]]
        ]
        | None
    )
    """A mapping from the item instance id to a mapping of the plug hash to
    a collections of the plug objectives being returned.

    This will be available when `aiobungie.ComponentType.ITEM_OBJECTIVES` is passed to the request.
    otherwise will be `None`.
    """

    plug_states: collections.Sequence[items.PlugItemState] | None
    """A sequence of the plug states.

    This will be available when `aiobungie.ComponentType.ITEM_SOCKETS` is passed to the request.
    otherwise will be `None`.
    """


@attrs.frozen(kw_only=True)
class VendorsComponent:
    """Represents vendors-only Bungie component."""


@attrs.frozen(kw_only=True, slots=False)
class StringVariableComponent:
    """Represents the profile string variable component.

    This component will be available when `aiobungie.ComponentType.STRING_VARIABLES`
    is passed to the request components. otherwise attributes will be `None`.

    Included Components
    -------------------
    - `StringVariables`
    """

    profile_string_variables: collections.Mapping[int, int] | None
    """A mapping from an expression mapping definition hash to its value."""

    character_string_variables: (
        collections.Mapping[int, collections.Mapping[int, int]] | None
    )
    """A mapping from the character id to a mapping from an expression mapping definition hash to its value."""


@attrs.frozen(kw_only=True, slots=False)
class MetricsComponent:
    """Represents the profile metrics component.

    This will be available when `aiobungie.ComponentType.METRICS`
    is passed to the request components.
    otherwise will be `None`.

    Included Components
    -------------------
    - `Metrics`
    """

    metrics: (
        collections.Sequence[
            collections.Mapping[int, tuple[bool, records_.Objective | None]]
        ]
        | None
    )
    """A sequence of mappings from the metrics hash to a tuple contains two elements.

    * The first is always a `bool` determines whether the object is visible or not.
    * The second is an `aiobungie.crates.Objective` of the metrics object if it has one. Otherwise it will be `None`.
    """

    root_node_hash: int | None
    """The metrics presentation root node hash."""


@attrs.frozen(kw_only=True)
class CharacterComponent(RecordsComponent):
    """Represents a character-only Bungie component.

    This includes all components that falls under the character object.

    Included Components
    -------------------
    - `Characters`
    - `CharacterInventories`
    - `CharacterProgression`
    - `CharacterRenderData`
    - `CharacterActivities`
    - `CharacterEquipments`
    - `PresentationNodes`
    - `CharacterCurrencyLookups`
    - `Collectibles`
    - `CharacterLoadouts`
    """

    character: character_.Character | None
    """The character component.

    This will be available when `aiobungie.ComponentType.CHARACTERS` is passed to the request.
    otherwise will be `None`.
    """

    inventory: collections.Sequence[profile.ProfileItemImpl] | None
    """A sequence of the character inventory items component.

    Those items may be Weapons, emblems, ships, sparrows, etc.

    This will always be `None` unless `aiobungie.ComponentType.CHARACTER_INVENTORY`
    is passed to the request components.
    """

    progressions: character_.CharacterProgression | None
    """The character progression component.

    This will always be `None` unless `aiobungie.ComponentType.CHARACTER_PROGRESSION`
    is passed to the request components.
    """

    render_data: character_.RenderedData | None
    """The character rendered data component.

    This will always be `None` unless `aiobungie.ComponentType.RENDER_DATA`
    is passed to the request components.
    """

    activities: activity.CharacterActivity | None
    """A sequence of the character activities component.

    This will always be `None` unless `aiobungie.ComponentType.CHARACTER_ACTIVITIES`
    is passed to the request components.
    """

    equipment: collections.Sequence[profile.ProfileItemImpl] | None
    """A sequence of the character equipment component.

    This will always be `None` unless `aiobungie.ComponentType.CHARACTER_EQUIPMENT`
    is passed to the request components.
    """

    item_components: ItemsComponent | None = attrs.field(repr=False)
    """A component that includes all items components for this character component."""

    nodes: collections.Mapping[int, records_.Node] | None
    """A mapping from the presentation node hash to a node object.

    This will always be `None` unless `aiobungie.ComponentType.PRESENTATION_NODES`
    is passed to the request components.
    """

    currency_lookups: collections.Sequence[items.Currency] | None
    """A sequence of the character currency lookups component.

    Notes
    -----
    * This will always be `None` unless `auth="access_token"` is passed to the request.
    * This will always be `None` unless `aiobungie.ComponentType.CURRENCY_LOOKUPS`
    is passed to the request components.
    """

    collectibles: items.Collectible | None
    """The character's collectibles component.

    This will always be `None` unless `aiobungie.ComponentType.COLLECTIBLES`
    """

    loadouts: collections.Sequence[character_.Loadout] | None
    """A sequence of loadouts that belongs to this character.

    for some reason this is only populated when `CHARACTER_INVENTORY` is used
    and not `CHARACTER_LOADOUTS` component.

    This will be available when `aiobungie.ComponentType.CHARACTERS_INVENTORY` is passed to the request.
    otherwise will be `None`.
    """


@attrs.frozen(kw_only=True)
class Commendation:
    """Basic fields found in the commendation component."""

    total_score: int

    node_percentages: collections.Mapping[int, int]
    """A mapping from the percentage for each commendation type out of total received"""

    score_detail_values: collections.Sequence[int]

    node_scores: collections.Mapping[int, int]

    commendation_scores: collections.Mapping[int, int]


@attrs.frozen(kw_only=True)
class Component(
    ProfileComponent, RecordsComponent, StringVariableComponent, MetricsComponent
):
    """Concrete implementation of all Bungie components.

    Components that requires auth will return `None` unless an `access_token` was passed to the request parameters.

    Example
    -------
    ```py
    import aiobungie

    # The components to get and return.
    components = (
        aiobungie.ComponentType.PROFILE,
        aiobungie.ComponentType.CHARACTERS,
        aiobungie.ComponentType.PROFILE_INVENTORIES,
    )
    profile = await client.fetch_profile(
        id,
        aiobungie.MembershipType.STEAM,
        components,
        # Assuming the component requires an auth token
        auth="ACCESS_TOKEN"
    )
    print(profile.profiles, profile.characters, profile.profile_inventories)
    ```
    """

    characters: collections.Mapping[int, character_.Character] | None
    """A mapping from character's id to`aiobungie.crates.Character`
    of the associated character within the character component.

    This will be available when `aiobungie.ComponentType.CHARACTERS` is passed to the request.
    otherwise will be `None`.
    """

    character_inventories: (
        collections.Mapping[int, collections.Sequence[profile.ProfileItemImpl]] | None
    )
    """A mapping from character's id to a sequence of their character inventory items component.

    Those items may be Weapons, emblems, ships, sparrows, etc.

    Notes
    -----
    * This will always be `None` unless `auth="access_token"` is passed to the request.
    * This will always be `None` unless `aiobungie.ComponentType.CHARACTER_INVENTORY`
    is passed to the request components.
    """

    character_progressions: (
        collections.Mapping[int, character_.CharacterProgression] | None
    )
    """A mapping from character's id to a character progression component.

    Notes
    -----
    * This will always be `None` unless `auth="access_token"` is passed to the request.
    * This will always be `None` unless `aiobungie.ComponentType.CHARACTER_PROGRESSION`
    is passed to the request components.
    """

    character_render_data: collections.Mapping[int, character_.RenderedData] | None
    """A mapping from character's id to a character rendered data component.

    This will always be `None` unless `aiobungie.ComponentType.RENDER_DATA`
    is passed to the request components.
    """

    character_activities: collections.Mapping[int, activity.CharacterActivity] | None
    """A mapping from character's id to a sequence of their character activities component.

    This will always be `None` unless `aiobungie.ComponentType.CHARACTER_ACTIVITIES`
    is passed to the request components.
    """

    character_equipments: (
        collections.Mapping[int, collections.Sequence[profile.ProfileItemImpl]] | None
    )
    """A mapping from character's id to a sequence of their character equipment component.

    This will always be `None` unless `aiobungie.ComponentType.CHARACTER_EQUIPMENT`
    is passed to the request components.
    """

    # character_uninstanced_component: collections.Mapping[int, UninstancedItemsComponent] | None
    """A mapping from the character id to its uninstanced item components."""

    character_collectibles: collections.Mapping[int, items.Collectible] | None
    """A mapping from each character ID to its collectibles component for this profile.

    This will always be `None` unless `aiobungie.ComponentType.COLLECTIBLES`
    """

    character_craftables: collections.Mapping[int, CraftablesComponent] | None
    """A mapping from character IDs to its bound craftable component.

    Notes
    -----
    * This will be available when `aiobungie.ComponentType.CRAFTABLES` is passed to the request component.
    """

    transitory: fireteams.FireteamParty | None
    """Profile Transitory component.

    This component is used to show minimal information about the player's current fireteam party along
    with the its members and the activity.

    This will always be `None` unless `aiobungie.ComponentType.TRANSITORY`
    is passed to the request components.
    """

    item_components: ItemsComponent | None = attrs.field(repr=False)
    """A component that includes all items components for this profile component."""

    profile_plugsets: (
        collections.Mapping[int, collections.Sequence[items.PlugItemState]] | None
    )
    """A mapping from the index of the plugset to a sequence of the profile's plug set objects."""

    character_plugsets: (
        collections.Mapping[
            int, collections.Mapping[int, collections.Sequence[items.PlugItemState]]
        ]
        | None
    )
    """A mapping from the character's id to mapping from the index of
    the plug set to a sequence of plug objects bound to that character.
    """

    character_nodes: (
        collections.Mapping[int, collections.Mapping[int, records_.Node]] | None
    )
    """A mapping from each character ID to a mapping of the node hash
    to a sequence of presentation nodes component.

    This will always be `None` unless `aiobungie.ComponentType.PRESENTATION_NODES`
    is passed to the request components.
    """

    platform_silver: collections.Mapping[str, profile.ProfileItemImpl] | None
    """A mapping from each platform name to its silver information.

    Notes
    -----
    * This will always be `None` unless `auth="access_token"` is passed to the request.
    * This will always be `None` unless `aiobungie.ComponentType.PLATFORM_SILVER`
    is passed to the request components.
    """

    profile_nodes: collections.Mapping[int, records_.Node] | None
    """A mapping from the profile presentation node hash to a node object.

    This will always be `None` unless `aiobungie.ComponentType.PRESENTATION_NODES`
    is passed to the request components.
    """

    character_currency_lookups: (
        collections.Mapping[int, collections.Sequence[items.Currency]] | None
    )
    """A mapping from each character ID to a sequence of its currency lookups.

    Notes
    -----
    * This will always be `None` unless `auth="access_token"` is passed to the request.
    * This will always be `None` unless `aiobungie.ComponentType.CURRENCY_LOOKUPS`
    is passed to the request components.
    """

    character_loadouts: (
        collections.Mapping[int, collections.Sequence[character_.Loadout]] | None
    )
    """A mapping from each character ID to a sequence of its loadouts.

    This component will always be `None` unless `aiobungie.ComponentType.CHARACTER_LOADOUTS`
    is passed to the request components.
    """

    profile_collectibles: items.Collectible | None
    """Represents this profile's collectibles component.

    This will always be `None` unless `aiobungie.ComponentType.COLLECTIBLES`
    """

    commendation: Commendation | None
    """Represents this profile's commendation component.

    This will be available when `aiobungie.ComponentType.` is passed to the request.
    otherwise will be `None`.
    """
