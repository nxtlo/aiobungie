'''
MIT License

Copyright (c) 2020 - Present nxtlo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from .. import error
from datetime import datetime
from typing import (
	List,
	Optional,
	Dict,
	Any,
	Union,
	Sequence,
	TYPE_CHECKING
)

# if TYPE_CHECKING:
from ..utils.enums import Component, DestinyCharecter, DestinyGender, DestinyRace
from ..utils import Image
from ..types.character import Character as CharacterPayload

__all__: Sequence[str] = (
	'Character'
	, 
)

class Character:
	__slots__: Sequence[str] = (
		'_resp', 'emblem_icon', 'emblem', 'light', 'total_played_time',
		'id', '_class', 'member_id', 'gender', 'race', 'last_played',
		'last_session', '_char'
	)

	_resp: Dict[str, Any]
	_char: DestinyCharecter

	if TYPE_CHECKING:
		emblem_icon: Optional[Union[Image, str]]
		emblem: Optional[Union[Image, str]]
		light: int
		total_played_time: int
		last_played: datetime
		id: int
		_class: DestinyCharecter
		member_id: int
		last_session: int
		race: DestinyRace
		gender: DestinyGender

	def __init__(self, *, char: DestinyCharecter, data: Any) -> None:
		self._resp = data.get('Response', {})['characters']['data']
		self._char = char
		self._update(self._resp)

	# This one right here is kinda Yandare type beat
	# i will find a better way to rewrite this lol.
	def _update(self, data: Dict[str, Any]) -> None:
		self._resp = [x for x in self._resp.values()]
		if self._char is DestinyCharecter.WARLOCK:
			lock = self._resp[2]
			self.id = lock.get('characterId')
			self.light = lock.get('light')
			self.emblem_icon = Image(lock.get('emblemPath'))
			self.emblem = Image(lock.get('emblemBackgroundPath'))
			self.member_id = lock.get('membershipId')
			self.total_played_time = lock.get('minutesPlayedTotal')
			self.gender = DestinyGender(data=lock.get('genderType'))
			self._class = DestinyCharecter(data=lock.get('classType'))
			self.last_session = lock.get('minutesPlayedThisSession')
			self.last_played = lock.get('dateLastPlayed')
			self.race = DestinyRace(data=lock.get('raceType'))
		elif self._char is DestinyCharecter.HUNTER:
			lock = self._resp[1]
			self.id = lock.get('characterId')
			self.light = lock.get('light')
			self.emblem_icon = Image(lock.get('emblemPath'))
			self.emblem = Image(lock.get('emblemBackgroundPath'))
			self.member_id = lock.get('membershipId')
			self.total_played_time = lock.get('minutesPlayedTotal')
			self.gender = DestinyGender(data=lock.get('genderType'))
			self._class = DestinyCharecter(data=lock.get('classType'))
			self.last_session = lock.get('minutesPlayedThisSession')
			self.last_played = lock.get('dateLastPlayed')
			self.race = DestinyRace(data=lock.get('raceType'))
		elif self._char is DestinyCharecter.TITAN:
			lock = self._resp[0]
			self.id = lock.get('characterId')
			self.light = lock.get('light')
			self.emblem_icon = Image(lock.get('emblemPath'))
			self.emblem = Image(lock.get('emblemBackgroundPath'))
			self.member_id = lock.get('membershipId')
			self.total_played_time = lock.get('minutesPlayedTotal')
			self.gender = DestinyGender(data=lock.get('genderType'))
			self._class = DestinyCharecter(data=lock.get('classType'))
			self.last_session = lock.get('minutesPlayedThisSession')
			self.last_played = lock.get('dateLastPlayed')
			self.race = DestinyRace(data=lock.get('raceType'))
		else:
			None