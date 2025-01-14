# -*- coding: utf-8 -*-

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

"""Standard implementation of Bungie Character and entities."""

from __future__ import annotations

__all__ = (
    "Character",
    "Loadout",
    "LoadoutItem",
    "Dye",
    "MinimalEquipments",
    "RenderedData",
    "CustomizationOptions",
    "CharacterProgression",
)

import typing

import attrs

from aiobungie import url

if typing.TYPE_CHECKING:
    import collections.abc as collections
    import datetime

    from aiobungie import builders
    from aiobungie.crates import milestones as milestones_
    from aiobungie.crates import progressions as progressions_
    from aiobungie.crates import records, season
    from aiobungie.internal import enums


@attrs.frozen(kw_only=True)
class Loadout:
    """Represents a character's loadout component in Destiny 2."""

    color_hash: int
    icon_hash: int
    name_hash: int
    items: collections.Sequence[LoadoutItem]
    """A sequence of this loadout's items."""


@attrs.frozen(kw_only=True)
class LoadoutItem:
    """Represents a single item in a character's loadout in Destiny 2."""

    instance_id: int = attrs.field(converter=int)
    """The item instance ID."""
    plug_hashes: collections.Sequence[int]
    """A sequence of this item's plug hashes."""


@attrs.frozen(kw_only=True)
class Dye:
    """Represents dyes rendered on a Destiny character."""

    channel_hash: int
    """The hash of the channel."""

    dye_hash: int
    """The dye's hash."""


@attrs.frozen(kw_only=True, repr=False)
class CustomizationOptions:
    """Raw data represents a character's customization options."""

    personality: int
    face: int
    skin_color: int
    lip_color: int
    eye_color: int
    hair_colors: collections.Sequence[int]
    feature_colors: collections.Sequence[int]
    decal_color: int
    wear_helmet: bool
    hair_index: int
    feature_index: int
    decal_index: int


@attrs.frozen(kw_only=True)
class MinimalEquipments:
    """Minimal information about a character's equipped items.

    This holds the items hash and collection of dyes.

    This is specifically used in CharacterRenderData profile component to render
    3D character object.
    """

    item_hash: int
    """The equipped items's hash."""

    dyes: collections.Collection[Dye]
    """An collection of the item rendering dyes"""


@attrs.frozen(kw_only=True)
class RenderedData:
    """Represents a character's rendered data profile component."""

    custom_dyes: collections.Collection[Dye]
    """A collection of the character's custom dyes."""

    customization: CustomizationOptions
    """Data about what character customization options you picked."""

    equipment: collections.Sequence[MinimalEquipments]
    """A sequence of minimal view of this character's equipment."""


@attrs.frozen(kw_only=True)
class CharacterProgression:
    """Represents a character progression profile component."""

    progressions: collections.Mapping[int, progressions_.Progression]
    """A Mapping from progression's hash to progression object."""

    factions: collections.Mapping[int, progressions_.Factions]
    """A Mapping from progression faction's hash to its faction object."""

    milestones: collections.Mapping[int, milestones_.Milestone]
    """A Mapping from the milestone's hash to a milestone object."""

    checklists: collections.Mapping[int, collections.Mapping[int, bool]]

    seasonal_artifact: season.CharacterScopedArtifact
    """Data related to your progress on the current season's artifact that can vary per character."""

    uninstanced_item_objectives: collections.Mapping[
        int, collections.Sequence[records.Objective]
    ]
    """A Mapping from an uninstanced inventory item hash to a sequence of its objectives."""


@attrs.frozen(kw_only=True)
class Character:
    """Base properties of a Destiny 2 character component."""

    id: int
    """This character's id"""

    member_id: int
    """The membership ID that is bound to this character."""

    member_type: enums.MembershipType
    """The membership type that is bound to this character."""

    light: int
    """This character's light, currently known as power level."""

    gender: enums.Gender
    """This character's gender. i.e., Male, Female."""

    race: enums.Race
    """This character's race, i.e., EXO, Awoken, etc."""

    emblem: builders.Image | None
    """If this character has an emblem equipped and isn't undefined. This field will be populated."""

    emblem_icon: builders.Image | None
    """If this character has an emblem equipped and isn't undefined. This field will be populated with its icon."""

    emblem_hash: int | None
    """If this character has an emblem equipped and isn't undefined. This field will be populated with its hash."""

    emblem_color: tuple[int, int, int, int]
    """A shortcut for getting the background color of the user's currently equipped emblem without having to do a DestinyInventoryItemDefinition lookup.

    The tuple contains 4 integers represented as `(R, G, B, A)`
    """

    last_played: datetime.datetime
    """The last date that the user played Destiny on this character."""

    minutes_played_this_session: int
    """If the user is currently playing, this is how long they've been playing. """

    total_played_time: int
    """Character's total played time in minutes."""

    class_type: enums.Class
    """This character's class."""

    title_hash: int | None
    """If this character has a title equipped, you can use this hash to get its information from the manifest.

    The manifest definition is `DestinyRecordDefinition`
    """

    level: int
    """The base level of this character."""

    percent_to_next_level: float
    """A number between 0 and 100, indicating the whole and fractional % remaining to get to the next character level."""

    stats: collections.Mapping[enums.Stat, int]
    """A mapping from the character stats detail to its value.

    This include stuff like `Mobility`, `Recovery`, `Intellect`, etc.

    Example
    -------
    ```py
    for stat_name, stat_value in stats.items():
        print(stat_name.name.title(), stat_value)
    ```
    """

    @property
    def power_level(self) -> int:
        """An alias to `Character.light`"""
        return self.light

    @property
    def url(self) -> str:
        """A URL of the character at Bungie.net."""
        return f"{url.BASE}/en/Gear/{int(self.member_type)}/{self.member_id}/{self.id}"
