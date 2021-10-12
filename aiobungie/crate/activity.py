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

"""Basic implementation for a Bungie a activity.

NOTE that this is still under development ages,
and you might face some major bugs.
"""

from __future__ import annotations

__all__ = ("Activity", "PostActivity")

import typing
from datetime import datetime

import attr

from aiobungie.internal import enums
from aiobungie.internal import traits


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class PostActivity:
    """Represents a Destiny 2 post activity details."""

    period: datetime = attr.field(repr=True, eq=False, hash=False)
    """The post activity's period utc date."""

    starting_phase: int = attr.field(repr=False, eq=False, hash=False)
    """The postt activity starting phase index.
    For an example if it was 0 that means it's a fresh run"""

    reference_id: int = attr.field(repr=True, eq=False, hash=False)
    """The post activity reference id. AKA the activity hash."""

    mode: typing.Optional[enums.GameMode] = attr.field(repr=True, eq=False, hash=False)
    """The post activity's game mode, Can be `Undefined` if unknown."""

    modes: typing.List[enums.GameMode] = attr.field(repr=False, eq=False, hash=False)
    """A list of the post activity's game mode."""

    membership_type: enums.MembershipType = attr.field(repr=True, eq=False, hash=False)
    """The post activity's membership type."""

    players: typing.Sequence[typing.Dict[str, typing.Any]] = attr.field(repr=False)

    # def get_players(self) -> typing.Sequence[player.Player]:
    #     """Returns a sequence of the players that were in this activity.

    #     Returns
    #     -------
    #     `typing.Sequence[aiobungie.crate.Player]`
    #         the players that were in this activity.
    #     """

    #     players_entries: typing.List[player.Player] = [
    #         isplayer["player"]["destinyUserInfo"] for isplayer in self.players
    #     ]

    #     for raw_player in players_entries:
    #         players_entries.append(raw_player)

    #     return players_entries

    @property
    def is_fresh(self) -> bool:
        """Determines if the activity was fresh or no."""
        return self.starting_phase == 0

    def __int__(self) -> int:
        return self.reference_id


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class Activity:
    """Represents a Bungie Activity."""

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    is_completed: str = attr.field(repr=False, hash=False, eq=False)
    """Check if the activity was completed or no."""

    hash: int = attr.field(hash=True, repr=True, eq=False)
    """The activity's hash."""

    instance_id: int = attr.field(repr=True)
    """The activity's instance id."""

    mode: enums.GameMode = attr.field(hash=False, repr=True)
    """The activity mode or type."""

    kills: int = attr.field(repr=False, eq=False, hash=False)
    """Activity's kills."""

    deaths: int = attr.field(repr=False, eq=False, hash=False)
    """Activity's deaths."""

    period: datetime = attr.field(repr=True, eq=False, hash=False)
    """When did the activity occurred in UTC datetime."""

    assists: int = attr.field(repr=False, eq=False, hash=False)
    """Activity's assists"""

    duration: str = attr.field(repr=True, eq=False, hash=False)
    """A string of The activity's duration, Example format `7m 42s`"""

    player_count: int = attr.field(repr=False, eq=False, hash=False)
    """Activity's player count."""

    member_type: enums.MembershipType = attr.field(repr=False, eq=False, hash=False)
    """The activity player's membership type."""

    kd: float = attr.field(repr=True, eq=False, hash=False)
    """Activity's kill/death ratio."""

    modes: typing.List[enums.GameMode] = attr.field(repr=False, eq=False, hash=False)
    """A list of the post activity's game mode."""

    opponents_defeated: int = attr.field(repr=False)
    """Activity's opponents kills."""

    efficiency: float = attr.field(repr=False)
    """Activity's efficienty."""

    score: int = attr.field(repr=False)
    """Activity's score."""

    completion_reason: str = attr.field(repr=False)
    """The reason why the activity was completed. usually its Unknown."""

    async def post_report(self) -> PostActivity:
        """Get activity's data after its finished.

        Returns
        -------
        `.PostActivity`
        """
        return await self.net.request.fetch_post_activity(self.instance_id)

    def __int__(self) -> int:
        return self.instance_id
