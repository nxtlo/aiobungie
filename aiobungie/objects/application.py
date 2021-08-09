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

"""Basic implementation for a Bungie a application."""


from __future__ import annotations

__all__: typing.Sequence[str] = ("Application", "ApplicationOwner")

import typing

import attr

from aiobungie import url

from aiobungie.internal import impl
from ..internal import Image
from ..internal import Time
from ..internal import enums
from .user import UserLike

if typing.TYPE_CHECKING:
    from datetime import datetime


@attr.s(hash=True, repr=True, init=True, kw_only=True, weakref_slot=False, slots=True)
class ApplicationOwner(UserLike):
    """Represents a Bungie Application owner.

    Attributes
    -----------
    name: `builtins.str`
        The application owner name.
    id: `builtins.int`
        The application owner bungie id.
    icon: `aiobungie.internal.assets.Image`
        The application owner profile icon.
    is_public: `builtins.bool`
        Determines if the application owner's profile was public or private
    type: `aiobungie.internal.enums.MembershipType`
        The application owner's bungie membership type.
    """

    name: str = attr.field(repr=True, hash=False, eq=False)
    """The application owner name."""

    type: enums.MembershipType = attr.field(repr=True, hash=False, eq=True)
    """The membership of the application owner."""

    id: int = attr.field(repr=True, hash=True, eq=True)
    """The application owner's id."""

    icon: Image = attr.field(repr=False)
    """The application owner's icon."""

    is_public: bool = attr.field(repr=True)
    """The application owner's profile privacy."""
    
    @property
    def app(self) -> impl.RESTful:
        return self.app

    @property
    def link(self) -> str:
        return f"{url.BASE}/en/Profile/index/{int(self.type)}/{self.id}"

    @property
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """Returns a dict object of the application owner,
        This function is useful if you're binding to other REST apis.
        """
        return dict(
            id=self.id,
            name=self.name,
            is_public=self.is_public,
            icon=str(self.icon),
            type=self.type,
        )


@attr.s(hash=True, repr=True, init=True, kw_only=True, weakref_slot=False, slots=True)
class Application:
    """Represents a Bungie developer application.

    Attributes
    -----------
    name: `builtins.str`
        The app's name
    id: `builtins.int`
        The app's id.
    redirect_url: typing.Optional[`builtins.str`]:
        The app's redirect url, None if not Found.
    created_at: `datetime.datetime`
        The application's creation date in UTC time.
    published_at: `datetime.datetime`
        The application's publish date in UTC time.
    link: `builtins.str`
        The app's link if it exists.
    status: `builtins.str`
        The app's status.
    owner: `aiobungie.objects.ApplicationOwner`
        An object of The application owner.
    scope: `builtins.str`
        The app's scope
    """

    id: int = attr.field(repr=True, hash=True, eq=True)
    """App id"""

    name: str = attr.field(repr=True, hash=False, eq=False)
    """App name"""

    redirect_url: typing.Optional[str] = attr.field(repr=True)
    """App redirect url"""

    created_at: datetime = attr.field(repr=True)
    """App creation date in UTC timezone"""

    published_at: datetime = attr.field(repr=True)
    """App's publish date in UTC timezone"""

    link: str = attr.field(repr=True)
    """App's link"""

    status: int = attr.field(repr=False)
    """App's status"""

    scope: str = attr.field(repr=False)
    """App's scope"""

    owner: ApplicationOwner = attr.field(repr=True)
    """App's owner"""

    @property
    def human_timedelta(self) -> str:
        """Returns a human readble date of the app's creation date."""
        return Time.human_timedelta(self.created_at)

    @property
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """Returns a dict object of the application,
        This function is useful if you're binding to other REST apis.
        """
        return attr.asdict(self)

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.id
