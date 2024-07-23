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

__all__ = ("Application", "ApplicationMember")

import typing

import attrs

from aiobungie.crates import user as _user

if typing.TYPE_CHECKING:
    import collections.abc as collections
    from datetime import datetime


@attrs.frozen(kw_only=True)
class ApplicationMember:
    """Represents a Bungie developer-portal application team member."""

    role: int
    """The role of the application team member.

    To convert this to a string, use `.role_as_str` method.
    """

    api_eula_version: int
    """The EULA version of the API."""

    user: _user.PartialBungieUser
    """The Bungie.net user associated with the application team member."""

    def role_as_str(self) -> typing.Literal["Owner", "Member", "None"]:
        """Returns the role of the application team member as a string."""
        if self.role == 0:
            return "None"
        elif self.role == 1:
            return "Owner"

        return "Member"


@attrs.frozen(kw_only=True)
class Application:
    """Represents a Bungie developer application."""

    id: int
    """The application's id"""

    name: str
    """The application's name"""
    """App name"""

    redirect_url: str | None
    """The application's redirect url"""

    created_at: datetime
    """the application's creation date."""

    status_changed: datetime
    """If the application recently changed status, this will its datetime."""

    published_at: datetime
    """The application's publish date"""

    link: str
    """The application's link."""

    status: int
    """The application's status"""

    scope: str | None
    """Scopes that're supported by this application."""

    team: collections.Sequence[ApplicationMember]
    """A sequence of the application members."""

    origin: str
    """Origin field of this application."""
