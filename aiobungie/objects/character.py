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

"""Basic Implementation for a Bungie Character."""

from __future__ import annotations

__all__: Sequence[str] = ('Character', )

from ..utils import Image
from .. import error
from typing import (
	List,
	Optional,
	Dict,
	Any,
	Union,
	Sequence,
	TYPE_CHECKING
)

if TYPE_CHECKING:
	from ..utils.enums import Component, DestinyCharacter, DestinyGender, DestinyRace
	from datetime import datetime
	from ..types.character import Character as CharacterPayload


class Character:
	"""Represents a Bungie Character Object.

	A Bungie character object can be a Warlock, Titan or a Hunter.

	Attributes
	-----------
	light: `builtins.int`
		The character's light
	id: `builtins.int`
		The character's id
	gender: `aiobungie.utils.enums.DestinyGender`
		The character's gender
	race: `aiobungie.utils.enums.DestinyRace`
		The character's race
	emblem: typing.Optional[aiobungie.utils.assets.Image]
		The character's currnt equipped emblem.
	emblem_icon: typing.Optional[aiobungie.utils.assets.Image]
		The character's current icon for the equipped emblem.
	last_played: `datetime.datetime`
		When was this character last played date in UTC.
	last_session: `builtins.int`
		The player's last session.
	total_played_time: `builtins.int`
		Returns the total played time in seconds for the chosen character.
	member_id: `builtins.int`
		The character's member id.
	cls: `aiobungie.utils.enums.DestinyCharacter`
		The character's class.
	"""

	__slots__: Sequence[str] = (
		'emblem_icon', 
		'emblem', 
		'light', 
		'total_played_time',
		'id', 
		'cls',
		'member_id', 
		'gender', 
		'race', 
		'last_played',
		'last_session', 
		'_char'
	)

	_char: Union[DestinyCharacter, int]

	emblem_icon: Optional[Union[Image, str]]
	emblem: Optional[Union[Image, str]]
	light: int
	total_played_time: int
	last_played: datetime
	id: int
	cls: DestinyCharacter
	member_id: int
	last_session: int
	race: DestinyRace
	gender: DestinyGender

	def __init__(self, *, char: Union[DestinyCharacter, int], data: Any = ...) -> None:
		self._char = char
		self._update(data)

	def _update(self, data: Any = ...) -> None:
		...