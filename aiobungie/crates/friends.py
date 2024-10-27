# pyright: reportIncompatibleMethodOverride = false
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

"""Basic implementation of Bungie socials and friends resources."""

from __future__ import annotations

__all__ = ("Friend", "FriendRequestView")

import typing

import attrs

from aiobungie.crates import user as user_

if typing.TYPE_CHECKING:
    import collections.abc as collections

    from aiobungie.internal import enums


@attrs.frozen(kw_only=True)
class FriendRequestView:
    """A view of the pending friend requests queue."""

    incoming: collections.Sequence[Friend]
    """The incoming friend request view."""

    outgoing: collections.Sequence[Friend]
    """The outgoing friend request view."""


@attrs.frozen(kw_only=True)
class Friend(user_.Unique):
    """Represents a bungie friend in your account."""

    id: int
    """The friend's last seen at id."""

    type: enums.MembershipType
    """The friend's last seen membership type."""

    name: str | None
    """The friend's last seen global display name. This field could be UNDEFINED if the player hasn't logged in yet."""

    code: int | None
    """The friend's last seen global code. This field could be None if the player hasn't logged in yet."""

    online_status: enums.Presence
    """The friend's online status."""

    online_title: int
    """The friend's online title."""

    relationship: enums.Relationship
    """The friend's relationship type."""

    user: user_.BungieUser | None
    """The friend's bungie user account. This field is optional and can be None in some states."""
