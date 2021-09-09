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

"""A collection and entities of Bungie's Destiny players memberships."""

# This was supposed to be used for the `DestinyUser` object
# But it will be present here for future ideas.

from __future__ import annotations

__all__: list[str] = ["StadiaMember", "XboxMember", "PSNMember", "SteamMember"]

import typing

import attr

from aiobungie.crate import user
from aiobungie.internal import assets
from aiobungie.internal import enums
from aiobungie.internal import helpers


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class StadiaMember(user.UserLike):
    """Represent a Stadia membership for a bungie user.

    .. versionadded:: 0.2.5
    """

    id: int = attr.field(repr=True, hash=True, eq=True)
    """The member's id."""

    name: str = attr.field(repr=True, eq=False)
    """The member's name."""

    last_seen_name: str = attr.field(repr=True)
    """The member's last seen display name. You may use this field if `StadiaMember.name` is `Undefined`."""

    type: enums.MembershipType = attr.field(repr=True)
    """The member's membership type."""

    types: typing.Sequence[enums.MembershipType] = attr.field(repr=False)
    """A sequence of the member's membership types."""

    icon: assets.MaybeImage = attr.field(repr=False)
    """The profile's icon if it was present."""

    code: helpers.NoneOr[int] = attr.field(repr=True, eq=True, hash=False)
    """The member's name code. This field may be `None` if not found."""

    is_public: bool = attr.field(repr=False)
    """The member's profile privacy status."""

    @property
    def unique_name(self) -> helpers.NoneOr[str]:
        """The member's unique name. This field may be `None` or `Undefined` if not found."""
        return f"{self.name}#{self.code}"

    @property
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        return attr.asdict(self)


@attr.define(hash=True, kw_only=True, weakref_slot=False)
class XboxMember(user.UserLike):
    """Represent an Xbox membership for a bungie user.

    .. versionadded:: 0.2.5
    """

    id: int = attr.field(repr=True, hash=True, eq=True)
    """The member's id."""

    name: str = attr.field(repr=True, eq=False)
    """The member's name."""

    last_seen_name: str = attr.field(repr=True)
    """The member's last seen display name. You may use this field if `XboxMember.name` is `Undefined`."""

    type: enums.MembershipType = attr.field(repr=True)
    """The member's membership type."""

    types: typing.Sequence[enums.MembershipType] = attr.field(repr=False)
    """A sequence of the member's membership types."""

    icon: assets.MaybeImage = attr.field(repr=False)
    """The profile's icon if it was present."""

    code: helpers.NoneOr[int] = attr.field(repr=True, eq=True, hash=False)
    """The member's name code. This field may be `None` if not found."""

    is_public: bool = attr.field(repr=False)
    """The member's profile privacy status."""

    @property
    def unique_name(self) -> helpers.NoneOr[str]:
        """The member's unique name. This field may be `None` or `Undefined` if not found."""
        return f"{self.name}#{self.code}"

    @property
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        return attr.asdict(self)


@attr.define(hash=True, kw_only=True, weakref_slot=False)
class PSNMember(user.UserLike):
    """Represent a PSN membership for a bungie user.

    .. versionadded:: 0.2.5
    """

    id: int = attr.field(repr=True, hash=True, eq=True)
    """The member's id."""

    name: str = attr.field(repr=True, eq=False)
    """The member's name."""

    last_seen_name: str = attr.field(repr=True)
    """The member's last seen display name. You may use this field if `PSNMember.name` is `Undefined`."""

    type: enums.MembershipType = attr.field(repr=True)
    """The member's membership type."""

    types: typing.Sequence[enums.MembershipType] = attr.field(repr=False)
    """A sequence of the member's membership types."""

    icon: assets.MaybeImage = attr.field(repr=False)
    """The profile's icon if it was present."""

    code: helpers.NoneOr[int] = attr.field(repr=True, eq=True, hash=False)
    """The member's name code. This field may be `None` if not found."""

    is_public: bool = attr.field(repr=False)
    """The member's profile privacy status."""

    @property
    def unique_name(self) -> helpers.NoneOr[str]:
        """The member's unique name. This field may be `None` or `Undefined` if not found."""
        return f"{self.name}#{self.code}"

    @property
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        return attr.asdict(self)


@attr.define(hash=True, kw_only=True, weakref_slot=False)
class SteamMember(user.UserLike):
    """Represent a Steam membership for a bungie user.

    .. versionadded:: 0.2.5
    """

    id: int = attr.field(repr=True, hash=True, eq=True)
    """The member's id."""

    name: str = attr.field(repr=True, eq=False)
    """The member's name."""

    last_seen_name: str = attr.field(repr=True)
    """The member's last seen display name. You may use this field if `SteamMember.name` is `Undefined`."""

    type: enums.MembershipType = attr.field(repr=True)
    """The member's membership type."""

    types: typing.Sequence[enums.MembershipType] = attr.field(repr=False)
    """A sequence of the member's membership types."""

    icon: assets.MaybeImage = attr.field(repr=False)
    """The profile's icon if it was present."""

    code: helpers.NoneOr[int] = attr.field(repr=True, eq=True, hash=False)
    """The member's name code. This field may be `None` if not found."""

    is_public: bool = attr.field(repr=False)
    """The member's profile privacy status."""

    @property
    def unique_name(self) -> helpers.NoneOr[str]:
        """The member's unique name. This field may be `None` or `Undefined` if not found."""
        return f"{self.name}#{self.code}"

    @property
    def as_dict(self) -> typing.Dict[str, typing.Any]:
        return attr.asdict(self)
