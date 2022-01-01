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

"""Implementation of Bungie entity and definitions.

This is still not fully implemented and you may experince bugs.
This will include all Bungie Definitions.
"""

from __future__ import annotations

__all__: tuple[str, ...] = (
    "InventoryEntity",
    "Entity",
    "ObjectiveEntity",
    "BaseEntity",
    "ActivityEntity",
    "PlaylistActivityEntity",
    "InventoryEntityObjects",
    "SearchableEntity",
)

import abc
import typing

import attrs

from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    import collections.abc as collections

    from aiobungie import traits
    from aiobungie import typedefs
    from aiobungie import undefined
    from aiobungie.crate import activity
    from aiobungie.internal import assets


@typing.final
class GatingScope(enums.IntEnum):
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
class ValueUIStyle(enums.IntEnum):
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
    RED_PIPS = 11
    EXPLICIT_PERCENTAGE = 12
    RAW_FLOAT = 13


class Entity(abc.ABC):
    """An interface of any Bungie Definition/Entity.

    This is the main entity which all other entities should inherit from.
    it holds core information that all bungie entities has.
    """

    __slots__ = ()

    @property
    @abc.abstractmethod
    def net(self) -> traits.Netrunner:
        """A network state used for making external requests."""

    @property
    @abc.abstractmethod
    def name(self) -> undefined.UndefinedOr[str]:
        """Entity's name. This can be `UNDEFINED` if not found."""

    @property
    @abc.abstractmethod
    def icon(self) -> assets.MaybeImage:
        """An optional entity's icon if its filled."""

    @property
    @abc.abstractmethod
    def has_icon(self) -> bool:
        """A boolean that returns True if the entity has an icon."""

    @property
    @abc.abstractmethod
    def description(self) -> undefined.UndefinedOr[str]:
        """Entity's description"""

    @property
    @abc.abstractmethod
    def index(self) -> int:
        """The entity's index."""

    @property
    @abc.abstractmethod
    def hash(self) -> int:
        """Entity's hash."""

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return self.hash


@attrs.mutable(kw_only=True, weakref_slot=False)
class BaseEntity(Entity):
    """Concerate Bungie entity implementation."""

    # These are not attribs on purpose.
    # We dont want to redefine them again in the actual entity
    # implementation.

    net: traits.Netrunner = attrs.field(repr=False)
    """A network state used for making external requests."""

    hash: int
    """Entity's hash."""

    index: int
    """The entity's index."""

    name: undefined.UndefinedOr[str]
    """Entity's name."""

    description: undefined.UndefinedOr[str]
    """Entity's description"""

    icon: assets.MaybeImage = attrs.field(repr=False)
    """Entity's icon."""

    has_icon: bool = attrs.field(repr=False)
    """A boolean that returns True if the entity has an icon."""


@attrs.define(kw_only=True, weakref_slot=False, hash=True)
class SearchableEntity:
    """Represents an entity object returned from a seachable term."""

    suggested_words: list[str] = attrs.field(repr=False)
    """A list of suggested words that might make for better search results, based on the text searched for."""

    net: traits.Netrunner = attrs.field(repr=False, eq=False)
    """A network state used for making external requests."""

    hash: int = attrs.field()
    """Entity's hash."""

    entity_type: str = attrs.field()
    """The entity's type, i.e., `DestinyInventoryItemDefinition`."""

    name: str = attrs.field()
    """Entity's name."""

    description: undefined.UndefinedOr[str] = attrs.field()
    """Entity's description. Undefined if not set."""

    icon: assets.Image = attrs.field(repr=False)
    """Entity's icon."""

    has_icon: bool = attrs.field(repr=False)
    """Whether this entity has an icon or not."""

    weight: float = attrs.field(repr=False)
    """The ranking value for sorting that we calculated using our relevance formula."""

    async def fetch_self_item(self) -> typing.Optional[InventoryEntity]:
        """Fetch an item definition of this partial entity.

        Note
        ----
        This will return `None` if the entity type is not `DestinyInventoryItemDefinition`.

        Returns
        -------
        `typing.Optional[InventoryEntity]`
            An inventory item entity or `None` if its not.
        """
        if self.entity_type != "DestinyInventoryItemDefinition":
            return None
        return await self.net.request.fetch_inventory_item(self.hash)


# For the sake of not making stuff a little bit clunky, We separate the JSON objects
# from the normal fields.
@attrs.define(kw_only=True, weakref_slot=False, repr=False)
class InventoryEntityObjects:
    """JSON object found inside an inventory item definition."""

    action: typing.Optional[typedefs.JSONObject] = attrs.field()
    """"""

    set_data: typing.Optional[typedefs.JSONObject] = attrs.field()
    """If this item is a quest, this block will be non-null."""

    quality: typing.Optional[typedefs.JSONObject] = attrs.field()
    """If this item can have a level or stats, this block will be available."""

    preview: typing.Optional[typedefs.JSONObject] = attrs.field()
    """If this item can be Used or Acquired to gain other items
    (for instance, how Eververse Boxes can be consumed to get items from the box), this block will available.
    """

    value: typing.Optional[typedefs.JSONObject] = attrs.field()
    """The conceptual "Value" of an item, if any was defined."""

    source_data: typing.Optional[typedefs.JSONObject] = attrs.field()
    """If this item has a known source, this block will be available."""

    objectives: typing.Optional[typedefs.JSONObject] = attrs.field()
    """If this item has Objectives (extra tasks that can be accomplished related to the item,
    This field will be available.
    """

    plug: typing.Optional[typedefs.JSONObject] = attrs.field()
    """If this item is a Plug, this will be available."""

    gearset: typing.Optional[typedefs.JSONObject] = attrs.field()
    """"""

    metrics: typing.Optional[typedefs.JSONObject] = attrs.field()
    """If this item has available metrics to be shown, this block will be available."""

    sack: typing.Optional[typedefs.JSONObject] = attrs.field()
    """"""

    sockets: typing.Optional[typedefs.JSONObject] = attrs.field()
    """"""

    summary: typing.Optional[typedefs.JSONObject] = attrs.field()
    """"""

    talent_gird: typing.Optional[typedefs.JSONObject] = attrs.field()
    """"""

    stats: typing.Optional[typedefs.JSONObject] = attrs.field()
    """If this item can have stats (such as a weapon, armor, or vehicle),
    this block will be non-null and populated with the stats found on the item.
    """

    equipping_block: typing.Optional[typedefs.JSONObject] = attrs.field()
    """If this item can be equipped, this block will be available."""

    translation_block: typing.Optional[typedefs.JSONObject] = attrs.field()
    """If this item can be rendered, this block will be available."""

    investments_stats: typing.Optional[typedefs.JSONObject] = attrs.field()
    """"""

    perks: typing.Optional[typedefs.JSONObject] = attrs.field()
    """"""

    animations: collections.Sequence[typedefs.JSONObject] = attrs.field()
    """"""

    links: collections.Sequence[dict[str, str]] = attrs.field()
    """"""


@attrs.define(kw_only=True, hash=True, weakref_slot=False)
class InventoryEntity(BaseEntity, Entity):
    """Represents a bungie inventory item entity.

    This derives from `DestinyInventoryItemDefinition` definition.
    """

    type: enums.Item = attrs.field(repr=True, hash=False)
    """Entity's type. Can be undefined if nothing was found."""

    objects: InventoryEntityObjects = attrs.field(repr=False)
    """JSON objects found within the item."""

    trait_ids: list[str] = attrs.field(repr=False)
    """"""

    trait_hashes: list[int] = attrs.field(repr=False)
    """"""

    item_class: enums.Class = attrs.field(repr=False, hash=False, eq=False)
    """The entity's class type."""

    sub_type: enums.Item = attrs.field(repr=False, hash=False, eq=False)
    """The subtype of the entity. A type is a weapon or armor.
    A subtype is a handcannonn or leg armor for an example.
    """

    breaker_type: int = attrs.field(repr=False)
    """Some weapons and plugs can have a "Breaker Type",
    a special ability that works sort of like damage type vulnerabilities.
    """

    breaker_type_hash: typing.Optional[int] = attrs.field(repr=False)
    """The item breaker type hash."""

    damagetype_hashes: typing.Optional[collections.Sequence[int]] = attrs.field(
        repr=False
    )
    """"""

    damage_types: typing.Optional[collections.Sequence[int]] = attrs.field(repr=False)
    """The list of all damage types."""

    default_damagetype: int = attrs.field(repr=False)
    """"""

    default_damagetype_hash: typing.Optional[enums.DamageType] = attrs.field(repr=False)
    """"""

    collectible_hash: typing.Optional[int] = attrs.field(repr=False, hash=True)
    """If this item has a collectible related to it, this is the hash identifier of that collectible entry."""

    watermark_icon: typing.Optional[assets.Image] = attrs.field(repr=False, hash=False)
    """Entity's water mark."""

    watermark_shelved: typing.Optional[assets.Image] = attrs.field(
        repr=False, hash=False
    )
    """If available, this is the 'shelved' release watermark overlay for the icon."""

    secondary_icon: undefined.UndefinedOr[assets.Image] = attrs.field(
        repr=False, hash=False
    )
    """A secondary icon associated with the item.

    Currently this is used in very context specific applications, such as Emblem Nameplates.
    """

    secondary_overlay: undefined.UndefinedOr[assets.Image] = attrs.field(
        repr=False, hash=False
    )
    """The "secondary background" of the secondary icon."""

    secondary_special: undefined.UndefinedOr[assets.Image] = attrs.field(
        repr=False, hash=False
    )
    """The "special" background for the item. For Emblems"""

    background_colors: collections.Mapping[str, bytes] = attrs.field(
        repr=False, hash=False
    )
    """Most emblems have a background colour, This field represents them."""

    screenshot: undefined.UndefinedOr[assets.Image] = attrs.field(
        repr=False, hash=False
    )
    """Entity's screenshot."""

    ui_display_style: undefined.UndefinedOr[str] = attrs.field(repr=False)
    """"""

    tier_type: typing.Optional[int] = attrs.field(repr=False, hash=False)
    """Entity's tier type."""

    tier: typing.Optional[enums.ItemTier] = attrs.field(repr=False)
    """The item tier hash as an enum if exists."""

    tier_name: undefined.UndefinedOr[str] = attrs.field(repr=False)
    """A string version of the item tier. i.e., `Legendery`"""

    type_name: undefined.UndefinedOr[str] = attrs.field(repr=False, hash=False)
    """Entity's type name. i.e., `Grenade Launcher`."""

    type_and_tier_name: undefined.UndefinedOr[str] = attrs.field(hash=False)
    """Entity's tier and type name combined, i.e., `Legendery Grenade Launcher`."""

    bucket_hash: typing.Optional[int] = attrs.field(repr=False, hash=False)
    """The entity's bucket type hash, None if it doesn't have one."""

    recovery_bucket_hash: typing.Optional[int] = attrs.field(repr=False)
    """If the item is picked up by the lost loot queue,
    this is the hash identifier for the DestinyInventoryBucketDefinition.
    """

    max_stack_size: typing.Optional[int] = attrs.field(repr=False)
    """The maximum quantity of this item that can exist in a stack."""

    stack_label: undefined.UndefinedOr[str] = attrs.field(repr=False)
    """If this string is populated, you can't have more than one stack with this label in a given inventory."""

    tooltip_notifications: list[str] = attrs.field(repr=False)
    """"""

    display_source: undefined.UndefinedOr[str] = attrs.field(hash=False, repr=False)
    """String telling you about how you can find the item."""

    emblem_objective_hash: typing.Optional[int] = attrs.field(repr=False)
    """If the item is an emblem that has a special Objective attached to it, This will be its hash."""

    isinstance_item: bool = attrs.field(repr=False)
    """If True, This item is instanced."""

    expiration_tooltip: undefined.UndefinedOr[str] = attrs.field(repr=False)
    """If the item expires while playing in an activity, we show a different message."""

    expire_in_orbit_message: undefined.UndefinedOr[str] = attrs.field(repr=False)
    """If the item expires in orbit, This message will be available."""

    suppress_expiration: typing.Optional[bool] = attrs.field(repr=False)
    """"""

    lore_hash: typing.Optional[int] = attrs.field(repr=False, hash=False, eq=False)
    """The entity's lore hash. Can be undefined if no lore hash found."""

    is_equippable: bool = attrs.field(repr=False)
    """True if the entity can be equipped or False."""

    summary_hash: typing.Optional[int] = attrs.field(repr=False, hash=False, eq=False)
    """Entity's summary hash."""

    about: undefined.UndefinedOr[str] = attrs.field(repr=True, hash=False, eq=False)
    """Entity's about. Originally this is the flavorText field but to make readable its renamed to about.."""

    allow_actions: bool = attrs.field(repr=False)
    """"""

    has_postmaster_effect: bool = attrs.field(repr=False)
    """Whether something will occur if you transfer this item from postmaster or not."""

    not_transferable: bool = attrs.field(repr=False)
    """If True, this item cannot be transferred, Otherwise it can."""

    category_hashes: collections.Sequence[int] = attrs.field(repr=False)
    """"""

    season_hash: typing.Optional[int] = attrs.field(repr=False)


@attrs.define(kw_only=True, weakref_slot=False)
class ObjectiveEntity(BaseEntity, Entity):
    """Represents a bungie inventory item entity.

    This derives from `DestinyObjectiveDefinition` definition.
    """

    # TODO: document these.

    unlock_value_hash: int = attrs.field()

    minimum_visibility: int = attrs.field()

    completion_value: int = attrs.field()

    scope: typedefs.IntAnd[GatingScope] = attrs.field()

    location_hash: int = attrs.field()

    allowed_negative_value: bool = attrs.field()

    allowed_value_change: bool = attrs.field()

    counting_downward: bool = attrs.field()

    display_only_objective: bool = attrs.field()

    value_style: typedefs.IntAnd[ValueUIStyle] = attrs.field()

    complete_value_style: typedefs.IntAnd[ValueUIStyle] = attrs.field()

    progress_value_style: typedefs.IntAnd[ValueUIStyle] = attrs.field()

    allow_over_completion: bool = attrs.field()

    show_value_style: typedefs.IntAnd[ValueUIStyle] = attrs.field()

    progress_description: str = attrs.field()

    perks: dict[str, int] = attrs.field()

    stats: dict[str, int] = attrs.field()


@attrs.define(kw_only=True, hash=True, weakref_slot=False)
class ActivityEntity(BaseEntity, Entity):
    """Represents a Bungie Activity definition and its entities.

    This derives from `DestinyActivityDefinition` definition.
    """

    release_icon: assets.MaybeImage = attrs.field(repr=False)
    """The release icon of this activity if it has one."""

    release_time: int = attrs.field()
    """The release time of this activity."""

    unlock_hash: int = attrs.field(repr=False)
    """The completion unlock hash of this activity."""

    light_level: int = attrs.field()
    """Activity's light level."""

    place: typing.Union[
        typedefs.IntAnd[enums.Place], typedefs.IntAnd[enums.Place]
    ] = attrs.field()
    """The place of this activity."""

    type_hash: int = attrs.field(repr=False)
    """The activity's type hash. This bounds to activity types such as Strikes, Crucible, Raids, etc."""

    tier: typedefs.IntAnd[activity.Diffculity] = attrs.field()
    """Activity's diffculity tier."""

    image: assets.MaybeImage = attrs.field(repr=False)
    """Activity's pgcr image."""

    rewards: typing.Optional[collections.Sequence[activity.Rewards]] = attrs.field()
    """A sequence of this activity's rewards. Returns `None` if not found."""

    modifiers: typing.Optional[collections.Sequence[int]] = attrs.field(repr=False)
    """A sequence of the activity's modifier hashes. Returns `None` if not found."""

    challenges: typing.Optional[
        collections.Sequence[activity.Challenges]
    ] = attrs.field(repr=False)
    """A sequence of the activity's challenges. Returns `None` if not found."""

    is_playlist: bool = attrs.field()
    """Whether this activity is present in a playlist or not."""

    unlock_strings: typing.Optional[collections.Sequence[str]] = attrs.field(repr=False)
    """An optional status string that could be conditionally displayed about an activity"""

    inherits_free_room: bool = attrs.field(repr=False)
    """"""

    playlist_activities: typing.Optional[
        collections.Sequence[PlaylistActivityEntity]
    ] = attrs.field(repr=False)
    """Represents all of the possible activities that could be played in the Playlist,
    along with information that we can use to determine if they are active at the present time.
    """

    matchmaking: activity.Matchmaking = attrs.field(repr=False)
    """Information about matchmaking for this activity."""

    guided_game: typing.Optional[activity.GuidedGame] = attrs.field(repr=False)
    """Information about activity's guided game mode, If exists otherwise `None`."""

    mode: typing.Optional[typedefs.IntAnd[enums.GameMode]] = attrs.field(repr=False)
    """If this activity had an activity mode directly defined on it, this will be the hash of that mode."""

    mode_hash: typing.Optional[int] = attrs.field(repr=False)
    """If the activity had an activity mode directly defined on it, this will be the enum value of that mode."""

    mode_hashes: collections.Sequence[typedefs.IntAnd[enums.GameMode]] = attrs.field(
        repr=False
    )
    """The hash identifiers for Activity Modes relevant to this entry."""

    mode_types: collections.Sequence[typedefs.IntAnd[enums.GameMode]] = attrs.field(
        repr=False
    )
    """A sequence of the activity gamemode types."""

    loadouts: collections.Sequence[int] = attrs.field(repr=False)
    """The set of all possible loadout requirements that could be active for this activity.

    Only one will be active at any given time. and you can discover which one through
    activity-associated data such as Milestones that have activity info on them.
    """

    is_pvp: bool = attrs.field(repr=False)
    """Whether the activity is PvP or not."""

    phase_hashes: collections.Sequence[int] = attrs.field()
    """The list of phases or points of entry into an activity,
    along with information we can use to determine their gating and availability.
    """

    locations: collections.Collection[activity.Location] = attrs.field(repr=False)
    """A collection of location mappings affected by this activity."""


@attrs.define(kw_only=True, hash=True, weakref_slot=False)
class PlaylistActivityEntity:
    """Represents an activity playlists definition/entity.

    Derives `DestinyActivityPlaylistItemDefinition`
    """

    hash: int = attrs.field()
    """The hash identifier of the Activity that can be played."""

    mode_hash: typing.Optional[int] = attrs.field()
    """If this activity had an activity mode directly defined on it, this will be the hash of that mode."""

    mode: typing.Optional[typedefs.IntAnd[enums.GameMode]] = attrs.field()
    """If the activity had an activity mode directly defined on it, this will be the enum value of that mode."""

    mode_hashes: collections.Sequence[int] = attrs.field()
    """The hash identifiers for Activity Modes relevant to this entry."""

    mode_types: collections.Sequence[typedefs.IntAnd[enums.GameMode]] = attrs.field()
    """A sequence of the activity gamemode types."""

    # TODO: Implement a REST method for this.
    async def fetch_self(self) -> ActivityEntity:
        """Fetch the definition of this activivy."""
        raise NotImplementedError
