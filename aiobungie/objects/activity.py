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

__all__: Sequence[str] = (
	'Activity',
)

from typing import Dict, Sequence, Optional, Any, TYPE_CHECKING, Optional
from ..error import HashError
from ..utils.enums import GameMode, MembershipType, Raid

if TYPE_CHECKING:
	from datetime import datetime

class Activity:
	"""Represents a Bungie Activity object.

	An activity can be one of :class:`.GameMode`.

	Attributes
	-----------
	mode: :class:`.GameMode`:
		The activity mode or type.
	is_completed: :class:`str`:
		Check if the activity was completed or no.
	hash: :class:`.Raid`:
		This is a special attr used only for raids that returns the raid name.
	raw_hash: :class:`int`
		The activity's hash.
	duration: :class:`str`:
		A string of The activity's duration, Example format `7m 42s`
	kills: :class:`int`
		Activity's Total kills
	deaths: :class:`int`
		Activity's total deaths.
	assists: :class:`int`
		Activity's Total assists
	kd: :class:`int`
		Activity's kd ration.
	member_type: :class:`.MembershipType`:
		The activity member's membership type.
	players_count: :class:`int`
		Total players in the activity.
	when: :class:`typing.Optional[datetime.datetime]:
		When did the activity occurred in UTC datetime.
	"""
	__slots__: Sequence[str] = (
		'is_completed', 'mode', 'kills',
		'deaths', 'assists', 'kd', 'duration', 
		'player_count','when', 'member_type', 
		'hash'
	)
	is_completed: str
	hash: Raid # Only for raids since we're not going to store everysingle other activity.
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

	def _update(self, data: Dict[str, Any]):
		...