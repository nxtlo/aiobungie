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

"""Implementation of a Bungie a profile."""

from __future__ import annotations

__all__: tuple[str, ...] = (
    "Profile",
    "LinkedProfile",
    "ProfileProgression",
    "ProfileItemImpl",
)

import datetime
import typing

import attrs

from aiobungie.crates import entity
from aiobungie.crates import user
from aiobungie.internal import enums
from aiobungie.internal import helpers

if typing.TYPE_CHECKING:
    import collections.abc as collections

    from aiobungie import traits
    from aiobungie.crates import components
    from aiobungie.crates import season


@attrs.define(kw_only=True)
class LinkedProfile:
    """Represents a membership linked profile information summary."""

    net: traits.Netrunner = attrs.field(repr=False, eq=False, hash=False)
    """A network state used for making external requests."""

    profiles: collections.Sequence[user.DestinyMembership]
    """A sequence of destiny memberships for this profile."""

    bungie: user.PartialBungieUser
    """The profile's bungie membership."""

    profiles_with_errors: typing.Optional[collections.Sequence[user.DestinyMembership]]
    """A sequence of optional destiny memberships with errors.

    These profiles exists because they have missing fields. Otherwise this will be an empty array.
    """


@attrs.define(kw_only=True)
class ProfileProgression:
    """Represents a profile progression component details."""

    artifact: season.Artifact
    """The profile progression seasonal artifact."""

    # No repr for this since its kinda huge dict.
    checklist: collections.Mapping[int, collections.Mapping[int, bool]]
    """A mapping of int to another mapping of int to bool for the profile progression checklist."""


@attrs.mutable(kw_only=True)
class ProfileItemImpl:
    """Concrete implementation of any profile component item.

    This also can be a character equipment i.e. Weapons, Armor, Ships, etc.
    """

    net: traits.Netrunner = attrs.field(repr=False, hash=False, eq=False)
    """A network state used for making external requests."""

    hash: int
    """The item type hash."""

    quantity: int
    """The item quantity."""

    bind_status: enums.ItemBindStatus
    """The item binding status."""

    location: enums.ItemLocation
    """The item location."""

    bucket: int
    """The item bucket hash."""

    transfer_status: enums.TransferStatus
    """The item's transfer status."""

    lockable: bool
    """Whether the item can be locked or not."""

    state: enums.ItemState
    """The item's state."""

    dismantel_permissions: int
    """The item's dismantel permission."""

    is_wrapper: bool
    """Whether the item is a wrapper or not."""

    instance_id: typing.Optional[int]
    """An inventory item instance id if available, otherwise will be `None`."""

    ornament_id: typing.Optional[int]
    """The ornament id of this item if it has one. Will be `None` otherwise."""

    version_number: typing.Optional[int]
    """The item version number of available, other wise will be `None`."""

    @property
    def is_transferable(self) -> bool:
        """Check whether this item can be transferred or not."""
        return (
            self.transfer_status is enums.TransferStatus.CAN_TRANSFER
            and self.instance_id is not None  # noqa: W503
        )

    async def fetch_self(self) -> entity.InventoryEntity:
        """Fetch this profile item.

        Returns
        -------
        `aiobungie.crates.InventoryEntity`
            An inventory item definition entity.
        """
        return await self.net.request.fetch_inventory_item(self.hash)

    def __int__(self) -> int:
        return self.hash


@attrs.define(kw_only=True)
class Profile:
    """Represents a Bungie member profile-only component.

    This is only a `PROFILE` component and not the profile itself.
    See `aiobungie.crates.Component` for other components.
    """

    id: int
    """Profile's id"""

    net: traits.Netrunner = attrs.field(repr=False, hash=False, eq=False)
    """A network state used for making external requests."""

    name: str
    """Profile's name."""

    type: enums.MembershipType
    """Profile's type."""

    is_public: bool
    """Profile's privacy status."""

    last_played: datetime.datetime
    """Profile's last played Destiny 2 played date."""

    character_ids: list[int]
    """A list of the profile's character ids."""

    power_cap: int
    """The profile's current season power cap."""

    async def collect_characters(
        self, components: list[enums.ComponentType], auth: typing.Optional[str] = None
    ) -> collections.Sequence[components.CharacterComponent]:
        """Fetch this profile's characters.

        Parameters
        ----------
        components: `list[aiobungie.ComponentType]`
            A sequence of character components to collect and return.

        Other Parameters
        ----------------
        auth : `typing.Optional[str]`
            A Bearer access_token to make the request with.
            This is optional and limited to components that only requires an Authorization token.

        Returns
        -------
        `collections.Sequence[aiobungie.crates.CharacterComponent]`
            A sequence of the characters components.
        """
        return await helpers.awaits(
            *[
                self.net.request.fetch_character(
                    self.id, self.type, char_id, components, auth
                )
                for char_id in self.character_ids
            ]
        )

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return int(self.id)
