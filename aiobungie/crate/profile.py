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
    "ProfileItem",
    "ProfileItemImpl",
)

import abc
import datetime
import typing

import attr

from aiobungie.crate import entity
from aiobungie.crate import user
from aiobungie.internal import enums
from aiobungie.internal import helpers

if typing.TYPE_CHECKING:
    import collections.abc as collections

    from aiobungie import traits
    from aiobungie import typedefs
    from aiobungie.crate import components
    from aiobungie.crate import season


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class LinkedProfile:
    """Represents a membership linked profile information summary.

    You can iterate asynchronously through the profiles.

    Example
    -------
    ```py
    linked_profiles = await client.fetch_linked_profiles(..., ...)
    try:
        while True:
            async for profile in linked_profiles:
                real_profile = await profile.fetch_self_profile()
                    # Check if profiles Component is not None
                    if real_profile.profiles is not None:
                        print(repr(await real_profile.fetch_warlock()))
    except StopIteration:
        pass
    ```
    """

    net: traits.Netrunner = attr.field(repr=False, eq=False, hash=False)
    """A network state used for making external requests."""

    profiles: collections.Sequence[user.DestinyUser] = attr.field(repr=False)
    """A sequence of destiny memberships for this profile."""

    bungie: user.PartialBungieUser = attr.field(repr=True)
    """The profile's bungie membership."""

    profiles_with_errors: typing.Optional[
        collections.Sequence[user.DestinyUser]
    ] = attr.field(repr=False, eq=False)
    """A sequence of optional destiny memberships with errors.

    These profiles exists because they have missing fields. Otherwise this will be an empty array.
    """

    def __aiter__(self) -> helpers.AsyncIterator[user.DestinyUser]:
        return helpers.AsyncIterator(self.profiles)


@attr.define(hash=False, kw_only=True, weakref_slot=False, eq=False)
class ProfileProgression:
    """Represents a profile progression component details."""

    artifact: season.Artifact = attr.field()
    """The profile progression seasonal artifact."""

    # No repr for this since its kinda huge dict.
    checklist: collections.Mapping[int, collections.Mapping[int, bool]] = attr.field(
        repr=False
    )
    """A mapping of int to another mapping of int to bool for the profile progression checklist."""


class ProfileItem(abc.ABC):
    """An interfance for items information found in a profile component.

    Those fields may be found in a `ProfileInventories`, etc.
    """

    __slots__ = ()

    @property
    @abc.abstractmethod
    def net(self) -> traits.Netrunner:
        """A network state used for making external requests."""

    @property
    @abc.abstractmethod
    def hash(self) -> int:
        """The item type hash."""

    @property
    @abc.abstractmethod
    def quantity(self) -> int:
        """The item quantity."""

    @property
    @abc.abstractmethod
    def bind_status(self) -> enums.ItemBindStatus:
        """The item binding status."""

    @property
    @abc.abstractmethod
    def location(self) -> enums.ItemLocation:
        """The item location."""

    @property
    @abc.abstractmethod
    def bucket(self) -> int:
        """The item bucket hash."""

    @property
    @abc.abstractmethod
    def transfer_status(self) -> typedefs.IntAnd[enums.TransferStatus]:
        """The item's transfer status."""

    @property
    @abc.abstractmethod
    def lockable(self) -> bool:
        """Whether the item can be locked or not."""

    @property
    @abc.abstractmethod
    def state(self) -> enums.ItemState:
        """The item's state."""

    @property
    @abc.abstractmethod
    def dismantel_permissions(self) -> int:
        """The item's dismantel permission."""

    @property
    @abc.abstractmethod
    def is_wrapper(self) -> bool:
        """Whether the item is a wrapper or not."""

    async def fetch_self(self) -> entity.InventoryEntity:
        """Fetch this profile item.

        Returns
        -------
        `aiobungie.crate.InventoryEntity`
            An inventory item definition entity.
        """
        return await self.net.request.fetch_inventory_item(self.hash)


@attr.mutable(hash=True, kw_only=True, weakref_slot=False)
class ProfileItemImpl(ProfileItem):
    """Concrete implementation of any profile component item.

    This also can be a character equipment i.e. Weapons, Armor, Ships, etc.
    """

    net: traits.Netrunner = attr.field(repr=False, eq=False, hash=False)
    """A network state used for making external requests."""

    hash: int = attr.field(hash=True)
    """The item type hash."""

    quantity: int = attr.field(repr=True, hash=True)
    """The item quantity."""

    bind_status: enums.ItemBindStatus = attr.field(repr=False)
    """The item binding status."""

    location: enums.ItemLocation = attr.field(repr=True)
    """The item location."""

    bucket: int = attr.field(repr=False)
    """The item bucket hash."""

    transfer_status: typedefs.IntAnd[enums.TransferStatus] = attr.field(repr=False)
    """The item's transfer status."""

    lockable: bool = attr.field(repr=False)
    """Whether the item can be locked or not."""

    state: enums.ItemState = attr.field(repr=False)
    """The item's state."""

    dismantel_permissions: int = attr.field(repr=False)
    """The item's dismantel permission."""

    is_wrapper: bool = attr.field(repr=False)
    """Whether the item is a wrapper or not."""

    instance_id: typing.Optional[int] = attr.field(repr=True)
    """An inventory item instance id if available, otherwise will be `None`."""

    ornament_id: typing.Optional[int] = attr.field(repr=False)
    """The ornament id of this item if it has one. Will be `None` otherwise."""

    version_number: typing.Optional[int] = attr.field(repr=False)
    """The item version number of available, other wise will be `None`."""

    @property
    def is_transferable(self) -> bool:
        """Check whether this item can be transferred or not."""
        return (
            self.transfer_status is enums.TransferStatus.CAN_TRANSFER
            and self.instance_id is not None  # noqa: W503
        )


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class Profile:
    """Represents a Bungie member profile-only component.

    This is only a `PROFILE` component and not the profile itself.
    See `aiobungie.crate.Component` for other components.
    """

    id: int = attr.field(repr=True, hash=True, eq=False)
    """Profile's id"""

    net: traits.Netrunner = attr.field(repr=False, eq=False)
    """A network state used for making external requests."""

    name: str = attr.field(repr=True, eq=False)
    """Profile's name."""

    type: enums.MembershipType = attr.field(repr=True, eq=False)
    """Profile's type."""

    is_public: bool = attr.field(repr=True, eq=False)
    """Profile's privacy status."""

    last_played: datetime.datetime = attr.field(repr=False, eq=False)
    """Profile's last played Destiny 2 played date."""

    character_ids: list[int] = attr.field(repr=False, eq=False)
    """A list of the profile's character ids."""

    power_cap: int = attr.field(repr=False, eq=False)
    """The profile's current seaspn power cap."""

    async def _await_all_chars(
        self, *components: enums.ComponentType, **options: str
    ) -> collections.Collection[components.CharacterComponent]:
        return await helpers.awaits(
            *[
                self.net.request.fetch_character(
                    self.id, self.type, char_id, *components, **options
                )
                for char_id in self.character_ids
            ]
        )

    # TODO: Support for "async with" instead?
    async def collect_characters(
        self, *components: enums.ComponentType, **options: str
    ) -> collections.Collection[components.CharacterComponent]:
        """Gather and collect all characters this profile has at once.

        Parameters
        ----------
        *components: `aiobungie.ComponentType`
            Multiple arguments of character components to collect and return.

        Other Parameters
        ----------------
        auth : `typing.Optional[str]`
            A passed kwarg Bearer access_token to make the request with.
            This is optional and limited to components that only requires an Authorization token.
        **options : `str`
            Other keyword arguments for the request to expect.
            This is only here for the `auth` option which's a kwarg.

        Returns
        -------
        `collections.Collection[aiobungie.crate.CharacterComponent]`
            A collection of the characters component.
        """
        return await self._await_all_chars(*components, **options)

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return int(self.id)
