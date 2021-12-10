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
    "RecordState",
    "Objective",
    "Record",
    "CharacterRecord",
    "RecordScores",
)

import typing

import attr

from aiobungie import undefined
from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    from aiobungie import traits
    from aiobungie import typedefs
    from aiobungie.crate import entity


@typing.final
class RecordState(enums.IntEnum):
    """An enum for records component states."""

    NONE = 0
    REDEEMED = 1
    UNAVAILABLE = 2
    OBJECTIVE_NOT_COMPLETED = 4
    OBSCURED = 8
    INVISIBLE = 16
    ENTITLEMENT_UNOWNED = 32
    CAN_EQUIP_TITLE = 64
    UNDEFINED = 999


@attr.mutable(kw_only=True, weakref_slot=True, hash=False)
class Objective:
    """Represents a Destiny 2 record objective."""

    net: traits.Netrunner = attr.field(repr=False)

    hash: int = attr.field(hash=True)
    """The objective hash."""

    visible: bool = attr.field()
    """Whether the objective is visible or not."""

    complete: bool = attr.field()
    """Whether the objective is completed or not."""

    completion_value: int = attr.field(repr=False)
    """An integer represents the objective completion value."""

    progress: int = attr.field(repr=False)
    """An integer represents the objective progress."""

    async def fetch_self(self) -> entity.ObjectiveEntity:
        """Perform an HTTP request fetching this objective entity definition.

        Returns
        -------
        `aiobungie.crate.ObjectiveEntity`
            An objective entity definition.
        """
        return await self.net.request.fetch_objective_entity(self.hash)


@attr.mutable(kw_only=True, weakref_slot=True, hash=False)
class RecordScores:
    """Represents the records scores.

    This includes active, lifetime and legacy scores.
    """

    current_score: int = attr.field()
    """The active triumphs score."""

    legacy_score: int = attr.field()
    """The legacy triumphs score."""

    lifetime_score: int = attr.field()
    """The lifetime triumphs score. This includes both legacy and current scores."""


@attr.define(kw_only=True, weakref_slot=True, hash=False)
class Record:
    """Represents a Bungie profile records/triumphs component."""

    scores: typing.Optional[RecordScores] = attr.field(repr=False)
    """Information about the global records score."""

    categories_node_hash: undefined.UndefinedOr[int] = attr.field()
    """ The hash for the root presentation node definition of Triumph categories.

    This will be `UNDEFINED` if not found.
    """

    seals_node_hash: undefined.UndefinedOr[int] = attr.field()
    """The hash for the root presentation node definition of Triumph Seals.

    This will be `UNDEFINED` if not found.
    """

    state: typedefs.IntAnd[RecordState] = attr.field()
    """Record's state. This will be an int if the state is a sum of multiple states."""

    objectives: typing.Optional[list[Objective]] = attr.field(repr=False)
    """A list of the record objectives. The objectives are optional and may be `None` if not found."""

    interval_objectives: typing.Optional[list[Objective]] = attr.field(repr=False)
    """A list of the interval record objectives. The objectives are optional and may be `None` if not found."""

    redeemed_count: int = attr.field(repr=False)
    """The number of times this record has been redeemed."""

    completion_times: typing.Optional[int] = attr.field(repr=False)
    """An optional number of time this record has been completed, `None` if not found."""

    reward_visibility: typing.Optional[list[bool]] = attr.field(repr=False)
    """An optional list of bool for the record reward visibility."""


@attr.define(kw_only=True, weakref_slot=True)
class CharacterRecord(Record):
    """Represents a character focused records component.

    This derives from `Record` but returns a character focused's records.
    """

    record_hashes: list[int] = attr.field(hash=False)
    """A list of int of the featured record hashes."""

    async def fetch_records(self) -> typing.NoReturn:
        raise NotImplementedError
