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

"""Basic implementation for a Bungie a clan."""


from __future__ import annotations

__all__: Sequence[str] = ["Clan", "ClanOwner"]

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence

import attr

from aiobungie import url

from ..internal import Image, Time
from ..internal.enums import MembershipType
from .user import UserCard

if TYPE_CHECKING:
    from datetime import datetime


class ClanMembers:
    __slots__: Sequence[str] = ()


@attr.s(eq=True, hash=True, init=True, kw_only=True, slots=True, weakref_slot=False)
class ClanOwner(UserCard):
    """Represents a Bungie clan owner.


    Attributes
    -----------
    id: `builtins.int`
        The clan owner's membership id
    name: `builtins.str`
        The clan owner's display name
    last_online: `builtins.str`
        An aware `builtins.str` version of a `datetime.datetime` object.
    type: `aiobungie.internal.enums.MembershipType`
        Returns the clan owner's membership type.
        This could be Xbox, Steam, PSN, Blizzard or ALL,
        if the membership type is not recognized it will return `builtins.NoneType`.
    clan_id: `builtins.int`
        The clan owner's clan id
    joined_at: Optional[datetime.datetime]:
        The clan owner's join date in UTC.
    icon: `aiobungie.internal.assets.Image`
        Returns the clan owner's icon from Image.
    is_public: `builtins.bool`
        Returns True if the clan's owner profile is public or False if not.
    types: typing.List[builtins.int]:
        returns a List of `builtins.int` of the clan owner's types.
    """

    id: int = attr.ib(hash=True, repr=True)
    """The user id."""

    name: str = attr.ib(repr=True)
    """The user name."""

    is_public: Optional[bool] = attr.ib(hash=False, repr=True, eq=False)
    """Returns if the user profile is public or no."""

    type: MembershipType = attr.ib(hash=False, repr=True, eq=True)
    """Returns the membership type of the user."""

    types: Optional[List[int]] = attr.ib(hash=True, repr=False, eq=False)
    """Returns a list of the member ship's membership types."""

    last_online: datetime = attr.ib(repr=False)
    """An aware `datetime.datetime` object of the user's last online date UTC."""

    clan_id: int = attr.ib(repr=True)
    """Owner's current clan id."""

    icon: Image = attr.ib(repr=False)
    """Owner's profile icom"""

    joined_at: datetime = attr.ib(repr=True)
    """Owner's bungie join date."""

    @property
    def human_timedelta(self) -> str:
        """Returns a human readble date of the clan owner's last login."""
        return Time.human_timedelta(self.last_online)

    @property
    def link(self) -> Optional[str]:
        """Returns the user's profile link."""
        return f"{url.BASE}/en/Profile/index/{int(self.type)}/{self.id}"

    @property
    def as_dict(self) -> Dict[str, Any]:
        """Returns a dict object of the clan owner,
        This function is useful if you're binding to other REST apis.
        """
        return dict(
            id=self.id,
            name=self.name,
            is_public=self.is_public,
            icon=str(self.icon),
            types=self.type,
            joined_at=self.joined_at,
            type=self.type,
            clan_id=self.clan_id,
            last_online=self.last_online,
        )


@attr.s(eq=True, hash=True, init=True, kw_only=True, slots=True, weakref_slot=False)
class Clan:
    """Represents a Bungie clan object.

    Attributes
    -----------
    name: `builtins.str`
        The clan's name
    id: `builtins.int`
        The clans's id
    created_at: `datetime.datetime`
        Returns the clan's creation date in UTC time.
    description: `builtins.str`
        The clan's description.
    is_public: `builtins.bool`
        Returns True if the clan is public and False if not.
    banner: `aiobungie.internal.assets.Image`
        Returns the clan's banner
    avatar: `aiobungie.internal.assets.Image`
        Returns the clan's avatar
    about: `builtins.str`
        The clan's about.
    tags: `builtins.str`
        The clan's tags
    owner: `aiobungie.objects.ClanOwner`
        Returns an object of the clan's owner.
        See `aiobungie.objects.ClanOwner` for info.
    """

    id: int = attr.ib(hash=True, repr=True, eq=True)
    """The clan id"""

    name: str = attr.ib(repr=True)
    """The clan's name"""

    created_at: datetime = attr.ib(repr=True)
    """Clan's creation date time in UTC."""

    member_count: int = attr.ib(repr=True)
    """Clan's member count."""

    description: str = attr.ib(repr=True, eq=False)
    """Clan's description"""

    is_public: bool = attr.ib(repr=True, eq=False)
    """Clan's privacy status."""

    banner: Image = attr.ib(repr=False)
    """Clan's banner"""

    avatar: Image = attr.ib(repr=False)
    """Clan's avatar"""

    about: str = attr.ib(repr=True, eq=False)
    """Clan's about title."""

    tags: List[str] = attr.ib(repr=False)
    """A list of the clan's tags."""

    owner: ClanOwner = attr.ib(repr=True)
    """The clan owner."""

    @property
    def human_timedelta(self) -> str:
        """Returns a human readble date of the clan's creation date."""
        return Time.human_timedelta(self.created_at)

    @property
    def url(self) -> str:
        return f"{url.BASE}/en/ClanV2/Index?groupId={self.id}"

    @property
    def as_dict(self) -> Dict[str, Any]:
        """Returns a dict object of the player,
        This function is useful if you're binding to other REST apis.
        """
        return dict(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            is_public=self.is_public,
            avatar=str(self.avatar),
            banner=str(self.banner),
            about=self.about,
            description=self.description,
            tags=self.tags,
        )
