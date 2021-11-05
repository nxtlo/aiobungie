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

"""Module for all client interfaces."""

from __future__ import annotations

__all__ = ("ClientBase", "Netrunner", "Serializable", "RESTful")

import typing

if typing.TYPE_CHECKING:
    from aiohttp import typedefs

    from aiobungie import client as base_client
    from aiobungie import interfaces
    from aiobungie import rest
    from aiobungie.internal import factory


@typing.runtime_checkable
class Netrunner(typing.Protocol):
    """A supertype protocol represents The `ClientBase`.

    Objects with this protocol can make requests from outside the base client.
    """

    __slots__: typing.Sequence[str] = ()

    @property
    def request(self) -> base_client.Client:
        """Returns a client network state for making external requests."""


@typing.runtime_checkable
class Serializable(typing.Protocol):
    """A serializable supertype object protocol.

    Objects with this protocol can serialize JSON REST payloads into
    a Python data class objects using the client factory.
    """

    __slots__: typing.Sequence[str] = ()

    @property
    def serialize(self) -> factory.Factory:
        """Returns the entity factory for the client."""


@typing.runtime_checkable
class RESTful(typing.Protocol):
    """A RESTful only supertype object protocol."""

    __slots__: typing.Sequence[str] = ()

    async def close(self) -> None:
        """Close the rest client."""

    async def static_request(
        self,
        method: typing.Union[rest.RequestMethod, str],
        path: typedefs.StrOrURL,
        auth: typing.Optional[str] = None,
        **kwargs: typing.Any
    ) -> typing.Any:
        """Raw http request given a valid bungie endpoint.

        Parameters
        ----------
        method : `typing.Union[aiobungie.rest.RequestMethod, str]`
            The request method, This may be `GET`, `POST`, `PUT`, etc.
        path: `typing.Union[str, yarl.URL]`
            The bungie endpoint or path.
            A path must look something like this
            `Destiny2/3/Profile/46111239123/...`
        auth : `typing.Optional[str]`
            An optional bearer token for methods that requires OAuth2 Authorization header.
        **kwargs: `typing.Any`
            Any other key words to pass to the request.

        Returns
        -------
        `typing.Any`
            Any object.
        """


@typing.runtime_checkable
class ClientBase(Netrunner, Serializable, typing.Protocol):
    """A Pythonic Client supertype, serializble and netrunner protocol."""

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
            # DO SOME ASYNC WORK

        # Run the coro.
        client.run(main())
        ```
        """

    @property
    def rest(self) -> interfaces.RESTInterface:
        """Returns the REST client for the this client."""
