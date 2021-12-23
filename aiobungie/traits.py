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
    import collections.abc as collections

    from aiobungie import client as base_client
    from aiobungie import interfaces
    from aiobungie import rest
    from aiobungie.internal import factory as factory_


@typing.runtime_checkable
class Netrunner(typing.Protocol):
    """A supertype protocol represents The `ClientBase`.

    Objects with this protocol can make requests from outside the base client.
    """

    __slots__ = ()

    @property
    def request(self) -> base_client.Client:
        """Returns a client network state for making external requests."""
        raise NotImplementedError


@typing.runtime_checkable
class Serializable(typing.Protocol):
    """A serializable supertype object protocol.

    Objects with this protocol can serialize JSON REST payloads into
    a Python data class objects using the client factory.
    """

    __slots__ = ()

    @property
    def factory(self) -> factory_.Factory:
        """Returns the entity factory for the client."""
        raise NotImplementedError


@typing.runtime_checkable
class RESTful(typing.Protocol):
    """A RESTful only supertype object protocol."""

    __slots__ = ()

    def build_oauth2_url(
        self, client_id: typing.Optional[int] = None
    ) -> typing.Optional[str]:
        """Builds an OAuth2 URL.

        Parameters
        ----------
        client_id : `typing.Optional[int]`
            An optional client id to provide, If left `None` it will roll back to the id passed
            to the `RESTClient`, If both is `None` this method will return `None`.

        Returns
        -------
        `typing.Optional[str]`
            If the client id was provided as a parameter or provided in `aiobungie.RESTClient`,
            A complete URL will be returned.
            Otherwise `None` will be returned.
        """
        raise NotImplementedError

    @property
    def client_id(self) -> typing.Optional[int]:
        """Return the client id of this REST client if provided, Otherwise None"""
        raise NotImplementedError

    async def close(self) -> None:
        """Close the rest client."""
        raise NotImplementedError

    async def static_request(
        self,
        method: typing.Union[rest.RequestMethod, str],
        path: str,
        auth: typing.Optional[str] = None,
        **kwargs: typing.Any
    ) -> typing.Any:
        """Raw http request given a valid bungie endpoint.

        Parameters
        ----------
        method : `typing.Union[aiobungie.rest.RequestMethod, str]`
            The request method, This may be `GET`, `POST`, `PUT`, etc.
        path: `str`
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
        raise NotImplementedError


@typing.runtime_checkable
class ClientBase(Netrunner, Serializable, typing.Protocol):
    """A Pythonic Client supertype, serializble and netrunner protocol."""

    __slots__ = ()

    def run(
        self, future: collections.Coroutine[None, None, None], debug: bool = False
    ) -> None:
        """Runs a Coro function until its complete.
        This is equivalent to asyncio.get_event_loop().run_until_complete(...)

        Parameters
        ----------
        future: `collections.Coroutine[None, None, None]`
            A coroutine object.
        debug : `bool`
            Either to enable asyncio debug or not. Disabled by default.

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
        raise NotImplementedError
