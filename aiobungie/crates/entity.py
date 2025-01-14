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

"""Implementation of `some` Bungie definitions resources.

Unfortunately this doesn't implement all of the definitions, But the most important ones such as `InventoryItemEntity` and `ActivityEntity`.
"""

from __future__ import annotations

__all__ = (
    "InventoryEntity",
    "Entity",
    "ObjectiveEntity",
    "ActivityEntity",
    "PlaylistActivityEntity",
    "InventoryEntityObjects",
    "SearchableEntity",
    "ObjectiveUIStyle",
)

import typing

import attrs

from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    import collections.abc as collections

    from aiobungie import builders, typedefs
    from aiobungie.crates import activity


@typing.final
class GatingScope(int, enums.Enum):
    """An enum represents restrictive type of gating that is being performed by an entity.

    This is useful as a shortcut to avoid a lot of lookups when determining whether the gating on an Entity
    applies to everyone equally, or to their specific Profile or Character states.
    """

    NONE = 0
    GLOBAL = 1
    CLAN = 2
    PROFILE = 3
    CHARACTER = 4
    ITEM = 5
    ASSUMED_WORST_CASE = 6


@typing.final
class ValueUIStyle(int, enums.Enum):
    AUTOMATIC = 0
    FRACTION = 1
    CHECK_BOX = 2
    PERCENTAGE = 3
    DATETIME = 4
    FRACTION_FLOAT = 5
    INTEGER = 6
    TIME_DURATION = 7
    HIDDEN = 8
    MULTIPLIER = 9
    GREEN_PIPS = 10
    RED_PIPS = 11
    EXPLICIT_PERCENTAGE = 12
    RAW_FLOAT = 13
    LEVEL_AND_REWARD = 14


@typing.final
class ObjectiveUIStyle(int, enums.Enum):
    NONE = 0
    HIGHLIGHTED = 1
    CRAFTING_WEAPON_LEVEL = 2
    CRAFTING_WEAPON_LEVEL_PROGRESS = 3
    CRAFTING_WEAPON_TIMESTAMP = 4
    CRAFTING_MEMENTOS = 5
    CRAFTING_MEMENTO_TITLE = 6


@attrs.frozen(kw_only=True)
class Entity:
    """Represents any entity in Destiny 2.
    This can be item definition, activity definition, etc.

    This is the core object which all other entities should inherit from.
    It holds core information that all bungie entities has.
    """

    hash: int
    """Entity's hash."""

    index: int
    """The entity's index."""

    name: str | None
    """Entity's name, `None` if the entity name was empty."""

    description: str | None
    """Entity's description, `None` if the entity description was empty."""

    icon: builders.Image
    """Entity's icon."""

    has_icon: bool = attrs.field(repr=False)
    """A boolean that returns True if the entity has an icon."""


@attrs.frozen(kw_only=True)
class SearchableEntity:
    """Represents an entity object returned from a searchable term."""

    suggested_words: collections.Sequence[str]
    """A list of suggested words that might make for better search results, based on the text searched for."""

    hash: int
    """Entity's hash."""

    entity_type: str
    """The entity's type, i.e., `DestinyInventoryItemDefinition`."""

    name: str
    """Entity's name."""

    description: str | None
    """Entity's description. `None` if not set."""

    icon: builders.Image
    """Entity's icon."""

    has_icon: bool
    """Whether this entity has an icon or not."""

    weight: float
    """The ranking value for sorting that we calculated using our relevance formula."""


# We separate the JSON objects within the InventoryEntity from the object itself
# just to organize them better.
@attrs.frozen(kw_only=True, repr=False)
class InventoryEntityObjects:
    """JSON object found inside an inventory item definition."""

    action: typedefs.JSONObject | None
    """"""

    set_data: typedefs.JSONObject | None
    """If this item is a quest, this block will be non-null."""

    quality: typedefs.JSONObject | None
    """If this item can have a level or stats, this block will be available."""

    preview: typedefs.JSONObject | None
    """If this item can be Used or Acquired to gain other items
    (for instance, how Eververse Boxes can be consumed to get items from the box), this block will available.
    """

    value: typedefs.JSONObject | None
    """The conceptual "Value" of an item, if any was defined."""

    source_data: typedefs.JSONObject | None
    """If this item has a known source, this block will be available."""

    objectives: typedefs.JSONObject | None
    """If this item has Objectives (extra tasks that can be accomplished related to the item,
    This field will be available.
    """

    plug: typedefs.JSONObject | None
    """If this item is a Plug, this will be available."""

    gearset: typedefs.JSONObject | None
    """"""

    metrics: typedefs.JSONObject | None
    """If this item has available metrics to be shown, this block will be available."""

    sack: typedefs.JSONObject | None
    """"""

    sockets: typedefs.JSONObject | None
    """"""

    summary: typedefs.JSONObject | None
    """"""

    talent_gird: typedefs.JSONObject | None
    """"""

    stats: typedefs.JSONObject | None
    """If this item can have stats (such as a weapon, armor, or vehicle),
    this block will be non-null and populated with the stats found on the item.
    """

    equipping_block: typedefs.JSONObject | None
    """If this item can be equipped, this block will be available."""

    translation_block: typedefs.JSONObject | None
    """If this item can be rendered, this block will be available."""

    investments_stats: typedefs.JSONObject | None
    """"""

    perks: typedefs.JSONObject | None
    """"""

    animations: collections.Sequence[typedefs.JSONObject]
    """"""

    links: collections.Sequence[dict[str, str]]
    """"""


@attrs.frozen(kw_only=True)
class InventoryEntity(Entity):
    """Represents a bungie inventory item entity.

    This derives from `DestinyInventoryItemDefinition` definition.
    """

    type: enums.ItemType
    """Entity's type. Can be undefined if nothing was found."""

    about: str | None
    """Entity's about. Originally this is the flavorText field but to make readable its renamed to about.."""

    objects: InventoryEntityObjects = attrs.field(repr=False)
    """JSON objects found within the item."""

    trait_ids: collections.Sequence[str] = attrs.field(repr=False)
    """"""

    trait_hashes: collections.Sequence[int] = attrs.field(repr=False)
    """"""

    item_class: enums.Class = attrs.field(repr=False)
    """The entity's class type."""

    sub_type: enums.ItemSubType = attrs.field(repr=False)
    """The subtype of the entity. A type is a weapon or armor.

    A subtype is a Hand Cannon or leg armor for an example.
    """

    breaker_type: int = attrs.field(repr=False)
    """Some weapons and plugs can have a "Breaker Type",
    a special ability that works sort of like damage type vulnerabilities.
    """

    breaker_type_hash: int | None = attrs.field(repr=False)
    """The item breaker type hash."""

    damagetype_hashes: collections.Sequence[int] | None = attrs.field(repr=False)
    """"""

    damage_types: collections.Sequence[int] | None = attrs.field(repr=False)
    """The list of all damage types."""

    default_damagetype: int = attrs.field(repr=False)
    """"""

    default_damagetype_hash: int | None = attrs.field(repr=False)
    """"""

    collectible_hash: int | None = attrs.field(repr=False)
    """If this item has a collectible related to it, this is the hash identifier of that collectible entry."""

    watermark_icon: builders.Image | None = attrs.field(repr=False)
    """Entity's water mark."""

    watermark_shelved: builders.Image | None = attrs.field(repr=False)
    """If available, this is the 'shelved' release watermark overlay for the icon."""

    secondary_icon: builders.Image | None = attrs.field(repr=False)
    """A secondary icon associated with the item.

    Currently this is used in very context specific applications, such as Emblem Nameplates.
    """

    secondary_overlay: builders.Image | None = attrs.field(repr=False)
    """The "secondary background" of the secondary icon."""

    secondary_special: builders.Image | None = attrs.field(repr=False)
    """The "special" background for the item. For Emblems"""

    background_colors: collections.Mapping[str, bytes] = attrs.field(repr=False)
    """Most emblems have a background colour, This field represents them."""

    screenshot: builders.Image | None = attrs.field(repr=False)
    """Entity's screenshot."""

    ui_display_style: str | None = attrs.field(repr=False)
    """"""

    tier_type: enums.TierType | None = attrs.field(repr=False, hash=False)
    """Entity's tier type. This can be Exotic, Rare, or Common etc."""

    tier: enums.ItemTier | None = attrs.field(repr=False)
    """The item tier hash as an enum if exists."""

    tier_name: str | None = attrs.field(repr=False)
    """A string version of the item tier. i.e., `Legendery`"""

    type_name: str | None = attrs.field(repr=False, hash=False)
    """Entity's type name. i.e., `Grenade Launcher`."""

    type_and_tier_name: str | None = attrs.field(hash=False)
    """Entity's tier and type name combined, i.e., `Legendary Grenade Launcher`."""

    bucket_hash: int | None = attrs.field(repr=False, hash=False)
    """The entity's bucket type hash, None if it doesn't have one."""

    recovery_bucket_hash: int | None = attrs.field(repr=False)
    """If the item is picked up by the lost loot queue,
    this is the hash identifier for the DestinyInventoryBucketDefinition.
    """

    max_stack_size: int | None = attrs.field(repr=False)
    """The maximum quantity of this item that can exist in a stack."""

    stack_label: str | None = attrs.field(repr=False)
    """If this string is populated, you can't have more than one stack with this label in a given inventory."""

    tooltip_notifications: collections.Sequence[str] = attrs.field(repr=False)
    """"""

    display_source: str | None = attrs.field(hash=False, repr=False)
    """String telling you about how you can find the item."""

    emblem_objective_hash: int | None = attrs.field(repr=False)
    """If the item is an emblem that has a special Objective attached to it, This will be its hash."""

    isinstance_item: bool = attrs.field(repr=False)
    """If True, This item is instanced."""

    expiration_tooltip: str | None = attrs.field(repr=False)
    """If the item expires while playing in an activity, we show a different message."""

    expire_in_orbit_message: str | None = attrs.field(repr=False)
    """If the item expires in orbit, This message will be available."""

    suppress_expiration: bool | None = attrs.field(repr=False)
    """"""

    lore_hash: int | None = attrs.field(repr=False)
    """The entity's lore hash. Can be undefined if no lore hash found."""

    is_equippable: bool = attrs.field(repr=False)
    """True if the entity can be equipped or False."""

    summary_hash: int | None = attrs.field(repr=False)
    """Entity's summary hash."""

    allow_actions: bool = attrs.field(repr=False)
    """"""

    has_postmaster_effect: bool = attrs.field(repr=False)
    """Whether something will occur if you transfer this item from postmaster or not."""

    not_transferable: bool = attrs.field(repr=False)
    """If True, this item cannot be transferred, Otherwise it can."""

    category_hashes: collections.Sequence[int] = attrs.field(repr=False)
    """"""

    season_hash: int | None = attrs.field(repr=False)


@attrs.frozen(kw_only=True, weakref_slot=False)
class ObjectiveEntity(Entity):
    """Represents a bungie inventory item entity.

    This derives from `DestinyObjectiveDefinition` definition.
    """

    # TODO: document these.

    unlock_value_hash: int

    minimum_visibility: int

    completion_value: int

    scope: GatingScope

    location_hash: int

    allowed_negative_value: bool

    allowed_value_change: bool

    counting_downward: bool

    display_only_objective: bool

    value_style: ValueUIStyle

    complete_value_style: ValueUIStyle

    progress_value_style: ValueUIStyle

    allow_over_completion: bool

    show_value_style: ValueUIStyle

    progress_description: str

    perks: dict[str, int]

    stats: dict[str, int]

    ui_label: str

    ui_style: ObjectiveUIStyle


@attrs.frozen(kw_only=True, hash=True, weakref_slot=False)
class ActivityEntity(Entity):
    """Represents a Bungie Activity definition and its entities.

    This derives from `DestinyActivityDefinition` definition.
    """

    release_icon: builders.Image
    """The release icon of this activity if it has one."""

    release_time: int
    """The release time of this activity."""

    unlock_hash: int
    """The completion unlock hash of this activity."""

    light_level: int
    """Activity's light level."""

    place: enums.Place
    """The place of this activity."""

    type_hash: int
    """The activity's type hash. This bounds to activity types such as Strikes, Crucible, Raids, etc."""

    tier: activity.Difficulty
    """Activity's difficulty tier."""

    image: builders.Image
    """Activity's pgcr image."""

    rewards: collections.Sequence[activity.Rewards] | None
    """A sequence of this activity's rewards. Returns `None` if not found."""

    modifiers: collections.Sequence[int] | None
    """A sequence of the activity's modifier hashes. Returns `None` if not found."""

    challenges: collections.Sequence[activity.Challenges] | None
    """A sequence of the activity's challenges. Returns `None` if not found."""

    is_playlist: bool
    """Whether this activity is present in a playlist or not."""

    unlock_strings: collections.Sequence[str] | None
    """An optional status string that could be conditionally displayed about an activity"""

    inherits_free_room: bool
    """"""

    playlist_activities: collections.Sequence[PlaylistActivityEntity] | None
    """Represents all of the possible activities that could be played in the Playlist,
    along with information that we can use to determine if they are active at the present time.
    """

    matchmaking: activity.Matchmaking
    """Information about matchmaking for this activity."""

    guided_game: activity.GuidedGame | None
    """Information about activity's guided game mode, If exists otherwise `None`."""

    mode: enums.GameMode | None
    """If this activity had an activity mode directly defined on it, this will be the hash of that mode."""

    mode_hash: int | None
    """If the activity had an activity mode directly defined on it, this will be the enum value of that mode."""

    mode_hashes: collections.Sequence[enums.GameMode] = attrs.field(repr=False)
    """The hash identifiers for Activity Modes relevant to this entry."""

    mode_types: collections.Sequence[enums.GameMode] = attrs.field(repr=False)
    """A sequence of the activity gamemode types."""

    loadouts: collections.Sequence[int]
    """The set of all possible loadout requirements that could be active for this activity.

    Only one will be active at any given time. and you can discover which one through
    activity-associated data such as Milestones that have activity info on them.
    """

    is_pvp: bool
    """Whether the activity is PvP or not."""

    phase_hashes: collections.Sequence[int]
    """The list of phases or points of entry into an activity,
    along with information we can use to determine their gating and availability.
    """

    locations: collections.Collection[activity.Location]
    """A collection of location mappings affected by this activity."""


@attrs.frozen(kw_only=True, hash=True, weakref_slot=False)
class PlaylistActivityEntity:
    """Represents an activity playlists definition/entity.

    Derives `DestinyActivityPlaylistItemDefinition`
    """

    hash: int
    """The hash identifier of the Activity that can be played."""

    mode_hash: int | None
    """If this activity had an activity mode directly defined on it, this will be the hash of that mode."""

    mode: enums.GameMode | None
    """If the activity had an activity mode directly defined on it, this will be the enum value of that mode."""

    mode_hashes: collections.Sequence[int]
    """The hash identifiers for Activity Modes relevant to this entry."""

    mode_types: collections.Sequence[enums.GameMode]
    """A sequence of the activity game-mode types."""
