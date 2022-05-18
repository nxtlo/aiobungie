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

"""Implementation of Bungie socials and friends."""

from __future__ import annotations

__all__: list[str] = ["Friend", "FriendRequestView"]

import typing

import attrs

from aiobungie.internal import helpers

if typing.TYPE_CHECKING:
    import collections.abc as collections

    from aiobungie import traits
    from aiobungie import typedefs
    from aiobungie import undefined
    from aiobungie.crates import user as user_
    from aiobungie.internal import enums


@attrs.define(kw_only=True)
class FriendRequestView:
    """A view of the pending friend requests queue."""

    incoming: collections.Sequence[Friend]
    """The incoming friend request view."""

    outgoing: collections.Sequence[Friend]
    """The outgoing friend request view."""


@attrs.define(kw_only=True)
class Friend:
    """Represents a bungie friend in your account."""

    net: traits.Netrunner = attrs.field(repr=False, eq=False, hash=False)
    """A network state we use to make external requests."""

    id: int
    """The friend's last seen at id."""

    type: enums.MembershipType
    """The friend's last seen membership type."""

    name: undefined.UndefinedOr[str]
    """The friend's last seen global display name. This field could be Undefined if the player hasn't logged in yet."""

    code: typedefs.NoneOr[int]
    """The friend's last seen global code. This field could be None if the player hasn't logged in yet."""

    online_status: enums.Presence
    """The friend's online status."""

    online_title: int
    """The friend's online title."""

    relationship: enums.Relationship
    """The friend's relationship type."""

    user: typedefs.NoneOr[user_.BungieUser]
    """The friend's bungie user account. This field is optional and can be None in some states."""

    @property
    def unique_name(self) -> str:
        """Friend's global unique display name."""
        return f"{self.name}#{self.code}"

    async def accept(self, access_token: str, /) -> None:
        """Accepts this friend's request.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Raises
        ------
        `aiobungie.NotFound`
            This user was not found in your pending requests.
        """
        await self.net.request.rest.accept_friend_request(access_token, self.id)

    async def decline(self, access_token: str, /) -> None:
        """Decline this friend request.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Raises
        ------
        `aiobungie.NotFound`
            This user is not found in your pending requests.
        """
        await self.net.request.rest.decline_friend_request(access_token, self.id)

    async def remove(self, access_token: str, /) -> None:
        """Removed an existing friend from your friend list.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Raises
        ------
        `aiobungie.NotFound`
            This friend was is found in your friend list.
        """
        await self.net.request.rest.remove_friend(access_token, self.id)

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
        `None`
            None
        """
        await self.net.request.rest.remove_friend_request(access_token, self.id)

    @helpers.unimplemented()
    async def fetch_platform_friends(
        self, access_token: str, /, platform: enums.MembershipType
    ) -> None:
        """Gets the platform friend of the requested type.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        platform : `aiobungie.MembershipType`
            The friend memebrship type.

        Raises
        ------
        `aiobungie.NotFound`
            The requested friend was not found.
        """

    def __str__(self) -> str:
        return self.unique_name

    def __int__(self) -> int:
        return self.id
