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

"""A base module for all client implementation."""

from __future__ import annotations

__all__ = ("RESTful", "Netrunner")

import typing

from aiobungie import client as client_


@typing.runtime_checkable
class Netrunner(typing.Protocol):
    """A netrunner client represents The rest client.
    This is only used for making external requests.
    """

    __slots__: typing.Sequence[str] = ()

    @property
    def request(self) -> client_.Client:
        """Returns a client network state for making external requests."""
        raise NotImplementedError


@typing.runtime_checkable
class RESTful(Netrunner, typing.Protocol):
    """A Resuful and netrunner client protocol."""

    __slots__: typing.Sequence[str] = ()

    def run(
        self, future: typing.Coroutine[typing.Any, None, None], debug: bool = False
    ) -> None:
        """Runs a Coro function until its complete.
        This is equivalent to asyncio.get_event_loop().run_until_complete(...)

        Parameters
        ----------
        future: `typing.Coroutine[typing.Any, typing.Any, typing.Any]`
            Your coro function.

        Example
        -------
        ```py
        async def main() -> None:
            player = await client.fetch_player("Fate")
            print(player.name)

        client.run(main())
        ```
        """
        raise NotImplementedError
