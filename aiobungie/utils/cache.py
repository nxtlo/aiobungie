from typing import (
	Dict
	, Sequence
	, Final
	, Any
)
import asyncio
import logging
import aredis

log: Final[logging.Logger] = logging.getLogger(__name__)

class RefreshNotFound(Exception):
	pass

class AccessNotFound(Exception):
	pass

class EmptyCache(Exception):
	pass

__all__: Sequence[str] = (
	'RedisCache', 'MemoryCache', 'Hash'
)

class Hash:
	'''
	Implementation of redis hash.

	Attributes
	-----------
	inject: :class:`aredis.StrictRedis`:
		an Injector for your redis client.
	'''
	__slots__: Sequence = (
		'_injector',
	)
	def __init__(self, inject: aredis.StrictRedis) -> None:
		self._injector = inject

	async def set(self, hash: str, field: str, value: str) -> Any:
		'''
		Creates a new hash with field name and a value.

		Paramaters
		-----------
		hash: :class:`str`:
			The hash name.
		firld: :class:`str`:
			The field name.
		value: :class:`str`:
			The value for the field.
		'''
		return await self._injector.execute_command("HSET {} {} {}".format(hash, field, value))

	async def setx(self, hash: str, field: str) -> Any:
		'''
		A method thats similar to :meth:`Hash.set`
		but will not replace the value if one is already exists.

		Paramaters
		----------
		hash: :class:`str`:
			The hash name.
		field: :class:`str`:
			The field name
		'''
		await self._injector.execute_command(f"HSETNX {hash} {field}")

	async def flush(self, hash: str) -> Any:
		'''
		Removes a hash.

		Paramaters
		-----------
		hash: :class:`str`:
			The hash name.

		'''
		cmd = await self._injector.execute_command(f"DEL {hash}")
		if cmd != 1:
			log.warn(f"Result is {cmd}, Means hash {hash} doesn't exists. returning.")
			return
		return cmd

	async def len(self, hash: str) -> int:
		'''
		Returns the length of the hash.

		Paramaters
		-----------
		hash: :class:`str`:
			The hash name.
		'''
		return await self._injector.execute_command("HLEN {}".format(hash))


	async def all(self, hash: str) -> Any:
		'''
		Returns all values from a hash.

		Paramaters
		-----------
		hash: :class:`str`:
			The hash name.

		Returns
		-------
		:class:`List[Any]`:
			a List of any values.
		'''
		coro = await self._injector.execute_command(f"HVALS {hash}")
		for tries in range(5):
			for k, v in enumerate(coro):
				val = str(v, 'utf-8')
				try:
					return f'{k}: {val}'
				except TypeError:
					log.debug("Couldn't format data")
					await asyncio.sleep(1 + tries * 2)
					continue
		return coro

	async def delete(self, hash: str, field: str) -> Any:
		'''
		Deletes a field from the provided hash.

		Paramaters
		----------
		hash: :class:`str`:
			The hash name.
		field: :class:`str`:
			The field you want to delete.
		'''
		return await self._injector.execute_command(f"HDEL {hash} {field}")

	async def exists(self, hash: str, field: str) -> bool:
		'''
		Returns True if the field exists in the hash.

		Paramaters
		----------
		hash: :class:`str`:
			The hash name.
		field: :class:`str`;
			The field name
		
		Returns: :class:`bool`:
			True if field exists in hash and False if not.
		'''

	async def get(self, hash: str, field: str) -> str:
		'''
		Returns the value associated with field in the hash stored at key.

		Paramaters
		----------
		hash: :class:`str`:
			The hash name.
		field: :class:`str`:
			The field name

		Returns
		--------
		:class:`AnyStr`
		'''
		coro = await self._injector.execute_command(f"HGET {hash} {field}")
		try:
			val = str(coro, 'utf-8')
		except TypeError:
			raise aredis.ResponseError(f"Key doesn't exists in {hash} field {field}")
		else:
			return val


class RedisCache:
	'''
	Redis Cache for access and refresh tokens.
	'''
	__slots__: Sequence[str] = (
		'_pool', 'hash'
	)
	def __init__(self) -> None:
		self._pool: aredis.StrictRedis = aredis.StrictRedis('127.0.0.1', port=6379, db=0)
		self.hash: Hash = Hash(self._pool)

	async def flush(self) -> None:
		await self._pool.flushdb()

	async def ttl(self, key: str) -> Any:
		return await self._pool.ttl(key)

	async def put(self, key: str, value: str, expires: int = 0) -> None:
		await self._pool.set(key, value)
		if expires:
			await self.expire(key, expires)
		log.debug(f"Set Key {key} With value {value} 'expires at' {expires if expires else ''}")

	async def remove(self, key: str) -> None:
		try:
			await self._pool.delete(key)
		except KeyError:
			pass

	async def expire(self, key: str, time: int) -> None:
		await self._pool.expire(key, time)

class MemoryCache:
	'''
	Implemention for token and refresh_token in memory cache.
	'''
	__slots__: Sequence[str] = ('_token', '_refresh', '__entry')


	def __init__(self, token: str, refresh: str) -> None:
		self._token: str = token
		self._refresh: str = refresh
		self.__entry: Dict[str, str] = {}

	def getToken(self) -> str:
		'''Retrives the access token from cache.'''
		try:
			if self.__entry['token'] is None:
				log.warn(self.__entry.items())
			raise ValueError("Token is not cached")
		except KeyError:
			pass
		return self.__entry['token']
	

	def getRefresh(self) -> str:
		try:
			if self.__entry['refresh'] is None:
				log.warn(self.__entry.items())
			raise ValueError("Refresh token is not cached")
		except KeyError:
			pass
		return self.__entry['refresh']
	
	def put(self) -> None:
		if not self._token:
			raise ValueError("Access Token is Missing!")
		elif not self._refresh:
			raise ValueError("Refresh token is Missing")
		self.__entry['token'] = self._token
		self.__entry['refresh'] = self._refresh
		log.info("Tokens cached.")

	def clear(self) -> None:
		self.__entry.clear()
		log.info("Cache cleared.")

	def pop(self, item: str) -> None:
		if self.__entry.get(item) is not None:
			self.__entry.pop(item)
			log.info(f"Poped item {item}")
		raise EmptyCache(f"Item {item} was not found in cache")

	def all(self) -> list:
		return sorted([i for i in self.__entry.items()])

	def refreshNext(self, token: str, refresh: str) -> None:
		self.clear() # Clear the cache
		self.__entry['token'] = token
		self.__entry['refresh'] = refresh

	async def refreshTokens(self, token: str, refresh: str) -> None:
		if self.__entry.items() is None:
			raise EmptyCache(f"The cache is empty, Values found: {self.__entry.items()}")
		try:
			self.refreshNext(token, refresh)
		except KeyboardInterrupt:
			raise Warning("Your keyboard cancled the loop.")
		log.info("Token refreshed")