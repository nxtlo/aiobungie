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

__all__ = ("Profile", "ProfileComponent", "LinkedProfile")

import abc
import datetime
import logging
import typing

import attr

from aiobungie.crate import character
from aiobungie.crate import user
from aiobungie.internal import enums
from aiobungie.internal import helpers

if typing.TYPE_CHECKING:
    from aiobungie.internal import traits

log: typing.Final[logging.Logger] = logging.getLogger(__name__)


class ProfileComponent(abc.ABC):
    """An interface that include all bungie profile components.
    Some fields may or may not be available here.
    """

    __slots__: typing.Sequence[str] = ()

    @property
    @abc.abstractmethod
    def net(self) -> traits.Netrunner:
        """A network state used for making external requests."""

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

    async def fetch_titan(self) -> character.Character:
        """Returns the titan character of the profile owner."""
        # We're ignoring the types for the character since
        char = await self.net.request.fetch_character(
            int(self.id), self.type, enums.Class.TITAN
        )
        assert isinstance(char, character.Character)
        return char

    async def fetch_hunter(self) -> character.Character:
        """Returns the hunter character of the profile owner."""
        char = await self.net.request.fetch_character(
            self.id, self.type, enums.Class.HUNTER
        )
        assert isinstance(char, character.Character)
        return char

    async def fetch_warlock(self) -> character.Character:
        """Returns the Warlock character of the profile owner."""
        char = await self.net.request.fetch_character(
            self.id, self.type, enums.Class.WARLOCK
        )
        assert isinstance(char, character.Character)
        return char


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class LinkedProfile:
    """Represents a membership linked profile information summary.

    You can iterate asynchronously through the profiles.

    Example
    -------
    ```py
    profiles = await client.fetch_linked_profiles(..., ...)
    try:
        while True:
            async for profile in profiles:
                real_profile = await profile.fetch_self_profile()
                print(repr(await real_profile.warlock()))
    except StopIteration:
        pass
    ```
    """

    net: traits.Netrunner = attr.field(repr=False, eq=False, hash=False)
    """A network state used for making external requests."""

    profiles: typing.Sequence[user.DestinyUser] = attr.field(repr=True)
    """A sequence of destiny memberships for this profile."""

    bungie: user.PartialBungieUser = attr.field(repr=True)
    """The profile's bungie membership."""

    profiles_with_errors: typing.Optional[
        typing.Sequence[user.DestinyUser]
    ] = attr.field(repr=True, eq=False)
    """A sequence of optional destiny memberships with errors.

    These profiles exists because they have missing fields. Otherwise this will be an empty array.
    """

    def __aiter__(self) -> helpers.AsyncIterator[user.DestinyUser]:
        return helpers.AsyncIterator(self.profiles)


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class Profile(ProfileComponent):
    """Represents a Bungie member Profile.

    Bungie profiles requires components.
    But its kinda boring to pass multiple components to a parameter.
    So. The `.Profile` crate will include all Bungie components.
    to be accessiable as a crate.

    How?.
    For an example: to access the `Characters` component you'll need to pass `?component=200`.
    But here you can just return the character itself from the profile
    using `await .Profile.titan()` and the other character methods
    which returns a `aiobungie.crate.Character` crate.
    crates are basically classes/objects.

    Example
    -------
    ```py
    client = aiobungie.Client(...)
    profile = await client.fetch_profile("Fate")

    # access the character component and get my warlock.
    warlock = await profile.fetch_warlock()

    assert warlock.light == 1320
    ```
    """

    id: int = attr.field(repr=True, hash=True, eq=False)
    """Profile's id"""

    net: traits.Netrunner = attr.field(repr=False, hash=False, eq=False)
    """A network state used for making external requests."""

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
