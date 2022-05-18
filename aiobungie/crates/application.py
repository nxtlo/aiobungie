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

"""Basic implementation of a Bungie a application."""


from __future__ import annotations

__all__ = ("Application", "ApplicationOwner")

import typing

import attrs

from aiobungie import undefined
from aiobungie import url
from aiobungie.crates import user
from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    from datetime import datetime

    from aiobungie import traits
    from aiobungie import typedefs
    from aiobungie.internal import assets


@attrs.define(kw_only=True)
class ApplicationOwner(user.UserLike):
    """Represents a Bungie Application owner."""

    net: traits.Netrunner = attrs.field(repr=False, hash=False, eq=False)
    """A network state used for making external requests."""

    name: undefined.UndefinedOr[str]
    """The application owner name. This can be `UNDEFINED` if not found."""

    type: enums.MembershipType
    """The membership of the application owner."""

    id: int
    """The application owner's id."""

    icon: assets.Image
    """The application owner's icon."""

    is_public: bool
    """The application owner's profile privacy."""

    code: typedefs.NoneOr[int]
    """The user like's unique display name code.
    This can be None if the user hasn't logged in after season of the lost update.
    """

    async def fetch_self(self) -> user.BungieUser:
        """Fetch the bungie user for this application owner.

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

    @property
    def last_seen_name(self) -> str:
        """The last seen name of the application owner. This will always returns `UNDEFINED`."""
        return str(undefined.Undefined)

    @property
    def link(self) -> str:
        return f"{url.BASE}/en/Profile/index/{int(self.type)}/{self.id}"


@attrs.define(kw_only=True)
class Application:
    """Represents a Bungie developer application."""

    id: int
    """App id"""

    name: str
    """App name"""

    redirect_url: typing.Optional[str]
    """App redirect url"""

    created_at: datetime
    """App creation date in UTC timezone"""

    published_at: datetime
    """App's publish date in UTC timezone"""

    link: str
    """App's link"""

    status: int
    """App's status"""

    scope: undefined.UndefinedOr[str]
    """App's scope"""

    owner: ApplicationOwner
    """App's owner"""

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.id
