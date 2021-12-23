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

"""Implementation of Bungie milestones."""

from __future__ import annotations

__all__: tuple[str, ...] = (
    "MilestoneContent",
    "MilestoneItems",
    "Milestone",
    "MilestoneActivity",
    "MilestoneQuest",
    "MilestoneVendor",
    "MilestoneActivityPhase",
    "QuestStatus",
    "MilestoneReward",
    "MilestoneRewardEntry",
)

import typing

import attr

if typing.TYPE_CHECKING:
    import collections.abc as collections
    import datetime

    from aiobungie import traits
    from aiobungie import typedefs
    from aiobungie import undefined
    from aiobungie.crate import entity
    from aiobungie.crate import records


@attr.define(hash=False, weakref_slot=False, kw_only=True)
class MilestoneItems:
    """Represents items the may be found inside a milestone."""

    title: undefined.UndefinedOr[str] = attr.field(repr=True)
    """The item title. This may be `UNDEFINED` if not specified."""

    hashes: collections.Sequence[int] = attr.field(repr=True)
    """The items hashes"""


@attr.define(hash=False, weakref_slot=False, kw_only=True)
class MilestoneContent:
    """Represents information about a Destiny milestone content."""

    about: undefined.UndefinedOr[str] = attr.field(repr=True)
    """About this milestone."""

    status: undefined.UndefinedOr[str] = attr.field(repr=True, eq=True)
    """The milestone's status. This field may be `UNDEFINED` if not specified."""

    tips: collections.Sequence[undefined.UndefinedOr[str]] = attr.field(repr=True)
    """A sequence of the milestone's tips. fields in the sequence may be `UNDEFINED` if not specified."""

    items: typedefs.NoneOr[MilestoneItems] = attr.field(repr=True)
    """An optional items for this miletones. This may return `None` if nothing was found."""


@attr.define(weakref_slot=False, kw_only=True)
class MilestoneActivityPhase:
    """Represents information about a milestone activity phase."""

    is_completed: bool = attr.field()
    """Whether this phase has been completed or not."""

    hash: int = attr.field()
    """The phase's hash."""


@attr.define(weakref_slot=False, kw_only=True)
class MilestoneActivity:
    """Represents a Bungie milestone activity."""

    hash: int = attr.field()
    """The activity hash."""

    challenges: collections.Sequence[records.Objective] = attr.field(repr=False)
    """A sequence of objetvies/challenges bound to this activity."""

    modifier_hashes: typing.Optional[list[int]] = attr.field(repr=False)
    """An optional list of the activity's modifier hashes."""

    boolean_options: typing.Optional[collections.Mapping[int, bool]] = attr.field(
        repr=False
    )
    """An optional mapping from int to bool of the activity available options."""

    phases: typing.Optional[
        collections.Collection[MilestoneActivityPhase]
    ] = attr.field(repr=False)
    """An optional collection of the activity phases."""


@attr.define(weakref_slot=False, kw_only=True)
class QuestStatus:
    """Information that an available quest status has."""

    net: traits.Netrunner = attr.field(repr=False)

    quest_hash: int = attr.field(hash=True)
    """The quest hash."""

    step_hash: int = attr.field(hash=True)
    """The quest step hash."""

    vendor_hash: typing.Optional[int] = attr.field(repr=False)
    """If the quest has a related Vendor that you should talk to
    in order to initiate the quest/earn rewards/continue the quest
    """

    step_objectives: collections.Sequence[records.Objective] = attr.field(
        hash=False, repr=False
    )
    """A sequence of the step objectives bound to this quest status."""

    is_completed: bool = attr.field(hash=False)
    """Whether this quest status has been redeemed or not."""

    is_tracked: bool = attr.field(hash=False, repr=False)
    """Whether the player is tracking this quest status or not."""

    started: bool = attr.field(hash=False, repr=False)
    """Whether this quest status has started by the player or not."""

    is_redeemed: bool = attr.field(repr=False)
    """Whether the quest has been redmeed or not."""

    item_instance_id: int = attr.field(hash=True)
    """ The current Quest Step will be an instanced item in the player's inventory.

    If you care about that, this is the instance ID of that item.
    """

    async def fetch_quest(self) -> entity.InventoryEntity:
        """Fetch the definition of this quest.

        Returns
        -------
        `aiobungie.crate.InventoryEntity`
            The fetched inventory item definition/entity.
        """
        return await self.net.request.fetch_inventory_item(self.quest_hash)

    async def fetch_step(self) -> entity.InventoryEntity:
        """Fetch the definition of this quest step.

        Returns
        -------
        `aiobungie.crate.InventoryEntity`
            The fetched inventory item definition/entity.
        """
        return await self.net.request.fetch_inventory_item(self.step_hash)


@attr.define(weakref_slot=False, kw_only=True)
class MilestoneQuest:

    item_hash: int = attr.field(hash=True)

    status: QuestStatus = attr.field(repr=False, hash=False)


@attr.define(weakref_slot=False, kw_only=True)
class MilestoneVendor:
    """Represents a vendor found inside a milestone object."""

    vendor_hash: int = attr.field(hash=True)

    preview_itemhash: typing.Optional[int] = attr.field(hash=True)


@attr.define(weakref_slot=False, kw_only=True)
class MilestoneRewardEntry:
    """Represents a charatcer-specific data for a milestone reward entry."""

    entry_hash: int = attr.field(hash=True)
    """The entry hash."""

    is_earned: bool = attr.field(hash=False)
    """Whether the entry has been earned or not."""

    is_redeemed: bool = attr.field(hash=False)
    """Whether the entry has been redeemed or not."""


@attr.define(weakref_slot=False, kw_only=True, eq=False)
class MilestoneReward:
    """Represents a summary of rewards that can be earned from a milestone."""

    category_hash: int = attr.field(hash=True)

    entries: collections.Collection[MilestoneRewardEntry] = attr.field(
        hash=False, repr=False
    )
    """A collections of reward entries for this category."""


@attr.define(weakref_slot=False, kw_only=True)
class Milestone:
    """Represents a milestone at Bungie."""

    hash: int = attr.field(hash=True)
    """Milestone hash."""

    available_quests: typing.Optional[
        collections.Sequence[MilestoneQuest]
    ] = attr.field(repr=False, hash=False, eq=False)
    """If there're active quests related to this milestone. they will appear here."""

    activities: typing.Optional[collections.Sequence[MilestoneActivity]] = attr.field(
        repr=False, hash=False, eq=False
    )
    """A sequence of activities related to this milestone."""

    vendors: typing.Optional[collections.Sequence[MilestoneVendor]] = attr.field(
        repr=False, hash=False, eq=False
    )
    """A sequence of vendors related to this milestone."""

    start_date: typing.Optional[datetime.datetime] = attr.field(hash=False)
    """If the date of the milestone is known. This will be returned."""

    end_date: typing.Optional[datetime.datetime] = attr.field(hash=False)
    """If the end date of the milestone is known. This will be returned."""

    order: int = attr.field(repr=False, hash=False)

    rewards: typing.Optional[collections.Collection[MilestoneReward]] = attr.field(
        hash=False
    )
    """A colelctions of rewards that can be earned from this miletone"""
