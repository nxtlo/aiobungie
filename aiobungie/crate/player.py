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

"""Basic implementation for a Bungie a player."""


from __future__ import annotations

__all__ = ("Player",)


import typing

import attr

from aiobungie.crate.user import UserLike
from aiobungie.internal import Image
from aiobungie.internal import impl
from aiobungie.internal.enums import MembershipType


@attr.s(hash=True, repr=True, init=True, kw_only=True, weakref_slot=False, slots=True)
class Player(UserLike):
    """Represents a Bungie Destiny 2 Player."""

    icon: Image = attr.field(repr=False, hash=False, eq=False)
    """The player's icon."""

    id: int = attr.field(repr=True, hash=True)
    """The player's id."""

    name: str = attr.field(repr=True, eq=False, hash=False)
    """The player's name"""

    is_public: bool = attr.field(repr=True, eq=True, hash=False)
    """The player's profile privacy."""

    type: MembershipType = attr.field(repr=True, eq=True, hash=False)
    """The profile's membership type."""

    @property
    def net(self) -> impl.Netrunner:
        """A network state used for making external requests."""
        return self.net

    @property
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """Returns a dict object of the player."""

        return attr.asdict(self)

    def __int__(self) -> int:
        return int(self.id)

    def __str__(self) -> str:
        return self.name
