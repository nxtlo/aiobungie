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
    from aiobungie.crates import records
    from aiobungie.crates import season
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
    """A Destiny 2 character."""

    id: int
    """Character's id"""

    member_id: int
    """The character's member id."""

    member_type: enums.MembershipType
    """The character's membership type."""

    light: int
    """Character's light"""

    gender: enums.Gender
    """Character's gender"""

    race: enums.Race
    """Character's race"""

    emblem: builders.Image | None
    """Character's emblem, If included."""

    emblem_icon: builders.Image | None
    """Character's emblem icon, If included."""

    emblem_hash: int | None
    """Character's emblem hash, If included."""

    last_played: datetime.datetime
    """Character's last played date."""

    total_played_time: int
    """Character's total played time in seconds."""

    class_type: enums.Class
    """Character's class."""

    title_hash: int | None
    """Character's equipped title hash."""

    level: int
    """Character's base level."""

    stats: collections.Mapping[enums.Stat, int]
    """A mapping of the character stats and its level."""

    @property
    def power_level(self) -> int:
        """An alias to the player's light level."""
        return self.light

    @property
    def url(self) -> str:
        """A URL of the character at Bungie.net."""
        return f"{url.BASE}/en/Gear/{int(self.member_type)}/{self.member_id}/{self.id}"
