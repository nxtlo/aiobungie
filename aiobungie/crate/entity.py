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

"""Bungie entity definitions implementation.

This is still not fully implemented and you may experince bugs.
This will include all Bungie Definitions.
"""

from __future__ import annotations

__all__: typing.Sequence[str] = ["InventoryEntity", "Entity"]

import abc
import typing

import attr

from aiobungie.internal import assets
from aiobungie.internal import enums
from aiobungie.internal import impl


@attr.s(kw_only=True, hash=True, weakref_slot=False, slots=True, init=True, eq=True)
class Entity(abc.ABC):
    """An interface of a Bungie Definition Entity.

    This is the main entity which all other entities should inherit from.
    it holds core information that all bungie entities has.
    """

    @property
    @abc.abstractmethod
    def net(self) -> impl.Netrunner:
        """A network state used for making external requests."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Entity's name"""

    @property
    @abc.abstractmethod
    def icon(self) -> typing.Optional[assets.Image]:
        """An optional entity's icon if its filled."""

    @property
    @abc.abstractmethod
    def has_icon(self) -> bool:
        """A boolean that returns True if the entity has an icon."""

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """Entity's description"""

    @property
    @abc.abstractmethod
    def index(self) -> int:
        """The entity's index."""

    @property
    @abc.abstractmethod
    def hash(self) -> int:
        """Entity's hash."""

    @property
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """Returns an instance of the entity as a dict"""
        return attr.asdict(self)

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return self.hash


@attr.s(kw_only=True, hash=True, weakref_slot=False, slots=True, init=True, eq=True)
class InventoryEntity(Entity):
    """Represents a bungie inventory item entity.

    This derives from `DestinyInventoryItemDefinition` definition.
    """

    net: impl.Netrunner = attr.field(repr=False, hash=False, eq=False)
    """A network state used for making external requests."""

    hash: int = attr.field(repr=True, hash=True, eq=True)
    """Entity's hash."""

    index: int = attr.field(repr=True, hash=False, eq=False)
    """Entity's index."""

    name: str = attr.field(repr=True, hash=False, eq=False)
    """Entity's name"""

    description: str = attr.field(repr=True)
    """Entity's description."""

    icon: typing.Optional[assets.Image] = attr.field(repr=False, hash=False, eq=False)
    """Entity's icon"""

    has_icon: bool = attr.field(repr=False, hash=False, eq=False)
    """A boolean that returns True if the entity has an icon."""

    type: typing.Optional[enums.Item] = attr.field(repr=True, hash=False)
    """Entity's type."""

    type_name: typing.Optional[str] = attr.field(repr=True, hash=False, eq=False)
    """Entity's type name. i.e., `Grenade Launcher`"""

    water_mark: typing.Optional[assets.Image] = attr.field(
        repr=False, hash=False, eq=False
    )
    """Entity's water mark."""

    tier: typing.Optional[enums.ItemTier] = attr.field(repr=True, hash=False, eq=False)
    """Entity's "tier."""

    tier_name: typing.Optional[str] = attr.field(repr=False, eq=False)
    """A string version of the item tier."""

    bucket_type: typing.Optional[int] = attr.field(repr=True, hash=False, eq=False)
    """The entity's bucket type, None if unknown"""

    stats: typing.Optional[typing.Dict[str, typing.Any]] = attr.field(
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
    """The entity's lore hash"""

    item_class: typing.Optional[enums.Class] = attr.field(
        repr=False, hash=False, eq=False
    )
    """The entity's class type."""

    sub_type: typing.Optional[enums.Item] = attr.field(repr=False, hash=False, eq=False)
    """The subtype of the entity. A type is a weapon or armor.
    A subtype is a handcannonn or leg armor for an example.
    """

    is_equippable: typing.Optional[bool] = attr.field(repr=False, hash=False, eq=False)
    """True if the entity can be equipped or False."""

    summary_hash: typing.Optional[int] = attr.field(repr=False, hash=False, eq=False)
    """Entity's summary hash."""

    damage: typing.Optional[enums.DamageType] = attr.field(
        repr=False, hash=False, eq=False
    )
    """Entity's damage type. Only works for weapons."""

    about: typing.Optional[str] = attr.field(repr=True, hash=False, eq=False)
    """Entity's about."""

    banner: typing.Optional[assets.Image] = attr.field(repr=False, eq=False, hash=False)
    """Entity's banner."""
