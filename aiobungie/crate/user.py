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

"""Basic implementation for a Bungie a user."""


from __future__ import annotations

__all__ = ("User", "PartialUser", "UserLike", "HardLinkedMembership", "UserThemes")

import abc
import typing
from datetime import datetime

import attr

from aiobungie.internal import Image
from aiobungie.internal import enums
from aiobungie.internal import helpers
from aiobungie.internal import impl
from aiobungie.internal import time


@attr.s(eq=True, hash=True, init=True, kw_only=True, slots=True, weakref_slot=False)
class HardLinkedMembership:
    """Represents hard linked Bungie user membership.

    This currently only supports SteamID which's a public credenitial.
    Also Cross-Save Aware.
    """

    type: enums.MembershipType = attr.field(repr=True)
    """The hard link user membership type."""

    id: int = attr.field(repr=True, hash=True, eq=False)
    """The hard link user id"""

    cross_save_type: enums.MembershipType = attr.field(
        repr=True, hash=False, eq=False, default=enums.MembershipType.NONE
    )
    """The hard link user's crpss save membership type. Default is set to None-0"""


@attr.s(eq=True, hash=True, init=True, kw_only=True, slots=True, weakref_slot=False)
class UserThemes:
    """Represents a Bungie User theme."""

    id: int = attr.field(repr=True)
    """The theme id."""

    name: helpers.NoneOr[str] = attr.field(repr=True)
    """An optional theme name. if not found this field will be `None`"""

    description: helpers.NoneOr[str] = attr.field(repr=True)
    """An optional theme description. This field could be `None` if no description found."""


@attr.s(eq=True, hash=True, init=True, kw_only=True, slots=True, weakref_slot=False)
class PartialUser(abc.ABC):
    """A partial user crate."""

    @property
    @abc.abstractmethod
    def steam_name(self) -> typing.Optional[str]:
        """The user's steam username or None."""

    @property
    @abc.abstractmethod
    def twitch_name(self) -> typing.Optional[str]:
        """The user's twitch username or None."""

    @property
    @abc.abstractmethod
    def blizzard_name(self) -> typing.Optional[str]:
        """The user's blizzard username or None."""

    @property
    @abc.abstractmethod
    def psn_name(self) -> typing.Optional[str]:
        """The user's psn username or None."""

    @property
    @abc.abstractmethod
    def about(self) -> typing.Optional[str]:
        """The user's about section."""

    @property
    @abc.abstractmethod
    def locale(self) -> typing.Optional[str]:
        """The user's profile locale."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """The user's name."""

    @property
    @abc.abstractmethod
    def picture(self) -> typing.Optional[Image]:
        """The user's profile picture if its set."""

    @property
    @abc.abstractmethod
    def updated_at(self) -> datetime:
        """The user's last profile update."""

    @property
    @abc.abstractmethod
    def is_deleted(self) -> bool:
        """Determines if the user is deleted or not."""

    @property
    @abc.abstractmethod
    def status(self) -> typing.Optional[str]:
        """The user's profile status."""

    @property
    @abc.abstractmethod
    def created_at(self) -> datetime:
        """Returns the user's creation date in UTC timezone."""

    @property
    def human_timedelta(self) -> str:
        return time.human_timedelta(self.created_at)


@attr.s(eq=True, hash=True, init=True, kw_only=True, slots=True, weakref_slot=False)
class User(PartialUser):
    """Represents Bungie user."""

    id: int = attr.field(hash=True, repr=True)
    """The user's id"""

    created_at: datetime = attr.field(hash=True, repr=True, eq=False)
    """The user's creation date in UTC timezone."""

    name: str = attr.field(hash=False, eq=False, repr=True)
    """The user's name."""

    is_deleted: bool = attr.field(repr=True, eq=False, hash=False)
    """Returns True if the user is deleted"""

    about: typing.Optional[str] = attr.field(repr=True, hash=False, eq=False)
    """The user's about, Default is None if nothing is Found."""

    updated_at: datetime = attr.field(repr=True, hash=False, eq=False)
    """The user's last updated om UTC date."""

    psn_name: typing.Optional[str] = attr.field(repr=True, hash=False, eq=False)
    """The user's psn id if it exists."""

    steam_name: typing.Optional[str] = attr.field(repr=True, hash=False, eq=False)
    """The user's steam name if it exists"""

    twitch_name: typing.Optional[str] = attr.field(repr=True, hash=False, eq=False)
    """The user's twitch name if it exists."""

    blizzard_name: typing.Optional[str] = attr.field(repr=True, hash=False, eq=False)
    """The user's blizzard name if it exists."""

    status: typing.Optional[str] = attr.field(repr=True, hash=False, eq=False)
    """The user's bungie status text"""

    locale: typing.Optional[str] = attr.field(repr=False, hash=False, eq=False)
    """The user's locale."""

    picture: Image = attr.field(repr=False, hash=False, eq=False)
    """The user's profile picture."""

    @property
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """Returns a dict object of the user."""
        return attr.asdict(self)

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return int(self.id)


@attr.s(eq=True, hash=True, init=True, kw_only=True, slots=True, weakref_slot=False)
class UserLike(abc.ABC):
    """The is meant for any Member / user / like crate."""

    @property
    @abc.abstractmethod
    def net(self) -> impl.Netrunner:
        """A network state used for making external requests."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """The user's name."""

    @property
    @abc.abstractmethod
    def is_public(self) -> typing.Optional[bool]:
        """Returns if the user profile is public or no."""

    @property
    @abc.abstractmethod
    def type(self) -> typing.Optional[enums.MembershipType]:
        """Returns the user type of the user."""

    @property
    @abc.abstractmethod
    def icon(self) -> Image:
        """The user's icon."""

    @property
    def link(self) -> typing.Optional[str]:
        """Returns the user's profile link."""

    @property
    @abc.abstractmethod
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """Returns an instance of the UserLike as a dict."""

    def __str__(self) -> str:
        return self.name
