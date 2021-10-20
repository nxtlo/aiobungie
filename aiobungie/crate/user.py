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

__all__: tuple[str, ...] = (
    "User",
    "UserLike",
    "HardLinkedMembership",
    "UserThemes",
    "BungieUser",
    "PartialBungieUser",
    "DestinyUser",
)

import abc
import typing

import attr

from aiobungie.crate import profile
from aiobungie.internal import assets
from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    from datetime import datetime

    from aiobungie.internal import helpers
    from aiobungie.internal import traits


class UserLike(abc.ABC):
    """An ABC that's used for all userlike objects."""

    __slots__: typing.Sequence[str] = ()

    @property
    @abc.abstractmethod
    def id(self) -> int:
        """The user like's id."""

    @property
    @abc.abstractmethod
    def name(self) -> helpers.UndefinedOr[str]:
        """The user like's name."""

    @property
    @abc.abstractmethod
    def last_seen_name(self) -> str:
        """The user like's last seen name."""

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
    def icon(self) -> assets.MaybeImage:
        """The user like's icon."""
        return assets.Image.partial()

    @property
    @abc.abstractmethod
    def code(self) -> helpers.NoneOr[int]:
        """The user like's unique display name code.
        This can be None if the user hasn't logged in after season of the lost update.
        """

    @property
    @abc.abstractmethod
    def unique_name(self) -> str:
        """The user like's display name. This includes the full name with the user name code."""
        return f"{self.name}#{self.code}"

    @property
    def link(self) -> str:
        """The user like's profile link."""

    def __str__(self) -> str:
        return self.last_seen_name

    def __int__(self) -> int:
        return self.id


# This is meant for Bungie destiny users which's different from a normal bungie user.
@attr.define(hash=False, kw_only=True, weakref_slot=False)
class PartialBungieUser:
    """Represents partial bungie user.

    This is usually used for bungie users that are missing attributes not present in `BungieUser`,
    i.e., Clan members, Owners, Moderators and any other object the has a `bungie` attribute.

    .. note::
        You can fetch the actual bungie user of this partial user
        by using `PartialBungieUser.fetch_self()` method.
    """

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    name: helpers.UndefinedOr[str] = attr.field(repr=True)
    """The user's name. Field may be undefined if not found."""

    id: int = attr.field(repr=True, hash=True)
    """The user's id."""

    type: enums.MembershipType = attr.field(repr=True)
    """The user's membership type."""

    crossave_override: enums.MembershipType = attr.field(repr=False)
    """The user's crossave override membership."""

    is_public: bool = attr.field(repr=False)
    """The user's privacy."""

    icon: assets.MaybeImage = attr.field(repr=False)
    """The user's icon."""

    async def fetch_self(self) -> BungieUser:
        """Fetch the Bungie user of this partial user.

        Returns
        -------
        `aiobungie.crate.BungieUser`
            A Bungie net user.

        Raises
        ------
        `aiobungie.UserNotFound`
            The user was not found.
        """
        user = await self.net.request.fetch_user(self.id)
        assert isinstance(user, BungieUser)
        return user


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class BungieUser:
    """Represents a Bungie user."""

    id: int = attr.field(hash=True, repr=True)
    """The user's id"""

    created_at: datetime = attr.field(hash=True, repr=True, eq=False)
    """The user's creation date in UTC timezone."""

    name: helpers.UndefinedOr[str] = attr.field(hash=False, eq=False, repr=True)
    """The user's name."""

    unique_name: str = attr.field(repr=False)
    """The user's unique name which includes their unique code.
    This field could be None if no unique name found.
    """

    theme_id: int = attr.field(repr=False)
    """User profile's theme id."""

    show_activity: bool = attr.field(repr=False)
    """`True` if the user is showing their activity status and `False` if not."""

    theme_name: str = attr.field(repr=False)
    """User's profile theme name."""

    display_title: str = attr.field(repr=False)
    """User's display title."""

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

    stadia_name: typing.Optional[str] = attr.field(repr=False, hash=False, eq=False)
    """The user's stadia name if it exists."""

    status: typing.Optional[str] = attr.field(repr=False, hash=False, eq=False)
    """The user's bungie status text"""

    locale: typing.Optional[str] = attr.field(repr=False, hash=False, eq=False)
    """The user's locale."""

    picture: assets.MaybeImage = attr.field(repr=False, hash=False, eq=False)
    """The user's profile picture."""

    code: helpers.NoneOr[int] = attr.field(repr=True)
    """The user's unique display name code.
    This can be None if the user hasn't logged in after season of the lost update.
    """

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return self.id


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class DestinyUser(UserLike):
    """Represents a Bungie user's Destiny memberships."""

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    id: int = attr.field(repr=True, hash=True, eq=True)
    """The member's id."""

    name: helpers.UndefinedOr[str] = attr.field(repr=True, eq=False)
    """The member's name."""

    last_seen_name: str = attr.field(repr=True)
    """The member's last seen display name. You may use this field if `DestinyUser.name` is `Undefined`."""

    type: enums.MembershipType = attr.field(repr=True)
    """The member's membership type."""

    types: typing.Sequence[enums.MembershipType] = attr.field(repr=False)
    """A sequence of the member's membership types."""

    icon: assets.MaybeImage = attr.field(repr=False)
    """The member's icon if it was present."""

    code: helpers.NoneOr[int] = attr.field(repr=True, eq=True, hash=False, default=0)
    """The member's name code. This field may be `None` if not found."""

    is_public: bool = attr.field(repr=False, default=False)
    """The member's profile privacy status."""

    crossave_override: typing.Union[enums.MembershipType, int] = attr.field(repr=False)
    """The member's corssave override membership type."""

    async def fetch_self_profile(self) -> profile.Profile:
        """Fetch the player's profile.

        Returns
        -------
        `aiobungie.crate.Profile`
            The profile of this membership.
        """
        profile_ = await self.net.request.fetch_profile(self.id, self.type)
        assert isinstance(profile_, profile.Profile)
        return profile_

    @property
    def unique_name(self) -> str:
        """The member's unique name. This field may be `Undefined` if not found."""
        return f"{self.name}#{self.code}"


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class HardLinkedMembership:
    """Represents hard linked Bungie user membership.

    This currently only supports SteamID which's a public credenitial.
    Also Cross-Save Aware.
    """

    type: enums.MembershipType = attr.field(repr=True, hash=False)
    """The hard link user membership type."""

    id: int = attr.field(repr=True, hash=True, eq=False)
    """The hard link user id"""

    cross_save_type: enums.MembershipType = attr.field(
        repr=True, hash=False, eq=False, default=enums.MembershipType.NONE
    )
    """The hard link user's crpss save membership type. Default is set to None-0"""

    def __int__(self) -> int:
        return self.id


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class UserThemes:
    """Represents a Bungie User theme."""

    id: int = attr.field(repr=True, hash=True)
    """The theme id."""

    name: helpers.UndefinedOr[str] = attr.field(repr=True)
    """An optional theme name. if not found this field will be `None`"""

    description: helpers.UndefinedOr[str] = attr.field(repr=True)
    """An optional theme description. This field could be `None` if no description found."""

    def __int__(self) -> int:
        return self.id


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class User:
    """Concrete representtion of a Bungie user.

    This includes both Bungie net and Destiny memberships information.
    """

    bungie: BungieUser = attr.field(repr=True)
    """The user's bungie net membership."""

    destiny: typing.Sequence[DestinyUser] = attr.field(repr=True)
    """A sequence of the user's Destiny memberships."""
