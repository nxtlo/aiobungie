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

__all__ = (
    "Clan",
    "ClanMember",
    "ClanAdmin",
    "ClanFeatures",
    "ClanConversation",
    "ClanBanner",
    "GroupMember",
)

import typing

import attr

from aiobungie import url
from aiobungie.crate import user
from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    from datetime import datetime

    from aiobungie.internal import assets
    from aiobungie.internal import helpers
    from aiobungie.internal import traits


@attr.define(kw_only=True, hash=False, weakref_slot=False)
class ClanFeatures:
    """Represents Bungie clan features."""

    max_members: int = attr.field(repr=True)
    """The maximum members the clan can have"""

    max_membership_types: int = attr.field(repr=False)
    """The maximum membership types the clan can have"""

    capabilities: int = attr.field(repr=False)
    """An int that represents the clan's capabilities."""

    membership_types: typing.List[enums.MembershipType] = attr.field(repr=True)
    """The clan's membership types."""

    invite_permissions: bool = attr.field(repr=False)
    """True if the clan has permissions to invite."""

    update_banner_permissions: bool = attr.field(repr=False)
    """True if the clan has permissions to updates its banner."""

    update_culture_permissions: bool = attr.field(repr=False)

    join_level: int = attr.field(repr=True)
    """The clan's join level."""


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class ClanConversation:
    """Represents a clan conversation."""

    group_id: int = attr.field(repr=True)
    """The clan or group's id."""

    id: int = attr.field(repr=True, hash=True)
    """The conversation's id"""

    chat_enabled: bool = attr.field(repr=True)
    """`True` if the Conversation's chat is enabled."""

    name: helpers.UndefinedOr[str] = attr.field(repr=True)
    """Conversation chat's name."""

    security: int = attr.field(repr=False)
    """Conversation's security level."""


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class ClanBanner:
    """Representation of information of the clan banner."""

    id: int = attr.field(repr=True)
    """The banner's id."""

    foreground: assets.MaybeImage = attr.field(repr=True)
    """The banner's foreground. This field can be `UNDEFINED` if not found."""

    background: assets.MaybeImage = attr.field(repr=True)
    """The banner's background. This field can be `UNDEFINED` if not found."""


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class ClanMember(user.UserLike):
    """Represents a Bungie clan member."""

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    id: int = attr.field(repr=True, hash=True)
    """Clan member's id"""

    name: helpers.UndefinedOr[str] = attr.field(repr=True)
    """Clan member's name. This can be `UNDEFINED` if not found."""

    last_seen_name: str = attr.field(repr=True)
    """The clan member's last seen display name"""

    type: enums.MembershipType = attr.field(repr=True)
    """Clan member's membership type."""

    types: typing.Sequence[enums.MembershipType] = attr.field(repr=False)
    """A sequence of the available clan member membership types."""

    icon: assets.MaybeImage = attr.field(repr=False)
    """Clan member's icon"""

    is_public: bool = attr.field(repr=False)
    """`builtins.True` if the clan member is public."""

    group_id: int = attr.field(repr=True)
    """The member's group id."""

    is_online: bool = attr.field(repr=False, default=None)
    """True if the clan member is online or not."""

    last_online: datetime = attr.field(repr=False, default=None)
    """The date of the clan member's last online in UTC time zone."""

    joined_at: datetime = attr.field(repr=False, default=None)
    """The clan member's join date in UTC time zone."""

    code: helpers.NoneOr[int] = attr.field(repr=True)
    """The clan member's bungie display name code
    This is new and was added in Season of the lost update

    .. versionadded:: 0.2.5
    """

    bungie: user.PartialBungieUser = attr.field(repr=True)
    """The clan member's bungie partial net user.

    .. note:: This only returns a partial bungie net user.
    You can fetch the fully implemented user using `aiobungie.crate.PartialBungieUser.fetch_self()` method.
    """

    @property
    def unique_name(self) -> str:
        """The clan member's unique name which includes their unique code.

        .. versionadded:: 0.2.5
        """
        return f"{self.name}#{self.code}"

    @property
    def link(self) -> str:
        """Clan member's profile link."""
        return f"{url.BASE}/en/Profile/index/{int(self.type)}/{self.id}"

    # These are not implemented yet
    # Since they requires OAuth2.

    async def ban(
        self,
        access_token: str,
        /,
        *,
        comment: typing.Optional[str] = None,
        length: int = 0,
    ) -> None:
        """Ban this member from the clan.

        .. note::
            This request requires OAuth2: oauth2: `AdminGroups` scope.

        Parameters
        ----------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.

        Other Parameters
        ----------------
        length: `int`
            An optional ban length. Default is 0
        comment: `typing.Optional[str]`
            An optional comment to this ban. Default is `None`

        Returns
        -------
        `None`
            None
        """
        return await self.net.request.ban_clan_member(
            access_token,
            self.group_id,
            self.id,
            self.type,
            comment=comment,
            length=length,
        )

    async def unban(self, access_token: str, /) -> None:
        """Unbans this member from the clan.

        .. note::
            This request requires OAuth2: oauth2: `AdminGroups` scope.

        Positional arguments
        --------------------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.

        Returns
        -------
        `None`
            None
        """
        return await self.net.request.unban_clan_member(
            access_token,
            group_id=self.group_id,
            membership_id=self.id,
            membership_type=self.type,
        )

    async def kick(self, access_token: str, /) -> Clan:
        """Kick this member from the clan.

        .. note::
            This request requires OAuth2: oauth2: `AdminGroups` scope.

        Parameters
        ----------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.

        Returns
        -------
        `aiobungie.crate.clan.Clan`
            The clan that represents the kicked member.
        """
        return await self.net.request.kick_clan_member(
            access_token,
            group_id=self.group_id,
            membership_id=self.id,
            membership_type=self.type,
        )


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class GroupMember:
    """Represents information about joined groups/clans for a member."""

    net: traits.Netrunner = attr.field(repr=False)

    inactive_memberships: helpers.NoneOr[dict[int, bool]] = attr.field(repr=False)
    """The member's inactive memberships if provided. This will be `None` if not provided."""

    member_type: enums.ClanMemberType = attr.field(repr=True)
    """The member's member type."""

    is_online: bool = attr.field(repr=False)
    """Whether the member is online or not."""

    last_online: datetime = attr.field(repr=False)
    """An awre UTC datetime of the member's last online status."""

    group_id: int = attr.field(repr=True)
    """The group id of this member."""

    join_date: datetime = attr.field(repr=False)
    """An awre UTC datetime of the member's join date."""

    member: user.DestinyUser = attr.field(repr=True)
    """The member's destiny object that represents the group member."""

    group: Clan = attr.field(repr=True)
    """The member's group/clan object that represents the group member."""

    async def fetch_self_clan(self) -> Clan:
        """Fetch an up-todate clan/group object of the current group.

        Returns
        -------
        `Clan`
            The clan object.
        """
        return await self.net.request.fetch_clan_from_id(self.group_id)


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class ClanAdmin(user.UserLike):
    """Represents a clan admin."""

    member_type: enums.ClanMemberType = attr.field(repr=True)
    """The clan admin's member type.
    This can be Admin or owner or any other type.

    .. versionadded:: 0.2.5
    """

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    total_admins: int = attr.field(repr=True)
    """The total count of the clan admins."""

    id: int = attr.field(repr=True, hash=True)
    """Clan admin's id"""

    name: helpers.UndefinedOr[str] = attr.field(repr=True)
    """Clan admin's name. This can be `UNDEFINED` if not found."""

    last_seen_name: str = attr.field(repr=False)
    """The clan admin's last seen display name"""

    type: enums.MembershipType = attr.field(repr=True)
    """Clan admin's membership type."""

    types: typing.Sequence[enums.MembershipType] = attr.field(repr=False)
    """A sequence of the available clan admin membership types."""

    icon: assets.MaybeImage = attr.field(repr=False)
    """Clan admin's icon"""

    is_public: bool = attr.field(repr=False)
    """`builtins.True` if the clan admin is public."""

    group_id: int = attr.field(repr=True)
    """The admin's group or clan id."""

    is_online: bool = attr.field(repr=False, default=None)
    """True if the clan admin is online or not."""

    last_online: datetime = attr.field(repr=False, default=None)
    """The date of the clan admin's last online in UTC time zone."""

    joined_at: datetime = attr.field(repr=False, default=None)
    """The clan admin's join date in UTC time zone."""

    code: helpers.NoneOr[int] = attr.field(repr=True)
    """The clan admin's bungie display name code
    This is new and was added in Season of the lost update

    .. versionadded:: 0.2.5
    """

    bungie: user.PartialBungieUser = attr.field(repr=True)
    """The clan admin's bungie partial net user.

    .. note:: This only returns a partial bungie net user.
    You can fetch the fully implemented user using
    `aiobungie.crate.PartialBungieUser.fetch_self()` method.
    """

    async def fetch_clan(self) -> Clan:
        """Fetch the clan that represents the clan admins.

        Returns
        -------
        `Clan`
            The clan admins clan.
        """
        return await self.net.request.fetch_clan_from_id(self.group_id)

    @property
    def unique_name(self) -> str:
        """The admin's unique name which includes their unique code.

        .. versionadded:: 0.2.5
        """
        return f"{self.name}#{self.code}"

    @property
    def link(self) -> str:
        """Clan member's profile link."""
        return f"{url.BASE}/en/Profile/index/{int(self.type)}/{self.id}"


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class Clan:
    """Represents a Bungie clan."""

    net: traits.Netrunner = attr.field(repr=False, eq=False, hash=False)
    """A network state used for making external requests."""

    id: int = attr.field(hash=True, repr=True, eq=True)
    """The clan id"""

    type: enums.GroupType = attr.field(repr=True)
    """The clan type."""

    name: str = attr.field(repr=True)
    """The clan's name"""

    created_at: datetime = attr.field(repr=True)
    """Clan's creation date time in UTC."""

    member_count: int = attr.field(repr=True)
    """Clan's member count."""

    motto: str = attr.field(repr=False, eq=False)
    """Clan's motto."""

    is_public: bool = attr.field(repr=False, eq=False)
    """Clan's privacy status."""

    banner: assets.MaybeImage = attr.field(repr=False)
    """Clan's banner"""

    avatar: assets.MaybeImage = attr.field(repr=False)
    """Clan's avatar"""

    about: str = attr.field(repr=False, eq=False)
    """Clan's about title."""

    tags: typing.List[str] = attr.field(repr=False)
    """A list of the clan's tags."""

    owner: helpers.NoneOr[ClanMember] = attr.field(repr=True)
    """The clan owner. This field could be `None` if not found."""

    features: ClanFeatures = attr.field(repr=False, hash=False, eq=False)
    """The clan features."""

    async def fetch_member(
        self, name: str, type: enums.MembershipType = enums.MembershipType.NONE, /
    ) -> ClanMember:
        """Fetch a specific clan member by their name and membership type.

        if the memberhship type is None we will
        try to return the first member matches the name.
        its also better to leave this parameter on None
        since usually only one player has this name.

        Parameters
        ----------
        name: `builtins.str`
            The clan member name.
        type: `aiobungie.MembershipType`
            The member's membership type. Default is 0
            which returns any member matches the name.

        Returns
        --------
        `ClanMember`

        Raises
        ------
        `aiobungie.ClanNotFound`
            The clan was not found.

        `aiobungie.NotFound`
            The member was not found
        """
        return await self.net.request.fetch_clan_member(self.id, name, type)

    async def fetch_members(
        self, type: enums.MembershipType = enums.MembershipType.NONE, /
    ) -> typing.Sequence[ClanMember]:
        """Fetch the members of the clan.

        if the memberhship type is None it will
        All membership types.

        Parameters
        ----------
        type: `aiobungie.MembershipType`
            Filters the membership types to return.
            Default is `aiobungie.MembershipType.NONE` which returns all membership types.

        Returns
        --------
        `typing.Sequence[ClanMember]`
            A sequence of the clan members found in this clan.

        Raises
        ------
        `aiobungie.ClanNotFound`
            The clan was not found.
        """
        return await self.net.request.fetch_clan_members(self.id, type)

    # These ones is not implemented since it
    # requires OAUth2

    async def fetch_banned_members(self) -> typing.Sequence[ClanMember]:
        """Fetch members who has been banned from the clan.

        .. warning::
            This method is still not implemented.

        Returns
        --------
        `typing.Sequence[aiobungie.crate.clans.ClanMember]`
            A sequence of clan members or are banned.
        """
        raise NotImplementedError

    async def fetch_pending_members(self) -> typing.Sequence[ClanMember]:
        """Fetch members who are waiting to get accepted.

        .. warning::
            This method is still not implemented.

        Returns
        --------
        `typing.Sequence[aiobungie.crate.clans.ClanMember]`
            A sequence of clan members who are awaiting
            to get accepted to the clan.
        """
        raise NotImplementedError

    async def fetch_invited_members(self) -> typing.Sequence[ClanMember]:
        """Fetch members who has been invited.

        .. warning::
            This method is still not implemented.

        Returns
        --------
        `typing.Sequence[aiobungie.crate.clans.ClanMember]`
            A sequence of members who have been invited.
        """
        raise NotImplementedError

    @property
    def url(self) -> str:
        return f"{url.BASE}/en/ClanV2/Index?groupId={self.id}"

    def __int__(self) -> int:
        return self.id

    def __str__(self) -> str:
        return self.name
