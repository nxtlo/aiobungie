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

"""Basic implementation of Bungie records/triumphs resources."""

from __future__ import annotations

__all__ = (
    "Objective",
    "Record",
    "CharacterRecord",
    "RecordScores",
    "Node",
)

import typing

import attrs

from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    import collections.abc as collections


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


@attrs.frozen(kw_only=True)
class Node:
    """Represent a Destiny 2 presentation node."""

    state: int
    """The state of this node."""

    objective: Objective | None

    progress_value: int
    """How much of the presentation node is considered to be completed so far by the given character/profile."""

    completion_value: int
    """The value at which the presentation node is considered to be completed."""

    record_category_score: int | None
    """If available, this is the current score for the record category that this node represents."""


@attrs.mutable(kw_only=True)
class Objective:
    """Represents a Destiny 2 record objective."""

    hash: int
    """The objective hash."""

    visible: bool
    """Whether the objective is visible or not."""

    complete: bool
    """Whether the objective is completed or not."""

    completion_value: int
    """An integer represents the objective completion value."""

    progress: int | None
    """If progress has been made, and the progress can be measured numerically,
    this will be the value of that progress."""

    destination_hash: int | None
    """The hash of the Destiny 2 objective destination. If it has one."""

    activity_hash: int | None
    """If the Objective has an Activity associated with it,
    this is the unique identifier of the Activity being referred to.
    """


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


@attrs.frozen(kw_only=True)
class Record:
    """Represents a Bungie profile records/triumphs component."""

    scores: RecordScores | None
    """Information about the global records score."""

    categories_node_hash: int | None
    """ The hash for the root presentation node definition of Triumph categories."""

    seals_node_hash: int | None
    """The hash for the root presentation node definition of Triumph Seals."""

    state: RecordState
    """Record's state. This will be an int if the state is a sum of multiple states."""

    objectives: collections.Sequence[Objective] | None
    """A list of the record objectives. The objectives are optional and may be `None` if not found."""

    interval_objectives: collections.Sequence[Objective] | None
    """A list of the interval record objectives. The objectives are optional and may be `None` if not found."""

    redeemed_count: int
    """The number of times this record has been redeemed."""

    completion_times: int | None
    """An optional number of time this record has been completed, `None` if not found."""

    reward_visibility: collections.Sequence[bool] | None
    """An optional list of bool for the record reward visibility."""


@attrs.frozen(kw_only=True)
class CharacterRecord(Record):
    """Represents a character focused records component.

    This derives from `Record` but returns a character focused's records.
    """

    record_hashes: collections.Sequence[int]
    """A list of int of the featured record hashes."""
