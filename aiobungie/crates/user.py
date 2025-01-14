# pyright: reportIncompatibleMethodOverride = false
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

"""Basic implementation of Bungie user components."""

from __future__ import annotations

__all__ = (
    "User",
    "Unique",
    "HardLinkedMembership",
    "UserThemes",
    "BungieUser",
    "PartialBungieUser",
    "DestinyMembership",
    "UserCredentials",
    "SearchableDestinyUser",
    "SanitizedMembership",
)

import abc
import typing

import attrs

from aiobungie import builders, url
from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    import collections.abc as collections
    from datetime import datetime


class Unique(abc.ABC):
    """An interface for common fields that Destiny2/Bungie membership/user objects has.

    You can use this interface as a type hint for objects that contains minimal information.

    Example
    -------
    ```py
    def print_options(user: crates.Unique) -> None:
        print(
        "Welcome", user.unique_name,
        "You membership type is", user.type,
        "You profile link is", user.link
    )

    my_user = await client.fetch_bungie_user(00000)
    print_options(my_user) # accepts a bungie user.

    my_friends = await client.fetch_friends('token')
    for friend in my_friends:
        print_options(friend) # Friend is also unique
    ```
    """

    __slots__ = ()

    @property
    @abc.abstractmethod
    def id(self) -> int:
        """The user's id."""

    @property
    @abc.abstractmethod
    def name(self) -> str | None:
        """The user's name."""

    @property
    @abc.abstractmethod
    def type(self) -> enums.MembershipType:
        """The membership type of this user."""

    @property
    @abc.abstractmethod
    def code(self) -> int | None:
        """The user like's unique display name code.

        This can be `None` if the user hasn't logged in after season of the lost update.
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


@attrs.frozen(kw_only=True)
class PartialBungieUser(Unique):
    """The result of a partial `BungieUser` information. also known as battle-net membership.

    The difference between the two is that some memberships return information
    about their `Bungie` user, but is incomplete, so this get used instead.

    This is what's used for objects that contain `.bungie_user` field,
    for an example `ClanMember.bungie_user`

    .. note::
        You can fetch the actual bungie user of this partial user
        by using `PartialBungieUser.fetch_self()` method.
    """

    name: str | None
    """The user's name. Field may be `None` if not found."""

    code: int | None
    """The user's global name code. Field may be `None` if not found."""

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

    icon: builders.Image
    """The user's icon."""


@attrs.frozen(kw_only=True)
class BungieUser(Unique):
    """Represents a user at Bungie.net."""

    id: int
    """The user's id"""

    type: enums.MembershipType = attrs.field(default=enums.MembershipType.BUNGIE)
    """The type of this user, always returns `aiobungie.MembershipType.BUNGIE`"""

    created_at: datetime
    """The user's creation datetime."""

    name: str | None
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

    about: str | None
    """The user's about, Default is None if nothing is Found."""

    updated_at: datetime
    """The user's last updated om UTC date."""

    psn_name: str | None
    """The user's psn id if it exists."""

    steam_name: str | None
    """The user's steam name if it exists"""

    twitch_name: str | None
    """The user's twitch name if it exists."""

    blizzard_name: str | None
    """The user's blizzard name if it exists."""

    stadia_name: str | None
    """The user's stadia name if it exists."""

    egs_name: str | None
    """The user's EpicGames name if it exists."""

    profile_ban_expire: datetime | None
    """If this user's profile was banned, this is the expire date for it."""

    status: str | None
    """The user's bungie status text"""

    locale: str | None
    """The user's locale."""

    picture: builders.Image
    """The user's profile picture."""

    code: int | None
    """The user's unique display name code.
    This can be None if the user hasn't logged in after season of the lost update.
    """

    @property
    def profile_url(self) -> str:
        """The user's profile URL at Bungie.net"""
        return f"{url.BASE}/7/en/User/Profile/254/{self.id}"

    @property
    def link(self) -> str:
        return self.profile_url


@attrs.frozen(kw_only=True)
class DestinyMembership(Unique):
    """Represents a Bungie user's Destiny 2 membership."""

    id: int
    """The member's id."""

    name: str | None
    """The member's name."""

    last_seen_name: str
    """The member's last seen display name. This sometimes can be an empty string."""

    type: enums.MembershipType
    """The member's membership type."""

    types: collections.Sequence[enums.MembershipType]
    """A sequence of the member's membership types."""

    icon: builders.Image
    """The member's icon if it was present."""

    code: int | None
    """The member's name code. This field may be `None` if not found."""

    is_public: bool
    """The member's profile privacy status."""

    crossave_override: enums.MembershipType
    """The member's crossave override membership type."""


@attrs.frozen(kw_only=True)
class SearchableDestinyUser:
    """Represents the results of the searched users details."""

    name: str | None
    """The user's global display name."""

    code: int | None
    """The user's global display name code if set."""

    bungie_id: int | None
    """The user's Bungie.net id if set."""

    memberships: collections.Sequence[DestinyMembership]
    """A sequence of the user's Destiny 2 memberships."""


@attrs.frozen(kw_only=True)
class HardLinkedMembership:
    """Represents hard linked Bungie user membership.

    This currently only supports SteamID which's a public credentials.
    Also Cross-Save Aware.
    """

    type: enums.MembershipType
    """The hard link user membership type."""

    id: int
    """The hard link user id"""

    cross_save_type: enums.MembershipType
    """The hard link user's cross save membership type. Default is set to None-0"""

    def __int__(self) -> int:
        return self.id


@attrs.frozen(kw_only=True)
class UserCredentials:
    """Represents a Bungie user's credential types.

    Those credentials should be the linked profiles such as Twitch, Steam, Blizzard, etc.
    """

    type: enums.CredentialType
    """The credential type."""

    display_name: str
    """The user display name for this credential."""

    is_public: bool
    """Whether this credential is public or not."""

    self_as_string: str | None
    """The self credential as string,

    For an example if a Steam user's credentials this will be the id as a string.
    """

    def __str__(self) -> str:
        return self.display_name


@attrs.frozen(kw_only=True)
class UserThemes:
    """Represents a Bungie user theme."""

    id: int
    """The theme id."""

    name: str | None
    """An optional theme name. if not found this field will be `None`"""

    description: str | None
    """An optional theme description. This field could be `None` if no description found."""

    def __int__(self) -> int:
        return self.id


@attrs.frozen(kw_only=True)
class SanitizedMembership:
    """Collections of display names linked to a membership."""

    epic_games: str | None
    """The membership's EpicGames username if it's linked."""

    psn: str | None
    """The membership's Playstation Network username if it's linked."""

    steam: str | None
    """The membership's Steam username if it's linked."""

    twitch: str | None
    """The membership's Twitch username if it's linked."""

    xbox: str | None
    """The membership's Xbox username if it's linked."""


@attrs.frozen(kw_only=True)
class User:
    """Represents a user with both Destiny memberships and Bungie.net profile."""

    bungie_user: BungieUser
    """The user's bungie net user."""

    memberships: collections.Sequence[DestinyMembership]
    """A sequence of the user's Destiny memberships."""

    primary_membership_id: int | None
    """If the user has a primary membership id, This field will be available."""
