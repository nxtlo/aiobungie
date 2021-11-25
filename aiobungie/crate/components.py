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

"""Bungie profile components implementation.

Components are returned when fetching a profile. All components may or may not be available
since it depends on components passed to the request or due to privacy by the profile owner.
"""

from __future__ import annotations

__all__: tuple[str, ...] = ("Component", "ComponentPrivacy", "ComponentFields")

import collections.abc as collections
import typing

import attr

from aiobungie.crate import character
from aiobungie.crate import profile
from aiobungie.crate import records as records_
from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    from aiobungie import traits
    from aiobungie.crate import activity


@typing.final
class ComponentPrivacy(enums.IntEnum):
    """An enum the provides privacy settings for profile components."""

    NONE = 0
    PUBLIC = 1
    PRIVATE = 2


@typing.final
class ComponentFields(enums.Enum):
    """An enum that provides fields found in a base component response."""

    PRIVACY = ComponentPrivacy
    DISABLED = False


@attr.mutable(weakref_slot=False, kw_only=True, hash=False)
class Component:
    """Implementation of a Bungie profile components.

    This includes all profile components that are available and not private.

    Private components will return `None` unless an `access_token` was passed to the request
    `**options` parameters.

    Example
    -------
    ```py
    import aiobungie

    # The components to get and return.
    components = (
        aiobungie.ComponentType.PROFILE,
        aiobungie.ComponentType.CHARACTERS,
        aiobungie.ComponentType.PROFILE_INVENTORIES,
    )
    profile = await client.fetch_profile(
        id,
        aiobungie.MembershipType.STEAM,
        *components,
        # Assuming the component requires an auth token
        auth="Some Bearer access token"
    )
    if items := profile.profile_inventories:
        for item in items:
            if item.hash == 1946491241:
                # Fetch the item if it's a truth-teller.
                my_item = await item.fetch_self()
                print(my_item.name, my_item.banner, my_item.icon)
                # Try to transfer the item.
                if item.instance_id and item.transfer_status is aiobungie.TransferStatus.CAN_TRANSFER:
                    try:
                        await client.rest.transfer_item(...)
                    except Exception as e:
                        print(f"Couldn't transfer the item {e}")
    ```
    """

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    profiles: typing.Optional[profile.Profile] = attr.field()
    """The profile component.

    This will be available when `aiobungie.ComponentType.PROFILE` is passed to the request components.
    otherwise will be `None`.
    """

    profile_progression: typing.Optional[profile.ProfileProgression] = attr.field()
    """The profile progression component.

    This will be available when `aiobungie.ComponentType.PROFILE_PROGRESSION`
    is passed to the request components.
    otherwise will be `None`.
    """

    profile_currencies: typing.Optional[
        collections.Sequence[profile.ProfileItemImpl]
    ] = attr.field()
    """A sequence of profile currencies component.

    Notes
    -----
    * This will always be `None` unless `auth="access_token"` is passed to the request.
    * This will always be `None` unless `aiobungie.ComponentType.PROFILE_CURRENCIES`
    is passed to the request components.
    """

    profile_inventories: typing.Optional[
        collections.Sequence[profile.ProfileItemImpl]
    ] = attr.field()
    """A sequence of profile inventories items component.

    Notes
    -----
    * This will always be `None` unless `auth="access_token"` is passed to the request.
    * This will always be `None` unless `aiobungie.ComponentType.PROFILE_INVENTORIES`
    is passed to the request components.
    """

    characters: typing.Optional[typing.Mapping[int, character.Character]] = attr.field()
    """A mapping of character's id to`aiobungie.crate.Character`
    of the associated character within the character component.

    This will be available when `aiobungie.ComponentType.CHARACTERS` is passed to the request.
    otherwise will be `None`.
    """

    character_inventories: typing.Optional[
        collections.Mapping[int, collections.Sequence[profile.ProfileItemImpl]]
    ] = attr.field()
    """A mapping of character's id to a sequence of their character inventorie items component.

    Those items may be Weapons, emblems, ships, sparrows, etc.

    Notes
    -----
    * This will always be `None` unless `auth="access_token"` is passed to the request.
    * This will always be `None` unless `aiobungie.ComponentType.CHARACTER_INVENTORY`
    is passed to the request components.
    """

    # character_progressions

    # character_render_data

    character_activities: typing.Optional[
        collections.Mapping[int, activity.CharacterActivity]
    ] = attr.field()
    """A mapping of character's id to a sequence of their character activities component.

    This will always be `None` unless `aiobungie.ComponentType.CHARACTER_ACTIVITES`
    is passed to the request components.
    """

    character_equipments: typing.Optional[
        collections.Mapping[int, collections.Sequence[profile.ProfileItemImpl]]
    ] = attr.field()
    """A mapping of character's id to a sequence of their character equipment component.

    This will always be `None` unless `aiobungie.ComponentType.CHARACTER_EQUIPMENT`
    is passed to the request components.
    """

    profile_records: typing.Optional[
        collections.Mapping[int, records_.Record]
    ] = attr.field()
    """A mapping of the profile record id to a record component.

    This will be available when `aiobungie.ComponentType.RECORDS`
    is passed to the request components.
    otherwise will be `None`.
    """

    character_records: typing.Optional[
        collections.Mapping[int, records_.CharacterRecord]
    ] = attr.field()
    """A mapping of character record ids to a character record component.

    This will be available when `aiobungie.ComponentType.RECORDS`
    is passed to the request components.
    otherwise will be `None`.
    """

    # # TODO: ^ and return `list[vendors.Vendor]`
    # vendors

    # # TODO: ^ and return `vendors.VendorSale`
    # vendor_sales
