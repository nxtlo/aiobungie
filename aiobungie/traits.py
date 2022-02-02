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

"""Interfaces used for the main clients implementations."""

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
    """A supertype protocol represents a readonly `ClientBase`.

    Clients that implements this can make requests from outside the base client.
    This is useually used within the `aiobungie.crate` implementations for easier access to the base client instance.
    """

    __slots__ = ()

    @property
    def request(self) -> base_client.Client:
        """A readonly `ClientBase` instance used for external requests."""
        raise NotImplementedError


@typing.runtime_checkable
class Serializable(typing.Protocol):
    """A supertype protocol for deserializable clients.

    Clients that implements this can deserialize JSON REST payloads into
    a Python `aiobungie.crate` object using the client `aiobungie.internal.factory.Factory`.
    """

    __slots__ = ()

    @property
    def factory(self) -> factory_.Factory:
        """Returns the marshalling factory for the client."""
        raise NotImplementedError


@typing.runtime_checkable
class RESTful(typing.Protocol):
    """A RESTful only supertype protocol.

    Clients with this are raw-only JSON REST clients. i.e., `aiobungie.rest.RESTClient`
    """

    __slots__ = ()

    def build_oauth2_url(
        self, client_id: typing.Optional[int] = None
    ) -> typing.Optional[str]:
        """Builds an OAuth2 URL using the provided user REST/Base client secret/id.

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

    @property
    def metadata(self) -> collections.MutableMapping[typing.Any, typing.Any]:
        """A mutable mapping storage for the user's needs."""
        raise NotImplementedError

    async def close(self) -> None:
        """Close the rest client."""
        raise NotImplementedError

    async def static_request(
        self,
        method: typing.Union[rest.RequestMethod, str],
        path: str,
        auth: typing.Optional[str] = None,
        json: typing.Optional[dict[str, typing.Any]] = None,
        **kwargs: typing.Any,
    ) -> typing.Any:
        """Perform an HTTP request given a valid Bungie endpoint.

        Parameters
        ----------
        method : `typing.Union[aiobungie.rest.RequestMethod, str]`
            The request method, This may be `GET`, `POST`, `PUT`, etc.
        path: `str`
            The Bungie endpoint or path.
            A path must look something like this `Destiny2/3/Profile/46111239123/...`
        auth : `typing.Optional[str]`
            An optional bearer token for methods that requires OAuth2 Authorization header.
        json : `typing.Optional[dict[str, typing.Any]]`
            An optional JSON data to include in the request.
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
    """A supertype that implements all protocols.

    This can also access its REST client via `ClientBase.rest`
    """

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
            await fetch(...)

        # Run the coro.
        client.run(main())
        ```
        """

    @property
    def rest(self) -> interfaces.RESTInterface:
        """Returns the REST client for the this client."""
        raise NotImplementedError

    @property
    def metadata(self) -> collections.MutableMapping[typing.Any, typing.Any]:
        """A mutable mapping storage for the user's needs."""
        raise NotImplementedError
