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

"""Basic implementation of Bungie profiles components."""

from __future__ import annotations

__all__ = (
    "Profile",
    "LinkedProfile",
    "ProfileProgression",
    "ProfileItemImpl",
)

import datetime
import typing

import attrs

from aiobungie.crates import user
from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    import collections.abc as collections

    from aiobungie.crates import season


@attrs.frozen(kw_only=True)
class LinkedProfile:
    """Represents a membership linked profile information summary."""

    profiles: collections.Sequence[user.DestinyMembership]
    """A sequence of Destiny2 memberships for this profile."""

    bungie_user: user.PartialBungieUser
    """The Bungie user that's bound to this profile."""

    profiles_with_errors: collections.Sequence[user.DestinyMembership] | None
    """A sequence of Destiny2 memberships with errors.

    These profiles exists because they have missing fields. Otherwise this will be `None`.
    """


@attrs.frozen(kw_only=True)
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

    This can be a character equipment, i.e., Weapon, Armor, Ship, etc.
    """

    hash: int
    """The item hash."""

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

    dismantle_permissions: int
    """The item's dismantle permission."""

    is_wrapper: bool
    """Whether the item is a wrapper or not."""

    instance_id: int | None
    """An inventory item instance id if available, otherwise will be `None`."""

    ornament_id: int | None
    """The ornament id of this item if it has one. Will be `None` otherwise."""

    version_number: int | None
    """The item version number of available, other wise will be `None`."""


@attrs.frozen(kw_only=True)
class Profile:
    """Represents a Bungie member profile-only component.

    This is only a `PROFILE` component and not the profile itself.
    See `aiobungie.crates.Component` for other components.
    """

    user: user.DestinyMembership
    """Basic information about this profile's user information."""

    last_played: datetime.datetime
    """Profile's last played Destiny 2 played date."""

    character_ids: collections.Sequence[int]
    """A sequence of the profile's character IDs."""

    power_cap: int
    """The current season reward power cap."""

    season_hashes: collections.Sequence[int]
    """An immutable sequence of Destiny 2 season hashes this profile participated in."""

    versions_owned: enums.GameVersions
    """An enum flag representing the DLCs this profile owns."""

    season_hash: int
    """ The hash of the current season. You can use this hash to fetch the definition of this season."""

    guardian_rank: int
    """The in-game guardian rank of this profile."""

    highest_guardian_rank: int
    """The highest achieved in-game guardian rank of this profile."""

    renewed_guardian_rank: int
    """The renewed guardian rank of this profile."""

    event_card_hashes: collections.Sequence[int]
