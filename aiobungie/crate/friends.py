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

__all__: list[str] = ["Friend", "FriendRequestView"]

import typing

import attr

if typing.TYPE_CHECKING:
    from aiobungie.crate import user as user_
    from aiobungie.internal import enums
    from aiobungie.internal import helpers
    from aiobungie.internal import traits


@attr.define(weakref_slot=False, hash=False, kw_only=True)
class FriendRequestView:
    """A view of the pending friend requests queue."""

    incoming: typing.Sequence[Friend] = attr.field(repr=True, hash=False)
    """The incoming friend request view."""

    outgoing: typing.Sequence[Friend] = attr.field(repr=True, hash=False)
    """The outgoing friend request view."""


@attr.define(weakref_slot=False, hash=False, kw_only=True)
class Friend:
    """Represents a bungie friend in your account."""

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

    async def accept(self, access_token: str, /) -> None:
        """Accepts a friend request.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Raises
        ------
        `aiobungie.NotFound`
            The friend was not found in your pending requests.
        """
        await self.net.request.rest.accept_friend_request(access_token, self.id)

    async def decline(self, access_token: str, /) -> None:
        """Decline a friend request.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Raises
        ------
        `aiobungie.NotFound`
            The friend was not found in your pending requests.
        """
        await self.net.request.rest.decline_friend_request(access_token, self.id)

    async def add(self, access_token: str, /) -> None:
        """Adds a bungie member to your friend list.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Raises
        ------
        `aiobungie.NotFound`
            The player was not found.
        """
        await self.net.request.rest.send_friend_request(access_token, self.id)

    async def remove(self, access_token: str, /) -> None:
        """Removed an existing friend from your friend list.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Raises
        ------
        `aiobungie.NotFound`
            The friend was not found in your friend list.
        """
        await self.net.request.rest.remove_friend(access_token, self.id)

    async def pending(self, access_token: str, /) -> FriendRequestView:
        """Returns the pending friend requests.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Returns
        -------
        `FriendRequestView`
            A friend requests view object includes a sequence of incoming and outgoing requests.
        """
        return await self.net.request.fetch_friend_requests(access_token)

    async def remove_request(self, access_token: str, /) -> None:
        """Removed an existing friend request.

        .. note::
            The friend request must be on your friend request list.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Returns
        -------
        `builtins.NoneType`
            None
        """
        await self.net.request.rest.remove_friend_request(access_token, self.id)

    # N/A ?
    # async def fetch_platform_friends(self, access_token: str, /, platform: enums.MembershipType) -> None:
    #     """Gets the platform friend of the requested type.

    #     Parameters
    #     ----------
    #     access_token : `str`
    #         The bearer access token associated with the bungie account.
    #     platform : `aiobungie.MembershipType`
    #         The friend memebrship type.

    #     Raises
    #     ------
    #     `aiobungie.NotFound`
    #         The requested friend was not found.
    #     """

    async def is_pending(self, access_token: str, /, id: int) -> bool:
        """Check if a member is in the pending incoming requests by their id.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        id: `int`
            The member's id to look up.

        Returns
        -------
        `bool`
            A boolean `True` if the passed id is in the pending friend list. `False` if not.
        """
        pending_requests = await self.pending(access_token)
        for friend_request in pending_requests.incoming:
            if id == friend_request.id:
                return True
        return False
