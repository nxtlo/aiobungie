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

"""Interfaces used for the core aiobungie implementations."""

from __future__ import annotations

import pathlib

__all__ = ("ClientApp", "Netrunner", "Serializable", "RESTful", "Debug")

import typing

if typing.TYPE_CHECKING:
    import collections.abc as collections

    from aiobungie import builders
    from aiobungie import client
    from aiobungie import interfaces
    from aiobungie import rest
    from aiobungie.internal import factory as factory_


@typing.runtime_checkable
class Netrunner(typing.Protocol):
    """Types that can run external requests.

    These requests are performed by a reference of your `aiobungie.Client` instance.

    Example
    -------
    ```py
    import aiobungie

    membership = aiobungie.crate.DestinyMembership(…)
    # Access the base client that references this membership.
    external_request = await membership.net.request.fetch_user(…)
    ```
    """

    __slots__ = ()

    @property
    def request(self) -> client.Client:
        """A readonly `ClientApp` instance used for external requests."""
        raise NotImplementedError


@typing.runtime_checkable
class Serializable(typing.Protocol):
    """Types which can deserialize REST payloads responses
    into a `aiobungie.crate` implementation using the `Serializable.factory` property.

    Only `ClientApp` implement this trait
    """

    __slots__ = ()

    @property
    def factory(self) -> factory_.Factory:
        """Returns the marshalling factory for the client."""
        raise NotImplementedError


@typing.runtime_checkable
class Debug(typing.Protocol):
    """Objects that are able to enable debugging REST calls."""

    def enable_debugging(
        self,
        level: typing.Union[typing.Literal["TRACE"], bool] = False,
        file: typing.Optional[typing.Union[pathlib.Path, str]] = None,
        /,
    ) -> None:
        """Enables debugging for the REST calls.

        Logging Levels
        --------------
        * `False`: This will disable logging.
        * `True`: This will set the level to `DEBUG` and enable logging minimal information.
        * `"TRACE"` | `aiobungie.TRACE`: This will log the response headers along with the minimal information.

        Parameters
        -----------
        level : `str | bool | int`
            The level of debugging to enable.
        file : `pathlib.Path | str | None`
            The file path to write the debug logs to. If provided.
        """
        raise NotImplementedError


@typing.runtime_checkable
class RESTful(Debug, typing.Protocol):
    """Types which it is possible to interact with the API directly
    which provides RESTful functionalities.

    Only `aiobungie.RESTClient` implement this trait,
    `ClientApp` may access its RESTClient using `ClientApp.rest` property.
    """

    __slots__ = ()

    @property
    def client_id(self) -> typing.Optional[int]:
        """Return the client id of this REST client if provided, Otherwise None."""
        raise NotImplementedError

    @property
    def metadata(self) -> collections.MutableMapping[typing.Any, typing.Any]:
        """A mutable mapping storage for the user's needs.

        This mapping is useful for storing any kind of data that the user may need.

        Example
        -------
        ```py
        import aiobungie

        client = aiobungie.RESTClient(…)

        async with client:
            # Fetch auth tokens and store them
            client.metadata["tokens"] = await client.fetch_access_token("code")

        # Some other time.
        async with client:
            # Retrieve the tokens
            tokens: aiobungie.OAuth2Response = client.metadata["tokens"]

            # Use them to fetch your user.
            user = await client.fetch_current_user_memberships(tokens.access_token)
        ```
        """
        raise NotImplementedError

    @property
    def is_alive(self) -> bool:
        """Returns `True` if the REST client is alive and `False` otherwise."""
        raise NotImplementedError

    def build_oauth2_url(
        self, client_id: typing.Optional[int] = None
    ) -> typing.Optional[builders.OAuthURL]:
        """Builds an OAuth2 URL using the provided user REST/Base client secret/id.

        You can't get the complete string URL by using `.compile()` method.

        Parameters
        ----------
        client_id : `int | None`
            An optional client id to provide, If left `None` it will roll back to the id passed
            to the `RESTClient`, If both is `None` this method will return `None`.

        Returns
        -------
        `aiobungie.builders.OAuthURL | None`
            If the client id was provided as a parameter or provided in `aiobungie.RESTClient`,
            A complete OAuthURL object will be returned.
            Otherwise `None` will be returned.
        """
        raise NotImplementedError

    def open(self) -> None:
        """Prepare and opens the REST client connection.

        This method is automatically called when using `async with` contextmanager.

        Raises
        ------
        `RuntimeError`
            If the client is already open.
        """
        raise NotImplementedError

    async def close(self) -> None:
        """Close this REST client session if it was acquired.

        This method is automatically called when using `async with` contextmanager.

        Raises
        ------
        `RuntimeError`
            If the client is already closed.
        """
        raise NotImplementedError

    async def static_request(
        self,
        method: typing.Union[rest.RequestMethod, str],
        path: str,
        *,
        auth: typing.Optional[str] = None,
        json: typing.Optional[dict[str, typing.Any]] = None,
    ) -> rest.ResponseSig:
        """Perform an HTTP request given a valid Bungie endpoint.

        Parameters
        ----------
        method : `aiobungie.rest.RequestMethod | str`
            The request method, This may be `GET`, `POST`, `PUT`, etc.
        path: `str`
            The Bungie endpoint or path.
            A path must look something like this `Destiny2/3/Profile/46111239123/...`
        auth : `str | None`
            An optional bearer token for methods that requires OAuth2 Authorization header.
        json : `dict[str, typing.Any] | None`
            An optional JSON data to include in the request.

        Returns
        -------
        `aiobungie.rest.ResponseSig`
            The response payload.
        """
        raise NotImplementedError


@typing.runtime_checkable
class ClientApp(Netrunner, Serializable, typing.Protocol):
    """Core trait for the standard `aiobungie.Client` implementation.

    This includes all aiobungie traits.
    """

    __slots__ = ()

    def run(
        self, future: collections.Coroutine[None, None, None], debug: bool = False
    ) -> None:
        """Runs a coroutine function until its complete.

        This is equivalent to `asyncio.get_event_loop().run_until_complete(...)`

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

        # Run the coroutine.
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
