from .. import error
from ..utils import Component, DestinyCharecter, ImageProtocol, DestinyGender, DestinyRace
from datetime import datetime
from typing import (
	List,
	Optional,
	Dict,
	Any,
	Union,
	Sequence
)

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

	emblem_icon: Optional[Union[ImageProtocol, str]]
	emblem: Optional[Union[ImageProtocol, str]]
	light: int
	total_played_time: int
	last_played: datetime
	id: int
	_class: DestinyCharecter
	member_id: int
	last_session: int
	race: DestinyRace
	gender: DestinyGender
	_resp: Dict[str, Any]
	_char: DestinyCharecter

	def __init__(self, *, char: DestinyCharecter, data: Dict[str, Any]) -> None:
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
			self.emblem_icon = ImageProtocol(lock.get('emblemPath'))
			self.emblem = ImageProtocol(lock.get('emblemBackgroundPath'))
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
			self.emblem_icon = ImageProtocol(lock.get('emblemPath'))
			self.emblem = ImageProtocol(lock.get('emblemBackgroundPath'))
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
			self.emblem_icon = ImageProtocol(lock.get('emblemPath'))
			self.emblem = ImageProtocol(lock.get('emblemBackgroundPath'))
			self.member_id = lock.get('membershipId')
			self.total_played_time = lock.get('minutesPlayedTotal')
			self.gender = DestinyGender(data=lock.get('genderType'))
			self._class = DestinyCharecter(data=lock.get('classType'))
			self.last_session = lock.get('minutesPlayedThisSession')
			self.last_played = lock.get('dateLastPlayed')
			self.race = DestinyRace(data=lock.get('raceType'))
		else:
			None