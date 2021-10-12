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

"""Bungie social and friends crate."""

from __future__ import annotations

__all__: list[str] = ["Friend"]

import typing

import attr

from aiobungie.crate import user as user_

if typing.TYPE_CHECKING:
    from aiobungie.internal import enums
    from aiobungie.internal import helpers
    from aiobungie.internal import traits


@attr.define(slots=True, init=True, weakref_slot=False, hash=True, repr=True)
class Friend(user_.UserLike):
    """Represents a bungie friend in your account..

    .. versionadded:: 0.2.5
    """

    net: traits.Netrunner = attr.field(repr=False)
    """A network state we use to make external requests."""

    id: int = attr.field(repr=False, hash=True)
    """The friend's last seen at id."""

    type: enums.MembershipType = attr.field(repr=True)
    """The friend's last seen membership type."""

    name: helpers.UndefinedOr[str] = attr.field(repr=True)
    """The friend's last seen global display name. This field could be Undefined if the player hasn't logged in yet."""

    code: helpers.NoneOr[int] = attr.field(repr=True)
    """The friend's last seen global code. This field could be None if the player hasn't logged in yet."""

    online_status: enums.Presence = attr.field(repr=False)
    """The friend's online status."""

    online_title: int = attr.field(repr=False)
    """The friend's online title."""

    relationship: enums.Relationship = attr.field(repr=False)
    """The friend's relationship type."""

    user: helpers.NoneOr[user_.User] = attr.field(repr=True)
    """The friend's bungie user account. This field is optional and can be None in some states."""

    @property
    def unique_name(self) -> str:
        """The friend's global unique display name. This field could be None if the player hasn't logged in yet."""
        return self.unique_name

    # POST methods will not be implemented currently.

    async def accept(self, id: int, /) -> None:
        """Accepts a friend request.

        Parameters
        ----------
        id : `builtins.int`
            The friend's id you want to accept.

        Returns
        -------
        `builtins.NoneType`
            None

        Raises
        ------
        `aiobungie.NotFound`
            The friend was not found in your pending requests.

        """

    async def decline(self, id: int, /) -> None:
        """Decline a friend request.

        Parameters
        ----------
        id : `builtins.int`
            The friend's id you want to decline.

        Returns
        -------
        `builtins.NoneType`
            None

        Raises
        ------
        `aiobungie.NotFound`
            The friend was not found in your pending requests.
        """

    async def add(self, id: int, /) -> None:
        """Adds a bungie member to your friend list.

        Parameters
        ----------
        id : `builtins.int`
            The friend's id you want to add.

        Returns
        -------
        `builtins.NoneType`
            None

        Raises
        ------
        `aiobungie.NotFound`
            The player was not found.
        """

    async def remove(self, id: int, /) -> None:
        """Removed an existing friend from your friend list.

        Parameters
        ----------
        id : `builtins.int`
            The friend's id you want to remove.

        Returns
        -------
        `builtins.NoneType`
            None

        Raises
        ------
        `aiobungie.NotFound`
            The friend was not found in your friend list.
        """

    async def pending(self) -> typing.Sequence[Friend]:
        """Returns the pending friend requests.

        Parameters
        ----------
        id : `builtins.int`
            The friend's id you want to remove.

        Returns
        -------
        `typing.Sequence[Friend]`
            A sequence of pending friend requests.
        """

    async def remove_request(self, id: int, /) -> None:
        """Removed an existing friend request.

        .. note::
            The friend request must be on your friend request list.

        Parameters
        ----------
        id : `builtins.int`
            The friend's id you want to remove.

        Returns
        -------
        `builtins.NoneType`
            None
        """

    async def fetch_platform_friends(self, platform: enums.MembershipType, /) -> None:
        """Gets the platform friend of the requested type.

        Parameters
        ----------
        platform : `aiobungie.MembershipType`
            The friend memebrship type.

        Raises
        ------
        `aiobungie.NotFound`
            The requested friend was not found.
        """

    async def is_pending(self, id: int) -> bool:
        for friend in await self.pending():
            if id == friend.id:
                return True
        return False
