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

"""Standard implementation of Bungie items."""

from __future__ import annotations

__all__: tuple[str, ...] = (
    "ItemPerk",
    "ItemInstance",
    "ItemEnergy",
    "ItemStatsView",
    "PlugItemState",
    "ItemSocket",
    "ItemPerk",
)

import typing

import attrs

from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    import collections.abc as collections

    from aiobungie.internal import assets


class ItemBreakerType(enums.IntEnum):
    """An enum for Destiny2 item breaker types."""

    NONE = 0
    SHIELD_PIERCING = 1
    DISRUPTION = 2
    STAGGER = 3

    OVERLOAD = DISRUPTION
    """An alias to SHIELD_PIERCING"""
    UNSTOPABLE = STAGGER
    """An alias to STAGGER"""
    ANTI_BARRIER = SHIELD_PIERCING
    """An alias to SHIELD_PIERCING."""


class ItemEnergyType(enums.IntEnum):
    """An enum for Destiny 2 item energy types for Armor 2.0, Ghosts 2.0 and stasis subclasses."""

    ANY = 0
    ARC = 1
    SOLAR = 2
    VOID = 3
    GHOST = 4
    SUBCLASS = 5
    STASIS = 6


@attrs.define(hash=True, kw_only=True, weakref_slot=False)
class ItemSocket:
    """Information found in a profile item sockets component."""

    plug_hash: typing.Optional[int] = attrs.field(hash=True)
    """The plug item hash."""

    is_enabled: bool = attrs.field(hash=False)
    """Whether this plug is enabled or not."""

    is_visible: typing.Optional[bool] = attrs.field(hash=False)
    """Either the plug is visible or not."""

    enable_fail_indexes: typing.Optional[list[int]] = attrs.field(
        repr=False, hash=False
    )
    """If a plug is inserted but not enabled,
    this field will be available with indexes into the plug item definition.
    """


@attrs.define(hash=True, kw_only=True, weakref_slot=False)
class PlugItemState:
    """Information about a plug item's state."""

    item_hash: typing.Optional[int]
    """The hash of this item."""

    can_insert: bool
    """Whether this item can be plugged into a socket or not. """

    is_enabled: bool
    """Whether this item is enabled or not."""

    insert_fail_indexes: typing.Optional[list[int]]

    enable_fail_indexes: typing.Optional[list[int]]
    """If a plug is inserted but not enabled,
    this field will be available with indexes into the plug item definition.
    """


@attrs.define(kw_only=True)
class ItemPerk:
    """Represents a Destiny 2 perk."""

    hash: typing.Optional[int]
    """Perk's hash."""

    icon: assets.Image
    """Perk's icon."""

    is_active: bool
    """Either the perk is active or not."""

    is_visible: bool
    """Either the perk is visible or not."""


@attrs.define(kw_only=True)
class ItemEnergy:
    """Represents a Destiny 2 item instance energy."""

    hash: typing.Optional[int]
    """The hash of the energy,"""

    type: ItemEnergyType
    """The energy type."""

    capacity: int
    """The total capcacity of energy that the item currently has."""

    used_energy: int
    """The amount if energy in use by inserted plugs."""

    unused_energy: int
    """The amount of energy still available for inserting new plugs."""


@attrs.define(kw_only=True)
class ItemStatsView:
    """A view of a Destiny 2 item stats."""

    stat_hash: typing.Optional[int]
    """The stat hash if set."""

    value: typing.Optional[int]
    """The value of this stat if set."""


@attrs.define(kw_only=True)
class ItemInstance:
    """Represents an instance item for a character."""

    damage_type: enums.DamageType
    """The item's damage type."""

    damage_type_hash: typing.Optional[int]
    """The hash of the item damage type."""

    primary_stat: typing.Optional[ItemStatsView]
    """The item's primary stats if has one."""

    item_level: int
    """The level of this item."""

    quality: int
    """The quality of this item."""

    is_equipped: bool
    """Whether the item is equipped to the character or not."""

    can_equip: bool
    """Whether this item can be equipped or not."""

    equip_required_level: int
    """The required level to be able to equip this item."""

    required_equip_unlock_hashes: typing.Optional[collections.Collection[int]]
    """If available, A collections of hash flags mapped to a its definitions
    needed in oreder to equip this item will be returned.
    """

    cant_equip_reason: int
    """If the item can't be equipped, This will be the reason why."""

    breaker_type: typing.Optional[ItemBreakerType]
    """If them item has a breaker type, this field will be available."""

    breaker_type_hash: typing.Optional[int]
    """If them item has a breaker type hash, this field will be available."""

    energy: typing.Optional[ItemEnergy]