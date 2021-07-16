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

'''A module for Encrypting and Decrypting for OAuth2 data.'''


from __future__ import annotations

__all__ = ['Crypt']

from typing import Union, Sequence, Final
from cryptography.fernet import Fernet
from logging import getLogger, Logger

log: Final[Logger] = getLogger(__name__)



class Crypt:
	'''
	an Object half inherits `cryptography.Fernet` to decrypt and encrypt data.

	Attributes
	-----------
	entry: `builtins.bytes`
		The data entry you wanna encrypt and decrypt
	
	instance: `cryptography.Fernet`
		The default for this attr is `cryptography.Fernet` and should not be changed
		it can be None or your own `cryptography.Fernet` instance.
	'''
	__slots__: Sequence[str] = ('_entry', '_instance')

	def __init__(self, entry: bytes) -> None:
		self._entry = entry
		self._instance: Fernet = Fernet(Fernet.generate_key())

	def encrypt(self) -> bytes:
		return self._instance.encrypt(self._entry)

	def decrypt(self, token: bytes, ttl: int = None) -> Union[bytes, str]:
		key = self._instance.decrypt(token, ttl)
		if not key:
			log.warn(f"Couldn't decrypt key.")
		return key.strip()