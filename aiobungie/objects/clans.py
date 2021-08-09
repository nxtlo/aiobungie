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

__all__: typing.List[str] = ["Clan", "ClanOwner", "ClanMember", "ClanFeatures"]


import typing

import attr

from aiobungie import url
from aiobungie.internal import impl

from ..internal import Image
from ..internal import Time
from ..internal.enums import MembershipType, GroupType
from .user import UserLike

if typing.TYPE_CHECKING:
    import types
    from datetime import datetime


@attr.s(eq=True, hash=True, init=True, kw_only=True, slots=True, weakref_slot=False)
class ClanFeatures:
    """Implementation of a bungie clan features."""

    max_members: int = attr.field(repr=True)
    """The maximum members the clan can have"""

    max_membership_types: int = attr.field(repr=False)
    """The maximum membership types the clan can have"""

    capabilities: int = attr.field(repr=False)
    """An int that represents the clan's capabilities."""

    membership_types: typing.List[MembershipType] = attr.field(repr=True)
    """The clan's membership types."""

    invite_permissions: bool = attr.field(repr=False)
    """True if the clan has permissions to invite."""

    update_banner_permissions: bool = attr.field(repr=False)
    """True if the clan has permissions to updates its banner."""

    update_culture_permissions: bool = attr.field(repr=False)

    join_level: int = attr.field(repr=True)
    """The clan's join level."""


@attr.s(eq=True, hash=True, init=True, kw_only=True, slots=True, weakref_slot=False)
class ClanMember(UserLike):
    """Represents a Destiny 2 clan member."""

    app: impl.RESTful = attr.field(repr=False)
    """A client app that we may use for externalr requests."""

    id: int = attr.field(repr=True, hash=True)
    """Clan member's id"""

    name: str = attr.field(repr=True)
    """Clan member's name"""

    type: MembershipType = attr.field(repr=True)
    """Clan member's membership type."""

    icon: Image = attr.field(repr=False)
    """Clan member's icon"""

    is_public: bool = attr.field(repr=True)
    """`builtins.True` if the clan member is public."""

    group_id: int = attr.field(repr=True)
    """The member's group id."""

    is_online: bool = attr.field(repr=True)
    """True if the clan member is online or not."""

    last_online: datetime = attr.field(repr=False)
    """The date of the clan member's last online in UTC time zone."""

    joined_at: datetime = attr.field(repr=False)
    """The clan member's join date in UTC time zone."""

    @property
    def link(self) -> typing.Optional[str]:
        """Clan member's profile link."""
        return f"{url.BASE}/en/Profile/index/{int(self.type)}/{self.id}"

    @property
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        return attr.asdict(self)

    # These are not implemented yet
    # Since they requires OAuth2.

    async def ban(self) -> None:
        """Bans a clan member from the clan.
        This requires OAuth2: AdminGroups scope.
        """
        raise NotImplementedError

    async def unban(self) -> None:
        """Unbans a clan member clan.
        This requires OAuth2: AdminGroups scope.
        """
        raise NotImplementedError

    async def kick(self) -> None:
        """Kicks a clan member from the clan.
        The requires OAuth2: AdminsGroup scope.
        """
        raise NotImplementedError


@attr.s(eq=True, hash=True, init=True, kw_only=True, slots=True, weakref_slot=False)
class ClanOwner(UserLike):
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

    id: int = attr.field(hash=True, repr=True)
    """The user id."""

    name: str = attr.field(repr=True)
    """The user name."""

    is_public: typing.Optional[bool] = attr.field(hash=False, repr=True, eq=False)
    """Returns if the user profile is public or no."""

    type: MembershipType = attr.field(hash=False, repr=True, eq=True)
    """Returns the membership type of the user."""

    types: typing.Optional[typing.List[int]] = attr.field(
        hash=True, repr=False, eq=False
    )
    """Returns a list of the member ship's membership types."""

    last_online: datetime = attr.field(repr=False)
    """An aware `datetime.datetime` object of the user's last online date UTC."""

    clan_id: int = attr.field(repr=True)
    """Owner's current clan id."""

    icon: Image = attr.field(repr=False)
    """Owner's profile icom"""

    joined_at: datetime = attr.field(repr=True)
    """Owner's bungie join date."""

    @property
    def human_timedelta(self) -> str:
        """Returns a human readble date of the clan owner's last login."""
        return Time.human_timedelta(self.last_online)

    @property
    def link(self) -> typing.Optional[str]:
        """Returns the user's profile link."""
        return f"{url.BASE}/en/Profile/index/{int(self.type)}/{self.id}"

    @property
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """Returns a dict object of the clan owner,
        This function is useful if you're binding to other REST apis.
        """
        return attr.asdict(self)

    def __int__(self) -> int:
        return self.id

    def __str__(self) -> str:
        return self.name


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

    app: impl.RESTful = attr.field(repr=False, eq=False, hash=False)
    """A client app the we may use for external requests."""

    id: int = attr.field(hash=True, repr=True, eq=True)
    """The clan id"""

    type: GroupType = attr.field(repr=True)
    """The clan type."""

    name: str = attr.field(repr=True)
    """The clan's name"""

    created_at: datetime = attr.field(repr=True)
    """Clan's creation date time in UTC."""

    member_count: int = attr.field(repr=True)
    """Clan's member count."""

    description: str = attr.field(repr=True, eq=False)
    """Clan's description"""

    is_public: bool = attr.field(repr=True, eq=False)
    """Clan's privacy status."""

    banner: Image = attr.field(repr=False)
    """Clan's banner"""

    avatar: Image = attr.field(repr=False)
    """Clan's avatar"""

    about: str = attr.field(repr=True, eq=False)
    """Clan's about title."""

    tags: typing.List[str] = attr.field(repr=False)
    """A list of the clan's tags."""

    owner: ClanOwner = attr.field(repr=True)
    """The clan owner."""

    features: ClanFeatures = attr.field(repr=False, hash=False, eq=False)
    """The clan features."""

    async def fetch_member(
        self, name: str, type: MembershipType = MembershipType.NONE, /
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
        """
        return await self.app.rest.fetch_clan_member(self.id, name, type)

    async def fetch_members(
        self, type: MembershipType = MembershipType.NONE, /
    ) -> typing.Dict[str, int]:
        """Fetch the members of the clan.

        if the memberhship type is None it will
        All membership types.

        Parameters
        ----------
        type: `aiobungie.MembershipType`
            Filters the membership types to return.
            Default is 0 which returns all membership types.

        Returns
        --------
        `typing.Dict[str, int]`
            A dict that holds a key of the clan members's name
            and a value of the clan members's id.
        """
        return await self.app.rest.fetch_clan_members(self.id, type)

    # These ones is not implemented since it 
    # requires OAUth2

    async def fetch_banned_members(
        self
    ) -> typing.Sequence[ClanMember]:
        """Fetch members who has been banned from the clan.

        Returns
        --------
        `typing.Sequence[aiobungie.objects.clans.ClanMember]`
            A sequence of clan members or are banned.
        """
        raise NotImplementedError

    async def fetch_pending_members(
        self
    ) -> typing.Sequence[ClanMember]:
        """Fetch members who are waiting to get accepted.

        Returns
        --------
        `typing.Sequence[aiobungie.objects.clans.ClanMember]`
            A sequence of clan members who are awaiting 
            to get accepted to the clan.
        """
        raise NotImplementedError

    async def fetch_invited_members(
        self
    ) -> typing.Sequence[ClanMember]:
        """Fetch members who has been invited.

        Returns
        --------
        `typing.Sequence[aiobungie.objects.clans.ClanMember]`
            A sequence of members who have been invited.
        """
        raise NotImplementedError

    @property
    def human_timedelta(self) -> str:
        """Returns a human readble date of the clan's creation date."""
        return Time.human_timedelta(self.created_at)

    @property
    def url(self) -> str:
        return f"{url.BASE}/en/ClanV2/Index?groupId={self.id}"

    @property
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """Returns an instance of the object as a dict"""
        return attr.asdict(self)

    def __int__(self) -> int:
        return self.id

    def __str__(self) -> str:
        return self.name
