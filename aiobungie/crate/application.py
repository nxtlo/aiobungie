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

__all__ = ("Application", "ApplicationOwner")

import typing

import attr

from aiobungie import url
from aiobungie.crate import user
from aiobungie.internal import enums
from aiobungie.internal import helpers

if typing.TYPE_CHECKING:
    from datetime import datetime

    from aiobungie.internal import assets
    from aiobungie.internal import traits


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class ApplicationOwner(user.UserLike):
    """Represents a Bungie Application owner."""

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    name: helpers.UndefinedOr[str] = attr.field(repr=True, hash=False, eq=False)
    """The application owner name. This can be `UNDEFINED` if not found."""

    type: enums.MembershipType = attr.field(repr=True, hash=False, eq=True)
    """The membership of the application owner."""

    id: int = attr.field(repr=True, hash=True, eq=True)
    """The application owner's id."""

    icon: assets.MaybeImage = attr.field(repr=False)
    """The application owner's icon."""

    is_public: bool = attr.field(repr=True)
    """The application owner's profile privacy."""

    code: helpers.NoneOr[int] = attr.field(repr=True)
    """The user like's unique display name code.
    This can be None if the user hasn't logged in after season of the lost update.
    """

    async def fetch_self(self) -> user.BungieUser:
        """Fetch the bungie user for this application owner.

        Returns
        -------
        `aiobungie.crate.BungieUser`
            A Bungie net user.

        Raises
        ------
        `aiobungie.UserNotFound`
            The user was not found.
        """
        user_ = await self.net.request.fetch_user(self.id)
        assert isinstance(user_, user.BungieUser)
        return user_

    @property
    def unique_name(self) -> str:
        """The application owner's unique name."""
        return self.unique_name

    @property
    def last_seen_name(self) -> str:
        # This is always undefined since an application
        # dev doesn't have this field.
        return str(helpers.Undefined)

    @property
    def link(self) -> str:
        return f"{url.BASE}/en/Profile/index/{int(self.type)}/{self.id}"


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class Application:
    """Represents a Bungie developer application."""

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

    scope: helpers.UndefinedOr[str] = attr.field(repr=False)
    """App's scope"""

    owner: ApplicationOwner = attr.field(repr=True)
    """App's owner"""

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.id
