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

"""Implementation of Bungie users."""

from __future__ import annotations

__all__: tuple[str, ...] = (
    "User",
    "HardLinkedMembership",
    "UserThemes",
    "BungieUser",
    "PartialBungieUser",
    "DestinyMembership",
    "UserCredentials",
    "SearchableDestinyUser",
)

import abc
import typing

import attrs

from aiobungie import url
from aiobungie.crates import components as components_
from aiobungie.internal import assets
from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    import collections.abc as collections
    from datetime import datetime

    from aiobungie import traits
    from aiobungie import typedefs
    from aiobungie import undefined


class UserLike(abc.ABC):
    """An interface for Bungie users implementation."""

    __slots__ = ()

    @property
    @abc.abstractmethod
    def id(self) -> int:
        """The user like's id."""

    @property
    @abc.abstractmethod
    def name(self) -> undefined.UndefinedOr[str]:
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
    def icon(self) -> assets.Image:
        """The user like's icon."""

    @property
    @abc.abstractmethod
    def code(self) -> typedefs.NoneOr[int]:
        """The user like's unique display name code.
        This can be None if the user hasn't logged in after season of the lost update.
        """

    @property
    def unique_name(self) -> str:
        """The user like's display name. This includes the full name with the user name code."""
        return f"{self.name}#{self.code}"

    @property
    def link(self) -> str:
        """The user like's profile link."""
        return f"{url.BASE}/en/Profile/index/{int(self.type)}/{self.id}"

    def __str__(self) -> str:
        return self.unique_name

    def __int__(self) -> int:
        return self.id


# This is meant for Bungie destiny users which's different from a normal bungie user.
@attrs.define(kw_only=True)
class PartialBungieUser:
    """Represents partial bungie user.

    This is usually used for bungie users that are missing attributes not present in `BungieUser`,
    i.e., Clan members, Owners, Moderators and any other object the has a `bungie` attribute.

    .. note::
        You can fetch the actual bungie user of this partial user
        by using `PartialBungieUser.fetch_self()` method.
    """

    net: traits.Netrunner = attrs.field(repr=False, eq=False, hash=False)
    """A network state used for making external requests."""

    name: undefined.UndefinedOr[str]
    """The user's name. Field may be undefined if not found."""

    id: int
    """The user's id."""

    type: enums.MembershipType
    """The user's membership type."""

    types: collections.Sequence[enums.MembershipType]
    """An array of applicable membership types for this user."""

    crossave_override: enums.MembershipType
    """The user's crossave override membership."""

    is_public: bool
    """The user's privacy."""

    icon: assets.Image
    """The user's icon."""

    async def fetch_self(self) -> BungieUser:
        """Fetch the Bungie user of this partial user.

        Returns
        -------
        `aiobungie.crates.BungieUser`
            A Bungie net user.

        Raises
        ------
        `aiobungie.NotFound`
            The user was not found.
        """
        return await self.net.request.fetch_bungie_user(self.id)

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return self.id


@attrs.define(kw_only=True)
class BungieUser:
    """Represents a user at Bungie.net."""

    id: int
    """The user's id"""

    created_at: datetime
    """The user's creation datetime."""

    name: undefined.UndefinedOr[str]
    """The user's name."""

    unique_name: str
    """The user's unique name which includes their unique code. This field could be None if no unique name found."""

    theme_id: int
    """User profile's theme id."""

    show_activity: bool
    """`True` if the user is showing their activity status and `False` if not."""

    theme_name: str
    """User's profile theme name."""

    display_title: str
    """User's display title."""

    is_deleted: bool
    """ True if the user is deleted"""

    about: typing.Optional[str]
    """The user's about, Default is None if nothing is Found."""

    updated_at: datetime
    """The user's last updated om UTC date."""

    psn_name: typing.Optional[str]
    """The user's psn id if it exists."""

    steam_name: typing.Optional[str]
    """The user's steam name if it exists"""

    twitch_name: typing.Optional[str]
    """The user's twitch name if it exists."""

    blizzard_name: typing.Optional[str]
    """The user's blizzard name if it exists."""

    stadia_name: typing.Optional[str]
    """The user's stadia name if it exists."""

    status: typing.Optional[str]
    """The user's bungie status text"""

    locale: typing.Optional[str]
    """The user's locale."""

    picture: assets.Image
    """The user's profile picture."""

    code: typedefs.NoneOr[int]
    """The user's unique display name code.
    This can be None if the user hasn't logged in after season of the lost update.
    """

    @property
    def profile_url(self) -> str:
        """The user's profile URL at Bungie.net"""
        return f"{url.BASE}/7/en/User/Profile/254/{self.id}"

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return self.id


@attrs.define(kw_only=True)
class DestinyMembership(UserLike):
    """Represents a Bungie user's Destiny 2 membership."""

    net: traits.Netrunner = attrs.field(repr=False, eq=False, hash=False)
    """A network state used for making external requests."""

    id: int
    """The member's id."""

    name: undefined.UndefinedOr[str]
    """The member's name."""

    last_seen_name: str
    """The member's last seen display name. This sometimes can be an empty string."""

    type: enums.MembershipType
    """The member's membership type."""

    types: collections.Sequence[enums.MembershipType]
    """A sequence of the member's membership types."""

    icon: assets.Image
    """The member's icon if it was present."""

    code: typedefs.NoneOr[int]
    """The member's name code. This field may be `None` if not found."""

    is_public: bool
    """The member's profile privacy status."""

    crossave_override: typing.Union[enums.MembershipType, int]
    """The member's corssave override membership type."""

    async def fetch_self_profile(
        self, components: list[enums.ComponentType], auth: typing.Optional[str] = None
    ) -> components_.Component:
        """Fetch this user's profile.

        Parameters
        ----------
        components : `list[aiobungie.ComponentType]`
            A list of profile components to collect and return.
            This either can be arguments of integers or `aiobungie.ComponentType`.

        Other Parameters
        ----------------
        auth : `typing.Optional[str]`
            A Bearer access_token to make the request with.
            This is optional and limited to components that only requires an Authorization token.

        Returns
        --------
        `aiobungie.crates.Component`
            A Destiny 2 player profile with its components.
            Only passed components will be available if they exists. Otherwise they will be `None`
        """
        return await self.net.request.fetch_profile(
            self.id, self.type, components, auth
        )


@attrs.define(kw_only=True)
class SearchableDestinyUser:
    """Represents the results of the searched users details."""

    name: undefined.UndefinedOr[str]
    """The user's global display name."""

    code: typing.Optional[int]
    """The user's global dsplay name code if set."""

    bungie_id: typing.Optional[int]
    """The user's Bungie.net id if set."""

    memberships: collections.Sequence[DestinyMembership]
    """A sequence of the user's Destiny 2 memberships."""


@attrs.define(kw_only=True)
class HardLinkedMembership:
    """Represents hard linked Bungie user membership.

    This currently only supports SteamID which's a public credenitial.
    Also Cross-Save Aware.
    """

    type: enums.MembershipType
    """The hard link user membership type."""

    id: int
    """The hard link user id"""

    cross_save_type: enums.MembershipType
    """The hard link user's crpss save membership type. Default is set to None-0"""

    def __int__(self) -> int:
        return self.id


@attrs.define(kw_only=True)
class UserCredentials:
    """Represents a Bungie user's credential types.

    Those credentials should be the linked profiles such as Twitch, Steam, Blizzard, etc.
    """

    type: enums.CredentialType
    """The credential type."""

    display_name: str
    """The user displayname for this credential."""

    is_public: bool
    """Whether this credential is public or not."""

    self_as_string: undefined.UndefinedOr[str]
    """The self credential as string,

    For an example if a Steam user's credentials this will be the id as a string.
    """

    def __str__(self) -> str:
        return self.display_name


@attrs.define(kw_only=True)
class UserThemes:
    """Represents a Bungie user theme."""

    id: int
    """The theme id."""

    name: undefined.UndefinedOr[str]
    """An optional theme name. if not found this field will be `None`"""

    description: undefined.UndefinedOr[str]
    """An optional theme description. This field could be `None` if no description found."""

    def __int__(self) -> int:
        return self.id


@attrs.define(kw_only=True)
class User:
    """Represents a user with both Destiny memberships and Bungie.net profile."""

    bungie: BungieUser
    """The user's bungie net user."""

    destiny: collections.Sequence[DestinyMembership]
    """A sequence of the user's Destiny memberships."""

    primary_membership_id: typing.Optional[int]
    """If the user has a primary membership id, This field will be available."""
