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

__all__: Sequence[str] = ("Character",)

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union

from .. import error, url
from ..internal import Image, Time, enums

if TYPE_CHECKING:
    from datetime import datetime

    from ..types.character import CharacterData, CharacterImpl


class Character:
    """Represents a Bungie Character Object.

    A Bungie character object can be a Warlock, Titan or a Hunter.

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
    cls: `aiobungie.internal.enums.Class`
            The character's class.
    level: `builtins.int`
            Character's base level.
    stats: `aiobungie.internal.enums.Stat`
            Character's current stats.
    """

    id: int
    """Character's id"""

    light: int
    """Character's light"""

    gender: enums.Gender
    """Character's gender"""

    race: enums.Race
    """Character's race"""

    emblem: Image
    """Character's emblem"""

    emblem_icon: Image
    """Character's emblem icon"""

    emblem_hash: int
    """Character's emblem hash."""

    last_played: datetime
    """Character's last played date."""

    total_played: int
    """Character's total plyed time minutes."""

    member_id: int
    """Character's member id."""

    member_type: enums.MembershipType
    """Character's membership type."""

    cls: enums.Class
    """Character's class."""

    title_hash: int
    """Character's equipped title hash."""

    level: int
    """Character's base level."""

    stats: enums.Stat
    """Character stats."""

    __slots__: Sequence[str] = (
        "id",
        "light",
        "gender",
        "race",
        "emblem",
        "emblem_icon",
        "emblem_hash",
        "last_played",
        "total_played",
        "member_id",
        "member_type",
        "cls",
        "level",
        "title_hash",
        "stats",
        "_char",  # ignored
    )

    def __init__(self, *, char: enums.Class, data: CharacterImpl) -> None:
        self._char = char
        self.update(data)

    @property
    def last_played_delta(self) -> str:
        """Last played in human delta time."""
        return Time.human_timedelta(Time.clean_date(str(self.last_played)))

    @property
    def url(self) -> str:
        """Returns the bungie url for the current character."""
        return f"{url.BASE}/en/Gear/{int(self.member_type)}/{self.member_id}/{self.id}"

    def as_dict(self) -> Dict[str, Any]:
        """Returns a dict object of the character,
        This function is useful if you're binding to other REST apis.
        """
        return dict(
            id=self.id,
            light=self.light,
            gender=self.gender,
            race=self.race,
            emblem=self.emblem,
            emblem_icon=self.emblem_icon,
            emblem_hash=self.emblem_hash,
            last_played=self.last_played,
            total_played=self.total_played,
            member_id=self.member_id,
            member_type=self.member_type,
            cls=self.cls,
            level=self.level,
            title_hash=self.title_hash,
            stats=self.stats,
        )

    def _check_char(self, payload: CharacterImpl, char: enums.Class) -> CharacterData:
        payload = [c for c in payload["characters"]["data"].values()]  # type: ignore
        return payload[char.value]  # type: ignore

    def __int__(self) -> int:
        return self.id

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__} id={self.id} gender={self.gender}"
            f" class={self.cls} race={self.race}"
        )

    def update(self, data: CharacterImpl) -> None:
        data = self._check_char(data, self._char)
        self.id = data["characterId"]
        self.gender = enums.Gender(data["genderType"])
        self.race = enums.Race(data["raceType"])
        self.cls = enums.Class(data["classType"])
        self.emblem = Image(str(data["emblemBackgroundPath"]))
        self.emblem_icon = Image(str(data["emblemPath"]))
        self.emblem_hash = data["emblemHash"]
        self.last_played = data["dateLastPlayed"]
        self.total_played = data["minutesPlayedTotal"]
        self.member_id = data["membershipId"]
        self.member_type = enums.MembershipType(data["membershipType"])
        self.level = data["baseCharacterLevel"]
        self.title_hash = data["titleRecordHash"]
        self.light = data["light"]
        self.stats = data["stats"]
