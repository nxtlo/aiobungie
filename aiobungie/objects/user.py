import logging
from ..utils import Image, Time
from ..error import UserNotFound
from typing import TYPE_CHECKING, Sequence, Optional, Union, Any, Final
from datetime import datetime

# if TYPE_CHECKING:
from ..types.user import User as UserPayload

log: Final[logging.Logger] = logging.getLogger(__name__)

class User:
	''' Represents a Bungie User object.

	Attributes
	----------
	id: :class:`int`:
		The user's id
	name: :class:`str`:
	is_deleted: :class:`bool`:
		Returns True if the user is deleted
	about: :class:`str`:
		The user's about, Default is None if nothing is Found.
	created_at: :class:`datetime`:
		The user's creation date in UTC date.
	updated_at: :class:`datetime`:
		The user's last updated om UTC date.
	psn_name: :class:`str`:
		The user's psn id if it exists.
	twitch_name: :class:`str`:
		The user's twitch name if it exists.
	blizzard_name: :class:`str`:
		The user's blizzard name if it exists.
	steam_name: :class:`str`:
		The user's steam name if it exists
	status: :class:`str`:
		The user's bungie status text
	locale: :class:`str`:
		The user's locale.
	picture: :class:`.Image`:
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
		'id'
	)

	def __init__(self, *, data: UserPayload, position: int = None) -> None:
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


	def _update(self, data: UserPayload, posotion: int = None) -> None:
		try:
			data = data or data[posotion] # type: ignore
		except IndexError:
			if posotion or posotion is None:
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