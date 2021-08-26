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

__all__ = ("User", "UserLike", "HardLinkedMembership", "UserThemes")

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
class UserLike(abc.ABC):
    """The is meant for any bungie userlike object."""

    @property
    @abc.abstractmethod
    def net(self) -> impl.Netrunner:
        """A network state used for making external requests."""

    @property
    @abc.abstractmethod
    def id(self) -> int:
        """The user like's id."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """The user like's name."""

    @property
    @abc.abstractmethod
    def is_public(self) -> bool:
        """True if the user profile is public or no."""

    @property
    @abc.abstractmethod
    def type(self) -> enums.MembershipType:
        """The user type of the user."""

    @property
    @abc.abstractmethod
    def icon(self) -> Image:
        """The user like's icon."""

    @property
    @abc.abstractmethod
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """An instance of the UserLike as a dict."""

    @property
    @abc.abstractmethod
    def code(self) -> helpers.NoneOr[int]:
        """The user like's unique display name code.
        This can be None if the user hasn't logged in after season of the lost update.

        .. versionadded:: 0.2.5
        """

    @property
    @abc.abstractmethod
    def unique_name(self) -> helpers.NoneOr[str]:
        """The user like's display name. This includes the full name with the user name code.

        .. versionadded:: 0.2.5
        """

    @property
    def link(self) -> str:
        """The user like's profile link."""
        raise NotImplementedError

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.id


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
class User:
    """Represents Bungie user."""

    id: int = attr.field(hash=True, repr=True)
    """The user's id"""

    created_at: datetime = attr.field(hash=True, repr=True, eq=False)
    """The user's creation date in UTC timezone."""

    name: str = attr.field(hash=False, eq=False, repr=True)
    """The user's name."""

    unique_name: helpers.NoneOr[str] = attr.field(repr=False)
    """The user's unique name which includes their unique code.
    This field could be None if no unique name found.
    
    .. versionadded:: 0.2.5
    """

    is_deleted: bool = attr.field(repr=False, eq=False, hash=False)
    """ True if the user is deleted"""

    about: typing.Optional[str] = attr.field(repr=True, hash=False, eq=False)
    """The user's about, Default is None if nothing is Found."""

    updated_at: datetime = attr.field(repr=False, hash=False, eq=False)
    """The user's last updated om UTC date."""

    psn_name: typing.Optional[str] = attr.field(repr=False, hash=False, eq=False)
    """The user's psn id if it exists."""

    steam_name: typing.Optional[str] = attr.field(repr=False, hash=False, eq=False)
    """The user's steam name if it exists"""

    twitch_name: typing.Optional[str] = attr.field(repr=False, hash=False, eq=False)
    """The user's twitch name if it exists."""

    blizzard_name: typing.Optional[str] = attr.field(repr=False, hash=False, eq=False)
    """The user's blizzard name if it exists."""

    status: typing.Optional[str] = attr.field(repr=False, hash=False, eq=False)
    """The user's bungie status text"""

    locale: typing.Optional[str] = attr.field(repr=False, hash=False, eq=False)
    """The user's locale."""

    picture: Image = attr.field(repr=False, hash=False, eq=False)
    """The user's profile picture."""

    code: helpers.NoneOr[int] = attr.field(repr=True)
    """The user's unique display name code. 
    This can be None if the user hasn't logged in after season of the lost update.
    
    .. versionadded:: 0.2.5
    """

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.id

    @property
    def human_timedelta(self) -> str:
        """A human readable date version of the user's creation date."""
        return time.human_timedelta(self.created_at)

    @property
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """a dict object of the user."""
        return attr.asdict(self)
