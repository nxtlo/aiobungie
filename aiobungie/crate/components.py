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

import typing

import attr

from aiobungie.crate import character
from aiobungie.crate import profile
from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    from aiobungie import traits


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
        typing.Sequence[profile.ProfileCurrencies]
    ] = attr.field()
    """A sequence of profile currencies component.

    Notes
    -----
    * This will always be `None` unless `auth="access_token"` is passed to the request.
    * This will always be `None` unless `aiobungie.ComponentType.PROFILE_CURRENCIES`
    is passed to the request components.
    """

    # profile_inventories

    characters: typing.Optional[typing.Mapping[int, character.Character]] = attr.field(
        default=None
    )
    """A mapping of character's id to`aiobungie.crate.Character`
    of the associated character within the character component.

    This will be available when `aiobungie.ComponentType.CHARACTERS` is passed to the request.
    otherwise will be `None`.
    """

    # character_inventories

    # character_progressions

    # character_render_data

    # character_activities

    # character_items

    # records

    # # TODO: ^ and return `list[vendors.Vendor]`
    # vendors

    # # TODO: ^ and return `vendors.VendorSale`
    # vendor_sales
