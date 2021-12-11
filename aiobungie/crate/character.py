# -*- coding: utf-8 -*-

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

"""Standard implementation of Bungie Character and entities."""

from __future__ import annotations

__all__: tuple[str, ...] = (
    "Character",
    "Dye",
    "MinimalEquipments",
    "RenderedData",
    "CustomizationOptions",
    "CharacterProgression",
)

import typing

import attr

from aiobungie import url
from aiobungie.internal import helpers

if typing.TYPE_CHECKING:
    import collections.abc as collections
    import datetime

    from aiobungie import traits
    from aiobungie import typedefs
    from aiobungie.crate import activity
    from aiobungie.crate import entity
    from aiobungie.crate import milestones as milestones_
    from aiobungie.crate import progressions as progressions_
    from aiobungie.crate import records
    from aiobungie.crate import season
    from aiobungie.internal import enums
    from aiobungie.internal.assets import Image


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class Dye:
    """Represents dyes rendered on a Destiny character."""

    channel_hash: int = attr.field()
    """The hash of the channel."""

    dye_hash: int = attr.field()
    """The dye's hash."""


@attr.define(hash=False, kw_only=True, weakref_slot=False, repr=False)
class CustomizationOptions:
    """Raw data represents a character's customization options."""

    personality: int = attr.field()

    face: int = attr.field()

    skin_color: int = attr.field()

    lip_color: int = attr.field()

    eye_color: int = attr.field()

    hair_colors: collections.Sequence[int] = attr.field()

    feature_colors: collections.Sequence[int] = attr.field()

    decal_color: int = attr.field()

    wear_helmet: bool = attr.field()

    hair_index: int = attr.field()

    feature_index: int = attr.field()

    decal_index: int = attr.field()


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class MinimalEquipments:
    """Minimal information about a character's equipped items.

    This holds the items hash and collection of dyes.

    This is specifacally used in CharacterRenderData profile component to render
    3D character object.
    """

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    item_hash: int = attr.field()
    """The equipped items's hash."""

    dyes: typing.Optional[collections.Collection[Dye]] = attr.field(repr=False)
    """An optional collection of the item rendering dyes"""

    async def fetch_my_item(self) -> entity.InventoryEntity:
        """Fetch the inventory item definition of this equipment."""
        return await self.net.request.fetch_inventory_item(self.item_hash)


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class RenderedData:
    """Represents a character's rendered data profile component."""

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    custom_dyes: collections.Collection[Dye] = attr.field(repr=False)
    """A collection of the character's custom dyes."""

    customization: CustomizationOptions = attr.field(repr=False)
    """Data about what character customization options you picked."""

    equipment: collections.Sequence[MinimalEquipments] = attr.field()
    """A sequence of minimal view of """

    async def fetch_my_items(
        self, *, limit: typing.Optional[int] = None
    ) -> collections.Collection[entity.InventoryEntity]:
        """Fetch the inventory item definition of all the equipment this component has.

        Other Parameters
        ----------
        limit : `typing.Optional[int]`
            An optional item limit to fetch. Default is the length of the equipment.

        Returns
        `collections.Collection[aiobungie.crate.InventoryEntity]`
            A collection of the returned item definitions.
        """
        return await helpers.awaits(
            *[item.fetch_my_item() for item in self.equipment[:limit]]
        )


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class CharacterProgression:
    """Represents a character progression profile component."""

    progressions: collections.Mapping[int, progressions_.Progression] = attr.field(
        repr=False
    )
    """A Mapping from progression's hash to progression object."""

    factions: collections.Mapping[int, progressions_.Factions] = attr.field(repr=False)
    """A Mapping from progression faction's hash to its faction object."""

    milestones: collections.Mapping[int, milestones_.Milestone] = attr.field(repr=False)
    """A Mapping from the milestone's hash to a milestone object."""

    checklists: collections.Mapping[int, collections.Mapping[int, bool]] = attr.field(
        repr=False
    )

    seasonal_artifact: season.CharacterScopedArtifact = attr.field()
    """Data related to your progress on the current season's artifact that can vary per character."""

    uninstanced_item_objectives: collections.Mapping[
        int, collections.Sequence[records.Objective]
    ] = attr.field(repr=False)
    """A Mapping from an uninstanced inventory item hash to a sequence of its objectives."""

    # Still not sure if this field returned or not.
    # unsinstanced_item_pers: collections.Mapping[int, ...]?


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class Character:
    """An implementation for a Bungie character."""

    net: traits.Netrunner = attr.field(repr=False, eq=False)
    """A network state used for making external requests."""

    id: int = attr.field(hash=True, repr=True)
    """Character's id"""

    member_id: int = attr.field(hash=True, repr=True)
    """The character's member id."""

    member_type: enums.MembershipType = attr.field(repr=True, hash=False)
    """The character's memberhip type."""

    light: int = attr.field(repr=True, hash=False)
    """Character's light"""

    gender: enums.Gender = attr.field(repr=True, hash=False)
    """Character's gender"""

    race: enums.Race = attr.field(repr=True, hash=False)
    """Character's race"""

    emblem: Image = attr.field(repr=False, hash=False)
    """Character's emblem"""

    emblem_icon: Image = attr.field(repr=False, hash=False)
    """Character's emblem icon"""

    emblem_hash: int = attr.field(repr=False, hash=False)
    """Character's emblem hash."""

    last_played: datetime.datetime = attr.field(repr=False, hash=False)
    """Character's last played date."""

    total_played_time: str = attr.field(repr=False, hash=False)
    """Character's total plyed time minutes."""

    class_type: enums.Class = attr.field(repr=True, hash=False)
    """Character's class."""

    title_hash: typing.Optional[int] = attr.field(repr=True, hash=False)
    """Character's equipped title hash."""

    level: int = attr.field(repr=False, hash=False)
    """Character's base level."""

    stats: typing.Mapping[enums.Stat, int] = attr.field(repr=False, hash=False)
    """A mapping of the character stats and its level."""

    async def fetch_activities(
        self,
        mode: typedefs.IntAnd[enums.GameMode],
        *,
        page: int = 0,
        limit: int = 250,
    ) -> collections.Sequence[activity.Activity]:
        """Fetch Destiny 2 activities this character.

        Parameters
        ----------
        mode: `aiobungie.typedefs.IntAnd[aiobungie.internal.enums.GameMode]`
            This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc.

        Other Parameters
        ----------------
        page: builtins.int
            The page number. Default is `0`
        limit: builtins.int
            Limit the returned result. Default is `250`.

        Returns
        -------
        `collections.Sequence[aiobungie.crate.Activity]`
            A sequence of the character's activities.

        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """
        return await self.net.request.fetch_activities(
            self.member_id, self.id, mode, self.member_type, page=page, limit=limit
        )

    async def transfer_item(
        self,
        access_token: str,
        /,
        item_id: int,
        item_hash: int,
        *,
        vault: bool = False,
        stack_size: int = 1,
    ) -> None:
        """Transfer an item from / to your vault.

        Notes
        -----
        * This method requires OAuth2: MoveEquipDestinyItems scope.
        * This method requires both item id and hash.

        Parameters
        ----------
        item_id : `int`
            The item id you to transfer.
        item_hash : `int`
            The item hash.

        Other Parameters
        ----------------
        stack_size : `int`
            The item stack size.
        valut : `bool`
            Whether to pill this item to your valut or not. Defaults to `False`.
        """
        await self.net.request.rest.transfer_item(
            access_token,
            item_id=item_id,
            character_id=self.id,
            item_hash=item_hash,
            member_type=self.member_type,
            vault=vault,
            stack_size=stack_size,
        )

    async def pull_item(
        self,
        access_token: str,
        /,
        item_id: int,
        item_hash: int,
        *,
        vault: bool = False,
        stack_size: int = 1,
    ) -> None:
        """Pull an item from the postmaster to this character.

        Notes
        -----
        * This method requires OAuth2: MoveEquipDestinyItems scope.
        * This method requires both item id and hash.

        Parameters
        ----------
        item_id : `int`
            The item id to pull.
        item_hash : `int`
            The item hash.

        Other Parameters
        ----------------
        stack_size : `int`
            The item stack size.
        valut : `bool`
            Whether to pill this item to your valut or not. Defaults to `False`.
        """
        await self.net.request.rest.pull_item(
            access_token,
            item_id=item_id,
            character_id=self.id,
            item_hash=item_hash,
            member_type=self.member_type,
            vault=vault,
            stack_size=stack_size,
        )

    async def equip_item(self, access_token: str, item_id: int, /) -> None:
        """Equip an item to this character.

        This requires the OAuth2: MoveEquipDestinyItems scope.
        Also You must have a valid Destiny account, and either be
        in a social space, in orbit or offline.

        Parameters
        ----------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.
        item_id : `builtins.int`
            The item id.
        """
        await self.net.request.rest.equip_item(
            access_token,
            item_id=item_id,
            character_id=self.id,
            membership_type=self.member_type,
        )

    async def equip_items(self, access_token: str, item_ids: list[int], /) -> None:
        """Equip multiple items to this character.

        This requires the OAuth2: MoveEquipDestinyItems scope.
        Also You must have a valid Destiny account, and either be
        in a social space, in orbit or offline.

        Parameters
        ----------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.
        item_ids: `list[builtins.int]`
            A list of item ids you want to equip for this character.
        """
        await self.net.request.rest.equip_items(
            access_token,
            item_ids=item_ids,
            character_id=self.id,
            membership_type=self.member_type,
        )

    @property
    def url(self) -> str:
        """A url for the character at bungie.net."""
        return f"{url.BASE}/en/Gear/{int(self.member_type)}/{self.member_id}/{self.id}"

    def __int__(self) -> int:
        return int(self.id)
