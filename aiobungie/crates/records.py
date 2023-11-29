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

"""Implementation of Bungie records/triumphs."""

from __future__ import annotations

__all__: tuple[str, ...] = (
    "Objective",
    "Record",
    "CharacterRecord",
    "RecordScores",
    "Node",
)

import typing

import attrs

from aiobungie import undefined
from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    from aiobungie import traits
    from aiobungie.crates import entity


@typing.final
class RecordState(enums.Flag):
    """An enum for records component states."""

    NONE = 0
    REDEEMED = 1 << 0
    UNAVAILABLE = 1 << 1
    OBJECTIVE_NOT_COMPLETED = 1 << 2
    OBSCURED = 1 << 3
    INVISIBLE = 1 << 4
    ENTITLEMENT_UNOWNED = 1 << 5
    CAN_EQUIP_TITLE = 1 << 6


@attrs.define(kw_only=True)
class Node:
    """Represent a Destiny 2 presentation node."""

    state: int
    """The state of this node."""

    objective: typing.Optional[Objective]

    progress_value: int
    """How much of the presentation node is considered to be completed so far by the given character/profile."""

    completion_value: int
    """The value at which the presenation node is considered to be completed."""

    record_category_score: typing.Optional[int]
    """If available, this is the current score for the record category that this node represents."""


@attrs.mutable(kw_only=True)
class Objective:
    """Represents a Destiny 2 record objective."""

    net: traits.Netrunner = attrs.field(repr=False, hash=False, eq=False)

    hash: int
    """The objective hash."""

    visible: bool
    """Whether the objective is visible or not."""

    complete: bool
    """Whether the objective is completed or not."""

    completion_value: int
    """An integer represents the objective completion value."""

    progress: typing.Optional[int]
    """If progress has been made, and the progress can be measured numerically,
    this will be the value of that progress."""

    destination_hash: typing.Optional[int]
    """The hash of the Destiny 2 objective destination. If it has one."""

    activity_hash: typing.Optional[int]
    """If the Objective has an Activity associated with it,
    this is the unique identifier of the Activity being referred to.
    """

    async def fetch_self(self) -> entity.ObjectiveEntity:
        """Perform an HTTP request fetching this objective entity definition.

        Returns
        -------
        `aiobungie.crates.ObjectiveEntity`
            An objective entity definition.
        """
        return await self.net.request.fetch_objective_entity(self.hash)


@attrs.mutable(kw_only=True)
class RecordScores:
    """Represents the records scores.

    This includes active, lifetime and legacy scores.
    """

    current_score: int
    """The active triumphs score."""

    legacy_score: int
    """The legacy triumphs score."""

    lifetime_score: int
    """The lifetime triumphs score. This includes both legacy and current scores."""


@attrs.define(kw_only=True)
class Record:
    """Represents a Bungie profile records/triumphs component."""

    scores: typing.Optional[RecordScores]
    """Information about the global records score."""

    categories_node_hash: undefined.UndefinedOr[int]
    """ The hash for the root presentation node definition of Triumph categories.

    This will be `UNDEFINED` if not found.
    """

    seals_node_hash: undefined.UndefinedOr[int]
    """The hash for the root presentation node definition of Triumph Seals.

    This will be `UNDEFINED` if not found.
    """

    state: RecordState
    """Record's state. This will be an int if the state is a sum of multiple states."""

    objectives: typing.Optional[list[Objective]]
    """A list of the record objectives. The objectives are optional and may be `None` if not found."""

    interval_objectives: typing.Optional[list[Objective]]
    """A list of the interval record objectives. The objectives are optional and may be `None` if not found."""

    redeemed_count: int
    """The number of times this record has been redeemed."""

    completion_times: typing.Optional[int]
    """An optional number of time this record has been completed, `None` if not found."""

    reward_visibility: typing.Optional[list[bool]]
    """An optional list of bool for the record reward visibility."""


@attrs.define(kw_only=True)
class CharacterRecord(Record):
    """Represents a character focused records component.

    This derives from `Record` but returns a character focused's records.
    """

    record_hashes: list[int]
    """A list of int of the featured record hashes."""
