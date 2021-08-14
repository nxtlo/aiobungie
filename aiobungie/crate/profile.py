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

"""Implementation for a Bungie a Profile."""

from __future__ import annotations

__all__: typing.Sequence[str] = ("Profile", "ProfileComponentImpl")

import attr
import abc
import datetime
import logging
import typing

from aiobungie.internal import Time
from aiobungie.internal import enums
from aiobungie.internal import impl

from aiobungie.crate.character import Character

log: typing.Final[logging.Logger] = logging.getLogger(__name__)


@attr.s(kw_only=True, hash=True, weakref_slot=False, slots=True, init=True, eq=True)
class ProfileComponentImpl(abc.ABC):
    """
    A partial interface that will/include all bungie profile components.

    Some fields may or may not be available here.
    """

    @property
    @abc.abstractmethod
    def app(self) -> impl.RESTful:
        """A client that we may to make rest requests."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Profile's name"""

    @property
    @abc.abstractmethod
    def type(self) -> enums.MembershipType:
        """Profile's membership type."""

    @property
    @abc.abstractmethod
    def last_played(self) -> datetime.datetime:
        """The profile user's last played date time."""

    @property
    @abc.abstractmethod
    def is_public(self) -> bool:
        """Profile's privacy status."""

    @property
    @abc.abstractmethod
    def character_ids(self) -> typing.List[int]:
        """A list of the profile's character ids."""

    @property
    @abc.abstractmethod
    def id(self) -> int:
        """The profile's id."""

    async def titan(self) -> Character:
        """Returns the titan character of the profile owner."""
        # We're ignoring the types for the character since
        char: Character = await self.app.rest.fetch_character(
            int(self.id), self.type, enums.Class.TITAN
        )
        return Character(
            id=char.id,
            class_type=char.class_type,
            emblem=char.emblem,
            emblem_hash=char.emblem_hash,
            emblem_icon=char.emblem_icon,
            light=char.light,
            last_played=char.last_played,
            level=char.level,
            member_id=char.member_id,
            member_type=char.member_type,
            gender=char.gender,
            race=char.race,
            total_played_time=char.total_played_time,
            title_hash=char.title_hash,
            stats=char.stats,
        )

    async def hunter(self) -> Character:
        """Returns the hunter character of the profile owner."""
        char: Character = await self.app.rest.fetch_character(
            self.id, self.type, enums.Class.HUNTER
        )
        return Character(
            id=char.id,
            class_type=char.class_type,
            emblem=char.emblem,
            emblem_hash=char.emblem_hash,
            emblem_icon=char.emblem_icon,
            light=char.light,
            last_played=char.last_played,
            level=char.level,
            member_id=char.member_id,
            member_type=char.member_type,
            gender=char.gender,
            race=char.race,
            total_played_time=char.total_played_time,
            title_hash=char.title_hash,
            stats=char.stats,
        )

    async def warlock(self) -> Character:
        """Returns the Warlock character of the profile owner."""
        char: Character = await self.app.rest.fetch_character(
            self.id, self.type, enums.Class.WARLOCK
        )
        return Character(
            id=char.id,
            class_type=char.class_type,
            emblem=char.emblem,
            emblem_hash=char.emblem_hash,
            emblem_icon=char.emblem_icon,
            light=char.light,
            last_played=char.last_played,
            level=char.level,
            member_id=char.member_id,
            member_type=char.member_type,
            gender=char.gender,
            race=char.race,
            total_played_time=char.total_played_time,
            title_hash=char.title_hash,
            stats=char.stats,
        )


@attr.s(kw_only=True, hash=True, weakref_slot=False, slots=True, init=True, eq=True)
class Profile(ProfileComponentImpl):
    """Represents a Bungie member Profile.

    Bungie profiles requires components. but in aiobungie
    you don't need to select a specific component since they will all/will be
    implemented.

    for an example: to access the `Character` component you'll need to pass `?component=200` right?.
    in aiobungie you can just do this.

    ```py
    profile = await client.fetch_profile("Fate")

    # access the character component and get my warlock.
    warlock = await profile.warlock()

    assert warlock.light == 1320
    ```
    """

    id: int = attr.field(repr=True, hash=True, eq=False)
    """Profile's id"""

    app: impl.RESTful = attr.field(repr=False, hash=False, eq=False)

    name: str = attr.field(repr=True, hash=False, eq=False)
    """Profile's name."""

    type: enums.MembershipType = attr.field(repr=True, hash=False, eq=False)
    """Profile's type."""

    is_public: bool = attr.field(repr=True, hash=False, eq=False)
    """Profile's privacy status."""

    last_played: datetime.datetime = attr.field(repr=True, hash=False, eq=False)
    """Profile's last played Destiny 2 played date."""

    character_ids: typing.List[int] = attr.field(repr=False, hash=False, eq=False)
    """A list of the profile's character ids."""

    power_cap: int = attr.field(repr=False, hash=False, eq=False)
    """The profile's current seaspn power cap."""

    # Components

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return int(self.id)

    @property
    def titan_id(self) -> int:
        """The titan id of the profile player."""
        return int(self.character_ids[0])

    @property
    def hunter_id(self) -> int:
        """The huter id of the profile player."""
        return int(self.character_ids[1])

    @property
    def warlock_id(self) -> int:
        """The warlock id of the profile player."""
        return int(self.character_ids[2])

    @property
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """Returns a dict object of the profile."""
        return attr.asdict(self)

    @property
    def human_timedelta(self) -> str:
        """Returns last_played attr but in human delta date."""
        return Time.human_timedelta(self.last_played)
