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

"""Basic Implementation for a Bungie Character."""

from __future__ import annotations

__all__: typing.Sequence[str] = ("CharacterComponent", "Character")

import abc
import datetime
import logging
import typing

import attr

from .. import url
from ..internal import Image, Time, enums

log: typing.Final[logging.Logger] = logging.getLogger(__name__)


@attr.s(kw_only=True, hash=True, weakref_slot=False, slots=True, init=True, eq=True)
class CharacterComponent(abc.ABC):
    """An interface for a Bungie character component."""

    @property
    @abc.abstractmethod
    def member_type(self) -> enums.MembershipType:
        """The character's membership type."""

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
    def stats(self) -> enums.Stat:
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

    @property
    def human_timedelta(self) -> str:
        """The player's last played time in a human readble date."""
        return Time.human_timedelta(Time.clean_date(str(self.last_played)))


@attr.s(kw_only=True, hash=True, weakref_slot=False, slots=True, init=True, eq=True)
class Character(CharacterComponent):
    """An implementation for a Bungie character.

    A Bungie character object can be a Warlock, Titan or a Hunter.

    This can only be accessed using the `aiobungie.Component` CHARACTERS component.

    Attributes
    -----------
    light: `builtins.int`
            The character's light
    id: `builtins.int`
            The character's id
    gender: `aiobungie.internal.enums.Gender`
            The character's gender
    race: `aiobungie.internal.enums.Race`
            The character's race
    emblem: `aiobungie.internal.assets.Image`
            The character's currnt equipped emblem.
    emblem_icon: `aiobungie.internal.assets.Image`
            The character's current icon for the equipped emblem.
    emblem_hash: `builtins.int`
            Character's emblem hash.
    last_played: `datetime.datetime`
            When was this character last played date in UTC.
    total_played: `builtins.int`
            Returns the total played time in seconds for the chosen character.
    member_id: `builtins.int`
            The character's member id.
    class_type: `aiobungie.internal.enums.Class`
            The character's class.
    level: `builtins.int`
            Character's base level.
    stats: `aiobungie.internal.enums.Stat`
            Character's current stats.
    title_hash: `typing.Optional[builtins.int]`
            The hash of the character's equipped title, Returns `builtins.NoneType`
            if no title is equipped.
    """

    id: int = attr.ib(hash=True, repr=True)
    """Character's id"""

    member_id: int = attr.ib(hash=True, repr=True)
    """The character's member id."""

    member_type: enums.MembershipType = attr.ib(repr=True, hash=False)
    """The character's memberhip type."""

    light: int = attr.ib(repr=True, hash=False)
    """Character's light"""

    gender: enums.Gender = attr.ib(repr=True, hash=False)
    """Character's gender"""

    race: enums.Race = attr.ib(repr=True, hash=False)
    """Character's race"""

    emblem: Image = attr.ib(repr=False, hash=False)
    """Character's emblem"""

    emblem_icon: Image = attr.ib(repr=False, hash=False)
    """Character's emblem icon"""

    emblem_hash: int = attr.ib(repr=False, hash=False)
    """Character's emblem hash."""

    last_played: datetime.datetime = attr.ib(repr=False, hash=False)
    """Character's last played date."""

    total_played_time: str = attr.ib(repr=False, hash=False)
    """Character's total plyed time minutes."""

    class_type: enums.Class = attr.ib(repr=True, hash=False)
    """Character's class."""

    title_hash: typing.Optional[int] = attr.ib(repr=True, hash=False)
    """Character's equipped title hash."""

    level: int = attr.ib(repr=False, hash=False)
    """Character's base level."""

    stats: enums.Stat = attr.ib(repr=False, hash=False)
    """Character stats."""

    @property
    def url(self) -> str:
        """A url for the character at bungie.net."""
        return f"{url.BASE}/en/Gear/{int(self.member_type)}/{self.member_id}/{self.id}"

    @property
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """Returns a dict object of the character,
        This function is useful if you're binding to other REST apis.
        """
        return dict(
            id=self.id,
            light=self.light,
            gender=self.gender,
            race=self.race,
            emblem=str(self.emblem),
            emblem_icon=str(self.emblem_icon),
            emblem_hash=self.emblem_hash,
            last_played=self.last_played,
            total_played_time=self.total_played_time,
            member_id=self.member_id,
            member_type=self.member_type,
            cls=str(self.class_type),
            level=self.level,
            title_hash=self.title_hash,
            stats=self.stats,
        )

    def __int__(self) -> int:
        return int(self.id)
