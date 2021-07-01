from typing import Union, Sequence, Optional, Any
from cryptography.fernet import Fernet
from logging import getLogger
import colorama

log = getLogger(__name__)

__all__ = (
	'Crypt',
)

class Crypt:
	__slots__: Sequence[str] = ('_entrie',)

	def __init__(self, entrie: Any = None) -> None:
		self._entrie = entrie

	def encrypt(self) -> None:
		_key = Fernet.generate_key()
		meth = Fernet(_key)
		try:
			return meth.encrypt(self._entrie)
		except Exception as e:
			raise f'<{e!r}>'

	def decrypt(self, token: Union[bytes, str], ttl: int = None) -> Union[bytes, str]:
		try:
			key = Fernet.decrypt(token, ttl)
		except Exception as e:
			log.warn(colorama.Fore.RED + f"Couldn't decrypt key due: {e!r}")
		return key.strip()