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

from typing import List, Sequence, Dict, Any, Optional, Union, TYPE_CHECKING

from ..internal import Image, Time
from ..error import ClanNotFound
from ..internal.enums import MembershipType

if TYPE_CHECKING:
    from datetime import datetime
    from ..types.clans import ClanImpl, ClanOwnerImpl


class ClanMembers:
    __slots__: Sequence[str] = ()


class ClanOwner:
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
        This could be Xbox, Steam, PSN, Blizzard or ALL, if the membership type is not recognized it will return `builtins.NoneType`.
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

    __slots__: Sequence[str] = (
        "id",
        "name",
        "type",
        "clan_id",
        "icon",
        "is_public",
        "joined_at",
        "types",
        "last_online",
    )

    id: int
    name: str
    last_online: str
    type: Optional[MembershipType]
    clan_id: int
    joined_at: str
    icon: Image
    is_public: bool
    types: List[int]

    def __init__(self, *, data: ClanOwnerImpl) -> None:
        self._update(data)

    def as_dict(self) -> Dict[str, Any]:
        """Returns a dict object of the clan owner,
        This function is useful if you're binding to other REST apis.
        """
        return dict(
            id=self.id,
            name=self.name,
            is_public=self.is_public,
            icon=self.icon,
            types=self.type,
            joined_at=self.joined_at,
            type=self.type,
            clan_id=self.clan_id,
            last_online=self.last_online,
        )

    def _update(self, data: ClanOwnerImpl) -> None:
        self.id = data["destinyUserInfo"]["membershipId"]
        self.name = data["destinyUserInfo"]["displayName"]
        self.icon = Image(str(data["destinyUserInfo"]["iconPath"]))
        convert = int(data["lastOnlineStatusChange"])
        self.last_online = Time.human_timedelta(Time.from_timestamp(convert))
        self.clan_id = data["groupId"]
        self.joined_at = data["joinDate"]
        self.types = data["destinyUserInfo"]["applicableMembershipTypes"]
        self.is_public = data["destinyUserInfo"]["isPublic"]
        self.type = MembershipType(data["destinyUserInfo"].get("membershipType", None))

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f"ClaOwner name={self.name} id={self.id} type={self.type} last_online={self.last_online}"

    def __bool__(self) -> bool:
        return self.is_public


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

    __slots__: Sequence[str] = (
        "id",
        "name",
        "created_at",
        "member_count",
        "description",
        "is_public",
        "banner",
        "avatar",
        "about",
        "tags",
        "owner",
    )

    id: int
    name: str
    created_at: datetime
    member_count: int
    description: str
    is_public: bool
    banner: Image
    avatar: Image
    about: str
    tags: List[str]
    owner: ClanOwner

    def __init__(self, data: ClanImpl) -> None:
        self._update(data=data)

    def as_dict(self) -> Dict[str, Any]:
        """Returns a dict object of the player,
        This function is useful if you're binding to other REST apis.
        """
        return dict(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            is_public=self.is_public,
            avatar=self.avatar,
            banner=self.banner,
            about=self.about,
            description=self.description,
            tags=self.tags,
            owner=self.owner,
        )

    def _update(self, data: ClanImpl) -> None:
        self.id = data["detail"]["groupId"]
        self.name = data["detail"]["name"]
        self.created_at = data["detail"]["creationDate"]
        self.member_count = data["detail"]["memberCount"]
        self.description = data["detail"]["about"]
        self.about = data["detail"]["motto"]
        self.is_public = data["detail"]["isPublic"]
        self.banner = Image(str(data["detail"]["bannerPath"]))
        self.avatar = Image(str(data["detail"]["avatarPath"]))
        self.tags = data["detail"]["tags"]
        self.owner = ClanOwner(data=data["founder"])

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> Union[Any, str]:
        return (
            f"<Clan id={self.id} name={self.name} created_at={self.created_at}"
            f" owner={self.owner} is_public={self.is_public} about={self.about}"
        )
