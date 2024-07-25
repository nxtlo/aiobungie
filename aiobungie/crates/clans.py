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

"""Implementation of a Bungie a clan and groups."""

from __future__ import annotations

__all__ = (
    "Clan",
    "Group",
    "ClanInfo",
    "ClanMember",
    "ClanFeatures",
    "ClanConversation",
    "ClanBanner",
    "GroupMember",
    "GroupDate",
)

import typing

import attrs

from aiobungie import url
from aiobungie.crates import user
from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    import collections.abc as collections
    from datetime import datetime

    from aiobungie import builders
    from aiobungie.crates import progressions as progressions_


@typing.final
class GroupDate(int, enums.Enum):
    ALL = 0
    PAST_DAY = 1
    PAST_WEEK = 2
    PAST_MONTH = 3
    PAST_YEAR = 4


@attrs.frozen(kw_only=True)
class ClanFeatures:
    """Represents Bungie clan features."""

    max_members: int
    """The maximum members the clan can have"""

    max_membership_types: int
    """The maximum membership types the clan can have"""

    capabilities: int
    """An int that represents the clan's capabilities."""

    membership_types: collections.Sequence[enums.MembershipType]
    """The clan's membership types."""

    invite_permissions: bool
    """True if the clan has permissions to invite."""

    update_banner_permissions: bool
    """True if the clan has permissions to updates its banner."""

    update_culture_permissions: bool

    join_level: int
    """The clan's join level."""


@attrs.frozen(kw_only=True)
class ClanConversation:
    """Represents a clan conversation."""

    group_id: int
    """The clan or group's id."""

    id: int
    """The conversation's id"""

    chat_enabled: bool
    """`True` if the Conversation's chat is enabled."""

    name: str | None
    """Conversation chat's name."""

    security: int
    """Conversation's security level."""


@attrs.frozen(kw_only=True)
class ClanBanner:
    """Representation of information of the clan banner."""

    id: int
    """The banner's id."""

    foreground: builders.Image
    """The banner's foreground."""

    background: builders.Image
    """The banner's background."""


@attrs.frozen(kw_only=True)
class ClanMember(user.DestinyMembership):
    """Represents a Bungie clan member."""

    group_id: int
    """The member's group id."""

    member_type: enums.ClanMemberType
    """The runtime type of this clan member."""

    is_online: bool
    """True if the clan member is online or not."""

    last_online: datetime
    """The date of the clan member's last online in UTC time zone."""

    joined_at: datetime
    """The clan member's join date in UTC time zone."""

    bungie_user: user.PartialBungieUser | None
    """The clan member's bungie partial net user if set. `None` if not found.

    .. note:: This only returns a partial bungie net user.
    You can fetch a detailed user with `PartialBungieUser.fetch_self()` method.
    """

    @property
    def is_admin(self) -> bool:
        """Check whether this member is a clan admin or not."""
        return self.member_type is enums.ClanMemberType.ADMIN

    @property
    def is_founder(self) -> bool:
        """Check whether this member is the clan founder or not."""
        return self.member_type is enums.ClanMemberType.FOUNDER


@attrs.frozen(kw_only=True)
class GroupMember:
    """Represents information about joined groups/clans for a member."""

    inactive_memberships: collections.Mapping[int, bool] | None
    """The member's inactive memberships if provided. This will be `None` if not provided."""

    member_type: enums.ClanMemberType
    """The member's member type."""

    is_online: bool
    """Whether the member is online or not."""

    last_online: datetime
    """Datetime of the member's last online date."""

    group_id: int
    """The group id of this member."""

    join_date: datetime
    """Datetime of the member's join date."""

    member: user.DestinyMembership
    """The member's destiny object that represents the group member."""

    group: Clan
    """The member's group/clan object that represents the group member."""

    def __int__(self) -> int:
        return self.group_id


@typing.final
class ClanInfo(typing.TypedDict):
    """This contract contains clan-specific group information. It does not include any investment data."""

    call_sign: str
    banner_data: collections.Mapping[str, int]
    """A key-value mapping that maps the clan's banner property name to its value"""


@attrs.frozen(kw_only=True)
class Group:
    """Basic information about a group."""

    group_id: int
    """The group id."""
    name: str
    """The group name."""
    group_type: enums.GroupType
    """The group type."""
    creation_date: datetime
    """The group creation date."""
    about: str
    """The about section of the group."""
    motto: str | None
    """The motto section of the group."""
    member_count: int
    """The amount of members in this group."""
    locale: str
    """The group's locale"""
    membership_option: int
    """THe membership option of the group."""
    capabilities: int
    """The capabilities of the group. See [Capabilities](https://bungie-net.github.io/multi/schema_GroupsV2-Capabilities.html#schema_GroupsV2-Capabilities)"""
    remote_group_id: int | None
    clan_info: ClanInfo | None
    """Information about this group, It doesn't include any investment data."""
    avatar_path: builders.Image
    """The avatar of the group represented as an image object."""
    theme: str


@attrs.frozen(kw_only=True)
class Clan:
    """Represents a Bungie clan."""

    id: int
    """The clan id"""

    type: enums.GroupType
    """The clan type."""

    name: str
    """The clan's name"""

    created_at: datetime
    """Clan's creation date time in UTC."""

    member_count: int
    """Clan's member count."""

    motto: str
    """Clan's motto."""

    is_public: bool
    """Clan's privacy status."""

    banner: builders.Image
    """Clan's banner"""

    avatar: builders.Image
    """Clan's avatar"""

    about: str
    """Clan's about title."""

    tags: collections.Sequence[str]
    """A list of the clan's tags."""

    theme: str
    """The set clan theme."""

    conversation_id: int

    allow_chat: bool

    chat_security: int

    progressions: collections.Mapping[int, progressions_.Progression]
    """A mapping from progression hash to a progression object."""

    banner_data: collections.Mapping[str, int]

    call_sign: str
    """The clan call sign."""

    owner: ClanMember | None
    """The clan owner. This field could be `None` if not found."""

    features: ClanFeatures
    """The clan features."""

    current_user_membership: collections.Mapping[str, ClanMember] | None
    """If an authorized user made this request and this user belongs to this clan.
    This field will be available.

    This maps from the membership type represented as a string to the authorized clan member.
    """

    @property
    def url(self) -> str:
        return f"{url.BASE}/en/ClanV2/Index?groupId={self.id}"
