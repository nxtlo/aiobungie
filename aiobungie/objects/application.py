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

from typing import Optional, Sequence, Dict, TYPE_CHECKING
from datetime import datetime
from ..utils import Image, Time
from .. import MembershipType
from ..types.application import Application as AppPayload, Team as TeamPayload
from ..types.user import UserCard

__all__: Sequence[str] = ('Application',)

class ApplicationOwner:
    ''' Represents a Bungie Application owner

    Attributes
    -----------
    name: :class:`str`:
        The application owner name.
    id: :class:`int`:
        The application owner bungie id.
    icon: :class:`.Image`:
        The application owner profile icon.
    is_public: :class:`bool`:
        Determines if the application owner's profile was public or private
    type: :class:`.MembershipType`:
        The application owner's bungie membership type.
    '''
    __slots__: Sequence[str] = (
        'name', 'id', 
        'icon', 'is_public', 
        'type',
    )

    def __init__(self, data: UserCard) -> None:
        self.name: str = data['displayName']
        self.type: MembershipType = data['membershipType']
        self.id: int = data['membershipId']
        self.icon: Image = Image(str(data['iconPath']))
        self.is_public: bool = data['isPublic']

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return (
            f"ApplicationOwner name={self.name} id={self.id} is_public={self.is_public}"
            f" icon={self.icon} type={self.type}"
        )

class Application:
    ''' Represents a Bungie developer application.

    Attributes
    -----------
    name: :class:`str`:
        The app's name
    id: :class:`int`:
        The app's id.
    redirect_url: :class:`str`:
        The app's redirect url, None if not Found.
    created_at: :class:`datetime.datetime`:
        The application's creation date in UTC time.
    published_at: :class:`datetime.datetime`
        The application's publish date in UTC time.
    link: :class:`str`:
        The app's link if it exists.
    status: :class:`str`:
        The app's status.
    owner: :class:`.ApplicationOwner`:
        An object of The application owner.
    scope: :class:`str`:
        The app's scope
    '''
    __slots__: Sequence[str] = (
        'id', 
        'name', 
        'redirect_url', 
        'created_at',
        'published_at', 
        'link', 
        'status', 
        'owner',
        'scope'
    )

    def __init__(self, data: AppPayload) -> None:
        self._update(data=data)

    def __int__(self) -> int:
        return int(self.id)

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return str(
            f'Application id={self.id} name={self.name} created_at={self.created_at}'
            f' status={self.status} redirect_url={self.redirect_url} owner={self.owner}'
        )

    def _update(self, data: AppPayload) -> None:
        self.id: int = data['applicationId']
        self.name: str = data['name']
        self.redirect_url: Optional[str] = data.get('redirectUrl', None)
        self.created_at: datetime = Time.clean_date(str(data['creationDate']))
        self.published_at: datetime = Time.clean_date(str(data['firstPublished']))
        self.link: str = data['link']
        self.status: int = data['status']
        self.scope: str = data['scope']
        self.owner: ApplicationOwner = ApplicationOwner(data=data['team'][0]['user']) # type: ignore