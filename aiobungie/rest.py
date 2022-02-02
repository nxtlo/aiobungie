# MIT License
#
# Copyright (c) 2020 = Present nxtlo
#
# Permission is hereby granted, free of charge, to typing.Any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF typing.Any KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR typing.Any CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Implementation of a RESTful client for Bungie's REST API.

This client only makes HTTP requests to the API and returns pure JSON objects.
"""

from __future__ import annotations

__all__: tuple[str, ...] = (
    "RESTClient",
    "RequestMethod",
    "OAuth2Response",
    "PlugSocketBuilder",
)

import asyncio
import contextlib
import datetime
import http
import logging
import os
import pathlib
import platform
import random
import sqlite3
import sys
import time
import typing
import uuid
import zipfile

import aiohttp
import attrs

from aiobungie import _info as info  # type: ignore[private-usage]
from aiobungie import error
from aiobungie import interfaces
from aiobungie import typedefs
from aiobungie import undefined
from aiobungie import url
from aiobungie.crate import fireteams
from aiobungie.internal import _backoff as backoff
from aiobungie.internal import enums
from aiobungie.internal import helpers
from aiobungie.internal import time as aiobungie_time

if typing.TYPE_CHECKING:
    import collections.abc as collections
    import types

    ResponseSigT = typing.TypeVar(
        "ResponseSigT",
        covariant=True,
        bound=typing.Union[
            typedefs.JSONArray,
            typedefs.JSONObject,
            int,
            None,
        ],
    )
    """The signature of the response."""

    ResponseSig = collections.Coroutine[None, None, ResponseSigT]
    """A type hint for a general coro method that returns a type
    that's mostly going to be on of `aiobungie.typedefs.JSONObject`
    or `aiobungie.typedefs.JSONArray`
    """

_LOG: typing.Final[logging.Logger] = logging.getLogger("aiobungie.rest")
_APP_JSON: typing.Final[str] = "application/json"
_RETRY_5XX: typing.Final[set[int]] = {500, 502, 503, 504}
_AUTH_HEADER: typing.Final[str] = sys.intern("Authorization")
_USER_AGENT_HEADERS: typing.Final[str] = sys.intern("User-Agent")
_USER_AGENT: typing.Final[
    str
] = f"AiobungieClient ({info.__about__}), ({info.__author__}), "
f"({info.__version__}), ({info.__url__}), "
f"{platform.python_implementation()}/{platform.python_version()} {platform.system()} "
f"{platform.architecture()[0]}, Aiohttp/{aiohttp.HttpVersion11}"  # type: ignore[UnknownMemberType]


class _Arc:
    __slots__ = ("_lock",)

    def __init__(self) -> None:
        self._lock = asyncio.Lock()

    async def __aenter__(self) -> None:
        await self.acquire()

    async def __aexit__(
        self,
        exception_type: typing.Optional[type[BaseException]],
        exception: typing.Optional[BaseException],
        exception_traceback: typing.Optional[types.TracebackType],
    ) -> None:
        self._lock.release()

    async def acquire(self) -> None:
        await self._lock.acquire()


@attrs.define(kw_only=True, repr=False)
class _Session:
    client_session: aiohttp.ClientSession

    @classmethod
    def acquire_session(
        cls,
        *,
        owner: bool = False,
        raise_status: bool = False,
        total_timeout: typing.Optional[float] = 30,
        connect: typing.Optional[float] = None,
        socket_read: typing.Optional[float] = None,
        socket_connect: typing.Optional[float] = None,
        **kwargs: typing.Any,
    ) -> _Session:
        session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False, **kwargs),
            headers={_USER_AGENT_HEADERS: _USER_AGENT},
            connector_owner=owner,
            raise_for_status=raise_status,
            timeout=aiohttp.ClientTimeout(
                total=total_timeout,
                sock_read=socket_read,
                sock_connect=socket_connect,
                connect=connect,
            ),
        )
        return _Session(client_session=session)

    async def __aenter__(self) -> _Session:
        return self

    async def __aexit__(
        self,
        exception_type: typing.Optional[type[BaseException]],
        exception: typing.Optional[BaseException],
        exception_traceback: typing.Optional[types.TracebackType],
    ) -> None:
        await self.close()

    async def close(self) -> None:
        # Close the TCP connector.
        if self.client_session.connector:
            await self.client_session.connector.close()
        await asyncio.sleep(0.025)


class RequestMethod(str, enums.Enum):
    """HTTP request methods enum."""

    GET = "GET"
    """GET methods."""
    POST = "POST"
    """POST methods."""
    PUT = "PUT"
    """PUT methods."""
    PATCH = "PATCH"
    """PATCH methods."""
    DELETE = "DELETE"
    """DELETE methods"""


@attrs.mutable(kw_only=True, repr=False)
class OAuth2Response:
    """Represents a proxy object for returned information from an OAuth2 successful response."""

    access_token: str
    """The returned OAuth2 `access_token` field."""

    refresh_token: str
    """The returned OAuth2 `refresh_token` field."""

    expires_in: int
    """The returned OAuth2 `expires_in` field."""

    token_type: str
    """The returned OAuth2 `token_type` field. This is usually just `Bearer`"""

    refresh_expires_in: int
    """The returned OAuth2 `refresh_expires_in` field."""

    membership_id: int
    """The returned BungieNet membership id for the authorized user."""

    @classmethod
    def build_response(cls, payload: typedefs.JSONObject, /) -> OAuth2Response:
        """Deserialize and builds the JSON object into this object."""
        return OAuth2Response(
            access_token=payload["access_token"],
            refresh_token=payload["refresh_token"],
            expires_in=int(payload["expires_in"]),
            token_type=payload["token_type"],
            refresh_expires_in=payload["refresh_expires_in"],
            membership_id=int(payload["membership_id"]),
        )


class PlugSocketBuilder:
    """A helper for building insert socket plugs.

    Example
    -------
    ```py
    import aiobungie

    rest = aiobungie.RESTClient(...)
    plug = (
        aiobungie.PlugSocketBuilder()
        .set_socket_array(0)
        .set_socket_index(0)
        .set_plug_item(3023847)
        .collect()
    )
    await rest.insert_socket_plug_free(..., plug=plug)
    ```
    """

    __slots__ = ("_map",)

    def __init__(self, map: typing.Optional[dict[str, int]] = None, /) -> None:
        self._map = map or {}

    def set_socket_array(self, socket_type: typing.Literal[0, 1]) -> PlugSocketBuilder:
        """Set the array socket type.

        Parameters
        ----------
        socket_type : `typing.Literal[0, 1]`
            Either 0, or 1. If set to 0 it will be the default,
            Otherwise if 1 it will be Intrinsic.

        Returns
        -------
        `Self`
            The class itself to allow chained methods.
        """
        self._map["socketArrayType"] = socket_type
        return self

    def set_socket_index(self, index: int) -> PlugSocketBuilder:
        """Set the socket index into the array.

        Parameters
        ----------
        index : `int`
            The socket index.

        Returns
        -------
        `Self`
            The class itself to allow chained methods.
        """
        self._map["socketIndex"] = index
        return self

    def set_plug_item(self, item_hash: int) -> PlugSocketBuilder:
        """Set the socket index into the array.

        Parameters
        ----------
        item_hash : `int`
            The hash of the item to plug.

        Returns
        -------
        `Self`
            The class itself to allow chained methods.
        """
        self._map["plugItemHash"] = item_hash
        return self

    def collect(self) -> dict[str, int]:
        """Collect the set values and return its map to be passed to the request.

        Returns
        -------
        `dict[str, int]`
            The built map.
        """
        return self._map


class RESTClient(interfaces.RESTInterface):
    """A RESTful client implementation for Bungie's API.

    This client is designed to only make HTTP requests and return JSON objects
    to provide RESTful functionality.

    This client is also used within `aiobungie.Client` which deserialize those returned JSON objects
    using the factory into Pythonic data classes objects which provide Python functionality.

    Example
    -------
    ```py
    import aiobungie

    async def main():
        async with aiobungie.RESTClient("TOKEN") as rest_client:
            req = await rest_client.fetch_clan_members(4389205)
            clan_members = req['results']
            for member in clan_members:
                for k, v in member['destinyUserInfo'].items():
                    print(k, v)
    ```

    Parameters
    ----------
    token : `str`
        A valid application token from Bungie's developer portal.

    Other Parameters
    ----------------
    max_retries : `int`
        The max retries number to retry if the request hit a `5xx` status code.
    client_secret : `typing.Optional[str]`
        An optional application client secret,
        This is only needed if you're fetching OAuth2 tokens with this client.
    client_id : `typing.Optional[int]`
        An optional application client id,
        This is only needed if you're fetching OAuth2 tokens with this client.
    """

    __slots__ = (
        "_token",
        "_session",
        "_max_retries",
        "_client_secret",
        "_client_id",
        "_metadata",
        "_lock",
    )

    def __init__(
        self,
        token: str,
        /,
        client_secret: typing.Optional[str] = None,
        client_id: typing.Optional[int] = None,
        *,
        max_retries: int = 4,
    ) -> None:
        self._session: typing.Optional[_Session] = None
        self._lock = _Arc()
        self._client_secret = client_secret
        self._client_id = client_id
        self._token: str = token
        self._max_retries = max_retries
        self._metadata: collections.MutableMapping[typing.Any, typing.Any] = {}

    def _acquire_session(self) -> _Session:
        asyncio.get_running_loop()
        if self._session is None:
            self._session = _Session.acquire_session(
                owner=False,
                raise_status=False,
                connect=None,
                socket_read=None,
                socket_connect=None,
            )
        return self._session

    @typing.final
    async def close(self) -> None:
        if self._session is not None:
            _LOG.info("Closing REST client.")
            await self._session.close()

    @property
    def client_id(self) -> typing.Optional[int]:
        return self._client_id

    @property
    def metadata(self) -> collections.MutableMapping[typing.Any, typing.Any]:
        return self._metadata

    @typing.final
    async def _request(
        self,
        method: typing.Union[RequestMethod, str],
        route: str,
        base: bool = False,
        oauth2: bool = False,
        auth: typing.Optional[str] = None,
        unwrapping: typing.Literal["json", "read"] = "json",
        json: typing.Optional[dict[str, typing.Any]] = None,
        **kwargs: typing.Any,
    ) -> typing.Any:

        retries: int = 0
        if self._token is not None:
            headers: dict[str, str]
            kwargs["headers"] = headers = {}
            headers["X-API-KEY"] = self._token
        else:
            raise ValueError("No API KEY was passed.")

        if auth is not None:
            headers[_AUTH_HEADER] = f"Bearer {auth}"

        # Handling endpoints
        endpoint = url.BASE

        if not base:
            endpoint = endpoint + url.REST_EP

        if oauth2:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            endpoint = endpoint + url.TOKEN_EP

        while True:
            try:
                async with (stack := contextlib.AsyncExitStack()):
                    await stack.enter_async_context(self._lock)

                    # We make the request here.
                    taken_time = time.monotonic()
                    response = await stack.enter_async_context(
                        self._acquire_session().client_session.request(
                            method=method,
                            url=f"{endpoint}/{route}",
                            json=json,
                            **kwargs,
                        )
                    )
                    response_time = (time.monotonic() - taken_time) * 1_000

                    await self._handle_ratelimit(response, method, str(route))

                    if response.status == http.HTTPStatus.NO_CONTENT:
                        return None

                    if unwrapping != "read":
                        data: typedefs.JSONObject = await response.json()

                    if 300 > response.status >= 200:
                        if unwrapping == "read":
                            # We want to read the bytes for the manifest response.
                            return await response.read()

                        if response.content_type == _APP_JSON:
                            if _LOG.isEnabledFor(logging.DEBUG):
                                _LOG.debug(
                                    "Method %s Route %s Status %i Time %.4fms",
                                    method,
                                    f"{url.REST_EP}/{route}",
                                    response.status,
                                    response_time,
                                )

                            # Return the response.
                            # oauth2 responses are not packed inside a Response object.
                            if oauth2:
                                return data

                            return data["Response"]
                    if (
                        response.status in _RETRY_5XX
                        and retries < self._max_retries  # noqa: W503
                    ):
                        backoff_ = backoff.ExponentialBackOff(maximum=6)
                        sleep_time = next(backoff_)
                        _LOG.warning(
                            "Received: %i, Message: %s, Sleeping for %.2f seconds, Remaining retries: %i",
                            response.status,
                            data["Message"],
                            sleep_time,
                            self._max_retries - retries,
                        )

                        retries += 1
                        await asyncio.sleep(sleep_time)
                        continue

                    raise await error.raise_error(response, data.get("ErrorStatus", ""))
            # eol
            except error.HTTPError:
                raise

    if not typing.TYPE_CHECKING:

        def __enter__(self) -> typing.NoReturn:
            cls = type(self)
            raise TypeError(
                f"{cls.__qualname__} is async only, use 'async with' instead."
            )

        def __exit__(
            self,
            exception_type: typing.Optional[type[BaseException]],
            exception: typing.Optional[BaseException],
            exception_traceback: typing.Optional[types.TracebackType],
        ) -> None:
            ...

    async def __aenter__(self) -> RESTClient:
        return self

    async def __aexit__(
        self,
        exception_type: typing.Optional[type[BaseException]],
        exception: typing.Optional[BaseException],
        exception_traceback: typing.Optional[types.TracebackType],
    ) -> None:
        if self._session:
            await self._session.close()

    # We don't want this to be super complicated.
    @typing.final
    @staticmethod
    async def _handle_ratelimit(
        response: aiohttp.ClientResponse,
        method: str,
        route: str,
    ) -> None:

        if response.status != http.HTTPStatus.TOO_MANY_REQUESTS:
            return

        if response.content_type != _APP_JSON:
            raise error.HTTPError(
                f"Being ratelmited on non JSON request, {response.content_type}.",
                http.HTTPStatus.TOO_MANY_REQUESTS,
            )

        json = await response.json()
        retry_after: float = json["ThrottleSeconds"]
        if retry_after >= 0:
            # Can't really do anything about this...
            sleep_time = float((retry_after + random.randint(0, 3)))

            _LOG.warning(
                "Ratelimited with method %s route %s. Sleeping for %f:,",
                method,
                route,
                sleep_time,
            )
            await asyncio.sleep(sleep_time)

        raise error.RateLimitedError(
            body=json,
            url=str(response.real_url),
            retry_after=retry_after,
        )

    @staticmethod
    @typing.no_type_check
    def _collect_components(
        *components: enums.ComponentType,
    ) -> typing.Union[str, type[str]]:
        try:
            if len(components) == 0:
                raise ValueError("No profile components passed.", components)

            # Need to get the int overload of the components to separate them.
            elif len(components) > 1:
                these = helpers.collect(*[int(k) for k in components])
            else:
                these = helpers.collect(int(*components))
            # In case it's a tuple, i.e., ALL_X
        except TypeError:
            these = helpers.collect(*list(str(c.value) for c in components))
        return these

    @typing.final
    def static_request(
        self,
        method: typing.Union[RequestMethod, str],
        path: str,
        auth: typing.Optional[str] = None,
        json: typing.Optional[dict[str, typing.Any]] = None,
        **kwargs: typing.Any,
    ) -> ResponseSig[typing.Any]:
        return self._request(method, path, auth=auth, json=json, **kwargs)

    @typing.final
    def build_oauth2_url(
        self, client_id: typing.Optional[int] = None
    ) -> typing.Optional[str]:
        client_id = client_id or self._client_id
        if client_id is None:
            return None

        return url.OAUTH2_EP_BUILDER.format(
            oauth_endpoint=url.OAUTH_EP,
            client_id=client_id,
            uuid=str(uuid.uuid4()),
        )

    async def fetch_oauth2_tokens(self, code: str, /) -> OAuth2Response:

        if not isinstance(self._client_id, int):
            raise TypeError(
                f"Expected (str) for client id but got {type(self._client_id).__qualname__}"  # type: ignore
            )

        if not isinstance(self._client_secret, str):
            raise TypeError(
                f"Expected (str) for client secret but got {type(self._client_secret).__qualname__}"  # type: ignore
            )

        headers = {
            "client_secret": self._client_secret,
        }

        data = (
            f"grant_type=authorization_code&code={code}"
            f"&client_id={self._client_id}&client_secret={self._client_secret}"
        )

        response = await self._request(
            RequestMethod.POST, "", headers=headers, data=data, oauth2=True
        )
        return OAuth2Response.build_response(response)

    async def refresh_access_token(self, refresh_token: str, /) -> OAuth2Response:
        if not isinstance(self._client_id, int):
            raise TypeError(
                f"Expected (str) for client id but got {type(self._client_id).__qualname__}"  # type: ignore
            )

        if not isinstance(self._client_secret, str):
            raise TypeError(
                f"Expected (str) for client secret but got {type(self._client_secret).__qualname__}"  # type: ignore
            )

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = await self._request(RequestMethod.POST, "", data=data, oauth2=True)
        return OAuth2Response.build_response(response)

    def fetch_bungie_user(self, id: int) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, f"User/GetBungieNetUserById/{id}/")

    def fetch_user_themes(self) -> ResponseSig[typedefs.JSONArray]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, "User/GetAvailableThemes/")

    def fetch_membership_from_id(
        self,
        id: int,
        type: typedefs.IntAnd[enums.MembershipType] = enums.MembershipType.NONE,
        /,
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET, f"User/GetMembershipsById/{id}/{int(type)}"
        )

    def fetch_player(
        self,
        name: str,
        code: int,
        type: typedefs.IntAnd[enums.MembershipType] = enums.MembershipType.ALL,
        /,
    ) -> ResponseSig[typedefs.JSONArray]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.POST,
            f"Destiny2/SearchDestinyPlayerByBungieName/{int(type)}",
            json={"displayName": name, "displayNameCode": code},
        )

    def search_users(self, name: str, /) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.POST,
            "User/Search/GlobalName/0",
            json={"displayNamePrefix": name},
        )

    def fetch_clan_from_id(
        self, id: int, /, access_token: typing.Optional[str] = None
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, f"GroupV2/{id}", auth=access_token)

    def fetch_clan(
        self,
        name: str,
        /,
        access_token: typing.Optional[str] = None,
        *,
        type: typedefs.IntAnd[enums.GroupType] = enums.GroupType.CLAN,
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET, f"GroupV2/Name/{name}/{int(type)}", auth=access_token
        )

    def fetch_clan_admins(self, clan_id: int, /) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, f"GroupV2/{clan_id}/AdminsAndFounder/")

    def fetch_clan_conversations(
        self, clan_id: int, /
    ) -> ResponseSig[typedefs.JSONArray]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET, f"GroupV2/{clan_id}/OptionalConversations/"
        )

    def fetch_application(self, appid: int, /) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, f"App/Application/{appid}")

    def fetch_character(
        self,
        member_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
        character_id: int,
        *components: enums.ComponentType,
        **options: str,
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        collector = self._collect_components(*components)
        return self._request(
            RequestMethod.GET,
            f"Destiny2/{int(membership_type)}/Profile/{member_id}/"
            f"Character/{character_id}/?components={collector}",
            auth=options.get("auth"),
        )

    def fetch_activities(
        self,
        member_id: int,
        character_id: int,
        mode: typedefs.IntAnd[enums.GameMode],
        membership_type: typedefs.IntAnd[
            enums.MembershipType
        ] = enums.MembershipType.ALL,
        *,
        page: int = 0,
        limit: int = 1,
    ) -> ResponseSig[typing.Any]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"Destiny2/{int(membership_type)}/Account/"
            f"{member_id}/Character/{character_id}/Stats/Activities"
            f"/?mode={int(mode)}&count={limit}&page={page}",
        )

    def fetch_vendor_sales(self) -> ResponseSig[typing.Any]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"Destiny2/Vendors/?components={int(enums.ComponentType.VENDOR_SALES)}",
        )

    def fetch_profile(
        self,
        memberid: int,
        type: typedefs.IntAnd[enums.MembershipType],
        *components: enums.ComponentType,
        **options: str,
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        collector = self._collect_components(*components)
        return self._request(
            RequestMethod.GET,
            f"Destiny2/{int(type)}/Profile/{int(memberid)}/?components={collector}",
            auth=options.get("auth", None),
        )

    def fetch_entity(self, type: str, hash: int) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET, route=f"Destiny2/Manifest/{type}/{hash}"
        )

    def fetch_inventory_item(self, hash: int, /) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self.fetch_entity("DestinyInventoryItemDefinition", hash)

    def fetch_objective_entity(self, hash: int, /) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self.fetch_entity("DestinyObjectiveDefinition", hash)

    def fetch_groups_for_member(
        self,
        member_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
        /,
        *,
        filter: int = 0,
        group_type: typedefs.IntAnd[enums.GroupType] = enums.GroupType.CLAN,
    ) -> ResponseSig[typedefs.JSONObject]:
        return self._request(
            RequestMethod.GET,
            f"GroupV2/User/{int(member_type)}/{member_id}/{filter}/{int(group_type)}/",
        )

    def fetch_potential_groups_for_member(
        self,
        member_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
        /,
        *,
        filter: int = 0,
        group_type: typedefs.IntAnd[enums.GroupType] = enums.GroupType.CLAN,
    ) -> ResponseSig[typedefs.JSONObject]:
        return self._request(
            RequestMethod.GET,
            f"GroupV2/User/Potential/{int(member_type)}/{member_id}/{filter}/{int(group_type)}/",
        )

    def fetch_clan_members(
        self,
        clan_id: int,
        /,
        *,
        name: typing.Optional[str] = None,
        type: typedefs.IntAnd[enums.MembershipType] = enums.MembershipType.NONE,
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"/GroupV2/{clan_id}/Members/?memberType={int(type)}&nameSearch={name if name else ''}&currentpage=1",
        )

    def fetch_hardlinked_credentials(
        self,
        credential: int,
        type: typedefs.IntAnd[enums.CredentialType] = enums.CredentialType.STEAMID,
        /,
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"User/GetMembershipFromHardLinkedCredential/{int(type)}/{credential}/",
        )

    def fetch_user_credentials(
        self, access_token: str, membership_id: int, /
    ) -> ResponseSig[typedefs.JSONArray]:
        return self._request(
            RequestMethod.GET,
            f"User/GetCredentialTypesForTargetAccount/{membership_id}",
            auth=access_token,
        )

    def insert_socket_plug(
        self,
        action_token: str,
        /,
        instance_id: int,
        plug: typing.Union[PlugSocketBuilder, dict[str, int]],
        character_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[typedefs.JSONObject]:

        if isinstance(plug, PlugSocketBuilder):
            plug = plug.collect()

        body = {
            "actionToken": action_token,
            "itemInstanceId": instance_id,
            "plug": plug,
            "characterId": character_id,
            "membershipType": int(membership_type),
        }
        return self._request(
            RequestMethod.POST, "Destiny2/Actions/Items/InsertSocketPlug", json=body
        )

    def insert_socket_plug_free(
        self,
        access_token: str,
        /,
        instance_id: int,
        plug: typing.Union[PlugSocketBuilder, dict[str, int]],
        character_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[typedefs.JSONObject]:

        if isinstance(plug, PlugSocketBuilder):
            plug = plug.collect()

        body = {
            "itemInstanceId": instance_id,
            "plug": plug,
            "characterId": character_id,
            "membershipType": int(membership_type),
        }
        return self._request(
            RequestMethod.POST,
            "Destiny2/Actions/Items/InsertSocketPlugFree",
            json=body,
            auth=access_token,
        )

    def set_item_lock_state(
        self,
        access_token: str,
        state: bool,
        /,
        item_id: int,
        character_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[int]:
        body = {
            "state": state,
            "itemId": item_id,
            "characterId": character_id,
            "membership_type": int(membership_type),
        }
        return self._request(
            RequestMethod.POST,
            "Destiny2/Actions/Items/SetLockState",
            json=body,
            auth=access_token,
        )

    def set_quest_track_state(
        self,
        access_token: str,
        state: bool,
        /,
        item_id: int,
        character_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[int]:
        body = {
            "state": state,
            "itemId": item_id,
            "characterId": character_id,
            "membership_type": int(membership_type),
        }
        return self._request(
            RequestMethod.POST,
            "Destiny2/Actions/Items/SetTrackedState",
            json=body,
            auth=access_token,
        )

    async def fetch_manifest_path(self, language: str = "en", /) -> str:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        if language not in (
            langs := {
                "en",
                "fr",
                "es",
                "es-mx",
                "de",
                "it",
                "ja",
                "pt-br",
                "ru",
                "pl",
                "ko",
                "zh-cht",
                "zh-chs",
            }
        ):
            raise ValueError("Language must be in ", langs)
        request = await self._request(RequestMethod.GET, "Destiny2/Manifest")
        return str(request["mobileWorldContentPaths"][language])

    async def read_manifest_bytes(self, language: str = "en", /) -> bytes:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        content = await self.fetch_manifest_path(language)
        resp = await self._request(
            RequestMethod.GET, content, unwrapping="read", base=True
        )
        return bytes(resp)

    async def download_manifest(
        self, language: str = "en", name: str = "manifest.sqlite3"
    ) -> None:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        if os.path.exists("manifest.sqlite3"):
            raise FileExistsError("Manifest file already exists.")

        _LOG.debug("Downloading manifest...")
        try:
            # TODO: Use tempfile instead?
            with open("tmp-file.zip", "wb") as tmp:
                tmp.write(await self.read_manifest_bytes(language))

            with zipfile.ZipFile(tmp.name) as zipped:
                file = zipped.namelist()
                zipped.extractall(".")
                os.rename(file[0], name)
                _LOG.debug("Finished downloading manifest.")
        finally:
            pathlib.Path(tmp.name).unlink(missing_ok=True)

    @staticmethod
    def connect_manifest(
        path: typing.Optional[pathlib.Path] = None,
        connection: type[sqlite3.Connection] = sqlite3.Connection,
    ) -> sqlite3.Connection:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        path = path or pathlib.Path("./manifest.sqlite3")
        if not path.exists():
            raise FileNotFoundError(f"Manifest in path {path.name} doesn't exists.")
        return connection(path.name)

    def fetch_linked_profiles(
        self,
        member_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
        /,
        *,
        all: bool = False,
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"Destiny2/{int(member_type)}/Profile/{member_id}/LinkedProfiles/?getAllMemberships={all}",
        )

    def fetch_clan_banners(self) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, "Destiny2/Clan/ClanBannerDictionary/")

    def fetch_public_milestones(self) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, "Destiny2/Milestones/")

    def fetch_public_milestone_content(
        self, milestone_hash: int, /
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET, f"Destiny2/Milestones/{milestone_hash}/Content/"
        )

    def fetch_current_user_memberships(
        self, access_token: str, /
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            "User/GetMembershipsForCurrentUser/",
            auth=access_token,
        )

    def equip_item(
        self,
        access_token: str,
        /,
        item_id: int,
        character_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        payload = {
            "itemId": item_id,
            "characterId": character_id,
            "membershipType": int(membership_type),
        }

        return self._request(
            RequestMethod.POST,
            "Destiny2/Actions/Items/EquipItem/",
            json=payload,
            auth=access_token,
        )

    def equip_items(
        self,
        access_token: str,
        /,
        item_ids: list[int],
        character_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        payload = {
            "itemIds": item_ids,
            "characterId": character_id,
            "membershipType": int(membership_type),
        }
        return self._request(
            RequestMethod.POST,
            "Destiny2/Actions/Items/EquipItems/",
            json=payload,
            auth=access_token,
        )

    def ban_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
        *,
        length: int = 0,
        comment: undefined.UndefinedOr[str] = undefined.Undefined,
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        payload = {"comment": str(comment), "length": length}
        return self._request(
            RequestMethod.POST,
            f"GroupV2/{group_id}/Members/{int(membership_type)}/{membership_id}/Ban/",
            json=payload,
            auth=access_token,
        )

    def unban_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.POST,
            f"GroupV2/{group_id}/Members/{int(membership_type)}/{membership_id}/Unban/",
            auth=access_token,
        )

    def kick_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.POST,
            f"GroupV2/{group_id}/Members/{int(membership_type)}/{membership_id}/Kick/",
            auth=access_token,
        )

    def edit_clan(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        name: typedefs.NoneOr[str] = None,
        about: typedefs.NoneOr[str] = None,
        motto: typedefs.NoneOr[str] = None,
        theme: typedefs.NoneOr[str] = None,
        tags: typedefs.NoneOr[collections.Sequence[str]] = None,
        is_public: typedefs.NoneOr[bool] = None,
        locale: typedefs.NoneOr[str] = None,
        avatar_image_index: typedefs.NoneOr[int] = None,
        membership_option: typedefs.NoneOr[
            typedefs.IntAnd[enums.MembershipOption]
        ] = None,
        allow_chat: typedefs.NoneOr[bool] = None,
        chat_security: typedefs.NoneOr[typing.Literal[0, 1]] = None,
        call_sign: typedefs.NoneOr[str] = None,
        homepage: typedefs.NoneOr[typing.Literal[0, 1, 2]] = None,
        enable_invite_messaging_for_admins: typedefs.NoneOr[bool] = None,
        default_publicity: typedefs.NoneOr[typing.Literal[0, 1, 2]] = None,
        is_public_topic_admin: typedefs.NoneOr[bool] = None,
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        payload = {
            "name": name,
            "about": about,
            "motto": motto,
            "theme": theme,
            "tags": tags,
            "isPublic": is_public,
            "avatarImageIndex": avatar_image_index,
            "isPublicTopicAdminOnly": is_public_topic_admin,
            "allowChat": allow_chat,
            "chatSecurity": chat_security,
            "callsign": call_sign,
            "homepage": homepage,
            "enableInvitationMessagingForAdmins": enable_invite_messaging_for_admins,
            "defaultPublicity": default_publicity,
            "locale": locale,
        }
        if membership_option is not None:
            payload["membershipOption"] = int(membership_option)

        return self._request(
            RequestMethod.POST,
            f"GroupV2/{group_id}/Edit",
            json=payload,
            auth=access_token,
        )

    def edit_clan_options(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        invite_permissions_override: typedefs.NoneOr[bool] = None,
        update_culture_permissionOverride: typedefs.NoneOr[bool] = None,
        host_guided_game_permission_override: typedefs.NoneOr[
            typing.Literal[0, 1, 2]
        ] = None,
        update_banner_permission_override: typedefs.NoneOr[bool] = None,
        join_level: typedefs.NoneOr[typedefs.IntAnd[enums.ClanMemberType]] = None,
    ) -> ResponseSig[None]:

        payload = {
            "InvitePermissionOverride": invite_permissions_override,
            "UpdateCulturePermissionOverride": update_culture_permissionOverride,
            "HostGuidedGamePermissionOverride": host_guided_game_permission_override,
            "UpdateBannerPermissionOverride": update_banner_permission_override,
            "JoinLevel": int(join_level) if join_level else None,
        }

        return self._request(
            RequestMethod.POST,
            f"GroupV2/{group_id}/EditFounderOptions",
            json=payload,
            auth=access_token,
        )

    def fetch_friends(self, access_token: str, /) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            "Social/Friends/",
            auth=access_token,
        )

    def fetch_friend_requests(
        self, access_token: str, /
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            "Social/Friends/Requests",
            auth=access_token,
        )

    def accept_friend_request(
        self, access_token: str, /, member_id: int
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.POST,
            f"Social/Friends/Requests/Accept/{member_id}",
            auth=access_token,
        )

    def send_friend_request(
        self, access_token: str, /, member_id: int
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.POST,
            f"Social/Friends/Add/{member_id}",
            auth=access_token,
        )

    def decline_friend_request(
        self, access_token: str, /, member_id: int
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.POST,
            f"Social/Friends/Requests/Decline/{member_id}",
            auth=access_token,
        )

    def remove_friend(self, access_token: str, /, member_id: int) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.POST,
            f"Social/Friends/Remove/{member_id}",
            auth=access_token,
        )

    def remove_friend_request(
        self, access_token: str, /, member_id: int
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        return self._request(
            RequestMethod.POST,
            f"Social/Friends/Requests/Remove/{member_id}",
            auth=access_token,
        )

    def approve_all_pending_group_users(
        self,
        access_token: str,
        /,
        group_id: int,
        message: undefined.UndefinedOr[str] = undefined.Undefined,
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        return self._request(
            RequestMethod.POST,
            f"GroupV2/{group_id}/Members/ApproveAll",
            auth=access_token,
            json={"message": str(message)},
        )

    def deny_all_pending_group_users(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        message: undefined.UndefinedOr[str] = undefined.Undefined,
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        return self._request(
            RequestMethod.POST,
            f"GroupV2/{group_id}/Members/DenyAll",
            auth=access_token,
            json={"message": str(message)},
        )

    def add_optional_conversation(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        name: undefined.UndefinedOr[str] = undefined.Undefined,
        security: typing.Literal[0, 1] = 0,
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        payload = {"chatName": str(name), "chatSecurity": security}
        return self._request(
            RequestMethod.POST,
            f"GroupV2/{group_id}/OptionalConversations/Add",
            json=payload,
            auth=access_token,
        )

    def edit_optional_conversation(
        self,
        access_token: str,
        /,
        group_id: int,
        conversation_id: int,
        *,
        name: undefined.UndefinedOr[str] = undefined.Undefined,
        security: typing.Literal[0, 1] = 0,
        enable_chat: bool = False,
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        payload = {
            "chatEnabled": enable_chat,
            "chatName": str(name),
            "chatSecurity": security,
        }
        return self._request(
            RequestMethod.POST,
            f"GroupV2/{group_id}/OptionalConversations/Edit/{conversation_id}",
            json=payload,
            auth=access_token,
        )

    def transfer_item(
        self,
        access_token: str,
        /,
        item_id: int,
        item_hash: int,
        character_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
        *,
        stack_size: int = 1,
        vault: bool = False,
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        payload = {
            "characterId": character_id,
            "membershipType": int(member_type),
            "itemId": item_id,
            "itemReferenceHash": item_hash,
            "stackSize": stack_size,
            "transferToVault": vault,
        }
        return self._request(
            RequestMethod.POST,
            "Destiny2/Actions/Items/TransferItem",
            json=payload,
            auth=access_token,
        )

    def pull_item(
        self,
        access_token: str,
        /,
        item_id: int,
        item_hash: int,
        character_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
        *,
        stack_size: int = 1,
        vault: bool = False,
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        payload = {
            "characterId": character_id,
            "membershipType": int(member_type),
            "itemId": item_id,
            "itemReferenceHash": item_hash,
            "stackSize": stack_size,
            "transferToVault": vault,
        }
        return self._request(
            RequestMethod.POST,
            "Destiny2/Actions/Items/PullFromPostmaster",
            json=payload,
            auth=access_token,
        )

    def fetch_fireteams(
        self,
        activity_type: typedefs.IntAnd[fireteams.FireteamActivity],
        *,
        platform: typedefs.IntAnd[
            fireteams.FireteamPlatform
        ] = fireteams.FireteamPlatform.ANY,
        language: typing.Union[
            fireteams.FireteamLanguage, str
        ] = fireteams.FireteamLanguage.ALL,
        date_range: typedefs.IntAnd[
            fireteams.FireteamDate
        ] = fireteams.FireteamDate.ALL,
        page: int = 0,
        slots_filter: int = 0,
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"Fireteam/Search/Available/{int(platform)}/{int(activity_type)}/{int(date_range)}/{slots_filter}/{page}/?langFilter={str(language)}",  # noqa: E501 Line too long
        )

    def fetch_avaliable_clan_fireteams(
        self,
        access_token: str,
        group_id: int,
        activity_type: typedefs.IntAnd[fireteams.FireteamActivity],
        *,
        platform: typedefs.IntAnd[fireteams.FireteamPlatform],
        language: typing.Union[fireteams.FireteamLanguage, str],
        date_range: typedefs.IntAnd[
            fireteams.FireteamDate
        ] = fireteams.FireteamDate.ALL,
        page: int = 0,
        public_only: bool = False,
        slots_filter: int = 0,
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"Fireteam/Clan/{group_id}/Available/{int(platform)}/{int(activity_type)}/{int(date_range)}/{slots_filter}/{public_only}/{page}",  # noqa: E501
            json={"langFilter": str(language)},
            auth=access_token,
        )

    def fetch_clan_fireteam(
        self, access_token: str, fireteam_id: int, group_id: int
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"Fireteam/Clan/{group_id}/Summary/{fireteam_id}",
            auth=access_token,
        )

    def fetch_my_clan_fireteams(
        self,
        access_token: str,
        group_id: int,
        *,
        include_closed: bool = True,
        platform: typedefs.IntAnd[fireteams.FireteamPlatform],
        language: typing.Union[fireteams.FireteamLanguage, str],
        filtered: bool = True,
        page: int = 0,
    ) -> ResponseSig[typedefs.JSONObject]:
        payload = {"groupFilter": filtered, "langFilter": str(language)}
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"Fireteam/Clan/{group_id}/My/{int(platform)}/{include_closed}/{page}",
            json=payload,
            auth=access_token,
        )

    def fetch_private_clan_fireteams(
        self, access_token: str, group_id: int, /
    ) -> ResponseSig[int]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"Fireteam/Clan/{group_id}/ActiveCount",
            auth=access_token,
        )

    def fetch_post_activity(
        self, instance_id: int, /
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET, f"Destiny2/Stats/PostGameCarnageReport/{instance_id}"
        )

    def search_entities(
        self, name: str, entity_type: str, *, page: int = 0
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"Destiny2/Armory/Search/{entity_type}/{name}/",
            json={"page": page},
        )

    def fetch_unique_weapon_history(
        self,
        membership_id: int,
        character_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"Destiny2/{int(membership_type)}/Account/{membership_id}/Character/{character_id}/Stats/UniqueWeapons/",
        )

    def fetch_item(
        self,
        member_id: int,
        item_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
        *components: enums.ComponentType,
    ) -> ResponseSig[typedefs.JSONObject]:
        collector = self._collect_components(*components)
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"Destiny2/{int(membership_type)}/Profile/{member_id}/Item/{item_id}/?components={collector}",
        )

    def fetch_clan_weekly_rewards(
        self, clan_id: int, /
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET, f"Destiny2/Clan/{clan_id}/WeeklyRewardState/"
        )

    def fetch_available_locales(self) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, "GetAvailableLocales")

    def fetch_common_settings(self) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, "Settings")

    def fetch_user_systems_overrides(self) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, "UserSystemOverrides")

    def fetch_global_alerts(
        self, *, include_streaming: bool = False
    ) -> ResponseSig[typedefs.JSONArray]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET, f"GlobalAlerts/?includestreaming={include_streaming}"
        )

    def awainitialize_request(
        self,
        access_token: str,
        type: typing.Literal[0, 1],
        membership_type: typedefs.IntAnd[enums.MembershipType],
        /,
        *,
        affected_item_id: typing.Optional[int] = None,
        character_id: typing.Optional[int] = None,
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.

        body = {"type": type, "membershipType": int(membership_type)}

        if affected_item_id is not None:
            body["affectedItemId"] = affected_item_id

        if character_id is not None:
            body["characterId"] = character_id

        return self._request(
            RequestMethod.POST, "Destiny2/Awa/Initialize", json=body, auth=access_token
        )

    def awaget_action_token(
        self, access_token: str, correlation_id: str, /
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.POST,
            f"Destiny2/Awa/GetActionToken/{correlation_id}",
            auth=access_token,
        )

    def awa_provide_authorization_result(
        self,
        access_token: str,
        selection: int,
        correlation_id: str,
        nonce: collections.MutableSequence[typing.Union[str, bytes]],
    ) -> ResponseSig[int]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.

        body = {"selection": selection, "correlationId": correlation_id, "nonce": nonce}

        return self._request(
            RequestMethod.POST,
            "Destiny2/Awa/AwaProvideAuthorizationResult",
            json=body,
            auth=access_token,
        )

    def fetch_vendors(
        self,
        access_token: str,
        character_id: int,
        membership_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
        /,
        *components: enums.ComponentType,
        **options: typing.Optional[int],
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        components_ = self._collect_components(*components)
        route = (
            f"Destiny2/{int(membership_type)}/Profile/{membership_id}"
            f"/Character/{character_id}/Vendors/?components={components_}"
        )

        if "filter" in options:
            route = route + f"&filter={options['filter']}"

        return self._request(
            RequestMethod.GET,
            route,
            auth=access_token,
        )

    def fetch_vendor(
        self,
        access_token: str,
        character_id: int,
        membership_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
        vendor_hash: int,
        /,
        *components: enums.ComponentType,
    ) -> ResponseSig[typedefs.JSONObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        components_ = self._collect_components(*components)
        return self._request(
            RequestMethod.GET,
            (
                f"Platform/Destiny2/{int(membership_type)}/Profile/{membership_id}"
                f"/Character/{character_id}/Vendors/{vendor_hash}/?components={components_}"
            ),
            auth=access_token,
        )

    def fetch_application_api_usage(
        self,
        access_token: str,
        application_id: int,
        /,
        *,
        start: typing.Optional[datetime.datetime] = None,
        end: typing.Optional[datetime.datetime] = None,
    ) -> ResponseSig[typedefs.JSONObject]:

        end_date, start_date = aiobungie_time.parse_date_range(end, start)
        return self._request(
            RequestMethod.GET,
            f"App/ApiUsage/{application_id}/?end={end_date}&start={start_date}",
            auth=access_token,
        )

    def fetch_bungie_applications(self) -> ResponseSig[typedefs.JSONArray]:
        return self._request(RequestMethod.GET, "App/FirstParty")

    def fetch_content_type(self, type: str, /) -> ResponseSig[typedefs.JSONObject]:
        return self._request(RequestMethod.GET, f"Content/GetContentType/{type}/")

    def fetch_content_by_id(
        self, id: int, locale: str, /, *, head: bool = False
    ) -> ResponseSig[typedefs.JSONObject]:
        return self._request(
            RequestMethod.GET,
            f"Content/GetContentById/{id}/{locale}/",
            json={"head": head},
        )

    def fetch_content_by_tag_and_type(
        self, locale: str, tag: str, type: str, *, head: bool = False
    ) -> ResponseSig[typedefs.JSONObject]:
        return self._request(
            RequestMethod.GET,
            f"Content/GetContentByTagAndType/{tag}/{type}/{locale}/",
            json={"head": head},
        )

    def search_content_with_text(
        self,
        locale: str,
        /,
        content_type: str,
        search_text: str,
        tag: str,
        *,
        page: undefined.UndefinedOr[int] = undefined.Undefined,
        source: undefined.UndefinedOr[str] = undefined.Undefined,
    ) -> ResponseSig[typedefs.JSONObject]:

        body: typedefs.JSONObject = {}

        body["ctype"] = content_type
        body["searchtext"] = search_text
        body["tag"] = tag

        if page is not undefined.Undefined:
            body["currentpage"] = page
        else:
            body["currentpage"] = 1

        if source is not undefined.Undefined:
            body["source"] = source
        else:
            source = ""
        return self._request(RequestMethod.GET, f"Content/Search/{locale}/", json=body)

    def search_content_by_tag_and_type(
        self,
        locale: str,
        tag: str,
        type: str,
        *,
        page: undefined.UndefinedOr[int] = undefined.Undefined,
    ) -> ResponseSig[typedefs.JSONObject]:
        body: typedefs.JSONObject = {}
        body["currentpage"] = 1 if page is undefined.Undefined else page
        return self._request(
            RequestMethod.GET,
            f"Content/SearchContentByTagAndType/{tag}/{type}/{locale}/",
            json=body,
        )

    def search_help_articles(
        self, text: str, size: str, /
    ) -> ResponseSig[typedefs.JSONObject]:
        return self._request(
            RequestMethod.GET, f"Content/SearchHelpArticles/{text}/{size}/"
        )

    def fetch_topics_page(
        self,
        category_filter: int,
        group: int,
        date_filter: int,
        sort: typing.Union[str, bytes],
        *,
        page: undefined.UndefinedOr[int] = undefined.Undefined,
        locales: undefined.UndefinedOr[collections.Iterable[str]] = undefined.Undefined,
        tag_filter: undefined.UndefinedOr[str] = undefined.Undefined,
    ) -> ResponseSig[typedefs.JSONObject]:

        body: typedefs.JSONObject = {}
        if locales is not undefined.Undefined:
            body["locales"] = ",".join(str(locales))
        else:
            body["locales"] = ",".join([])

        if tag_filter is not undefined.Undefined:
            body["tagstring"] = tag_filter
        else:
            body["tagstring"] = ""

        page = 0 if page is not undefined.Undefined else page

        return self._request(
            RequestMethod.GET,
            f"Forum/GetTopicsPaged/{page}/{0}/{group}/{sort!s}/{date_filter}/{category_filter}/",
            json=body,
        )

    def fetch_core_topics_page(
        self,
        category_filter: int,
        date_filter: int,
        sort: typing.Union[str, bytes],
        *,
        page: undefined.UndefinedOr[int] = undefined.Undefined,
        locales: undefined.UndefinedOr[collections.Iterable[str]] = undefined.Undefined,
    ) -> ResponseSig[typedefs.JSONObject]:
        body: typedefs.JSONObject = {}

        if locales is not undefined.Undefined:
            body["locales"] = ",".join(str(locales))
        else:
            body["locales"] = ",".join([])

        return self._request(
            RequestMethod.GET,
            f"Forum/GetCoreTopicsPaged/{0 if page is undefined.Undefined else page}"
            f"/{sort!s}/{date_filter}/{category_filter}/",
            json=body,
        )

    def fetch_posts_threaded_page(
        self,
        parent_post: bool,
        page: int,
        page_size: int,
        parent_post_id: int,
        reply_size: int,
        root_thread_mode: bool,
        sort_mode: int,
        show_banned: typing.Optional[str] = None,
    ) -> ResponseSig[typedefs.JSONObject]:
        return self._request(
            RequestMethod.GET,
            f"Forum/GetPostsThreadedPaged/{parent_post}/{page}/"
            f"{page_size}/{reply_size}/{parent_post_id}/{root_thread_mode}/{sort_mode}/",
            json={"showbanned": show_banned},
        )

    def fetch_posts_threaded_page_from_child(
        self,
        child_id: bool,
        page: int,
        page_size: int,
        reply_size: int,
        root_thread_mode: bool,
        sort_mode: int,
        show_banned: typing.Optional[str] = None,
    ) -> ResponseSig[typedefs.JSONObject]:
        return self._request(
            RequestMethod.GET,
            f"Forum/GetPostsThreadedPagedFromChild/{child_id}/"
            f"{page}/{page_size}/{reply_size}/{root_thread_mode}/{sort_mode}/",
            json={"showbanned": show_banned},
        )

    def fetch_post_and_parent(
        self, child_id: int, /, *, show_banned: typing.Optional[str] = None
    ) -> ResponseSig[typedefs.JSONObject]:
        return self._request(
            RequestMethod.GET,
            f"Forum/GetPostAndParent/{child_id}/",
            json={"showbanned": show_banned},
        )

    def fetch_posts_and_parent_awaiting(
        self, child_id: int, /, *, show_banned: typing.Optional[str] = None
    ) -> ResponseSig[typedefs.JSONObject]:
        return self._request(
            RequestMethod.GET,
            f"Forum/GetPostAndParentAwaitingApproval/{child_id}/",
            json={"showbanned": show_banned},
        )

    def fetch_topic_for_content(self, content_id: int, /) -> ResponseSig[int]:
        return self._request(
            RequestMethod.GET, f"Forum/GetTopicForContent/{content_id}/"
        )

    def fetch_forum_tag_suggestions(
        self, partial_tag: str, /
    ) -> ResponseSig[typedefs.JSONObject]:
        return self._request(
            RequestMethod.GET,
            "Forum/GetForumTagSuggestions/",
            json={"partialtag": partial_tag},
        )

    def fetch_poll(self, topic_id: int, /) -> ResponseSig[typedefs.JSONObject]:
        return self._request(RequestMethod.GET, f"Forum/Poll/{topic_id}/")

    def fetch_recuirement_thread_summaries(self) -> ResponseSig[typedefs.JSONArray]:
        return self._request(RequestMethod.POST, "Forum/Recruit/Summaries/")

    def fetch_recommended_groups(
        self,
        accecss_token: str,
        /,
        *,
        date_range: int = 0,
        group_type: typedefs.IntAnd[enums.GroupType] = enums.GroupType.CLAN,
    ) -> ResponseSig[typedefs.JSONArray]:
        return self._request(
            RequestMethod.POST,
            f"GroupV2/Recommended/{int(group_type)}/{date_range}/",
            auth=accecss_token,
        )

    def fetch_available_avatars(self) -> ResponseSig[dict[str, int]]:
        return self._request(RequestMethod.GET, "GroupV2/GetAvailableAvatars/")

    def fetch_user_clan_invite_setting(
        self,
        access_token: str,
        /,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[bool]:
        return self._request(
            RequestMethod.GET,
            f"GroupV2/GetUserClanInviteSetting/{int(membership_type)}/",
            auth=access_token,
        )

    def fetch_banned_group_members(
        self, access_token: str, group_id: int, /, *, page: int = 1
    ) -> ResponseSig[typedefs.JSONObject]:
        return self._request(
            RequestMethod.GET,
            f"GroupV2/{group_id}/Banned/?currentpage={page}",
            auth=access_token,
        )

    def fetch_pending_group_memberships(
        self, access_token: str, group_id: int, /, *, current_page: int = 1
    ) -> ResponseSig[typedefs.JSONObject]:
        return self._request(
            RequestMethod.GET,
            f"GroupV2/{group_id}/Members/Pending/?currentpage={current_page}",
            auth=access_token,
        )

    def fetch_invited_group_memberships(
        self, access_token: str, group_id: int, /, *, current_page: int = 1
    ) -> ResponseSig[typedefs.JSONObject]:
        return self._request(
            RequestMethod.GET,
            f"GroupV2/{group_id}/Members/InvitedIndividuals/?currentpage={current_page}",
            auth=access_token,
        )

    def invite_member_to_group(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
        *,
        message: undefined.UndefinedOr[str] = undefined.Undefined,
    ) -> ResponseSig[typedefs.JSONObject]:
        return self._request(
            RequestMethod.POST,
            f"GroupV2/{group_id}/Members/IndividualInvite/{int(membership_type)}/{membership_id}/",
            auth=access_token,
            json={"message": str(message)},
        )

    def cancel_group_member_invite(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[typedefs.JSONObject]:
        return self._request(
            RequestMethod.POST,
            f"GroupV2/{group_id}/Members/IndividualInviteCancel/{int(membership_type)}/{membership_id}/",
            auth=access_token,
        )
