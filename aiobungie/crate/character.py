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

"""Basic Implementation of a Bungie Character."""

from __future__ import annotations

__all__ = ("CharacterComponent", "Character")

import abc
import datetime
import typing

import attr

from aiobungie import url
from aiobungie.internal import Image
from aiobungie.internal import enums


class CharacterComponent(abc.ABC):
    """An interface for a Bungie character component."""

    __slots__: typing.Sequence[str] = ()

    @property
    @abc.abstractmethod
    def member_type(self) -> enums.MembershipType:
        """The character's membership type."""

    @property
    @abc.abstractmethod
    def member_id(self) -> int:
        """The profile's member id."""

    @property
    @abc.abstractmethod
    def id(self) -> int:
        """The character's member id."""

    @property
    @abc.abstractmethod
    def light(self) -> int:
        """The character's light."""

    @property
    @abc.abstractmethod
    def stats(self) -> dict[int, int]:
        """The character's stats."""

    @property
    @abc.abstractmethod
    def url(self) -> str:
        """The character's url at bungie.net."""

    @property
    @abc.abstractmethod
    def emblem(self) -> Image:
        """The character's current equipped emblem."""

    @property
    @abc.abstractmethod
    def last_played(self) -> datetime.datetime:
        """The character's last played time."""

    @property
    @abc.abstractmethod
    def emblem_icon(self) -> Image:
        """The character's current equipped emblem icon."""

    @property
    @abc.abstractmethod
    def emblem_hash(self) -> int:
        """The character's current equipped emblem hash."""

    @property
    @abc.abstractmethod
    def race(self) -> enums.Race:
        """The character's race."""

    @property
    @abc.abstractmethod
    def gender(self) -> enums.Gender:
        """The character's gender."""

    @property
    @abc.abstractmethod
    def total_played_time(self) -> str:
        """Character's total played time in hours."""

    @property
    @abc.abstractmethod
    def class_type(self) -> enums.Class:
        """The character's class."""

    @property
    @abc.abstractmethod
    def title_hash(self) -> typing.Optional[int]:
        """
        The character's title hash.
        This is Optional and can be None if no title was found.
        """

    async def equip(self, item: int, /) -> None:
        """Equip an item to this character.

        This requires the OAuth2: MoveEquipDestinyItems scope.
        Also You must have a valid Destiny account, and either be
        in a social space, in orbit or offline.

        Parameters
        ----------
        item: `builtins.int`
            The item id you want to equip for this character.

        Returns
        -------
        `builtins.None`.

        Raises
        ------
        `NotImplementedError`
            This endpoint is currently not implemented.
        """

        # Required params:
        # POST request.
        # itemId: item,
        # characterId: self,
        # membershipType: int(self.member_type)

        raise NotImplementedError

    async def equip_items(self, items: typing.List[int], /) -> None:
        """Equip multiple items to this character.

        This requires the OAuth2: MoveEquipDestinyItems scope.
        Also You must have a valid Destiny account, and either be
        in a social space, in orbit or offline.

        Parameters
        ----------
        items: `typing.List[builtins.int]`
            A list of item ids you want to equip for this character.

        Returns
        -------
        `builtins.None`.

        Raises
        ------
        `NotImplementedError`
            This endpoint is currently not implemented.
        """

        # Required params:
        # POST request.
        # items: List[items],
        # characterId: self,
        # membershipType: int(self.member_type)

        raise NotImplementedError


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class Character(CharacterComponent):
    """An implementation for a Bungie character."""

    id: int = attr.field(hash=True, repr=True)
    """Character's id"""

    member_id: int = attr.field(hash=True, repr=True)
    """The character's member id."""

    member_type: enums.MembershipType = attr.field(repr=True, hash=False)
    """The character's memberhip type."""

    light: int = attr.field(repr=True, hash=False)
    """Character's light"""

    gender: enums.Gender = attr.field(repr=True, hash=False)
    """Character's gender"""

    race: enums.Race = attr.field(repr=True, hash=False)
    """Character's race"""

    emblem: Image = attr.field(repr=False, hash=False)
    """Character's emblem"""

    emblem_icon: Image = attr.field(repr=False, hash=False)
    """Character's emblem icon"""

    emblem_hash: int = attr.field(repr=False, hash=False)
    """Character's emblem hash."""

    last_played: datetime.datetime = attr.field(repr=False, hash=False)
    """Character's last played date."""

    total_played_time: str = attr.field(repr=False, hash=False)
    """Character's total plyed time minutes."""

    class_type: enums.Class = attr.field(repr=True, hash=False)
    """Character's class."""

    title_hash: typing.Optional[int] = attr.field(repr=True, hash=False)
    """Character's equipped title hash."""

    level: int = attr.field(repr=False, hash=False)
    """Character's base level."""

    stats: dict[int, int] = attr.field(repr=False, hash=False)
    """Character stats."""

    @property
    def url(self) -> str:
        """A url for the character at bungie.net."""
        return f"{url.BASE}/en/Gear/{int(self.member_type)}/{self.member_id}/{self.id}"

    def __int__(self) -> int:
        return int(self.id)
