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

__all__ = (
    "RESTClient",
    "RESTPool",
    "RequestMethod",
    "TRACE",
)

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

from aiobungie import builders
from aiobungie import error
from aiobungie import interfaces
from aiobungie import metadata
from aiobungie import typedefs
from aiobungie import url
from aiobungie.crates import fireteams
from aiobungie.internal import _backoff as backoff
from aiobungie.internal import enums
from aiobungie.internal import helpers
from aiobungie.internal import time

if typing.TYPE_CHECKING:
    import collections.abc as collections
    import types

_LOG: logging.Logger = logging.getLogger("aiobungie.rest")
_MANIFEST_LANGUAGES: typing.Final[set[str]] = {
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
_APP_JSON: str = "application/json"
_RETRY_5XX: set[int] = {500, 502, 503, 504}
_AUTH_HEADER: str = sys.intern("Authorization")
_USER_AGENT_HEADERS: str = sys.intern("User-Agent")
_USER_AGENT: str = (
    f"AiobungieClient (Author: {metadata.__author__}), "
    f"(Version: {metadata.__version__}), (URL: {metadata.__url__})"
)

TRACE: typing.Final[int] = logging.DEBUG - 5
"""The trace logging level for the `RESTClient` responses.

You can enable this with the following code

>>> import logging
>>> logging.getLogger("aiobungie.rest").setLevel(aiobungie.TRACE)
# or
>>> logging.basicConfig(level=aiobungie.TRACE)
# Or
>>> client = aiobungie.RESTClient(..., enable_debug="TRACE")
# Or if you're using `aiobungie.Client`
>>> client = aiobungie.Client(...)
>>> client.rest.enable_debugging(level=aiobungie.TRACE, file="rest_logs.txt") # optional file
"""

logging.addLevelName(TRACE, "TRACE")


def _collect_components(components: list[enums.ComponentType], /) -> str:
    collector: list[str] = []

    for component in components:
        if isinstance(component.value, tuple):
            collector.extend(str(c) for c in component.value)  # type: ignore
        else:
            collector.append(str(component.value))
    return ",".join(collector)


def _uuid() -> str:
    return uuid.uuid4().hex


def _ensure_manifest_language(language: str) -> None:
    langs = "\n".join(_MANIFEST_LANGUAGES)
    if language not in _MANIFEST_LANGUAGES:
        raise ValueError(
            f"{language} is not a valid manifest language, "
            f"valid languages are: {langs}"
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
    p = _get_path(file_name, path).open("wb")
    with p as file:
        file.write(helpers.dumps(helpers.loads(data)))


def _write_sqlite_bytes(
    data: bytes,
    path: pathlib.Path | str = "./",
    file_name: str = "manifest",
) -> None:
    try:
        with open(f"{_uuid()}.zip", "wb") as tmp:
            tmp.write(data)

        with zipfile.ZipFile(tmp.name) as zipped:
            file = zipped.namelist()

            if file:
                zipped.extractall(".")

                os.rename(file[0], _get_path(file_name, path, sql=True))
                _LOG.debug("Finished downloading manifest.")

    finally:
        pathlib.Path(tmp.name).unlink(missing_ok=True)


class _JSONPayload(aiohttp.BytesPayload):
    def __init__(
        self, value: typing.Any, dumps: typedefs.Dumps = helpers.dumps
    ) -> None:
        super().__init__(dumps(value), content_type=_APP_JSON, encoding="UTF-8")


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


class RESTPool:
    """Pool of `RESTClient` instances.

    This allows to create multiple instances of `RESTClient`s that can be acquired
    which share the same TCP connector.

    Example
    -------
    ```py
    import aiobungie

    client_pool = aiobungie.RESTPool("token", client_id=1234, client_secret='secret')

    # Using a context manager to acquire an instance
    # from the pool and close it after.
    async with client_pool.acquire() as rest:
        ...
    ```

    Parameters
    ----------
    token : `str`
        A valid application token from Bungie's developer portal.

    Other Parameters
    ----------------
    max_retries : `int`
        The max retries number to retry if the request hit a `5xx` status code.
    client_secret : `str | None`
        An optional application client secret,
        This is only needed if you're fetching OAuth2 tokens with this client.
    client_id : `int | None`
        An optional application client id,
        This is only needed if you're fetching OAuth2 tokens with this client.
    enable_debugging : `bool | str`
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
        client_session: aiohttp.ClientSession | None = None,
        dumps: typedefs.Dumps = helpers.dumps,
        loads: typedefs.Loads = helpers.loads,
        max_retries: int = 4,
        enable_debugging: typing.Literal["TRACE"] | bool | int = False,
    ) -> None:
        self._client_secret = client_secret
        self._client_id = client_id
        self._token = token
        self._max_retries = max_retries
        self._metadata: collections.MutableMapping[typing.Any, typing.Any] = {}
        self._enable_debug = enable_debugging
        self._client_session = client_session
        self._loads = loads
        self._dumps = dumps

    @property
    def client_id(self) -> int | None:
        return self._client_id

    @property
    def metadata(self) -> collections.MutableMapping[typing.Any, typing.Any]:
        """Pool's Metadata. This is different from client instance metadata."""
        return self._metadata

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
            enable_debugging=self._enable_debug,
            client_session=self._client_session,
        )


class RESTClient(interfaces.RESTInterface):
    """A RESTful client implementation for Bungie's API.

    This client is designed to only make HTTP requests and return JSON objects
    to provide RESTful functionality.

    This client is the core for `aiobungie.Client` which deserialize those returned JSON objects
    using the factory into Pythonic data classes objects which provide Python functionality.

    Example
    -------
    ```py
    import aiobungie

    client = aiobungie.RESTClient("TOKEN")
    async with client:
        response = await client.fetch_clan_members(4389205)
        for member in response['results']:
            for key, value in member['destinyUserInfo'].items():
                print(key, value)
    ```

    Parameters
    ----------
    token : `str`
        A valid application token from Bungie's developer portal.

    Other Parameters
    ----------------
    max_retries : `int`
        The max retries number to retry if the request hit a `5xx` status code.
    client_secret : `str | None`
        An optional application client secret,
        This is only needed if you're fetching OAuth2 tokens with this client.
    client_id : `int | None`
        An optional application client id,
        This is only needed if you're fetching OAuth2 tokens with this client.
    enable_debugging : `bool | str`
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
    )

    def __init__(
        self,
        token: str,
        /,
        *,
        client_secret: str | None = None,
        client_id: int | None = None,
        client_session: aiohttp.ClientSession | None = None,
        dumps: typedefs.Dumps = helpers.dumps,
        loads: typedefs.Loads = helpers.loads,
        max_retries: int = 4,
        enable_debugging: typing.Literal["TRACE"] | bool | int = False,
    ) -> None:
        self._session = client_session
        self._lock: asyncio.Lock | None = None
        self._client_secret = client_secret
        self._client_id = client_id
        self._token: str = token
        self._max_retries = max_retries
        self._dumps = dumps
        self._loads = loads
        self._metadata: collections.MutableMapping[typing.Any, typing.Any] = {}

        self._set_debug_level(enable_debugging)

    @property
    def client_id(self) -> int | None:
        return self._client_id

    @property
    def metadata(self) -> collections.MutableMapping[typing.Any, typing.Any]:
        return self._metadata

    @property
    def is_alive(self) -> bool:
        return self._session is not None

    @typing.final
    async def close(self) -> None:
        if self._session is None:
            raise RuntimeError("REST client is not running.")

        await self._session.close()
        self._session = None

    @typing.final
    def open(self) -> None:
        """Open a new client session. This is called internally with contextmanager usage."""
        if self._session:
            raise RuntimeError("Cannot open REST client when it's already open.")

        self._session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(),
            connector_owner=True,
            raise_for_status=False,
            timeout=aiohttp.ClientTimeout(total=30.0),
        )

    @typing.final
    def enable_debugging(
        self,
        level: typing.Literal["TRACE"] | bool | int = False,
        file: pathlib.Path | str | None = None,
        /,
    ) -> None:
        self._set_debug_level(level, file)

    @typing.final
    async def static_request(
        self,
        method: RequestMethod | str,
        path: str,
        *,
        auth: str | None = None,
        json: collections.Mapping[str, typing.Any] | None = None,
    ) -> typedefs.JSONIsh:
        return await self._request(method, path, auth=auth, json=json)

    @typing.final
    def build_oauth2_url(
        self, client_id: int | None = None
    ) -> builders.OAuthURL | None:
        client_id = client_id or self._client_id
        if client_id is None:
            return None

        return builders.OAuthURL(client_id=client_id)

    @staticmethod
    def _set_debug_level(
        level: typing.Literal["TRACE"] | bool | int = False,
        file: pathlib.Path | str | None = None,
    ) -> None:
        file_handler = logging.FileHandler(file, mode="w") if file else None
        if level == "TRACE" or level == TRACE:
            logging.basicConfig(
                level=TRACE, handlers=[file_handler] if file_handler else None
            )

        elif level:
            logging.basicConfig(
                level=logging.DEBUG, handlers=[file_handler] if file_handler else None
            )

    async def _request(
        self,
        method: RequestMethod | str,
        route: str,
        *,
        base: bool = False,
        oauth2: bool = False,
        auth: str | None = None,
        unwrapping: typing.Literal["json", "read"] = "json",
        json: collections.Mapping[str, typing.Any] | None = None,
        data: collections.Mapping[str, typing.Any] | None = None,
        params: collections.Mapping[str, typing.Any] | None = None,
        headers: dict[str, typing.Any] | None = None,
    ) -> typedefs.JSONIsh:
        # This is not None when opening the client.
        assert self._session is not None

        retries: int = 0
        headers = headers or {}

        headers.setdefault(_USER_AGENT_HEADERS, _USER_AGENT)
        headers["X-API-KEY"] = self._token

        if auth is not None:
            headers[_AUTH_HEADER] = f"Bearer {auth}"

        # Handling endpoints
        endpoint = url.BASE

        if not base:
            endpoint = endpoint + url.REST_EP

        if oauth2:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            endpoint = endpoint + url.TOKEN_EP

        if self._lock is None:
            self._lock = asyncio.Lock()

        if json:
            headers["Content-Type"] = _APP_JSON

        while True:
            async with (stack := contextlib.AsyncExitStack()):
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

                _LOG.debug(
                    "%s %s %s Time %.4fms",
                    method,
                    f"{endpoint}/{route}",
                    f"{response.status} {response.reason}",
                    response_time,
                )

                await self._handle_ratelimit(response, method, route)

                if response.status == http.HTTPStatus.NO_CONTENT:
                    return None

                if 300 > response.status >= 200:
                    if unwrapping == "read":
                        # We need to read the bytes for the manifest response.
                        return await response.read()

                    if response.content_type == _APP_JSON:
                        # json_data = self._loads(await response.read())
                        json_data = self._loads(await response.read())

                        _LOG.debug(
                            "%s %s %s Time %.4fms",
                            method,
                            f"{endpoint}/{route}",
                            f"{response.status} {response.reason}",
                            response_time,
                        )

                        if _LOG.isEnabledFor(TRACE):
                            cloned = headers.copy()
                            cloned.update(response.headers)  # type: ignore

                            _LOG.log(
                                TRACE,
                                "%s",
                                error.stringify_http_message(cloned),
                            )

                        # Return the response.
                        # oauth2 responses are not packed inside a Response object.
                        if oauth2:
                            return json_data  # type: ignore[no-any-return]

                        return json_data["Response"]  # type: ignore

                if (
                    response.status in _RETRY_5XX and retries < self._max_retries  # noqa: W503
                ):
                    backoff_ = backoff.ExponentialBackOff(maximum=6)
                    sleep_time = next(backoff_)
                    _LOG.warning(
                        "Got %i - %s. Sleeping for %.2f seconds. Remaining retries: %i",
                        response.status,
                        response.reason,
                        sleep_time,
                        self._max_retries - retries,
                    )

                    retries += 1
                    await asyncio.sleep(sleep_time)
                    continue

                raise await error.raise_error(response)

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
    @typing.final
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
            _LOG.warning(
                "We're being ratelimited, Method %s Route %s. Sleeping for %.2fs.",
                method,
                route,
                retry_after,
            )
            await asyncio.sleep(retry_after)
            max_calls += 1
            continue

    async def fetch_oauth2_tokens(self, code: str, /) -> builders.OAuth2Response:
        if not isinstance(self._client_secret, (str, int)):
            raise TypeError(
                "Expected (str, int) for client secret "
                f"but got {type(self._client_secret).__name__}"  # type: ignore
            )

        headers = {
            "client_secret": self._client_secret,
        }

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }

        response = await self._request(
            RequestMethod.POST, "", headers=headers, data=data, oauth2=True
        )
        assert isinstance(response, dict)
        return builders.OAuth2Response.build_response(response)

    async def refresh_access_token(
        self, refresh_token: str, /
    ) -> builders.OAuth2Response:
        if not isinstance(self._client_secret, (int, str)):
            raise TypeError(
                f"Expected (str, int) for client secret but got {type(self._client_secret).__name__}"  # type: ignore
            )

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }

        response = await self._request(RequestMethod.POST, "", data=data, oauth2=True)
        assert isinstance(response, dict)
        return builders.OAuth2Response.build_response(response)

    async def fetch_bungie_user(self, id: int) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET, f"User/GetBungieNetUserById/{id}/"
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_user_themes(self) -> typedefs.JSONArray:
        resp = await self._request(RequestMethod.GET, "User/GetAvailableThemes/")
        assert isinstance(resp, list)
        return resp

    async def fetch_membership_from_id(
        self,
        id: int,
        type: enums.MembershipType | int = enums.MembershipType.NONE,
        /,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET, f"User/GetMembershipsById/{id}/{int(type)}"
        )
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
            RequestMethod.POST,
            f"Destiny2/SearchDestinyPlayerByBungieName/{int(type)}",
            json={"displayName": name, "displayNameCode": code},
        )
        assert isinstance(resp, list)
        return resp

    async def search_users(self, name: str, /) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.POST,
            "User/Search/GlobalName/0",
            json={"displayNamePrefix": name},
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_clan_from_id(
        self, id: int, /, access_token: str | None = None
    ) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET, f"GroupV2/{id}", auth=access_token
        )
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
            RequestMethod.GET, f"GroupV2/Name/{name}/{int(type)}", auth=access_token
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_clan_admins(self, clan_id: int, /) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET, f"GroupV2/{clan_id}/AdminsAndFounder/"
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_clan_conversations(self, clan_id: int, /) -> typedefs.JSONArray:
        resp = await self._request(
            RequestMethod.GET, f"GroupV2/{clan_id}/OptionalConversations/"
        )
        assert isinstance(resp, list)
        return resp

    async def fetch_application(self, appid: int, /) -> typedefs.JSONObject:
        resp = await self._request(RequestMethod.GET, f"App/Application/{appid}")
        assert isinstance(resp, dict)
        return resp

    async def fetch_character(
        self,
        member_id: int,
        membership_type: enums.MembershipType | int,
        character_id: int,
        components: list[enums.ComponentType],
        auth: str | None = None,
    ) -> typedefs.JSONObject:
        collector = _collect_components(components)
        response = await self._request(
            RequestMethod.GET,
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
            RequestMethod.GET,
            f"Destiny2/{int(membership_type)}/Account/"
            f"{member_id}/Character/{character_id}/Stats/Activities"
            f"/?mode={int(mode)}&count={limit}&page={page}",
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_vendor_sales(self) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET,
            f"Destiny2/Vendors/?components={int(enums.ComponentType.VENDOR_SALES)}",
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_profile(
        self,
        membership_id: int,
        type: enums.MembershipType | int,
        components: list[enums.ComponentType],
        auth: str | None = None,
    ) -> typedefs.JSONObject:
        collector = _collect_components(components)
        response = await self._request(
            RequestMethod.GET,
            f"Destiny2/{int(type)}/Profile/{membership_id}/?components={collector}",
            auth=auth,
        )
        assert isinstance(response, dict)
        return response

    async def fetch_entity(self, type: str, hash: int) -> typedefs.JSONObject:
        response = await self._request(
            RequestMethod.GET, route=f"Destiny2/Manifest/{type}/{hash}"
        )
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
            RequestMethod.GET,
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
            RequestMethod.GET,
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
            RequestMethod.GET,
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
            RequestMethod.GET,
            f"User/GetMembershipFromHardLinkedCredential/{int(type)}/{credential}/",
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_user_credentials(
        self, access_token: str, membership_id: int, /
    ) -> typedefs.JSONArray:
        resp = await self._request(
            RequestMethod.GET,
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
            RequestMethod.POST, "Destiny2/Actions/Items/InsertSocketPlug", json=body
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
            RequestMethod.POST,
            "Destiny2/Actions/Items/InsertSocketPlugFree",
            json=body,
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

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
            RequestMethod.POST,
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
            RequestMethod.POST,
            "Destiny2/Actions/Items/SetTrackedState",
            json=body,
            auth=access_token,
        )
        assert isinstance(response, int)
        return response

    async def fetch_manifest_path(self) -> typedefs.JSONObject:
        path = await self._request(RequestMethod.GET, "Destiny2/Manifest")
        assert isinstance(path, dict)
        return path

    async def read_manifest_bytes(self, language: str = "en", /) -> bytes:
        _ensure_manifest_language(language)

        content = await self.fetch_manifest_path()
        resp = await self._request(
            RequestMethod.GET,
            content["mobileWorldContentPaths"][language],
            unwrapping="read",
            base=True,
        )
        assert isinstance(resp, bytes)
        return resp

    async def download_sqlite_manifest(
        self,
        language: str = "en",
        name: str = "manifest",
        path: pathlib.Path | str = ".",
        *,
        force: bool = False,
    ) -> pathlib.Path:
        complete_path = _get_path(name, path, sql=True)

        if complete_path.exists() and force:
            if force:
                _LOG.info(
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

        _LOG.info(f"Downloading manifest. Location: {complete_path!s}")
        data_bytes = await self.read_manifest_bytes(language)
        await asyncio.get_running_loop().run_in_executor(
            None, _write_sqlite_bytes, data_bytes, path, name
        )
        return _get_path(name, path, sql=True)

    async def download_json_manifest(
        self,
        file_name: str = "manifest",
        path: str | pathlib.Path = ".",
        language: str = "en",
    ) -> pathlib.Path:
        _ensure_manifest_language(language)

        _LOG.info(f"Downloading manifest JSON to {_get_path(file_name, path)!r}...")

        content = await self.fetch_manifest_path()
        json_bytes = await self._request(
            RequestMethod.GET,
            content["jsonWorldContentPaths"][language],
            unwrapping="read",
            base=True,
        )

        await asyncio.get_running_loop().run_in_executor(
            None, _write_json_bytes, json_bytes, file_name, path
        )
        _LOG.info("Finished downloading manifest JSON.")
        return _get_path(file_name, path)

    async def fetch_manifest_version(self) -> str:
        # This is guaranteed str.
        return (await self.fetch_manifest_path())["version"]  # type: ignore[no-any-return]

    async def fetch_linked_profiles(
        self,
        member_id: int,
        member_type: enums.MembershipType | int,
        /,
        *,
        all: bool = False,
    ) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET,
            f"Destiny2/{int(member_type)}/Profile/{member_id}/LinkedProfiles/?getAllMemberships={all}",
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_clan_banners(self) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET, "Destiny2/Clan/ClanBannerDictionary/"
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_public_milestones(self) -> typedefs.JSONObject:
        resp = await self._request(RequestMethod.GET, "Destiny2/Milestones/")
        assert isinstance(resp, dict)
        return resp

    async def fetch_public_milestone_content(
        self, milestone_hash: int, /
    ) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET, f"Destiny2/Milestones/{milestone_hash}/Content/"
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_current_user_memberships(
        self, access_token: str, /
    ) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET,
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
            RequestMethod.POST,
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
            RequestMethod.POST,
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
            RequestMethod.POST,
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
            RequestMethod.POST,
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
            RequestMethod.POST,
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
            RequestMethod.POST,
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
            RequestMethod.POST,
            f"GroupV2/{group_id}/EditFounderOptions",
            json=payload,
            auth=access_token,
        )

    async def fetch_friends(self, access_token: str, /) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET,
            "Social/Friends/",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_friend_requests(self, access_token: str, /) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET,
            "Social/Friends/Requests",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def accept_friend_request(self, access_token: str, /, member_id: int) -> None:
        await self._request(
            RequestMethod.POST,
            f"Social/Friends/Requests/Accept/{member_id}",
            auth=access_token,
        )

    async def send_friend_request(self, access_token: str, /, member_id: int) -> None:
        await self._request(
            RequestMethod.POST,
            f"Social/Friends/Add/{member_id}",
            auth=access_token,
        )

    async def decline_friend_request(
        self, access_token: str, /, member_id: int
    ) -> None:
        await self._request(
            RequestMethod.POST,
            f"Social/Friends/Requests/Decline/{member_id}",
            auth=access_token,
        )

    async def remove_friend(self, access_token: str, /, member_id: int) -> None:
        await self._request(
            RequestMethod.POST,
            f"Social/Friends/Remove/{member_id}",
            auth=access_token,
        )

    async def remove_friend_request(self, access_token: str, /, member_id: int) -> None:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        await self._request(
            RequestMethod.POST,
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
            RequestMethod.POST,
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
            RequestMethod.POST,
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
            RequestMethod.POST,
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
            RequestMethod.POST,
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
            RequestMethod.POST,
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
            "transferToVault": vault,
        }
        await self._request(
            RequestMethod.POST,
            "Destiny2/Actions/Items/PullFromPostmaster",
            json=payload,
            auth=access_token,
        )

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
            RequestMethod.GET,
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
            RequestMethod.GET,
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
            RequestMethod.GET,
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
            RequestMethod.GET,
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
            RequestMethod.GET,
            f"Fireteam/Clan/{group_id}/ActiveCount",
            auth=access_token,
        )
        assert isinstance(resp, int)
        return resp

    async def fetch_post_activity(self, instance_id: int, /) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET, f"Destiny2/Stats/PostGameCarnageReport/{instance_id}"
        )
        assert isinstance(resp, dict)
        return resp

    async def search_entities(
        self, name: str, entity_type: str, *, page: int = 0
    ) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET,
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
            RequestMethod.GET,
            f"Destiny2/{int(membership_type)}/Account/{membership_id}/Character/{character_id}/Stats/UniqueWeapons/",
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_item(
        self,
        member_id: int,
        item_id: int,
        membership_type: enums.MembershipType | int,
        components: list[enums.ComponentType],
    ) -> typedefs.JSONObject:
        collector = _collect_components(components)

        resp = await self._request(
            RequestMethod.GET,
            f"Destiny2/{int(membership_type)}/Profile/{member_id}/Item/{item_id}/?components={collector}",
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_clan_weekly_rewards(self, clan_id: int, /) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET, f"Destiny2/Clan/{clan_id}/WeeklyRewardState/"
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_available_locales(self) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET, "Destiny2/Manifest/DestinyLocaleDefinition/"
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_common_settings(self) -> typedefs.JSONObject:
        resp = await self._request(RequestMethod.GET, "Settings")
        assert isinstance(resp, dict)
        return resp

    async def fetch_user_systems_overrides(self) -> typedefs.JSONObject:
        resp = await self._request(RequestMethod.GET, "UserSystemOverrides")
        assert isinstance(resp, dict)
        return resp

    async def fetch_global_alerts(
        self, *, include_streaming: bool = False
    ) -> typedefs.JSONArray:
        resp = await self._request(
            RequestMethod.GET, f"GlobalAlerts/?includestreaming={include_streaming}"
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
            RequestMethod.POST, "Destiny2/Awa/Initialize", json=body, auth=access_token
        )
        assert isinstance(resp, dict)
        return resp

    async def awaget_action_token(
        self, access_token: str, correlation_id: str, /
    ) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.POST,
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
            RequestMethod.POST,
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
        components: list[enums.ComponentType],
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
            RequestMethod.GET,
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
        components: list[enums.ComponentType],
    ) -> typedefs.JSONObject:
        components_ = _collect_components(components)
        resp = await self._request(
            RequestMethod.GET,
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
            RequestMethod.GET,
            f"App/ApiUsage/{application_id}/?end={end_date}&start={start_date}",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_bungie_applications(self) -> typedefs.JSONArray:
        resp = await self._request(RequestMethod.GET, "App/FirstParty")
        assert isinstance(resp, list)
        return resp

    async def fetch_content_type(self, type: str, /) -> typedefs.JSONObject:
        resp = await self._request(RequestMethod.GET, f"Content/GetContentType/{type}/")
        assert isinstance(resp, dict)
        return resp

    async def fetch_content_by_id(
        self, id: int, locale: str, /, *, head: bool = False
    ) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET,
            f"Content/GetContentById/{id}/{locale}/",
            json={"head": head},
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_content_by_tag_and_type(
        self, locale: str, tag: str, type: str, *, head: bool = False
    ) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET,
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
            "ctype": content_type,
            "searchtext": search_text,
            "tag": tag,
            "source": source,
        }

        resp = await self._request(RequestMethod.GET, "Content/Search", params=body)
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
            RequestMethod.GET,
            f"Content/SearchContentByTagAndType/{tag}/{type}/{locale}/",
            params=body,
        )
        assert isinstance(resp, dict)
        return resp

    async def search_help_articles(
        self, text: str, size: str, /
    ) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET, f"Content/SearchHelpArticles/{text}/{size}/"
        )
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
            RequestMethod.GET,
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
            RequestMethod.GET,
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
            RequestMethod.GET,
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
            RequestMethod.GET,
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
            RequestMethod.GET,
            f"Forum/GetPostAndParent/{child_id}/",
            json={"showbanned": show_banned},
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_posts_and_parent_awaiting(
        self, child_id: int, /, *, show_banned: str | None = None
    ) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET,
            f"Forum/GetPostAndParentAwaitingApproval/{child_id}/",
            json={"showbanned": show_banned},
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_topic_for_content(self, content_id: int, /) -> int:
        resp = await self._request(
            RequestMethod.GET, f"Forum/GetTopicForContent/{content_id}/"
        )
        assert isinstance(resp, int)
        return resp

    async def fetch_forum_tag_suggestions(
        self, partial_tag: str, /
    ) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET,
            "Forum/GetForumTagSuggestions/",
            json={"partialtag": partial_tag},
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_poll(self, topic_id: int, /) -> typedefs.JSONObject:
        resp = await self._request(RequestMethod.GET, f"Forum/Poll/{topic_id}/")
        assert isinstance(resp, dict)
        return resp

    async def fetch_recruitment_thread_summaries(self) -> typedefs.JSONArray:
        resp = await self._request(RequestMethod.POST, "Forum/Recruit/Summaries/")
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
            RequestMethod.POST,
            f"GroupV2/Recommended/{int(group_type)}/{date_range}/",
            auth=access_token,
        )
        assert isinstance(resp, list)
        return resp

    async def fetch_available_avatars(self) -> collections.Mapping[str, int]:
        resp = await self._request(RequestMethod.GET, "GroupV2/GetAvailableAvatars/")
        assert isinstance(resp, dict)
        return resp

    async def fetch_user_clan_invite_setting(
        self,
        access_token: str,
        /,
        membership_type: enums.MembershipType | int,
    ) -> bool:
        resp = await self._request(
            RequestMethod.GET,
            f"GroupV2/GetUserClanInviteSetting/{int(membership_type)}/",
            auth=access_token,
        )
        assert isinstance(resp, bool)
        return resp

    async def fetch_banned_group_members(
        self, access_token: str, group_id: int, /, *, page: int = 1
    ) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET,
            f"GroupV2/{group_id}/Banned/?currentpage={page}",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_pending_group_memberships(
        self, access_token: str, group_id: int, /, *, current_page: int = 1
    ) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET,
            f"GroupV2/{group_id}/Members/Pending/?currentpage={current_page}",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_invited_group_memberships(
        self, access_token: str, group_id: int, /, *, current_page: int = 1
    ) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET,
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
            RequestMethod.POST,
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
            RequestMethod.POST,
            f"GroupV2/{group_id}/Members/IndividualInviteCancel/{int(membership_type)}/{membership_id}/",
            auth=access_token,
        )
        assert isinstance(resp, dict)
        return resp

    async def fetch_historical_definition(self) -> typedefs.JSONObject:
        resp = await self._request(RequestMethod.GET, "Destiny2/Stats/Definition/")
        assert isinstance(resp, dict)
        return resp

    async def fetch_historical_stats(
        self,
        character_id: int,
        membership_id: int,
        membership_type: enums.MembershipType | int,
        day_start: datetime.datetime,
        day_end: datetime.datetime,
        groups: list[enums.StatsGroupType | int],
        modes: collections.Sequence[enums.GameMode | int],
        *,
        period_type: enums.PeriodType = enums.PeriodType.ALL_TIME,
    ) -> typedefs.JSONObject:
        end, start = time.parse_date_range(day_end, day_start)
        resp = await self._request(
            RequestMethod.GET,
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
        groups: list[enums.StatsGroupType | int],
    ) -> typedefs.JSONObject:
        resp = await self._request(
            RequestMethod.GET,
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
            RequestMethod.GET,
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
            RequestMethod.POST,
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
            RequestMethod.POST,
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
            RequestMethod.POST,
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
            RequestMethod.POST,
            "Destiny2/Actions/Loadouts/ClearLoadout/",
            json={
                "loadoutIndex": loadout_index,
                "characterId": character_id,
                "membership_type": int(membership_type),
            },
            auth=access_token,
        )
        assert isinstance(response, int)
