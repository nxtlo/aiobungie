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

"""Interfaces used for the core aiobungie client implementations.

An aiobungie `trait` is a collection of methods defined for an known object. See `aiobungie.EmptyFactory` for more.
```
"""

from __future__ import annotations

from aiobungie import typedefs

__all__ = ("Compact", "Send", "Deserialize", "RESTful")

import logging
import pathlib
import sys
import typing

from aiobungie import builders

if typing.TYPE_CHECKING:
    import collections.abc as collections
    import os

    from aiobungie import api, client
    from aiobungie.internal import enums


# this isn't used anywhere right now. but we're keeping it for the future.
@typing.runtime_checkable
class Send(typing.Protocol):
    """Types that can send HTTP requests from an external resource.

    These requests are performed by a reference of your `aiobungie.Client` instance.

    Example
    -------
    ```py
    membership = aiobungie.crates.DestinyMembership(…)
    # Access the base client that references this membership.
    external_request = await membership.app.request.fetch_user(…)
    ```
    """

    __slots__ = ()

    @property
    def request(self) -> client.Client:
        """A read-only `aiobungie.Client` instance used for external requests."""
        raise NotImplementedError


@typing.runtime_checkable
class Deserialize(typing.Protocol):
    """Types which can deserialize REST payloads responses into a `aiobungie.crates`.

    They're responsible for turning a REST payload (`collections/bytes/etc`) into a `aiobungie.crates` basic implementation.
    """

    __slots__ = ()

    @property
    def framework(self) -> api.Framework:
        """An implementation of a `aiobungie.api.Framework` object used by your client."""
        raise NotImplementedError


@typing.runtime_checkable
class RESTful(typing.Protocol):
    """Types that interact with the API directly, they're able to perform REST calls.

    This trait is automatically implemented for `aiobungie.RESTClient`, for `aiobungie.Client` also which can be accessed via `aiobungie.Client.rest`.
    """

    __slots__ = ()

    @property
    def client_id(self) -> int | None:
        """Return the client id of this REST client if provided, Otherwise None."""
        raise NotImplementedError

    @property
    def metadata(self) -> collections.MutableMapping[typing.Any, typing.Any]:
        """A mutable mapping storage for the user's needs.

        This mapping is useful for storing any kind of data that the user may need
        to access later from a different process.

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

    @property
    def settings(self) -> builders.Settings:
        """Internal client settings used within the HTTP client session."""
        raise NotImplementedError

    @typing.final
    def with_debug(
        self,
        level: typing.Literal["TRACE"] | bool | int = True,
        file: str | os.PathLike[str] | None = None,
    ) -> None:
        """Enable debugging for this client with a level. Defaults to `True`.

        Parameters
        ----------
        level: `NotRequired[int | bool | typing.Literal["TRACE"] | None]`
            The level of the logger. This field is not required.
        file: `pathlib.Path | str | None`
            An optional file to write the logs into.

        Logging Levels
        --------------
        * `False`: This will disable logging.
        * `True`: This will set the level to `DEBUG` and enable logging minimal information.
        * `"TRACE" | aiobungie.TRACE`: This will log the response headers along with the minimal information.
        """
        logging.logThreads = False
        logging.logMultiprocessing = False
        logging.logProcesses = False
        logging.captureWarnings(True)

        format = "%(levelname)s %(asctime)23.23s %(name)s: %(message)s"

        # early exit, don't bother doing anything.
        if not level:
            return

        # something has already initialized this.
        if len(logging.root.handlers) != 0:
            return

        if isinstance(file, str):
            path = pathlib.Path(file)
            if path.expanduser().exists():
                file = path

        file_handler = (
            logging.FileHandler(file)
            if file is not None
            else logging.StreamHandler(sys.stdout),
        )
        if level == "TRACE" or level == logging.DEBUG - 5:
            logging.basicConfig(
                level=logging.getLevelName(logging.DEBUG - 5),
                format=format,
                handlers=file_handler,
            )

        elif level is True:
            logging.basicConfig(
                level=logging.DEBUG, format=format, handlers=file_handler
            )
        else:
            logging.basicConfig(level=level, format=format, handlers=file_handler)

    @typing.overload
    def build_oauth2_url(self, client_id: int) -> builders.OAuthURL: ...

    @typing.overload
    def build_oauth2_url(self) -> builders.OAuthURL | None: ...

    def build_oauth2_url(
        self, client_id: int | None = None
    ) -> builders.OAuthURL | None:
        """Construct a new `OAuthURL` url object.

        You can get the complete string representation of the url by calling `.compile()` on it.

        Parameters
        ----------
        client_id : `int | None`
            An optional client id to provide, If left `None` it will roll back to the id passed
            to the `RESTClient`, If both is `None` this method will return `None`.

        Returns
        -------
        `aiobungie.builders.OAuthURL | None`
            * If `client_id` was provided as a parameter, It guarantees to return a complete `OAuthURL` object
            * If `client_id` is set to `aiobungie.RESTClient` will be.
            * If both are `None` this method will return `None.
        """
        raise NotImplementedError

    @typing.final
    def build_fireteam_finder(
        self,
        membership_id: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> builders.FireteamBuilder:
        """Construct a new fireteam builder.

        This method exposes all of `FireteamFinder` routes ready.

        Example
        -------
        ```py
        client = RESTClient('token')
        finder = client.build_fireteam_finder(member_id, character_id, membership_type=3)

        async with client:
            await finder.host_lobby(...)
        ```

        Parameters
        ----------
        membership_id: `int`
            The main Destiny membership ID that will be used for this fireteam builder.
        character_id: `int`
            The main Destiny character ID that will be used for this fireteam builder.
        membership_type: `aiobungie.MembershipType` | `int`
            The main Destiny membership type that will be used for this fireteam builder.
        """
        return builders.FireteamBuilder(
            rest=self,
            membership_id=membership_id,
            character_id=character_id,
            membership_type=membership_type,
        )

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
        method: typing.Literal["GET", "DELETE", "POST", "PUT", "PATCH"],
        path: str,
        *,
        auth: str | None = None,
        json: collections.MutableMapping[str, typing.Any] | None = None,
        params: collections.Mapping[str, typing.Any] | None = None,
    ) -> typedefs.JSONIsh:
        """Perform an HTTP request given a valid Bungie endpoint.

        This method allows you to freely perform HTTP requests to Bungie's API.
        It provides authentication support, JSON bodies, URL parameters and out of
        the box exception handling.

        This method is useful for testing routes by yourself. or even calling
        routes that aiobungie doesn't support yet.

        Parameters
        ----------
        method : `str`
            The request method, This may be `GET`, `POST`, `PUT`, etc.
        path: `str`
            The Bungie endpoint or path.
            A path must look something like this `Destiny2/3/Profile/46111239123/...`

        Other Parameters
        ----------------
        auth : `str | None`
            An optional bearer token for methods that requires OAuth2 Authorization header.
        json : `MutableMapping[str, typing.Any] | None`
            An optional JSON mapping to include in the request.
        params : `MutableMapping[str, typing.Any] | None`
            An optional URL query parameters mapping to include in the request.

        Returns
        -------
        `aiobungie.typedefs.JSONIsh`
            The response payload.
        """
        raise NotImplementedError


@typing.runtime_checkable
class Compact(Deserialize, typing.Protocol):
    """A structural super-type that can perform all actions that other traits provide.

    This trait includes all aiobungie traits. is also automatically implemented for `aiobungie.Client`
    """

    __slots__ = ()

    @property
    def rest(self) -> api.RESTClient:
        """Returns the REST client for the this client."""
        raise NotImplementedError

    @property
    def metadata(self) -> collections.MutableMapping[typing.Any, typing.Any]:
        """A mutable mapping storage for the user's needs."""
        raise NotImplementedError

    @property
    def settings(self) -> builders.Settings:
        """Internal client settings used within the HTTP client session."""
        raise NotImplementedError
