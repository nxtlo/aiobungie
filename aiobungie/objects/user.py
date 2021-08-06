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

__all__: Sequence[str] = ["User", "PartialUser", "UserLike"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Optional, Sequence

import attr

from ..internal import Image, Time, enums

if TYPE_CHECKING:
    from datetime import datetime


@attr.s(eq=True, hash=True, init=True, kw_only=True, slots=True, weakref_slot=False)
class PartialUser(ABC):
    """The partial user object."""

    __slots__: Sequence[str] = ()

    @property
    @abstractmethod
    def steam_name(self) -> Optional[str]:
        """The user's steam username or None."""

    @property
    @abstractmethod
    def twitch_name(self) -> Optional[str]:
        """The user's twitch username or None."""

    @property
    @abstractmethod
    def blizzard_name(self) -> Optional[str]:
        """The user's blizzard username or None."""

    @property
    @abstractmethod
    def psn_name(self) -> Optional[str]:
        """The user's psn username or None."""

    @property
    @abstractmethod
    def about(self) -> Optional[str]:
        """The user's about section."""

    @property
    @abstractmethod
    def locale(self) -> Optional[str]:
        """The user's profile locale."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The user's name."""

    @property
    @abstractmethod
    def picture(self) -> Optional[Image]:
        """The user's profile picture if its set."""

    @property
    @abstractmethod
    def updated_at(self) -> datetime:
        """The user's last profile update."""

    @property
    @abstractmethod
    def is_deleted(self) -> bool:
        """Determines if the user is deleted or not."""

    @property
    @abstractmethod
    def status(self) -> Optional[str]:
        """The user's profile status."""

    @property
    @abstractmethod
    def created_at(self) -> datetime:
        """Retruns the user's creation date in UTC timezone."""

    @property
    def human_timedelta(self) -> str:
        return Time.human_timedelta(self.created_at)


@attr.s(eq=True, hash=True, init=True, kw_only=True, slots=True, weakref_slot=False)
class User(PartialUser):
    """Represents Bungie User object.

    Attributes
    ----------
    id: `builtins.int`
            The user's id
    name: `builtins.str`
            The user's name.
    is_deleted: `builtins.bool`
            Returns True if the user is deleted
    about: typing.Optional[builtins.str]
            The user's about, Default is None if nothing is Found.
    created_at: `datetime.datetime`
            The user's creation date in UTC date.
    updated_at: `datetime.datetime`
            The user's last updated om UTC date.
    psn_name: typing.Optional[builtins.str]
            The user's psn id if it exists.
    twitch_name: typing.Optional[builtins.str]
            The user's twitch name if it exists.
    blizzard_name: typing.Optional[builtins.str]
            The user's blizzard name if it exists.
    steam_name: typing.Optional[builtins.str]
            The user's steam name if it exists
    status: typing.Optional[builtins.str]
            The user's bungie status text
    locale: typing.Optional[builtins.str]
            The user's locale.
    picture: aiobungie.internal.assets.Image
            The user's avatar.
    """

    id: int = attr.field(hash=True, repr=True)
    """The user's id"""

    created_at: datetime = attr.field(hash=True, repr=True, eq=False)
    """The user's creation date in UTC timezone."""

    name: str = attr.field(hash=False, eq=False, repr=True)
    """The user's name."""

    is_deleted: bool = attr.field(repr=True, eq=False, hash=False)
    """Returns True if the user is deleted"""

    about: Optional[str] = attr.field(repr=True, hash=False, eq=False)
    """The user's about, Default is None if nothing is Found."""

    updated_at: datetime = attr.field(repr=True, hash=False, eq=False)
    """The user's last updated om UTC date."""

    psn_name: Optional[str] = attr.field(repr=True, hash=False, eq=False)
    """The user's psn id if it exists."""

    steam_name: Optional[str] = attr.field(repr=True, hash=False, eq=False)
    """The user's steam name if it exists"""

    twitch_name: Optional[str] = attr.field(repr=True, hash=False, eq=False)
    """The user's twitch name if it exists."""

    blizzard_name: Optional[str] = attr.field(repr=True, hash=False, eq=False)
    """The user's blizzard name if it exists."""

    status: Optional[str] = attr.field(repr=True, hash=False, eq=False)
    """The user's bungie status text"""

    locale: Optional[str] = attr.field(repr=False, hash=False, eq=False)
    """The user's locale."""

    picture: Image = attr.field(repr=False, hash=False, eq=False)
    """The user's profile picture."""

    @property
    def as_dict(self) -> Dict[str, Any]:
        """Returns a dict object of the user,
        This function is useful if you're binding to other REST apis.
        """
        return attr.asdict(self)


class UserLike(ABC):
    """The is meant for any Member / user / like objects."""

    __slots__: Sequence[str] = ()

    @property
    @abstractmethod
    def name(self) -> str:
        """The user's name."""

    @property
    @abstractmethod
    def is_public(self) -> Optional[bool]:
        """Returns if the user profile is public or no."""

    @property
    @abstractmethod
    def type(self) -> Optional[enums.MembershipType]:
        """Returns the user type of the user."""

    @property
    @abstractmethod
    def icon(self) -> Image:
        """The user's icon."""

    @property
    def link(self) -> Optional[str]:
        """Returns the user's profile link."""

    @property
    @abstractmethod
    def as_dict(self) -> Dict[str, Any]:
        """Returns an instance of the object attrs as a dict."""
        
    def __str__(self) -> str:
        return self.name
