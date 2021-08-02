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

"""A basic bungie entity definition implementation."""

from __future__ import annotations

__all__: typing.Sequence[str] = ["PartialEntity", "Entity"]

import abc
import typing
import attr

from aiobungie.internal import assets, enums, impl


@attr.s(kw_only=True, hash=True, weakref_slot=False, slots=True, init=True, eq=True)
class PartialEntity(abc.ABC):

    @property
    @abc.abstractmethod
    def app(self) -> impl.RESTful:
        """A client that we may use to make rest calls."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Entity's name"""

    @property
    @abc.abstractmethod
    def icon(self) -> assets.Image:
        """Entity's icon"""

    @property
    @abc.abstractmethod
    def banner(self) -> assets.Image:
        """Entity's large banner."""

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
    def type_name(self) -> str:
        """Entity's type name. i.e., `Grenade Launcher`"""

    @property
    @abc.abstractmethod
    def water_mark(self) -> typing.Optional[assets.Image]:
        """Entity's water mark."""

    @property
    @abc.abstractmethod
    def tier(self) -> enums.ItemTier:
        """Entity's "tier."""

    @property
    @abc.abstractmethod
    def tier_name(self) -> str:
        """A `builtins.str` version of the entity's tier and name."""

    @property
    @abc.abstractmethod
    def type(self) -> typing.Optional[enums.Item]:
        """The entity's type, None if unknown"""

    @property
    @abc.abstractmethod
    def bucket_type(self) -> typing.Optional[enums.Item]:
        """Entity's bucket type."""

    @property
    @abc.abstractmethod
    def stats(self) -> typing.Dict[str, typing.Any]:  # TODO: Serialize this.
        """Entity's stats. this currently returns a dict object
        of the stats.
        """

    @property
    @abc.abstractmethod
    def ammo_type(self) -> typing.Optional[enums.AmmoType]:
        """Entity's ammo type if it was a wepon, otherwise it will return None"""

    @property
    @abc.abstractmethod
    def lore_hash(self) -> int:
        """The entity's lore hash"""

    @property
    @abc.abstractmethod
    def item_class(self) -> enums.Class:
        """The entity's class type."""

    @property
    @abc.abstractmethod
    def sub_type(self) -> typing.Optional[enums.Item]:
        """The subtype of the entity. A type is a weapon or armor.
        A subtype is a handcannonn or leg armor for an example.
        """

    @property
    @abc.abstractmethod
    def is_equippable(self) -> bool:
        """True if the entity can be equipped or False."""

    @property
    @abc.abstractmethod
    def summary_hash(self) -> int:
        """Entity's summary hash."""

    @property
    @abc.abstractmethod
    def damage(self) -> typing.Optional[enums.DamageType]:
        """Entity's damage type. Only works for weapons."""

    @property
    @abc.abstractmethod
    def about(self) -> str:
        """Entity's about. you probably wanna use this instaed `Entity.description`"""


@attr.s(kw_only=True, hash=True, weakref_slot=False, slots=True, init=True, eq=True)
class Entity(PartialEntity):
    """A concrate implementation of a Bungie Item Definition Entity."""

    hash: int = attr.ib(repr=True, hash=True, eq=True)
    """Entity's hash."""

    index: int = attr.ib(repr=True, hash=False, eq=False)
    """Entity's index."""

    app: impl.RESTful = attr.ib(repr=False, hash=False, eq=False)
    """A client that we may use to make rest calls."""

    name: str = attr.ib(repr=True, hash=False, eq=False)
    """Entity's name"""

    icon: assets.Image = attr.ib(repr=False, hash=False, eq=False)
    """Entity's icon"""

    has_icon: bool = attr.ib(repr=False, hash=False, eq=False)
    """A boolean that returns True if the entity has an icon."""

    description: str = attr.ib(repr=True, hash=False, eq=False)
    """Entity's description. most entities don't use this so consider using
    `Entity.about` if you found an empty string.
    """

    type: typing.Optional[enums.Item] = attr.ib(repr=True, hash=False)
    """Entity's type."""

    type_name: str = attr.ib(repr=True, hash=False, eq=False)
    """Entity's type name. i.e., `Grenade Launcher`"""

    water_mark: typing.Optional[assets.Image] = attr.ib(
        repr=False, hash=False, eq=False
    )
    """Entity's water mark."""

    tier: enums.ItemTier = attr.ib(repr=True, hash=False, eq=False)
    """Entity's "tier."""

    tier_name: str = attr.ib(repr=False, eq=False)
    """A string version of the item tier."""

    bucket_type: typing.Optional[enums.Item] = attr.ib(repr=True, hash=False, eq=False)
    """The entity's bucket type, None if unknown"""

    stats: typing.Dict[str, typing.Any] = attr.ib(repr=False, hash=False, eq=False)
    """Entity's stats. this currently returns a dict object
    of the stats.
    """

    ammo_type: typing.Optional[enums.AmmoType] = attr.ib(
        repr=False, hash=False, eq=False
    )
    """Entity's ammo type if it was a wepon, otherwise it will return None"""

    lore_hash: int = attr.ib(repr=False, hash=False, eq=False)
    """The entity's lore hash"""

    item_class: enums.Class = attr.ib(repr=False, hash=False, eq=False)
    """The entity's class type."""

    sub_type: typing.Optional[enums.Item] = attr.ib(repr=False, hash=False, eq=False)
    """The subtype of the entity. A type is a weapon or armor.
    A subtype is a handcannonn or leg armor for an example.
    """

    is_equippable: bool = attr.ib(repr=False, hash=False, eq=False)
    """True if the entity can be equipped or False."""

    summary_hash: int = attr.ib(repr=False, hash=False, eq=False)
    """Entity's summary hash."""

    damage: typing.Optional[enums.DamageType] = attr.ib(
        repr=False, hash=False, eq=False
    )
    """Entity's damage type. Only works for weapons."""

    about: str = attr.ib(repr=True, hash=False, eq=False)
    """Entity's about."""

    banner: assets.Image = attr.ib(repr=False, eq=False, hash=False)
