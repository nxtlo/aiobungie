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

import attrs

if typing.TYPE_CHECKING:
    import collections.abc as collections
    import datetime

    from aiobungie import traits
    from aiobungie import typedefs
    from aiobungie import undefined
    from aiobungie.crates import entity
    from aiobungie.crates import records


@attrs.define(kw_only=True)
class MilestoneItems:
    """Represents items the may be found inside a milestone."""

    title: undefined.UndefinedOr[str]
    """The item title. This may be `UNDEFINED` if not specified."""

    hashes: collections.Sequence[int]
    """The items hashes"""


@attrs.define(kw_only=True)
class MilestoneContent:
    """Represents information about a Destiny milestone content."""

    about: undefined.UndefinedOr[str]
    """About this milestone."""

    status: undefined.UndefinedOr[str]
    """The milestone's status. This field may be `UNDEFINED` if not specified."""

    tips: collections.Sequence[undefined.UndefinedOr[str]]
    """A sequence of the milestone's tips. fields in the sequence may be `UNDEFINED` if not specified."""

    items: typedefs.NoneOr[MilestoneItems]
    """An optional items for this miletones. This may return `None` if nothing was found."""


@attrs.define(kw_only=True)
class MilestoneActivityPhase:
    """Represents information about a milestone activity phase."""

    is_completed: bool
    """Whether this phase has been completed or not."""

    hash: int
    """The phase's hash."""


@attrs.define(kw_only=True)
class MilestoneActivity:
    """Represents a Bungie milestone activity."""

    hash: int
    """The activity hash."""

    challenges: collections.Sequence[records.Objective]
    """A sequence of objetvies/challenges bound to this activity."""

    modifier_hashes: typing.Optional[list[int]]
    """An optional list of the activity's modifier hashes."""

    boolean_options: typing.Optional[collections.Mapping[int, bool]]
    """An optional mapping from int to bool of the activity available options."""

    phases: typing.Optional[collections.Collection[MilestoneActivityPhase]]
    """An optional collection of the activity phases."""


@attrs.define(kw_only=True)
class QuestStatus:
    """Information that an available quest status has."""

    net: traits.Netrunner = attrs.field(repr=False, eq=False, hash=False)

    quest_hash: int
    """The quest hash."""

    step_hash: int
    """The quest step hash."""

    vendor_hash: typing.Optional[int]
    """If the quest has a related Vendor that you should talk to
    in order to initiate the quest/earn rewards/continue the quest
    """

    step_objectives: collections.Sequence[records.Objective]
    """A sequence of the step objectives bound to this quest status."""

    is_completed: bool
    """Whether this quest status has been redeemed or not."""

    is_tracked: bool
    """Whether the player is tracking this quest status or not."""

    started: bool
    """Whether this quest status has started by the player or not."""

    is_redeemed: bool
    """Whether the quest has been redmeed or not."""

    item_instance_id: int
    """ The current Quest Step will be an instanced item in the player's inventory.

    If you care about that, this is the instance ID of that item.
    """

    async def fetch_quest(self) -> entity.InventoryEntity:
        """Fetch the definition of this quest.

        Returns
        -------
        `aiobungie.crates.InventoryEntity`
            The fetched inventory item definition/entity.
        """
        return await self.net.request.fetch_inventory_item(self.quest_hash)

    async def fetch_step(self) -> entity.InventoryEntity:
        """Fetch the definition of this quest step.

        Returns
        -------
        `aiobungie.crates.InventoryEntity`
            The fetched inventory item definition/entity.
        """
        return await self.net.request.fetch_inventory_item(self.step_hash)


@attrs.define(kw_only=True)
class MilestoneQuest:

    item_hash: int

    status: QuestStatus


@attrs.define(kw_only=True)
class MilestoneVendor:
    """Represents a vendor found inside a milestone object."""

    vendor_hash: int

    preview_itemhash: typing.Optional[int]


@attrs.define(kw_only=True)
class MilestoneRewardEntry:
    """Represents a charatcer-specific data for a milestone reward entry."""

    entry_hash: int
    """The entry hash."""

    is_earned: bool
    """Whether the entry has been earned or not."""

    is_redeemed: bool
    """Whether the entry has been redeemed or not."""


@attrs.define(kw_only=True)
class MilestoneReward:
    """Represents a summary of rewards that can be earned from a milestone."""

    category_hash: int

    entries: collections.Collection[MilestoneRewardEntry]
    """A collections of reward entries for this category."""


@attrs.define(kw_only=True)
class Milestone:
    """Represents a milestone at Bungie."""

    hash: int
    """Milestone hash."""

    available_quests: typing.Optional[collections.Sequence[MilestoneQuest]]
    """If there're active quests related to this milestone. they will appear here."""

    activities: typing.Optional[collections.Sequence[MilestoneActivity]]
    """A sequence of activities related to this milestone."""

    vendors: typing.Optional[collections.Sequence[MilestoneVendor]]
    """A sequence of vendors related to this milestone."""

    start_date: typing.Optional[datetime.datetime]
    """If the date of the milestone is known. This will be returned."""

    end_date: typing.Optional[datetime.datetime]
    """If the end date of the milestone is known. This will be returned."""

    order: int

    rewards: typing.Optional[collections.Collection[MilestoneReward]]
    """A colelctions of rewards that can be earned from this miletone"""
