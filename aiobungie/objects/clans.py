'''
MIT License

Copyright (c) 2020 - Present nxtlo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from datetime import datetime
from typing import (
    List,
    Sequence,
    Dict,
    Any,
    Optional,
    Union,
    TYPE_CHECKING
)

# if TYPE_CHECKING:
from ..utils import ImageProtocol, Time
from ..utils.enums import MembershipType
from ..types.clans import Clans as ClanPayload

class ClanMembers:
    ...

class ClanOwner:
    '''Represents a Bungie clan owner.

    Attributes
    -----------
    id: :class:`int`:
        The clan owner's membership id

    name: :class:`str`:
        The clan owner's display name

    last_online: :class:`str`:
        An aware :class:`str` version of a :class:`datetime.datetime.utc_now()` object.

    type: :class:`.MembershipType`:
        Returns the clan owner's membership type.
        This could be Xbox, Steam, PSN, Blizzard or ALL, it the membershiptype is not recognized it will return ``None``.
    
    clan_id: :class:`int`:
        The clan owner's clan id

    joined_at: Optional[:class:`datetime.utcnow()`]


    icon: :class:`.ImageProtocol`:
        Returns the clan owner's icon from ImageProtocol.

    is_public: :class:`bool`:
        Returns True if the clan's owner profile is public or False if not.

    types: :class:List[:class:`int`]:
        returns a List of :class:`int` of the clan owner's types.
    
    '''
    __slots__: Sequence[str] = (
        'id', 'name', 'type',
        'clan_id', 'icon', 'is_public',
        'joined_at', 'types', 'last_online'
    )
    if TYPE_CHECKING:
        id: int
        name: str
        last_online: str
        type: MembershipType
        clan_id: int
        joined_at: datetime
        icon: ImageProtocol
        is_public: bool
        types: List[int]

    def __init__(self, *, data) -> None:
        self._update(data)

    def _update(self, data) -> None:
        data = data['founder']
        self.id: int = data['destinyUserInfo']['membershipId']
        self.name: str = data['destinyUserInfo']['displayName']
        self.icon: ImageProtocol = ImageProtocol(data['destinyUserInfo']['iconPath'])
        self.last_online: str = Time.from_timestamp(data['lastOnlineStatusChange'])
        self.clan_id: int = data['groupId']
        self.joined_at: datetime = data['joinDate']
        self.types: List[int] = data['destinyUserInfo']['applicableMembershipTypes']
        self.is_public: bool = data['destinyUserInfo']['isPublic']
        self.type: MembershipType = MembershipType(data=data['destinyUserInfo']['membershipType'])


    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return (
            f'ClaOwner name={self.name} id={self.id} type={self.type} last_online={self.last_online}'
        )

    def __bool__(self) -> bool:
        return self.is_public

class Clan:
    """Represents a Bungie clan.

    Attributes
    -----------
    name: :class:`str`:
        The clan's name
    
    id: :class:`int`:
        The clans's id

    created_at: :class:`datetime.utcnow()`:
        Returns the clan's creation date in UTC time.

    description: :class:`str`:
        The clan's description.

    is_public: :class:`bool`:
        Returns True if the clan is public and False if not.

    banner: :class:`.ImageProtocol`:
        Returns the clan's banner

    avatar: :class:`.ImageProtocol`:
        Returns the clan's avatar

    about: :class:`str`:
        The clan's about.

    tag: :class:`str`:
        The clan's tag

    owner: :class:`.ClanOwner`:
        Returns an object of the clan's owner.
        See :class:`.ClanOwner` for info.
    """
    __slots__: Sequence[str] = (
        'id', 'name', 'created_at', 'edited_at',
        'member_count', 'description', 'is_public',
        'banner', 'avatar', 'about', 'tag', 'owner'
    )
    if TYPE_CHECKING:
        id: int
        name: str
        created_at: datetime
        member_count: int
        description: Any
        is_public: bool
        banner: ImageProtocol
        avatar: ImageProtocol
        about: str
        tag: str
        owner: ClanOwner

    def __init__(self, data: Any) -> None:
        self._update(data=data)

    def _update(self, data) -> None:
        data = data['Response']
        self.id: int = data['detail']['groupId']
        self.name = data['detail']['name']
        self.created_at = data['detail']['creationDate']
        self.member_count = data['detail']['memberCount']
        self.description = data['detail']['about']
        self.about = data['detail']['motto']
        self.is_public = data['detail']['isPublic']
        self.banner = ImageProtocol(data['detail']['bannerPath'])
        self.avatar = ImageProtocol(data['detail']['avatarPath'])
        self.tag = data
        self.owner = ClanOwner(data=data)

    def __str__(self) -> str:
        return str(self.name)


    def __repr__(self) -> Union[Any, str]:
        return (
            f'<Clan id={self.id} name={self.name} created_at={self.created_at}'
            f' owner={self.owner} is_public={self.is_public} about={self.about}'
        )