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

import attrs

from aiobungie import url
from aiobungie.internal import helpers

if typing.TYPE_CHECKING:
    import collections.abc as collections
    import datetime

    from aiobungie import traits
    from aiobungie import typedefs
    from aiobungie.crates import activity
    from aiobungie.crates import entity
    from aiobungie.crates import milestones as milestones_
    from aiobungie.crates import progressions as progressions_
    from aiobungie.crates import records
    from aiobungie.crates import season
    from aiobungie.internal import assets
    from aiobungie.internal import enums
    from aiobungie.internal import iterators


@attrs.define(kw_only=True)
class Dye:
    """Represents dyes rendered on a Destiny character."""

    channel_hash: int
    """The hash of the channel."""

    dye_hash: int
    """The dye's hash."""


@attrs.define(kw_only=True, repr=False)
class CustomizationOptions:
    """Raw data represents a character's customization options."""

    personality: int

    face: int

    skin_color: int

    lip_color: int

    eye_color: int

    hair_colors: collections.Sequence[int]

    feature_colors: collections.Sequence[int]

    decal_color: int

    wear_helmet: bool

    hair_index: int

    feature_index: int

    decal_index: int


@attrs.define(kw_only=True)
class MinimalEquipments:
    """Minimal information about a character's equipped items.

    This holds the items hash and collection of dyes.

    This is specifically used in CharacterRenderData profile component to render
    3D character object.
    """

    net: traits.Netrunner = attrs.field(repr=False, eq=False, hash=False)
    """A network state used for making external requests."""

    item_hash: int
    """The equipped items's hash."""

    dyes: typing.Optional[collections.Collection[Dye]]
    """An optional collection of the item rendering dyes"""

    async def fetch_my_item(self) -> entity.InventoryEntity:
        """Fetch the inventory item definition of this equipment."""
        return await self.net.request.fetch_inventory_item(self.item_hash)


@attrs.define(kw_only=True)
class RenderedData:
    """Represents a character's rendered data profile component."""

    net: traits.Netrunner = attrs.field(repr=False, eq=False, hash=False)
    """A network state used for making external requests."""

    custom_dyes: collections.Collection[Dye]
    """A collection of the character's custom dyes."""

    customization: CustomizationOptions
    """Data about what character customization options you picked."""

    equipment: collections.Sequence[MinimalEquipments]
    """A sequence of minimal view of this character's equipment."""

    async def fetch_my_items(
        self, *, limit: typing.Optional[int] = None
    ) -> collections.Collection[entity.InventoryEntity]:
        """Fetch the inventory item definition of all the equipment this component has.

        Other Parameters
        ----------
        limit : `typing.Optional[int]`
            An optional item limit to fetch. Default is the length of the equipment.

        Returns
        -------
        `collections.Collection[aiobungie.crates.InventoryEntity]`
            A collection of the fetched item definitions.
        """
        return await helpers.awaits(
            *[item.fetch_my_item() for item in self.equipment[:limit]]
        )


@attrs.define(kw_only=True)
class CharacterProgression:
    """Represents a character progression profile component."""

    progressions: collections.Mapping[int, progressions_.Progression]
    """A Mapping from progression's hash to progression object."""

    factions: collections.Mapping[int, progressions_.Factions]
    """A Mapping from progression faction's hash to its faction object."""

    milestones: collections.Mapping[int, milestones_.Milestone]
    """A Mapping from the milestone's hash to a milestone object."""

    checklists: collections.Mapping[int, collections.Mapping[int, bool]]

    seasonal_artifact: season.CharacterScopedArtifact
    """Data related to your progress on the current season's artifact that can vary per character."""

    uninstanced_item_objectives: collections.Mapping[
        int, collections.Sequence[records.Objective]
    ]
    """A Mapping from an uninstanced inventory item hash to a sequence of its objectives."""

    # Still not sure if this field returned or not.
    # unsinstanced_item_pers: collections.Mapping[int, ...]?


@attrs.define(kw_only=True)
class Character:
    """An implementation for a Bungie character."""

    net: traits.Netrunner = attrs.field(repr=False, eq=False, hash=False)
    """A network state used for making external requests."""

    id: int
    """Character's id"""

    member_id: int
    """The character's member id."""

    member_type: enums.MembershipType
    """The character's memberhip type."""

    light: int
    """Character's light"""

    gender: enums.Gender
    """Character's gender"""

    race: enums.Race
    """Character's race"""

    emblem: assets.Image
    """Character's emblem"""

    emblem_icon: assets.Image
    """Character's emblem icon"""

    emblem_hash: int
    """Character's emblem hash."""

    last_played: datetime.datetime
    """Character's last played date."""

    total_played_time: str
    """Character's total plyed time minutes."""

    class_type: enums.Class
    """Character's class."""

    title_hash: typing.Optional[int]
    """Character's equipped title hash."""

    level: int
    """Character's base level."""

    stats: typing.Mapping[enums.Stat, int]
    """A mapping of the character stats and its level."""

    async def fetch_activities(
        self,
        mode: typedefs.IntAnd[enums.GameMode],
        *,
        page: int = 0,
        limit: int = 250,
    ) -> iterators.Iterator[activity.Activity]:
        """Fetch Destiny 2 activities for this character.

        Parameters
        ----------
        mode: `aiobungie.typedefs.IntAnd[aiobungie.internal.enums.GameMode]`
            Filters the gamemodes to fetch. i.e., Nightfall, Strike, Iron Banner, etc.

        Other Parameters
        ----------------
        page : `int`
            The page number. Default is `0`
        limit: `int`
            Limit the returned result. Default is `250`.

        Returns
        -------
        `aiobungie.iterators.Iterator[aiobungie.crates.Activity]`
            A iterator over the character's activities.

        Raises
        ------
        `aiobungie.MembershipTypeError`
            The provided membership type was invalid.
        """
        return await self.net.request.fetch_activities(
            self.member_id,
            self.id,
            mode,
            membership_type=self.member_type,
            page=page,
            limit=limit,
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
