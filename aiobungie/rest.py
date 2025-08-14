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

"""Basic implementation of a RESTful clients for Bungie's REST API."""

from __future__ import annotations

__all__ = ("RESTClient", "RESTPool", "TRACE")

import asyncio
import contextlib
import datetime
import http
import logging
import os
import pathlib
import sys
import typing
import uuid
import zipfile

import aiohttp

from aiobungie import api, builders, error, metadata, typedefs, url
from aiobungie.crates import clans, fireteams
from aiobungie.internal import _backoff as backoff
from aiobungie.internal import enums, helpers, time

if typing.TYPE_CHECKING:
    import collections.abc as collections
    import concurrent.futures
    import types

    _HTTP_METHOD = typing.Literal["GET", "DELETE", "POST", "PUT", "PATCH"]
    _ALLOWED_LANGS = typing.Literal[
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
    ]

_MANIFEST_LANGUAGES: typing.Final[frozenset[_ALLOWED_LANGS]] = frozenset(
    (
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
    )
)

# Client headers.
_APP_JSON: str = "application/json"
_AUTH_HEADER: str = sys.intern("Authorization")
_USER_AGENT_HEADERS: str = sys.intern("User-Agent")
_USER_AGENT: str = (
    f"AiobungieClient (Author: {metadata.__author__}), "
    f"(Version: {metadata.__version__}), (URL: {metadata.__url__})"
)

# Possible internal error codes.
_RETRY_5XX: set[int] = {500, 502, 503, 504}

# HTTP methods.
_GET: typing.Final[str] = "GET"
_POST: typing.Final[str] = "POST"

# These are Currently unused.
# _DELETE: typing.Final[str] = "DELETE"
# _PUT: typing.Final[str] = "PUT"
# _PATCH: typing.Final[str] = "PATCH"


_LOGGER = logging.getLogger("aiobungie.rest")

TRACE: typing.Final[int] = logging.DEBUG - 5
"""The trace logging level for the `RESTClient` responses.

You can enable this with the following code

>>> import logging
>>> logging.getLogger("aiobungie.rest").setLevel(aiobungie.TRACE)
# or
>>> logging.basicConfig(level=aiobungie.TRACE)
# Or
>>> client = aiobungie.RESTClient(debug="TRACE")
# Or if you're using `aiobungie.Client`
>>> client = aiobungie.Client()
>>> client.rest.with_debug(level=aiobungie.TRACE, file="rest_logs.txt")
"""

logging.addLevelName(TRACE, "TRACE")


def _collect_components(
    components: collections.Sequence[enums.ComponentType],
    /,
) -> str:
    collector: collections.MutableSequence[str] = []

    for component in components:
        if isinstance(component.value, tuple):
            collector.extend(str(c) for c in component.value)  # pyright: ignore
        else:
            collector.append(str(component.value))
    return ",".join(collector)


def _uuid() -> str:
    return uuid.uuid4().hex


def _ensure_manifest_language(language: str) -> None:
    if language not in _MANIFEST_LANGUAGES:
        langs = "\n".join(_MANIFEST_LANGUAGES)
        raise ValueError(
            f"{language} is not a valid manifest language, valid languages are: {langs}"
        )


def _get_path(
    file_name: str, path: str | pathlib.Path, sql: bool = False
) -> pathlib.Path:
    if sql:
        return pathlib.Path(path).joinpath(file_name + ".sqlite3")
    return pathlib.Path(path).joinpath(file_name + ".json")


def _write_json_bytes(
    data: bytes,
    file_name: str = "manifest",
    path: pathlib.Path | str = "./",
) -> None:
    with _get_path(file_name, path).open("wb") as p:
        p.write(helpers.dumps(helpers.loads(data)))


def _write_sqlite_bytes(
    data: bytes,
    path: pathlib.Path | str = "./",
    file_name: str = "manifest",
) -> None:
    with open(f"{_uuid()}.zip", "wb") as tmp:
        tmp.write(data)
        try:
            with zipfile.ZipFile(tmp.name) as zipped:
                file = zipped.namelist()

                if file:
                    zipped.extractall(".")

                    os.rename(file[0], _get_path(file_name, path, sql=True))

        finally:
            pathlib.Path(tmp.name).unlink(missing_ok=True)


class _JSONPayload(aiohttp.BytesPayload):
    def __init__(
        self, value: typing.Any, dumps: typedefs.Dumps = helpers.dumps
    ) -> None:
        super().__init__(dumps(value), content_type=_APP_JSON, encoding="utf-8")


class RESTPool:
    """a Pool of `RESTClient` instances that shares the same TCP client connection.

    This allows you to acquire instances of `RESTClient`s from single settings and credentials.

    Example
    -------
    ```py
    import aiobungie
    import asyncio

    pool = aiobungie.RESTPool("token")

    async def get() -> None:
        await pool.start()

        async with pool.acquire() as client:
            await client.fetch_character(...)

        await pool.stop()

    asyncio.run(get())
    ```

    Parameters
    ----------
    token : `str`
        A valid application token from Bungie's developer portal.

    Other Parameters
    ----------------
    client_secret : `str | None`
        An optional application client secret,
        This is only needed if you're fetching OAuth2 tokens with this client.
    client_id : `int | None`
        An optional application client id,
        This is only needed if you're fetching OAuth2 tokens with this client.
    settings: `aiobungie.builders.Settings | None`
        The client settings to use, if `None` the default will be used.
    max_retries : `int`
        The max retries number to retry if the request hit a `5xx` status code.
    debug : `bool | str`
        Whether to enable logging responses or not.

    Logging Levels
    --------------
    * `False`: This will disable logging.
    * `True`: This will set the level to `DEBUG` and enable logging minimal information.
    Like the response status, route, taken time and so on.
    * `"TRACE" | aiobungie.TRACE`: This will log the response headers along with the minimal information.
    """

    __slots__ = (
        "_token",
        "_max_retries",
        "_client_secret",
        "_client_id",
        "_metadata",
        "_enable_debug",
        "_client_session",
        "_loads",
        "_dumps",
        "_settings",
    )

    # Looks like mypy doesn't like this.
    if typing.TYPE_CHECKING:
        _enable_debug: typing.Literal["TRACE"] | bool | int

    def __init__(
        self,
        token: str,
        /,
        *,
        client_secret: str | None = None,
        client_id: int | None = None,
        settings: builders.Settings | None = None,
        dumps: typedefs.Dumps = helpers.dumps,
        loads: typedefs.Loads = helpers.loads,
        max_retries: int = 4,
        debug: typing.Literal["TRACE"] | bool | int = False,
    ) -> None:
        self._client_secret = client_secret
        self._client_id = client_id
        self._token = token
        self._max_retries = max_retries
        self._metadata: collections.MutableMapping[typing.Any, typing.Any] = {}
        self._enable_debug = debug
        self._client_session: aiohttp.ClientSession | None = None
        self._loads = loads
        self._dumps = dumps
        self._settings = settings or builders.Settings()

    @property
    def client_id(self) -> int | None:
        """Return the client id of this REST client if provided, Otherwise None."""
        return self._client_id

    @property
    def metadata(self) -> collections.MutableMapping[typing.Any, typing.Any]:
        """A general-purpose mutable mapping you can use to store data.

        This mapping can be accessed from any process that has a reference to this pool.
        """
        return self._metadata

    @property
    def settings(self) -> builders.Settings:
        """Internal client settings used within the HTTP client session."""
        return self._settings

    @typing.overload
    def build_oauth2_url(self, client_id: int) -> builders.OAuthURL: ...

    @typing.overload
    def build_oauth2_url(self) -> builders.OAuthURL | None: ...

    @typing.final
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
        client_id = client_id or self._client_id
        if client_id is None:
            return None

        return builders.OAuthURL(client_id=client_id)

    async def start(self) -> None:
        """Start the TCP connection of this client pool.

        This will raise `RuntimeError` if the connection has already been started.

        Example
        -------
        ```py
        pool = aiobungie.RESTPool(...)

        async def run() -> None:
            await pool.start()
            async with pool.acquire() as client:
                # use client

        async def stop(self) -> None:
            await pool.close()
        ```
        """
        if self._client_session is not None:
            raise RuntimeError("<RESTPool> has already been started.") from None

        self._client_session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                use_dns_cache=self._settings.use_dns_cache,
                ttl_dns_cache=self._settings.ttl_dns_cache,
                ssl_context=self._settings.ssl_context,
                ssl=self._settings.ssl,
            ),
            connector_owner=True,
            raise_for_status=False,
            timeout=self._settings.http_timeout,
            trust_env=self._settings.trust_env,
            headers=self._settings.headers,
        )

    async def stop(self) -> None:
        """Stop the TCP connection of this client pool.

        This will raise `RuntimeError` if the connection has already been closed.

        Example
        -------
        ```py
        pool = aiobungie.RESTPool(...)

        async def run() -> None:
            await pool.start()
            async with pool.acquire() as client:
                # use client

        async def stop(self) -> None:
            await pool.close()
        ```
        """
        if self._client_session is None:
            raise RuntimeError("<RESTPool> is already stopped.")

        await self._client_session.close()
        self._client_session = None

    @typing.final
    def acquire(self) -> RESTClient:
        """Acquires a new `RESTClient` instance from this pool.

        Returns
        -------
        `RESTClient`
            An instance of a `RESTClient`.
        """
        return RESTClient(
            self._token,
            client_secret=self._client_secret,
            client_id=self._client_id,
            loads=self._loads,
            dumps=self._dumps,
            max_retries=self._max_retries,
            debug=self._enable_debug,
            client_session=self._client_session,
            owned_client=False,
            settings=self._settings,
        )


class RESTClient(api.RESTClient):
    """A single process REST client implementation.

    This client is designed to only make HTTP requests and return raw JSON objects.

    Example
    -------
    ```py
    import aiobungie

    client = aiobungie.RESTClient("TOKEN")
    async with client:
        response = await client.fetch_clan_members(4389205)
        for member in response['results']:
            print(member['destinyUserInfo'])
    ```

    Parameters
    ----------
    token : `str`
        A valid application token from Bungie's developer portal.

    Other Parameters
    ----------------
    client_secret : `str | None`
        An optional application client secret,
        This is only needed if you're fetching OAuth2 tokens with this client.
    client_id : `int | None`
        An optional application client id,
        This is only needed if you're fetching OAuth2 tokens with this client.
    settings: `aiobungie.builders.Settings | None`
        The client settings to use, if `None` the default will be used.
    owned_client: `bool`
        * If set to `True`, this client will use the provided `client_session` parameter instead,
        * If set to `True` and `client_session` is `None`, `ValueError` will be raised.
        * If set to `False`, aiobungie will initialize a new client session for you.

    client_session: `aiohttp.ClientSession | None`
        If provided, this client session will be used to make all the HTTP requests.
        The `owned_client` must be set to `True` for this to work.
    max_retries : `int`
        The max retries number to retry if the request hit a `5xx` status code.
    debug : `bool | str`
        Whether to enable logging responses or not.

    Logging Levels
    --------------
    * `False`: This will disable logging.
    * `True`: This will set the level to `DEBUG` and enable logging minimal information.
    * `"TRACE" | aiobungie.TRACE`: This will log the response headers along with the minimal information.
    """

    __slots__ = (
        "_token",
        "_session",
        "_lock",
        "_max_retries",
        "_client_secret",
        "_client_id",
        "_metadata",
        "_dumps",
        "_loads",
        "_owned_client",
        "_settings",
    )

    def __init__(
        self,
        token: str,
        /,
        *,
        client_secret: str | None = None,
        client_id: int | None = None,
        settings: builders.Settings | None = None,
        owned_client: bool = True,
        client_session: aiohttp.ClientSession | None = None,
        dumps: typedefs.Dumps = helpers.dumps,
        loads: typedefs.Loads = helpers.loads,
        max_retries: int = 4,
        debug: typing.Literal["TRACE"] | bool | int = False,
    ) -> None:
        if owned_client is False and client_session is None:
            raise ValueError(
                "Expected an owned client session, but got `None`, Cannot have `owned_client` set to `False` and `client_session` to `None`"
            )

        self._settings = settings or builders.Settings()
        self._session = client_session
        self._owned_client = owned_client
        self._lock: asyncio.Lock | None = None
        self._client_secret = client_secret
        self._client_id = client_id
        self._token: str = token
        self._max_retries = max_retries
        self._dumps = dumps
        self._loads = loads
        self._metadata: collections.MutableMapping[typing.Any, typing.Any] = {}
        self.with_debug(debug)

    @property
    def client_id(self) -> int | None:
        return self._client_id

    @property
    def metadata(self) -> collections.MutableMapping[typing.Any, typing.Any]:
        return self._metadata

    @property
    def is_alive(self) -> bool:
        return self._session is not None

    @property
    def settings(self) -> builders.Settings:
        return self._settings

    async def close(self) -> None:
        if self._session is None:
            raise RuntimeError("REST client is not running.")

        if self._owned_client:
            await self._session.close()
            self._session = None

    def open(self) -> None:
        """Open a new client session. This is called internally with contextmanager usage."""
        if self.is_alive and self._owned_client:
            raise RuntimeError("Cannot open REST client when it's already open.")

        if self._owned_client:
            self._session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(
                    use_dns_cache=self._settings.use_dns_cache,
                    ttl_dns_cache=self._settings.ttl_dns_cache,
                    ssl_context=self._settings.ssl_context,
                    ssl=self._settings.ssl,
                ),
                connector_owner=True,
                raise_for_status=False,
                timeout=self._settings.http_timeout,
                trust_env=self._settings.trust_env,
                headers=self._settings.headers,
            )

    @typing.final
    async def static_request(
        self,
        method: _HTTP_METHOD,
        path: str,
        *,
        auth: str | None = None,
        json: collections.Mapping[str, typing.Any] | None = None,
        params: collections.Mapping[str, typing.Any] | None = None,
    ) -> typedefs.JSONIsh:
        return await self._request(method, path, auth=auth, json=json, params=params)

    @typing.overload
    def build_oauth2_url(self, client_id: int) -> builders.OAuthURL: ...

    @typing.overload
    def build_oauth2_url(self) -> builders.OAuthURL | None: ...

    @typing.final
    def build_oauth2_url(
        self, client_id: int | None = None
    ) -> builders.OAuthURL | None:
        client_id = client_id or self._client_id
        if client_id is None:
            return None

        return builders.OAuthURL(client_id=client_id)

    @typing.final
    async def _request(
        self,
        method: _HTTP_METHOD,
        route: str,
        *,
        base: bool = False,
        oauth2: bool = False,
        auth: str | None = None,
        unwrap_bytes: bool = False,
        json: collections.Mapping[str, typing.Any] | None = None,
        data: collections.Mapping[str, typing.Any] | None = None,
        params: collections.Mapping[str, typing.Any] | None = None,
    ) -> typedefs.JSONIsh:
        # This is not None when opening the client.
        assert self._session is not None, (
            "This client hasn't been opened yet. Use `async with client` or `async with client.rest` "
            "before performing any request."
        )

        retries: int = 0
        headers: collections.MutableMapping[str, typing.Any] = {}

        headers[_USER_AGENT_HEADERS] = _USER_AGENT
        headers["X-API-KEY"] = self._token

        if auth is not None:
            headers[_AUTH_HEADER] = f"Bearer {auth}"

        # Handling endpoints
        endpoint = url.BASE

        if not base:
            endpoint = endpoint + url.REST_EP

        if oauth2:
            assert self._client_id, "Client ID is required to make authorized requests."
            assert self._client_secret, (
                "Client secret is required to make authorized requests."
            )
            headers["client_secret"] = self._client_secret

            headers["Content-Type"] = "application/x-www-form-urlencoded"
            endpoint = endpoint + url.TOKEN_EP

        if self._lock is None:
            self._lock = asyncio.Lock()

        if json:
            headers["Content-Type"] = _APP_JSON

        stack = contextlib.AsyncExitStack()
        while True:
            try:
                await stack.enter_async_context(self._lock)

                # We make the request here.
                taken_time = time.monotonic()
                response = await self._session.request(
                    method=method,
                    url=f"{endpoint}/{route}",
                    headers=headers,
                    data=_JSONPayload(json) if json else data,
                    params=params,
                )
                response_time = (time.monotonic() - taken_time) * 1_000

                _LOGGER.debug(
                    "METHOD: %s ROUTE: %s STATUS: %i ELAPSED: %.4fms",
                    method,
                    f"{endpoint}/{route}",
                    response.status,
                    response_time,
                )

                await self._handle_ratelimit(response, method, route)

            except aiohttp.ClientConnectionError as exc:
                if retries >= self._max_retries:
                    raise error.HTTPError(
                        str(exc),
                        http.HTTPStatus.SERVICE_UNAVAILABLE,
                    )
                backoff_ = backoff.ExponentialBackOff(maximum=8)

                timer = next(backoff_)
                _LOGGER.warning(
                    "Client received a connection error <%s> Retrying in %.2fs. Remaining retries: %s",
                    type(exc).__qualname__,
                    timer,
                    self._max_retries - retries,
                )
                retries += 1
                await asyncio.sleep(timer)
                continue

            finally:
                await stack.aclose()

            if response.status == http.HTTPStatus.NO_CONTENT:
                return None

            # Handle the successful response.
            if 300 > response.status >= 200:
                if unwrap_bytes:
                    # We need to read the bytes for the manifest response.
                    return await response.read()

                # Bungie get funky and return HTML instead of JSON when making an authorized
                # request with a dummy access token. We could technically read the page content
                # but that's Bungie's fault for not returning a JSON response.
                if response.content_type != _APP_JSON:
                    raise error.HTTPError(
                        message=f"Expected JSON response, Got {response.content_type}, "
                        f"{response.real_url.human_repr()}",
                        http_status=http.HTTPStatus(response.status),
                    )

                json_data = self._loads(await response.read())

                if _LOGGER.isEnabledFor(TRACE):
                    _LOGGER.log(
                        TRACE,
                        "%s",
                        error.stringify_headers(dict(response.headers)),
                    )

                    details: collections.MutableMapping[str, typing.Any] = {}
                    if json:
                        details["json"] = error.filtered_headers(json)

                    if data:
                        details["data"] = error.filtered_headers(data)

                    if params:
                        details["params"] = error.filtered_headers(params)

                    if details:
                        _LOGGER.log(TRACE, "%s", error.stringify_headers(details))

                # Return the response.
                # auth responses are not inside a Response object.
                if oauth2:
                    return json_data

                # The reason we have a type ignore is because the actual response type
                # is within this `Response` key.
                return json_data["Response"]  # type: ignore

            if (
                response.status in _RETRY_5XX and retries < self._max_retries  # noqa: W503
            ):
                backoff_ = backoff.ExponentialBackOff(maximum=6)
                sleep_time = next(backoff_)
                _LOGGER.warning(
                    "Got %i - %s. Sleeping for %.2f seconds. Remaining retries: %i",
                    response.status,
                    response.reason,
                    sleep_time,
                    self._max_retries - retries,
                )

                retries += 1
                await asyncio.sleep(sleep_time)
                continue

            raise await error.panic(response)

    async def __aenter__(self) -> RESTClient:
        self.open()
        return self

    async def __aexit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        exception_traceback: types.TracebackType | None,
    ) -> None:
        await self.close()

    # We don't want this to be super complicated.
    async def _handle_ratelimit(
        self,
        response: aiohttp.ClientResponse,
        method: str,
        route: str,
    ) -> None:
        if response.status != http.HTTPStatus.TOO_MANY_REQUESTS:
            return

        if response.content_type != _APP_JSON:
            raise error.HTTPError(
                f"Being ratelimited on non JSON request, {response.content_type}.",
                http.HTTPStatus.TOO_MANY_REQUESTS,
            )

        # The reason we have a type ignore here is that we guaranteed the content type is JSON above.
        json: typedefs.JSONObject = self._loads(await response.read())  # type: ignore
        retry_after = float(json.get("ThrottleSeconds", 15.0)) + 0.1
        max_calls: int = 0

        while True:
            if max_calls == 10:
                # Max retries by default. We raise an error here.
                raise error.RateLimitedError(
                    body=json,
                    url=str(response.real_url),
                    retry_after=retry_after,
                )

            # We sleep for a little bit to avoid funky behavior.
            _LOGGER.warning(
                "We're being ratelimited, Method %s Route %s. Sleeping for %.2fs.",
                method,
                route,
                retry_after,
            )
            await asyncio.sleep(retry_after)
            max_calls += 1
            continue

    async def fetch_oauth2_tokens(self, code: str, /) -> builders.OAuth2Response:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }

        response = await self._request(_POST, "", data=data, oauth2=True)
        assert isinstance(response, dict)
        return builders.OAuth2Response.build_response(response)

    async def refresh_access_token(
        self, refresh_token: str, /
    ) -> builders.OAuth2Response:
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }

        response = await self._request(_POST, "", data=data, oauth2=True)
        assert isinstance(response, dict)
        return builders.OAuth2Response.build_response(response)

    async def fetch_bungie_user(self, id: int) -> typedefs.JSONObject:
        resp = await self._request(_GET, f"User/GetBungieNetUserById/{id}/")
        assert isinstance(resp, dict)
        return resp

    async def fetch_user_themes(self) -> typedefs.JSONArray:
        resp = await self._request(_GET, "User/GetAvailableThemes/")
        assert isinstance(resp, list)
        return resp

    async def fetch_membership_from_id(
        self,
        id: int,
        type: enums.MembershipType | int = enums.MembershipType.NONE,
        /,
    ) -> typedefs.JSONObject:
        resp = await self._request(_GET, f"User/GetMembershipsById/{id}/{int(type)}")
        assert isinstance(resp, dict)
        return resp

    async def fetch_membership(
        self,
        name: str,
        code: int,
        type: enums.MembershipType | int = enums.MembershipType.ALL,
        /,
    ) -> typedefs.JSONArray:
        resp = await self._request(
            _POST,
            f"Destiny2/SearchDestinyPlayerByBungieName/{int(type)}",
            json={"displayName": name, "displayNameCode": code},
        )
        assert isinstance(resp, list)
        return resp

    async def fetch_sanitized_membership(
        self, membership_id: int, /
    ) -> typedefs.JSONObject:
        response = await self._request(
            _GET, f"User/GetSanitizedPlatformDisplayNames/{membership_id}/"
        )
        assert isinstance(response, dict)
        return response

    async def search_users(self, name: str, /) -> typedefs.JSONObject:
        resp = await self._request(
            _POST,
            "User/Search/GlobalName/0",
            json={"displayNamePrefix": name},
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_clan_from_id(
        self, id: int, /, access_token: str | None = None
    ) -> typedefs.JSONObject:
        resp = await self._request(_GET, f"GroupV2/{id}", auth=access_token)
        assert isinstance(resp, dict)
        return resp

    async def fetch_clan(
        self,
        name: str,
        /,
        access_token: str | None = None,
        *,
        type: enums.GroupType | int = enums.GroupType.CLAN,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET, f"GroupV2/Name/{name}/{int(type)}", auth=access_token
        )
        assert isinstance(resp, dict)
        return resp

    async def search_group(
        self,
        name: str,
        group_type: enums.GroupType | int = enums.GroupType.CLAN,
        *,
        creation_date: clans.GroupDate | int = 0,
        sort_by: int | None = None,
        group_member_count_filter: typing.Literal[0, 1, 2, 3] | None = None,
        locale_filter: str | None = None,
        tag_text: str | None = None,
        items_per_page: int | None = None,
        current_page: int | None = None,
        request_token: str | None = None,
    ) -> typedefs.JSONObject:
        payload: collections.MutableMapping[str, typing.Any] = {"name": name}

        # as the official documentation says, you're not allowed to use those fields
        # on a clan search. it is safe to send the request with them being `null` but not filled with a value.
        if (
            group_type == enums.GroupType.CLAN
            and group_member_count_filter is not None
            and locale_filter
            and tag_text
        ):
            raise ValueError(
                "If you're searching for clans, (group_member_count_filter, locale_filter, tag_text) must be None."
            )

        payload["groupType"] = int(group_type)
        payload["creationDate"] = int(creation_date)
        payload["sortBy"] = sort_by
        payload["groupMemberCount"] = group_member_count_filter
        payload["locale"] = locale_filter
        payload["tagText"] = tag_text
        payload["itemsPerPage"] = items_per_page
        payload["currentPage"] = current_page
        payload["requestToken"] = request_token
        payload["requestContinuationToken"] = request_token

        resp = await self._request(_POST, "GroupV2/Search/", json=payload)
        assert isinstance(resp, dict)
        return resp

    async def fetch_clan_admins(self, clan_id: int, /) -> typedefs.JSONObject:
        resp = await self._request(_GET, f"GroupV2/{clan_id}/AdminsAndFounder/")
        assert isinstance(resp, dict)
        return resp

    async def fetch_clan_conversations(self, clan_id: int, /) -> typedefs.JSONArray:
        resp = await self._request(_GET, f"GroupV2/{clan_id}/OptionalConversations/")
        assert isinstance(resp, list)
        return resp

    async def fetch_application(self, appid: int, /) -> typedefs.JSONObject:
        resp = await self._request(_GET, f"App/Application/{appid}")
        assert isinstance(resp, dict)
        return resp

    async def fetch_character(
        self,
        member_id: int,
        membership_type: enums.MembershipType | int,
        character_id: int,
        components: collections.Sequence[enums.ComponentType],
        auth: str | None = None,
    ) -> typedefs.JSONObject:
        collector = _collect_components(components)
        response = await self._request(
            _GET,
            f"Destiny2/{int(membership_type)}/Profile/{member_id}/"
            f"Character/{character_id}/?components={collector}",
            auth=auth,
        )
        assert isinstance(response, dict)
        return response

    async def fetch_activities(
        self,
        member_id: int,
        character_id: int,
        mode: enums.GameMode | int,
        membership_type: enums.MembershipType | int = enums.MembershipType.ALL,
        *,
        page: int = 0,
        limit: int = 1,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Destiny2/{int(membership_type)}/Account/"
            f"{member_id}/Character/{character_id}/Stats/Activities"
            f"/?mode={int(mode)}&count={limit}&page={page}",
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_vendor_sales(self) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Destiny2/Vendors/?components={int(enums.ComponentType.VENDOR_SALES)}",
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_profile(
        self,
        membership_id: int,
        type: enums.MembershipType | int,
        components: collections.Sequence[enums.ComponentType],
        auth: str | None = None,
    ) -> typedefs.JSONObject:
        collector = _collect_components(components)
        response = await self._request(
            _GET,
            f"Destiny2/{int(type)}/Profile/{membership_id}/?components={collector}",
            auth=auth,
        )
        assert isinstance(response, dict)
        return response

    async def fetch_entity(self, type: str, hash: int) -> typedefs.JSONObject:
        response = await self._request(_GET, route=f"Destiny2/Manifest/{type}/{hash}")
        assert isinstance(response, dict)
        return response

    async def fetch_inventory_item(self, hash: int, /) -> typedefs.JSONObject:
        resp = await self.fetch_entity("DestinyInventoryItemDefinition", hash)
        assert isinstance(resp, dict)
        return resp

    async def fetch_objective_entity(self, hash: int, /) -> typedefs.JSONObject:
        resp = await self.fetch_entity("DestinyObjectiveDefinition", hash)
        assert isinstance(resp, dict)
        return resp

    async def fetch_groups_for_member(
        self,
        member_id: int,
        member_type: enums.MembershipType | int,
        /,
        *,
        filter: int = 0,
        group_type: enums.GroupType | int = enums.GroupType.CLAN,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"GroupV2/User/{int(member_type)}/{member_id}/{filter}/{int(group_type)}/",
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_potential_groups_for_member(
        self,
        member_id: int,
        member_type: enums.MembershipType | int,
        /,
        *,
        filter: int = 0,
        group_type: enums.GroupType | int = enums.GroupType.CLAN,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"GroupV2/User/Potential/{int(member_type)}/{member_id}/{filter}/{int(group_type)}/",
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_clan_members(
        self,
        clan_id: int,
        /,
        *,
        name: str | None = None,
        type: enums.MembershipType | int = enums.MembershipType.NONE,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"/GroupV2/{clan_id}/Members/?memberType={int(type)}&nameSearch={name if name else ''}&currentpage=1",
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_hardlinked_credentials(
        self,
        credential: int,
        type: enums.CredentialType | int = enums.CredentialType.STEAMID,
        /,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"User/GetMembershipFromHardLinkedCredential/{int(type)}/{credential}/",
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_user_credentials(
        self, access_token: str, membership_id: int, /
    ) -> typedefs.JSONArray:
        resp = await self._request(
            _GET,
            f"User/GetCredentialTypesForTargetAccount/{membership_id}",
            auth=access_token,
        )
        assert isinstance(resp, list)
        return resp

    async def insert_socket_plug(
        self,
        action_token: str,
        /,
        instance_id: int,
        plug: builders.PlugSocketBuilder | collections.Mapping[str, int],
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> typedefs.JSONObject:
        if isinstance(plug, builders.PlugSocketBuilder):
            plug = plug.collect()

        body = {
            "actionToken": action_token,
            "itemInstanceId": instance_id,
            "plug": plug,
            "characterId": character_id,
            "membershipType": int(membership_type),
        }
        resp = await self._request(
            _POST, "Destiny2/Actions/Items/InsertSocketPlug", json=body
        )
        assert isinstance(resp, dict)
        return resp

    async def insert_socket_plug_free(
        self,
        access_token: str,
        /,
        instance_id: int,
        plug: builders.PlugSocketBuilder | collections.Mapping[str, int],
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> typedefs.JSONObject:
        if isinstance(plug, builders.PlugSocketBuilder):
            plug = plug.collect()

        body = {
            "itemInstanceId": instance_id,
            "plug": plug,
            "characterId": character_id,
            "membershipType": int(membership_type),
        }
        resp = await self._request(
            _POST,
            "Destiny2/Actions/Items/InsertSocketPlugFree",
            json=body,
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    @helpers.unstable
    async def set_item_lock_state(
        self,
        access_token: str,
        state: bool,
        /,
        item_id: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> int:
        body = {
            "state": state,
            "itemId": item_id,
            "characterId": character_id,
            "membershipType": int(membership_type),
        }
        response = await self._request(
            _POST,
            "Destiny2/Actions/Items/SetLockState",
            json=body,
            auth=access_token,
        )
        assert isinstance(response, int)
        return response

    async def set_quest_track_state(
        self,
        access_token: str,
        state: bool,
        /,
        item_id: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> int:
        body = {
            "state": state,
            "itemId": item_id,
            "characterId": character_id,
            "membership_type": int(membership_type),
        }
        response = await self._request(
            _POST,
            "Destiny2/Actions/Items/SetTrackedState",
            json=body,
            auth=access_token,
        )
        assert isinstance(response, int)
        return response

    async def fetch_manifest_path(self) -> typedefs.JSONObject:
        path = await self._request(_GET, "Destiny2/Manifest")
        assert isinstance(path, dict)
        return path

    async def read_manifest_bytes(self, language: _ALLOWED_LANGS = "en", /) -> bytes:
        _ensure_manifest_language(language)

        content = await self.fetch_manifest_path()
        resp = await self._request(
            _GET,
            content["mobileWorldContentPaths"][language],
            unwrap_bytes=True,
            base=True,
        )
        assert isinstance(resp, bytes)
        return resp

    async def download_sqlite_manifest(
        self,
        language: _ALLOWED_LANGS = "en",
        name: str = "manifest",
        path: pathlib.Path | str = ".",
        *,
        force: bool = False,
        executor: concurrent.futures.Executor | None = None,
    ) -> pathlib.Path:
        complete_path = _get_path(name, path, sql=True)

        if complete_path.exists():
            if force:
                _LOGGER.info(
                    f"Found manifest in {complete_path!s}. Forcing to Re-Download."
                )
                complete_path.unlink(missing_ok=True)

                return await self.download_sqlite_manifest(
                    language, name, path, force=force
                )

            else:
                raise FileExistsError(
                    "Manifest file already exists, "
                    "To force download, set the `force` parameter to `True`."
                )

        _LOGGER.info(f"Downloading manifest. Location: {complete_path!s}")
        data_bytes = await self.read_manifest_bytes(language)
        await asyncio.get_running_loop().run_in_executor(
            executor, _write_sqlite_bytes, data_bytes, path, name
        )
        _LOGGER.info("Finished downloading manifest.")
        return _get_path(name, path, sql=True)

    async def download_json_manifest(
        self,
        file_name: str = "manifest",
        path: str | pathlib.Path = ".",
        *,
        language: _ALLOWED_LANGS = "en",
        executor: concurrent.futures.Executor | None = None,
    ) -> pathlib.Path:
        _ensure_manifest_language(language)
        full_path = _get_path(file_name, path)
        _LOGGER.info(f"Downloading manifest JSON to {full_path!r}...")

        content = await self.fetch_manifest_path()
        json_bytes = await self._request(
            _GET,
            content["jsonWorldContentPaths"][language],
            unwrap_bytes=True,
            base=True,
        )

        assert isinstance(json_bytes, bytes)
        await asyncio.get_running_loop().run_in_executor(
            executor, _write_json_bytes, json_bytes, file_name, path
        )
        _LOGGER.info("Finished downloading manifest JSON.")
        return full_path

    async def fetch_manifest_version(self) -> str:
        # This is guaranteed str.
        return (await self.fetch_manifest_path())["version"]

    async def fetch_linked_profiles(
        self,
        member_id: int,
        member_type: enums.MembershipType | int,
        /,
        *,
        all: bool = False,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Destiny2/{int(member_type)}/Profile/{member_id}/LinkedProfiles/?getAllMemberships={all}",
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_clan_banners(self) -> typedefs.JSONObject:
        resp = await self._request(_GET, "Destiny2/Clan/ClanBannerDictionary/")
        assert isinstance(resp, dict)
        return resp

    async def fetch_public_milestones(self) -> typedefs.JSONObject:
        resp = await self._request(_GET, "Destiny2/Milestones/")
        assert isinstance(resp, dict)
        return resp

    async def fetch_public_milestone_content(
        self, milestone_hash: int, /
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET, f"Destiny2/Milestones/{milestone_hash}/Content/"
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_current_user_memberships(
        self, access_token: str, /
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            "User/GetMembershipsForCurrentUser/",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def equip_item(
        self,
        access_token: str,
        /,
        item_id: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> None:
        payload = {
            "itemId": item_id,
            "characterId": character_id,
            "membershipType": int(membership_type),
        }

        await self._request(
            _POST,
            "Destiny2/Actions/Items/EquipItem/",
            json=payload,
            auth=access_token,
        )

    async def equip_items(
        self,
        access_token: str,
        /,
        item_ids: collections.Sequence[int],
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> None:
        payload = {
            "itemIds": item_ids,
            "characterId": character_id,
            "membershipType": int(membership_type),
        }
        await self._request(
            _POST,
            "Destiny2/Actions/Items/EquipItems/",
            json=payload,
            auth=access_token,
        )

    async def ban_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
        *,
        length: int = 0,
        comment: str | None = None,
    ) -> None:
        payload = {"comment": str(comment), "length": length}
        await self._request(
            _POST,
            f"GroupV2/{group_id}/Members/{int(membership_type)}/{membership_id}/Ban/",
            json=payload,
            auth=access_token,
        )

    async def unban_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
    ) -> None:
        await self._request(
            _POST,
            f"GroupV2/{group_id}/Members/{int(membership_type)}/{membership_id}/Unban/",
            auth=access_token,
        )

    async def kick_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _POST,
            f"GroupV2/{group_id}/Members/{int(membership_type)}/{membership_id}/Kick/",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def edit_clan(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        name: str | None = None,
        about: str | None = None,
        motto: str | None = None,
        theme: str | None = None,
        tags: collections.Sequence[str] | None = None,
        is_public: bool | None = None,
        locale: str | None = None,
        avatar_image_index: int | None = None,
        membership_option: enums.MembershipOption | int | None = None,
        allow_chat: bool | None = None,
        chat_security: typing.Literal[0, 1] | None = None,
        call_sign: str | None = None,
        homepage: typing.Literal[0, 1, 2] | None = None,
        enable_invite_messaging_for_admins: bool | None = None,
        default_publicity: typing.Literal[0, 1, 2] | None = None,
        is_public_topic_admin: bool | None = None,
    ) -> None:
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

        await self._request(
            _POST,
            f"GroupV2/{group_id}/Edit",
            json=payload,
            auth=access_token,
        )

    async def edit_clan_options(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        invite_permissions_override: bool | None = None,
        update_culture_permissionOverride: bool | None = None,
        host_guided_game_permission_override: typing.Literal[0, 1, 2] | None = None,
        update_banner_permission_override: bool | None = None,
        join_level: enums.ClanMemberType | int | None = None,
    ) -> None:
        payload = {
            "InvitePermissionOverride": invite_permissions_override,
            "UpdateCulturePermissionOverride": update_culture_permissionOverride,
            "HostGuidedGamePermissionOverride": host_guided_game_permission_override,
            "UpdateBannerPermissionOverride": update_banner_permission_override,
            "JoinLevel": int(join_level) if join_level else None,
        }

        await self._request(
            _POST,
            f"GroupV2/{group_id}/EditFounderOptions",
            json=payload,
            auth=access_token,
        )

    async def report_player(
        self,
        access_token: str,
        /,
        activity_id: int,
        character_id: int,
        reason_hashes: collections.Sequence[int],
        reason_category_hashes: collections.Sequence[int],
    ) -> None:
        await self._request(
            _POST,
            f"Destiny2/Stats/PostGameCarnageReport/{activity_id}/Report/",
            json={
                "reasonCategoryHashes": reason_category_hashes,
                "reasonHashes": reason_hashes,
                "offendingCharacterId": character_id,
            },
            auth=access_token,
        )

    async def fetch_friends(self, access_token: str, /) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            "Social/Friends/",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_friend_requests(self, access_token: str, /) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            "Social/Friends/Requests",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def accept_friend_request(self, access_token: str, /, member_id: int) -> None:
        await self._request(
            _POST,
            f"Social/Friends/Requests/Accept/{member_id}",
            auth=access_token,
        )

    async def send_friend_request(self, access_token: str, /, member_id: int) -> None:
        await self._request(
            _POST,
            f"Social/Friends/Add/{member_id}",
            auth=access_token,
        )

    async def decline_friend_request(
        self, access_token: str, /, member_id: int
    ) -> None:
        await self._request(
            _POST,
            f"Social/Friends/Requests/Decline/{member_id}",
            auth=access_token,
        )

    async def remove_friend(self, access_token: str, /, member_id: int) -> None:
        await self._request(
            _POST,
            f"Social/Friends/Remove/{member_id}",
            auth=access_token,
        )

    async def remove_friend_request(self, access_token: str, /, member_id: int) -> None:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        await self._request(
            _POST,
            f"Social/Friends/Requests/Remove/{member_id}",
            auth=access_token,
        )

    async def approve_all_pending_group_users(
        self,
        access_token: str,
        /,
        group_id: int,
        message: str | None = None,
    ) -> None:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        await self._request(
            _POST,
            f"GroupV2/{group_id}/Members/ApproveAll",
            auth=access_token,
            json={"message": str(message)},
        )

    async def deny_all_pending_group_users(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        message: str | None = None,
    ) -> None:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        await self._request(
            _POST,
            f"GroupV2/{group_id}/Members/DenyAll",
            auth=access_token,
            json={"message": str(message)},
        )

    async def add_optional_conversation(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        name: str | None = None,
        security: typing.Literal[0, 1] = 0,
    ) -> None:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        payload = {"chatName": str(name), "chatSecurity": security}
        await self._request(
            _POST,
            f"GroupV2/{group_id}/OptionalConversations/Add",
            json=payload,
            auth=access_token,
        )

    async def edit_optional_conversation(
        self,
        access_token: str,
        /,
        group_id: int,
        conversation_id: int,
        *,
        name: str | None = None,
        security: typing.Literal[0, 1] = 0,
        enable_chat: bool = False,
    ) -> None:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        payload = {
            "chatEnabled": enable_chat,
            "chatName": str(name),
            "chatSecurity": security,
        }
        await self._request(
            _POST,
            f"GroupV2/{group_id}/OptionalConversations/Edit/{conversation_id}",
            json=payload,
            auth=access_token,
        )

    async def transfer_item(
        self,
        access_token: str,
        /,
        item_id: int,
        item_hash: int,
        character_id: int,
        member_type: enums.MembershipType | int,
        *,
        stack_size: int = 1,
        vault: bool = False,
    ) -> None:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        payload = {
            "characterId": character_id,
            "membershipType": int(member_type),
            "itemId": item_id,
            "itemReferenceHash": item_hash,
            "stackSize": stack_size,
            "transferToVault": vault,
        }
        await self._request(
            _POST,
            "Destiny2/Actions/Items/TransferItem",
            json=payload,
            auth=access_token,
        )

    async def pull_item(
        self,
        access_token: str,
        /,
        item_id: int,
        item_hash: int,
        character_id: int,
        member_type: enums.MembershipType | int,
        *,
        stack_size: int = 1,
        vault: bool = False,
    ) -> None:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        payload = {
            "characterId": character_id,
            "membershipType": int(member_type),
            "itemId": item_id,
            "itemReferenceHash": item_hash,
            "stackSize": stack_size,
        }
        await self._request(
            _POST,
            "Destiny2/Actions/Items/PullFromPostmaster",
            json=payload,
            auth=access_token,
        )
        if vault:
            await self.transfer_item(
                access_token,
                item_id=item_id,
                item_hash=item_hash,
                character_id=character_id,
                member_type=member_type,
                stack_size=stack_size,
                vault=True,
            )

    @helpers.unstable
    async def fetch_fireteams(
        self,
        activity_type: fireteams.FireteamActivity | int,
        *,
        platform: fireteams.FireteamPlatform | int = fireteams.FireteamPlatform.ANY,
        language: fireteams.FireteamLanguage | str = fireteams.FireteamLanguage.ALL,
        date_range: fireteams.FireteamDate | int = fireteams.FireteamDate.ALL,
        page: int = 0,
        slots_filter: int = 0,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Fireteam/Search/Available/{int(platform)}/{int(activity_type)}/{int(date_range)}/{slots_filter}/{page}/?langFilter={str(language)}",  # noqa: E501 Line too long
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_available_clan_fireteams(
        self,
        access_token: str,
        group_id: int,
        activity_type: fireteams.FireteamActivity | int,
        *,
        platform: fireteams.FireteamPlatform | int,
        language: fireteams.FireteamLanguage | str,
        date_range: fireteams.FireteamDate | int = fireteams.FireteamDate.ALL,
        page: int = 0,
        public_only: bool = False,
        slots_filter: int = 0,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Fireteam/Clan/{group_id}/Available/{int(platform)}/{int(activity_type)}/{int(date_range)}/{slots_filter}/{public_only}/{page}",  # noqa: E501
            json={"langFilter": str(language)},
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_clan_fireteam(
        self, access_token: str, fireteam_id: int, group_id: int
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Fireteam/Clan/{group_id}/Summary/{fireteam_id}",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_my_clan_fireteams(
        self,
        access_token: str,
        group_id: int,
        *,
        include_closed: bool = True,
        platform: fireteams.FireteamPlatform | int,
        language: fireteams.FireteamLanguage | str,
        filtered: bool = True,
        page: int = 0,
    ) -> typedefs.JSONObject:
        payload = {"groupFilter": filtered, "langFilter": str(language)}

        resp = await self._request(
            _GET,
            f"Fireteam/Clan/{group_id}/My/{int(platform)}/{include_closed}/{page}",
            json=payload,
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_private_clan_fireteams(
        self, access_token: str, group_id: int, /
    ) -> int:
        resp = await self._request(
            _GET,
            f"Fireteam/Clan/{group_id}/ActiveCount",
            auth=access_token,
        )
        assert isinstance(resp, int)
        return resp

    async def fetch_post_activity(self, instance_id: int, /) -> typedefs.JSONObject:
        resp = await self._request(
            _GET, f"Destiny2/Stats/PostGameCarnageReport/{instance_id}"
        )
        assert isinstance(resp, dict)
        return resp

    @helpers.unstable
    async def search_entities(
        self, name: str, entity_type: str, *, page: int = 0
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Destiny2/Armory/Search/{entity_type}/{name}/",
            json={"page": page},
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_unique_weapon_history(
        self,
        membership_id: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Destiny2/{int(membership_type)}/Account/{membership_id}/Character/{character_id}/Stats/UniqueWeapons/",
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_item(
        self,
        member_id: int,
        item_id: int,
        membership_type: enums.MembershipType | int,
        components: collections.Sequence[enums.ComponentType],
    ) -> typedefs.JSONObject:
        collector = _collect_components(components)

        resp = await self._request(
            _GET,
            f"Destiny2/{int(membership_type)}/Profile/{member_id}/Item/{item_id}/?components={collector}",
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_clan_weekly_rewards(self, clan_id: int, /) -> typedefs.JSONObject:
        resp = await self._request(_GET, f"Destiny2/Clan/{clan_id}/WeeklyRewardState/")
        assert isinstance(resp, dict)
        return resp

    async def fetch_available_locales(self) -> typedefs.JSONObject:
        resp = await self._request(_GET, "Destiny2/Manifest/DestinyLocaleDefinition/")
        assert isinstance(resp, dict)
        return resp

    async def fetch_common_settings(self) -> typedefs.JSONObject:
        resp = await self._request(_GET, "Settings")
        assert isinstance(resp, dict)
        return resp

    async def fetch_user_systems_overrides(self) -> typedefs.JSONObject:
        resp = await self._request(_GET, "UserSystemOverrides")
        assert isinstance(resp, dict)
        return resp

    async def fetch_global_alerts(
        self, *, include_streaming: bool = False
    ) -> typedefs.JSONArray:
        resp = await self._request(
            _GET, f"GlobalAlerts/?includestreaming={include_streaming}"
        )
        assert isinstance(resp, list)
        return resp

    async def awainitialize_request(
        self,
        access_token: str,
        type: typing.Literal[0, 1],
        membership_type: enums.MembershipType | int,
        /,
        *,
        affected_item_id: int | None = None,
        character_id: int | None = None,
    ) -> typedefs.JSONObject:
        body = {"type": type, "membershipType": int(membership_type)}

        if affected_item_id is not None:
            body["affectedItemId"] = affected_item_id

        if character_id is not None:
            body["characterId"] = character_id

        resp = await self._request(
            _POST, "Destiny2/Awa/Initialize", json=body, auth=access_token
        )
        assert isinstance(resp, dict)
        return resp

    async def awaget_action_token(
        self, access_token: str, correlation_id: str, /
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _POST,
            f"Destiny2/Awa/GetActionToken/{correlation_id}",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def awa_provide_authorization_result(
        self,
        access_token: str,
        selection: int,
        correlation_id: str,
        nonce: collections.MutableSequence[str | bytes],
    ) -> int:
        body = {"selection": selection, "correlationId": correlation_id, "nonce": nonce}

        resp = await self._request(
            _POST,
            "Destiny2/Awa/AwaProvideAuthorizationResult",
            json=body,
            auth=access_token,
        )
        assert isinstance(resp, int)
        return resp

    async def fetch_vendors(
        self,
        access_token: str,
        character_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
        /,
        components: collections.Sequence[enums.ComponentType],
        filter: int | None = None,
    ) -> typedefs.JSONObject:
        components_ = _collect_components(components)
        route = (
            f"Destiny2/{int(membership_type)}/Profile/{membership_id}"
            f"/Character/{character_id}/Vendors/?components={components_}"
        )

        if filter is not None:
            route = route + f"&filter={filter}"

        resp = await self._request(
            _GET,
            route,
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_vendor(
        self,
        access_token: str,
        character_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
        vendor_hash: int,
        /,
        components: collections.Sequence[enums.ComponentType],
    ) -> typedefs.JSONObject:
        components_ = _collect_components(components)
        resp = await self._request(
            _GET,
            (
                f"Destiny2/{int(membership_type)}/Profile/{membership_id}"
                f"/Character/{character_id}/Vendors/{vendor_hash}/?components={components_}"
            ),
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_application_api_usage(
        self,
        access_token: str,
        application_id: int,
        /,
        *,
        start: datetime.datetime | None = None,
        end: datetime.datetime | None = None,
    ) -> typedefs.JSONObject:
        end_date, start_date = time.parse_date_range(end, start)
        resp = await self._request(
            _GET,
            f"App/ApiUsage/{application_id}/?end={end_date}&start={start_date}",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_bungie_applications(self) -> typedefs.JSONArray:
        resp = await self._request(_GET, "App/FirstParty")
        assert isinstance(resp, list)
        return resp

    async def fetch_content_type(self, type: str, /) -> typedefs.JSONObject:
        resp = await self._request(_GET, f"Content/GetContentType/{type}/")
        assert isinstance(resp, dict)
        return resp

    async def fetch_content_by_id(
        self, id: int, locale: str, /, *, head: bool = False
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Content/GetContentById/{id}/{locale}/",
            json={"head": head},
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_content_by_tag_and_type(
        self, locale: str, tag: str, type: str, *, head: bool = False
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Content/GetContentByTagAndType/{tag}/{type}/{locale}/",
            json={"head": head},
        )
        assert isinstance(resp, dict)
        return resp

    async def search_content_with_text(
        self,
        locale: str,
        /,
        content_type: str,
        search_text: str,
        tag: str,
        *,
        page: int | None = None,
        source: str | None = None,
    ) -> typedefs.JSONObject:
        body: typedefs.JSONObject = {
            "locale": locale,
            "currentpage": page or 1,
            "ctype": content_type,
            "searchtxt": search_text,
            "searchtext": search_text,
            "tag": tag,
            "source": source,
        }

        resp = await self._request(_GET, "Content/Search", params=body)
        assert isinstance(resp, dict)
        return resp

    async def search_content_by_tag_and_type(
        self,
        locale: str,
        tag: str,
        type: str,
        *,
        page: int | None = None,
    ) -> typedefs.JSONObject:
        body: typedefs.JSONObject = {"currentpage": page or 1}

        resp = await self._request(
            _GET,
            f"Content/SearchContentByTagAndType/{tag}/{type}/{locale}/",
            params=body,
        )
        assert isinstance(resp, dict)
        return resp

    async def search_help_articles(
        self, text: str, size: str, /
    ) -> typedefs.JSONObject:
        resp = await self._request(_GET, f"Content/SearchHelpArticles/{text}/{size}/")
        assert isinstance(resp, dict)
        return resp

    async def fetch_topics_page(
        self,
        category_filter: int,
        group: int,
        date_filter: int,
        sort: str | bytes,
        *,
        page: int | None = None,
        locales: collections.Iterable[str] | None = None,
        tag_filter: str | None = None,
    ) -> typedefs.JSONObject:
        params = {
            "locales": ",".join(locales) if locales is not None else "en",
        }
        if tag_filter:
            params["tagstring"] = tag_filter

        resp = await self._request(
            _GET,
            f"Forum/GetTopicsPaged/{page or 0}/0/{group}/{sort!s}/{date_filter}/{category_filter}/",
            params=params,
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_core_topics_page(
        self,
        category_filter: int,
        date_filter: int,
        sort: str | bytes,
        *,
        page: int | None = None,
        locales: collections.Iterable[str] | None = None,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Forum/GetCoreTopicsPaged/{page or 0}"
            f"/{sort!s}/{date_filter}/{category_filter}/?locales={','.join(locales) if locales else 'en'}",
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_posts_threaded_page(
        self,
        parent_post: bool,
        page: int,
        page_size: int,
        parent_post_id: int,
        reply_size: int,
        root_thread_mode: bool,
        sort_mode: int,
        show_banned: str | None = None,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Forum/GetPostsThreadedPaged/{parent_post}/{page}/"
            f"{page_size}/{reply_size}/{parent_post_id}/{root_thread_mode}/{sort_mode}/",
            json={"showbanned": show_banned},
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_posts_threaded_page_from_child(
        self,
        child_id: bool,
        page: int,
        page_size: int,
        reply_size: int,
        root_thread_mode: bool,
        sort_mode: int,
        show_banned: str | None = None,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Forum/GetPostsThreadedPagedFromChild/{child_id}/"
            f"{page}/{page_size}/{reply_size}/{root_thread_mode}/{sort_mode}/",
            json={"showbanned": show_banned},
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_post_and_parent(
        self, child_id: int, /, *, show_banned: str | None = None
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Forum/GetPostAndParent/{child_id}/",
            json={"showbanned": show_banned},
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_posts_and_parent_awaiting(
        self, child_id: int, /, *, show_banned: str | None = None
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Forum/GetPostAndParentAwaitingApproval/{child_id}/",
            json={"showbanned": show_banned},
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_topic_for_content(self, content_id: int, /) -> int:
        resp = await self._request(_GET, f"Forum/GetTopicForContent/{content_id}/")
        assert isinstance(resp, int)
        return resp

    async def fetch_forum_tag_suggestions(
        self, partial_tag: str, /
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            "Forum/GetForumTagSuggestions/",
            json={"partialtag": partial_tag},
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_poll(self, topic_id: int, /) -> typedefs.JSONObject:
        resp = await self._request(_GET, f"Forum/Poll/{topic_id}/")
        assert isinstance(resp, dict)
        return resp

    async def fetch_recruitment_thread_summaries(self) -> typedefs.JSONArray:
        resp = await self._request(_POST, "Forum/Recruit/Summaries/")
        assert isinstance(resp, list)
        return resp

    async def fetch_recommended_groups(
        self,
        access_token: str,
        /,
        *,
        date_range: int = 0,
        group_type: enums.GroupType | int = enums.GroupType.CLAN,
    ) -> typedefs.JSONArray:
        resp = await self._request(
            _POST,
            f"GroupV2/Recommended/{int(group_type)}/{date_range}/",
            auth=access_token,
        )
        assert isinstance(resp, list)
        return resp

    async def fetch_available_avatars(self) -> collections.Mapping[str, int]:
        resp = await self._request(_GET, "GroupV2/GetAvailableAvatars/")
        assert isinstance(resp, dict)
        return resp

    async def fetch_user_clan_invite_setting(
        self,
        access_token: str,
        /,
        membership_type: enums.MembershipType | int,
    ) -> bool:
        resp = await self._request(
            _GET,
            f"GroupV2/GetUserClanInviteSetting/{int(membership_type)}/",
            auth=access_token,
        )
        assert isinstance(resp, bool)
        return resp

    async def fetch_banned_group_members(
        self, access_token: str, group_id: int, /, *, page: int = 1
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"GroupV2/{group_id}/Banned/?currentpage={page}",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_pending_group_memberships(
        self, access_token: str, group_id: int, /, *, current_page: int = 1
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"GroupV2/{group_id}/Members/Pending/?currentpage={current_page}",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_invited_group_memberships(
        self, access_token: str, group_id: int, /, *, current_page: int = 1
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"GroupV2/{group_id}/Members/InvitedIndividuals/?currentpage={current_page}",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def invite_member_to_group(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
        *,
        message: str | None = None,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _POST,
            f"GroupV2/{group_id}/Members/IndividualInvite/{int(membership_type)}/{membership_id}/",
            auth=access_token,
            json={"message": str(message)},
        )
        assert isinstance(resp, dict)
        return resp

    async def cancel_group_member_invite(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _POST,
            f"GroupV2/{group_id}/Members/IndividualInviteCancel/{int(membership_type)}/{membership_id}/",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_historical_definition(self) -> typedefs.JSONObject:
        resp = await self._request(_GET, "Destiny2/Stats/Definition/")
        assert isinstance(resp, dict)
        return resp

    async def fetch_historical_stats(
        self,
        character_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
        day_start: datetime.datetime,
        day_end: datetime.datetime,
        groups: collections.Sequence[enums.StatsGroupType | int],
        modes: collections.Sequence[enums.GameMode | int],
        *,
        period_type: enums.PeriodType = enums.PeriodType.ALL_TIME,
    ) -> typedefs.JSONObject:
        end, start = time.parse_date_range(day_end, day_start)
        resp = await self._request(
            _GET,
            f"Destiny2/{int(membership_type)}/Account/{membership_id}/Character/{character_id}/Stats/",
            json={
                "dayend": end,
                "daystart": start,
                "groups": [str(int(group)) for group in groups],
                "modes": [str(int(mode)) for mode in modes],
                "periodType": int(period_type),
            },
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_historical_stats_for_account(
        self,
        membership_id: int,
        membership_type: enums.MembershipType | int,
        groups: collections.Sequence[enums.StatsGroupType | int],
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Destiny2/{int(membership_type)}/Account/{membership_id}/Stats/",
            json={"groups": [str(int(group)) for group in groups]},
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_aggregated_activity_stats(
        self,
        character_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
        /,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            _GET,
            f"Destiny2/{int(membership_type)}/Account/{membership_id}/"
            f"Character/{character_id}/Stats/AggregateActivityStats/",
        )
        assert isinstance(resp, dict)
        return resp

    async def equip_loadout(
        self,
        access_token: str,
        /,
        loadout_index: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> None:
        response = await self._request(
            _POST,
            "Destiny2/Actions/Loadouts/EquipLoadout/",
            json={
                "loadoutIndex": loadout_index,
                "characterId": character_id,
                "membership_type": int(membership_type),
            },
            auth=access_token,
        )
        assert isinstance(response, int)

    async def snapshot_loadout(
        self,
        access_token: str,
        /,
        loadout_index: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
        *,
        color_hash: int | None = None,
        icon_hash: int | None = None,
        name_hash: int | None = None,
    ) -> None:
        response = await self._request(
            _POST,
            "Destiny2/Actions/Loadouts/SnapshotLoadout/",
            auth=access_token,
            json={
                "colorHash": color_hash,
                "iconHash": icon_hash,
                "nameHash": name_hash,
                "loadoutIndex": loadout_index,
                "characterId": character_id,
                "membershipType": int(membership_type),
            },
        )
        assert isinstance(response, int)

    async def update_loadout(
        self,
        access_token: str,
        /,
        loadout_index: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
        *,
        color_hash: int | None = None,
        icon_hash: int | None = None,
        name_hash: int | None = None,
    ) -> None:
        response = await self._request(
            _POST,
            "Destiny2/Actions/Loadouts/UpdateLoadoutIdentifiers/",
            auth=access_token,
            json={
                "colorHash": color_hash,
                "iconHash": icon_hash,
                "nameHash": name_hash,
                "loadoutIndex": loadout_index,
                "characterId": character_id,
                "membershipType": int(membership_type),
            },
        )
        assert isinstance(response, int)

    async def clear_loadout(
        self,
        access_token: str,
        /,
        loadout_index: int,
        character_id: int,
        membership_type: enums.MembershipType | int,
    ) -> None:
        response = await self._request(
            _POST,
            "Destiny2/Actions/Loadouts/ClearLoadout/",
            json={
                "loadoutIndex": loadout_index,
                "characterId": character_id,
                "membership_type": int(membership_type),
            },
            auth=access_token,
        )
        assert isinstance(response, int)

    async def force_drops_repair(self, access_token: str, /) -> bool:
        response = await self._request(
            _POST, "Tokens/Partner/ForceDropsRepair/", auth=access_token
        )
        assert isinstance(response, bool)
        return response

    async def claim_partner_offer(
        self,
        access_token: str,
        /,
        *,
        offer_id: str,
        bungie_membership_id: int,
        transaction_id: str,
    ) -> bool:
        response = await self._request(
            _POST,
            "Tokens/Partner/ClaimOffer/",
            json={
                "PartnerOfferId": offer_id,
                "BungieNetMembershipId": bungie_membership_id,
                "TransactionId": transaction_id,
            },
            auth=access_token,
        )
        assert isinstance(response, bool)
        return response

    async def fetch_bungie_rewards_for_user(
        self, access_token: str, /, membership_id: int
    ) -> typedefs.JSONObject:
        response = await self._request(
            _GET,
            f"Tokens/Rewards/GetRewardsForUser/{membership_id}/",
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def fetch_bungie_rewards_for_platform(
        self,
        access_token: str,
        /,
        membership_id: int,
        membership_type: enums.MembershipType | int,
    ) -> typedefs.JSONObject:
        response = await self._request(
            _GET,
            f"Tokens/Rewards/GetRewardsForPlatformUser/{membership_id}/{int(membership_type)}",
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def fetch_bungie_rewards(self) -> typedefs.JSONObject:
        response = await self._request(_GET, "Tokens/Rewards/BungieRewards/")
        assert isinstance(response, dict)
        return response

    async def fetch_fireteam_listing(self, listing_id: int) -> typedefs.JSONObject:
        response = await self._request(_GET, f"FireteamFinder/Listing/{listing_id}/")
        assert isinstance(response, dict)
        return response
