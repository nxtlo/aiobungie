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
    "GatingScope",
    "ValueUIStyle",
    "BaseEntity",
    "ActivityEntity",
    "PlaylistActivityEntity",
)

import abc
import typing

import attr

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


@attr.mutable(kw_only=True, weakref_slot=False)
class BaseEntity(Entity):
    """Concerate Bungie entity implementation."""

    # These are not attribs on purpose.
    # We dont want to redefine them again in the actual entity
    # implementation.

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    hash: int
    """Entity's hash."""

    index: int
    """The entity's index."""

    name: undefined.UndefinedOr[str]
    """Entity's name."""

    description: undefined.UndefinedOr[str]
    """Entity's description"""

    icon: assets.MaybeImage
    """Entity's icon."""

    has_icon: bool
    """A boolean that returns True if the entity has an icon."""


@attr.define(kw_only=True, hash=False, weakref_slot=False)
class InventoryEntity(BaseEntity, Entity):
    """Represents a bungie inventory item entity.

    This derives from `DestinyInventoryItemDefinition` definition.
    """

    type: undefined.UndefinedOr[enums.Item] = attr.field(repr=True, hash=False)
    """Entity's type. Can be undefined if nothing was found."""

    type_name: undefined.UndefinedOr[str] = attr.field(repr=True, hash=False, eq=False)
    """Entity's type name. i.e., `Grenade Launcher`"""

    water_mark: typing.Optional[assets.Image] = attr.field(
        repr=False, hash=False, eq=False
    )
    """Entity's water mark."""

    tier: typing.Optional[enums.ItemTier] = attr.field(repr=True, hash=False, eq=False)
    """Entity's "tier."""

    tier_name: undefined.UndefinedOr[str] = attr.field(repr=False, eq=False)
    """A string version of the item tier."""

    bucket_type: typing.Optional[int] = attr.field(repr=True, hash=False, eq=False)
    """The entity's bucket type, None if unknown"""

    stats: typing.Optional[dict[str, typing.Any]] = attr.field(
        repr=False, hash=False, eq=False
    )
    """Entity's stats. this currently returns a dict object
    of the stats.
    """

    ammo_type: typing.Optional[enums.AmmoType] = attr.field(
        repr=False, hash=False, eq=False
    )
    """Entity's ammo type if it was a wepon, otherwise it will return None"""

    lore_hash: typing.Optional[int] = attr.field(repr=False, hash=False, eq=False)
    """The entity's lore hash. Can be undefined if no lore hash found."""

    item_class: typing.Optional[enums.Class] = attr.field(
        repr=False, hash=False, eq=False
    )
    """The entity's class type."""

    sub_type: undefined.UndefinedOr[enums.Item] = attr.field(
        repr=False, hash=False, eq=False
    )
    """The subtype of the entity. A type is a weapon or armor.
    A subtype is a handcannonn or leg armor for an example.
    """

    is_equippable: undefined.UndefinedOr[bool] = attr.field(
        repr=False, hash=False, eq=False
    )
    """True if the entity can be equipped or False."""

    summary_hash: typing.Optional[int] = attr.field(repr=False, hash=False, eq=False)
    """Entity's summary hash."""

    damage: undefined.UndefinedOr[enums.DamageType] = attr.field(
        repr=False, hash=False, eq=False
    )
    """Entity's damage type. Only works for weapons."""

    about: undefined.UndefinedOr[str] = attr.field(repr=True, hash=False, eq=False)
    """Entity's about."""

    banner: typing.Optional[assets.Image] = attr.field(repr=False, eq=False, hash=False)
    """Entity's banner."""


@attr.define(kw_only=True, weakref_slot=False)
class ObjectiveEntity(BaseEntity, Entity):
    """Represents a bungie inventory item entity.

    This derives from `DestinyObjectiveDefinition` definition.
    """

    # TODO: document these.

    unlock_value_hash: int = attr.field()

    minimum_visibility: int = attr.field()

    completion_value: int = attr.field()

    scope: typedefs.IntAnd[GatingScope] = attr.field()

    location_hash: int = attr.field()

    allowed_negative_value: bool = attr.field()

    allowed_value_change: bool = attr.field()

    counting_downward: bool = attr.field()

    display_only_objective: bool = attr.field()

    value_style: typedefs.IntAnd[ValueUIStyle] = attr.field()

    complete_value_style: typedefs.IntAnd[ValueUIStyle] = attr.field()

    progress_value_style: typedefs.IntAnd[ValueUIStyle] = attr.field()

    allow_over_completion: bool = attr.field()

    show_value_style: typedefs.IntAnd[ValueUIStyle] = attr.field()

    progress_description: str = attr.field()

    perks: dict[str, int] = attr.field()

    stats: dict[str, int] = attr.field()


@attr.define(kw_only=True, hash=True, weakref_slot=False)
class ActivityEntity(BaseEntity, Entity):
    """Represents a Bungie Activity definition and its entities.

    This derives from `DestinyActivityDefinition` definition.
    """

    release_icon: assets.MaybeImage = attr.field(repr=False)
    """The release icon of this activity if it has one."""

    release_time: int = attr.field()
    """The release time of this activity."""

    unlock_hash: int = attr.field(repr=False)
    """The completion unlock hash of this activity."""

    light_level: int = attr.field()
    """Activity's light level."""

    place: typing.Union[
        typedefs.IntAnd[enums.Place], typedefs.IntAnd[enums.Place]
    ] = attr.field()
    """The place of this activity."""

    type_hash: int = attr.field(repr=False)
    """The activity's type hash. This bounds to activity types such as Strikes, Crucible, Raids, etc."""

    tier: typedefs.IntAnd[activity.Diffculity] = attr.field()
    """Activity's diffculity tier."""

    image: assets.MaybeImage = attr.field(repr=False)
    """Activity's pgcr image."""

    rewards: typing.Optional[collections.Sequence[activity.Rewards]] = attr.field()
    """A sequence of this activity's rewards. Returns `None` if not found."""

    modifiers: typing.Optional[collections.Sequence[int]] = attr.field(repr=False)
    """A sequence of the activity's modifier hashes. Returns `None` if not found."""

    challenges: typing.Optional[collections.Sequence[activity.Challenges]] = attr.field(
        repr=False
    )
    """A sequence of the activity's challenges. Returns `None` if not found."""

    is_playlist: bool = attr.field()
    """Whether this activity is present in a playlist or not."""

    unlock_strings: typing.Optional[collections.Sequence[str]] = attr.field(repr=False)
    """An optional status string that could be conditionally displayed about an activity"""

    inherits_free_room: bool = attr.field(repr=False)
    """"""

    playlist_activities: typing.Optional[
        collections.Sequence[PlaylistActivityEntity]
    ] = attr.field(repr=False)
    """Represents all of the possible activities that could be played in the Playlist,
    along with information that we can use to determine if they are active at the present time.
    """

    matchmaking: activity.Matchmaking = attr.field(repr=False)
    """Information about matchmaking for this activity."""

    guided_game: typing.Optional[activity.GuidedGame] = attr.field(repr=False)
    """Information about activity's guided game mode, If exists otherwise `None`."""

    mode: typing.Optional[typedefs.IntAnd[enums.GameMode]] = attr.field(repr=False)
    """If this activity had an activity mode directly defined on it, this will be the hash of that mode."""

    mode_hash: typing.Optional[int] = attr.field(repr=False)
    """If the activity had an activity mode directly defined on it, this will be the enum value of that mode."""

    mode_hashes: collections.Sequence[typedefs.IntAnd[enums.GameMode]] = attr.field(
        repr=False
    )
    """The hash identifiers for Activity Modes relevant to this entry."""

    mode_types: collections.Sequence[typedefs.IntAnd[enums.GameMode]] = attr.field(
        repr=False
    )
    """A sequence of the activity gamemode types."""

    loadouts: collections.Sequence[int] = attr.field(repr=False)
    """The set of all possible loadout requirements that could be active for this activity.

    Only one will be active at any given time. and you can discover which one through
    activity-associated data such as Milestones that have activity info on them.
    """

    is_pvp: bool = attr.field(repr=False)
    """Whether the activity is PvP or not."""

    phase_hashes: collections.Sequence[int] = attr.field()
    """The list of phases or points of entry into an activity,
    along with information we can use to determine their gating and availability.
    """

    locations: collections.Collection[activity.Location] = attr.field(repr=False)
    """A collection of location mappings affected by this activity."""


@attr.define(kw_only=True, hash=True, weakref_slot=False)
class PlaylistActivityEntity:
    """Represents an activity playlists definition/entity.

    Derives `DestinyActivityPlaylistItemDefinition`
    """

    hash: int = attr.field()
    """The hash identifier of the Activity that can be played."""

    mode_hash: typing.Optional[int] = attr.field()
    """If this activity had an activity mode directly defined on it, this will be the hash of that mode."""

    mode: typing.Optional[typedefs.IntAnd[enums.GameMode]] = attr.field()
    """If the activity had an activity mode directly defined on it, this will be the enum value of that mode."""

    mode_hashes: collections.Sequence[int] = attr.field()
    """The hash identifiers for Activity Modes relevant to this entry."""

    mode_types: collections.Sequence[typedefs.IntAnd[enums.GameMode]] = attr.field()
    """A sequence of the activity gamemode types."""

    async def fetch_self(self) -> ActivityEntity:
        """Fetch the definition of this activivy."""
