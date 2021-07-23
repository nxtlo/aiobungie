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

"""Basic implementation for a Bungie a activity."""


from __future__ import annotations

__all__: Sequence[str] = ("Activity",)

from typing import TYPE_CHECKING, Any, Dict, Optional, Sequence

from ..error import HashError
from ..internal.enums import GameMode, MembershipType, Raid

if TYPE_CHECKING:
    from datetime import datetime


class Activity:
    """Represents a Bungie Activity object.

    An activity can be one of `aiobungie.internal.enums.GameMode`.

    Attributes
    -----------
    mode: `aiobungie.internal.enums.GameMode`
            The activity mode or type.
    is_completed: `builtins.str`
            Check if the activity was completed or no.
    hash: `aiobungie.internal.enums.Raid`
            This is a special attr used only for raids that returns the raid name.
    raw_hash: `builtins.int`
            The activity's hash.
    duration: `builtins.str`
            A string of The activity's duration, Example format `7m 42s`
    kills: `builtins.int`
            Activity's Total kills
    deaths: `builtins.int`
            Activity's total deaths.
    assists: `builtins.int`
            Activity's Total assists
    kd: `builtins.int`
            Activity's kd ration.
    member_type: `aiobungie.internal.enums.MembershipType`
            The activity member's membership type.
    players_count: `builtins.int`
            Total players in the activity.
    when: typing.Optional[datetime.datetime]
            When did the activity occurred in UTC datetime.
    """

    __slots__: Sequence[str] = (
        "is_completed",
        "mode",
        "kills",
        "deaths",
        "assists",
        "kd",
        "duration",
        "player_count",
        "when",
        "member_type",
        "hash",
    )
    is_completed: str
    hash: Raid  # Only for raids since we're not going to store everysingle other activity.
    mode: GameMode
    kills: int
    deaths: int
    when: Optional[datetime]
    assists: int
    duration: str
    player_count: int
    member_type: MembershipType
    kd: int

    def __init__(self, *, data: Any) -> None:
        self._update(data)

    def as_dict(self) -> Dict[str, Any]:
        """Returns a dict object of the Activity,
        This function is useful if you're binding to other REST apis.
        """
        return dict(
            is_completed=self.is_completed,
            mode=self.mode,
            duration=self.duration,
            player_cout=self.player_count,
            when=self.when,
            kills=self.kills,
            deaths=self.deaths,
            assists=self.assists,
            kd=self.kd,
            member_type=self.member_type,
            hash=self.hash or None,
        )

    def _update(self, data: Dict[str, Any]):
        ...
