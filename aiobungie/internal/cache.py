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

"""aiobungie Redis and Memory cache."""


from __future__ import annotations

__all__: Sequence[str] = ("Cache", "Hash")

import asyncio
import logging
from typing import Any, Final, List, Sequence

import aredis

from aiobungie.objects import user as user

log: Final[logging.Logger] = logging.getLogger(__name__)
log.setLevel("DEBUG")


class Hash:
    """Implementation of redis hash.

    Attributes
    -----------
    inject: `aredis.StrictRedis`
        an Injector for your redis client.
    """

    __slots__: Sequence[str] = ("_injector",)

    def __init__(self, inject: aredis.StrictRedis, /) -> None:
        self._injector = inject

    async def set(self, hash: str, field: Any, value: Any) -> None:
        """Creates a new hash with field name and a value.

        Parameters
        -----------
        hash: `builtins.str`
                The hash name.
        field: `typing.Any`
                The field name.
        value: `typing.Any`
                The value for the field.
        """
        await self._injector.execute_command("HSET {} {} {}".format(hash, field, value))

    async def setx(self, hash: str, field: Any, value: Any) -> None:
        """A method thats similar to `Hash.set`
        but will not replace the value if one is already exists.

        Parameters
        ----------
        hash: `builtins.str`
                The hash name.
        field: `typing.Any`
                The field name
        value: `typing.Any`
            The value of the field.
        """
        await self._injector.execute_command(f"HSETNX {hash} {field} {value}")

    async def flush(self, *hashes: Sequence[str]) -> None:
        """Removes a hash.

        Parameters
        -----------
        hashes: `typing.Sequence[builtins.str]`
                    The hashes you desire to delete.
        """
        fmt = [h for h in [*tuple(hashes)]]
        for hash in fmt:
            print(hash)
            cmd = await self._injector.execute_command(f"DEL {str(hash)}")
        if cmd != 1:
            log.warning(
                f"Result is {cmd}, Means hash {hashes} doesn't exists. returning."
            )
            return
        print("Flushed", fmt)
        return cmd

    async def len(self, hash: str) -> int:
        """Returns the length of the hash.

        Parameters
        -----------
        hash: `builtins.str`
                The hash name.
        """
        return await self._injector.execute_command("HLEN {}".format(hash))

    async def hashes(self) -> List[str]:
        """Returns all hashes in the cache."""
        keys = await self._injector.execute_command("KEYS *")
        try:
            key = [str(key, "utf-8") for key in keys]
        except TypeError:
            raise
        return key

    async def all(self, hash: str) -> List[str]:
        """Returns all values from a hash.

        Parameters
        -----------
        hash: `builtins.str`
                The hash name.

        Returns
        -------
        `typing.List[builtins.str]`
            A list of string values.
        """
        coro = await self._injector.execute_command(f"HVALS {hash}")
        try:
            found = [str(vals, "utf-8") for vals in coro]
        except TypeError:
            raise
        return found

    async def delete(self, hash: str, field: Any) -> None:
        """Deletes a field from the provided hash.

        Parameters
        ----------
        hash: `builtins.str`
                The hash name.
        field: `typing.Any`
                The field you want to delete.
        """
        await self._injector.execute_command(f"HDEL {hash} {field}")

    async def exists(self, hash: str, field: Any) -> bool:
        """Returns True if the field exists in the hash.

        Parameters
        ----------
        hash: `builtins.str`
                The hash name.
        field: `typing.Any`
                The field name

        Returns: `builtins.bool`
                True if field exists in hash and False if not.
        """
        if await self.get(hash, field) is not None:
            return True
        return False

    async def get(self, hash: str, field: Any) -> str:
        """Returns the value associated with field in the hash stored at key.

        Parameters
        ----------
        hash: `builtins.str`
                The hash name.
        field: `typing.Any`
                The field name
        """
        coro = await self._injector.execute_command(f"HGET {hash} {field}")
        try:
            val = str(coro, "utf-8")
        except TypeError:
            raise aredis.ResponseError(f"Key doesn't exists in {hash} field {field}")
        else:
            return val


class Cache:
    """Redis Cache for interacting with aiobungie."""

    __slots__: Sequence[str] = ("_pool", "hash")

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 6379,
        db: int = 0,
        loop: asyncio.AbstractEventLoop = None,
        **kwargs,
    ) -> None:
        self._pool: aredis.StrictRedis = aredis.StrictRedis(
            host=host,
            port=port,
            db=db,
            kwargs=kwargs,
            loop=asyncio.get_event_loop() or loop,
        )
        self.hash: Hash = Hash(self._pool)

    async def set_user(self, user: user.User, /) -> None:
        await self.put(user.id, user.as_dict)

    async def get_user(self, user: user.User) -> user.User:
        return await self.get(user.id)

    async def flush(self) -> None:
        await self._pool.flushdb()

    async def ttl(self, key: str) -> Any:
        return await self._pool.ttl(key)

    async def get(self, key: Any) -> Any:
        try:
            result = await self._pool.get(key)
            result = str(result, "utf-8")
        except TypeError:
            raise
        return result

    async def put(self, key: Any, value: Any, expires: int = 0) -> None:
        await self._pool.set(key, value)
        if expires:
            await self.expire(key, expires)
        log.debug(
            f"Set Key {key} With value {value} 'expires at' {expires if expires else ''}"
        )

    async def remove(self, key: str) -> None:
        try:
            await self._pool.delete(key)
        except KeyError:
            pass

    async def expire(self, key: str, time: int) -> None:
        await self._pool.expire(key, time)
