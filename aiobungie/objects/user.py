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

"""Basic implementation for a Bungie a user."""


from __future__ import annotations

__all__: Sequence[str] = [
	'User'
]

import logging
from ..utils import Image, Time
from ..error import UserNotFound
from typing import TYPE_CHECKING, Sequence, Optional, Union, Any, Final

if TYPE_CHECKING:
	from datetime import datetime
	from ..types.user import User as UserPayload

log: Final[logging.Logger] = logging.getLogger(__name__)

class User:
	''' Represents a Bungie User object.

	Attributes
	----------
	id: `builtins.int`
		The user's id
	name: `builtins.str`
		The user's name.
	is_deleted: `builtins.bool`
		Returns True if the user is deleted
	about: typing.Optional[builtins.str]
		The user's about, Default is None if nothing is Found.
	created_at: `datetime.datetime`
		The user's creation date in UTC date.
	updated_at: `datetime.datetime`
		The user's last updated om UTC date.
	psn_name: typing.Optional[builtins.str]
		The user's psn id if it exists.
	twitch_name: typing.Optional[builtins.str]
		The user's twitch name if it exists.
	blizzard_name: typing.Optional[builtins.str]
		The user's blizzard name if it exists.
	steam_name: typing.Optional[builtins.str]
		The user's steam name if it exists
	status: typing.Optional[builtins.str]
		The user's bungie status text
	locale: typing.Optional[builtins.str]
		The user's locale.
	picture: typing.Optional[aiobungie.utils.assets.Image]
		The user's avatar.
	'''
	__slots__: Sequence[str] = (
		'is_deleted', 
		'about', 
		'created_at', 
		'updated_at',
		'psn_name', 
		'steam_name', 
		'twitch_name', 
		'blizzard_name',
		'status', 
		'locale', 
		'picture', 
		'name', 
		'id',
	)

	def __init__(self, *, data: UserPayload, position: int = 0) -> None:
		self._update(data, position)

	@property
	def human_time(self) -> str:
		'''Returns a human readble of the user's creation date'''
		return Time.human_timedelta(self.created_at)

	def __str__(self) -> str:
		return str(self.name)

	def __int__(self) -> int:
		return int(self.id)

	def __bool__(self) -> bool:
		return bool(self.is_deleted)

	def __hash__(self) -> int:
		return hash(self.id)
	
	def __repr__(self) -> str:
		return (
			f'User name={self.name} id={self.id} about={self.about} created_at={self.created_at}'
			f' blizzard_name={self.blizzard_name} steam_name={self.steam_name} status={self.status}'
		)

	def __eq__(self, other: Any) -> bool:
		return isinstance(other, User) and other.id == self.id

	def __ne__(self, other: Any) -> bool:
		return not self.__eq__(other)


	def _update(self, data: UserPayload, posotion: int = 0) -> None:
		try:
			data = data[posotion] # type: ignore
		except KeyError:
			pass
		except IndexError:
			if posotion or posotion == 0:
				raise UserNotFound("Player was not found.")

		self.id: int = data['membershipId']
		self.name: str = data['displayName']
		self.is_deleted: bool = data['isDeleted']
		self.about: Optional[str] = data['about']
		self.created_at: datetime = Time.clean_date(data['firstAccess'])
		self.updated_at: datetime = Time.clean_date(data['lastUpdate'])
		self.psn_name: Optional[str] = data.get('psnDisplayName', None)
		self.steam_name: Optional[str] = data.get('steamDisplayName', None)
		self.twitch_name: Optional[str] = data.get('twitchDisplayName', None)
		self.blizzard_name: Optional[str] = data.get('blizzardDisplayName', None)
		self.status: Optional[str] = data['statusText']
		self.locale: Optional[str] = data['locale']
		self.picture: Optional[Image] = Image(path=str(data['profilePicturePath']))