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

__all__: tuple[str, ...] = ("RESTClient", "RequestMethod")

import asyncio
import contextlib
import http
import logging
import platform
import random
import sys
import typing
from urllib import parse

import aiohttp
import attr

from aiobungie import _info as info
from aiobungie import error
from aiobungie import interfaces
from aiobungie import typedefs
from aiobungie import undefined
from aiobungie import url
from aiobungie.crate import fireteams
from aiobungie.internal import _backoff as backoff
from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    import types

    from aiohttp import typedefs as aiohttp_typedefs

    ResponseSigT = typing.TypeVar(
        "ResponseSigT",
        covariant=True,
        bound=typing.Union[typedefs.JsonArray, typedefs.JsonObject, int, None],
    )
    """The signature of the response."""

    ResponseSig = typing.Coroutine[typing.Any, typing.Any, ResponseSigT]
    """A type hint for a general coro method that returns a type
    that's mostly going to be on of `aiobungie.typedefs.JsonObject`
    or `aiobungie.typedefs.JsonArray`
    """

_LOG: typing.Final[logging.Logger] = logging.getLogger("aiobungie.rest")
_APP_JSON: typing.Final[str] = "application/json"
_RETRY_5XX: typing.Final[set[int]] = {500, 502, 503, 504}
_AUTH_HEADER: typing.Final[str] = sys.intern("Authorization")
_USER_AGENT_HEADERS: typing.Final[str] = sys.intern("User-Agent")
_USER_AGENT: typing.Final[str] = f"AiobungieClient/{info.__version__}"
f" ({info.__url__}) {platform.python_implementation()}/{platform.python_version()}"
f"Aiohttp/{aiohttp.HttpVersion11}"


async def handle_errors(
    response: aiohttp.ClientResponse, msg: typing.Optional[str] = None
) -> error.AiobungieError:

    if response.content_type != _APP_JSON:
        return error.HTTPException(
            f"Expected json content but got {response.content_type}, {str(response.real_url)}"
        )

    from_json = await response.json()
    data = [str(response.real_url), from_json, msg]

    if response.status == http.HTTPStatus.NOT_FOUND:
        return error.NotFound(*data)
    elif response.status == http.HTTPStatus.FORBIDDEN:
        return error.Forbidden(*data)
    elif response.status == http.HTTPStatus.UNAUTHORIZED:
        return error.Unauthorized(*data)

    status = http.HTTPStatus(response.status)

    if 400 <= status < 500:
        return error.ResponseError(*data, status)

    # For some WEIRD reason bungie doesn't follow the http
    # error codes protocol and almost return 5xx on any failed request
    # except very few. The only way currently to handle this is by their
    # custom error codes.
    # https://github.com/Bungie-net/api/issues/1542
    elif 500 <= status < 600:
        # No API key or method requires OAuth2 most likely.
        if msg in {
            "ApiKeyMissingFromRequest",
            "WebAuthRequired",
            "ApiInvalidOrExpiredKey",
            "AuthenticationInvalid",
        }:
            return error.Unauthorized(
                message=str(msg),
                long_message=from_json.get("Message", ""),
                url=str(response.real_url),
            )

        # API is down...
        elif msg == "SystemDisabled":
            raise OSError(*data)

        # Anything contains not found.
        elif msg and "NotFound" in msg or "UserCannotFindRequestedUser" == msg:
            return error.NotFound(*data)

        # Membership need to be alone.
        elif msg == "DestinyInvalidMembershipType":
            return error.MembershipTypeError(*data)

        # Any other messages.
        else:
            return error.InternalServerError(
                message=str(msg), long_message=from_json.get("Message", "")
            )
    # Not 5xx.
    else:
        return error.HTTPException(*data)


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
        if not self._lock.locked():
            await self._lock.acquire()


@attr.define()
class _Session:
    client_session: aiohttp.ClientSession = attr.field()

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
        # This currently set like this due to a bug.
        await self.client_session.close()
        await asyncio.sleep(0.025)


class RequestMethod(str, enums.Enum):
    """Request methods enum."""

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


class RESTClient(interfaces.RESTInterface):
    """A REST only client implementation for interacting with Bungie's REST API.

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

    Attributes
    ----------
    token : `builtins.str`
        A valid application token from Bungie's developer portal.
    max_retries : `builtins.int`
        The max retries number to retry if the request hit a `5xx` status code.
    """

    __slots__ = ("_token", "_session", "_max_retries")

    def __init__(self, token: str, /, *, max_retries: int = 4) -> None:
        self._session: typing.Optional[_Session] = None
        self._token: str = token
        self._max_retries = max_retries

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
            with contextlib.suppress(aiohttp.ClientError):
                await self._session.close()

    @typing.final
    async def _request(
        self,
        method: typing.Union[RequestMethod, str],
        route: aiohttp_typedefs.StrOrURL,
        base: bool = False,
        auth: typing.Optional[str] = None,
        type: typing.Literal["json", "read"] = "json",
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

        stack = contextlib.AsyncExitStack()
        while True:
            try:
                async with stack:
                    async with _Arc():

                        # We make the request here.
                        response = await stack.enter_async_context(
                            await self._acquire_session().client_session.request(
                                method=method,
                                url=f"{url.REST_EP if base is False else url.BASE}/{route}",
                                **kwargs,
                            )
                        )

                        await self._handle_ratelimit(response, method, str(route))

                        if response.status == http.HTTPStatus.NO_CONTENT:
                            return None

                        data = await response.json(encoding="utf-8")
                        if 300 > response.status >= 200:
                            if type == "read":
                                # We want to read the bytes for the manifest response.
                                data = await response.read()
                                return data

                            _LOG.debug(
                                "%s Request success from %s with status %i",
                                method,
                                f"{url.REST_EP}/{route}",
                                response.status,
                            )

                            if response.content_type == _APP_JSON:
                                try:
                                    return data["Response"]

                                # In case we didn't find the Response key
                                # its safer to just return the data.
                                except KeyError:
                                    _LOG.warning(
                                        "Couldn't return the response key, Data: %s",
                                        data,
                                    )
                                    return data

                        if (
                            response.status in _RETRY_5XX
                            and retries < self._max_retries  # noqa: W503
                        ):
                            backoff_ = backoff.ExponentialBackOff(maximum=6)
                            sleep_time = next(backoff_)
                            _LOG.warning(
                                f"Received: {response.status}, "
                                f"Message: {data['Message']}, "
                                f"sleeping for {sleep_time}, "
                                f"Remaining retries: {self._max_retries - retries}"
                            )

                            retries += 1
                            await asyncio.sleep(sleep_time)
                            continue

                        await self._handle_err(response, data["ErrorStatus"])

            except RuntimeError:
                continue

    if not typing.TYPE_CHECKING:

        def __enter__(self) -> typing.NoReturn:
            cls = type(self)
            raise TypeError(
                f"{cls.__qualname__} is async only, use async-with instead."
            )

        def __exit__(
            self,
            exception_type: typing.Optional[type[BaseException]],
            exception: typing.Optional[BaseException],
            exception_traceback: typing.Optional[types.TracebackType],
        ) -> None:
            return None

    async def __aexit__(
        self,
        exception_type: typing.Optional[type[BaseException]],
        exception: typing.Optional[BaseException],
        exception_traceback: typing.Optional[types.TracebackType],
    ) -> None:
        if self._session:
            await self._session.close()
        return None

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
            _LOG.error(
                f"we're being ratelmited on non JSON request, {response.content_type}."
            )
            raise RuntimeError

        json = await response.json()
        retry_after = json["ThrottleSeconds"]
        if retry_after == 0:
            # Can't really do anything about this.
            sleep_time = float((retry_after + random.randint(0, 3)))
        _LOG.warning(
            "We're being ratelimited with method %s route %s. Sleeping for %f:,",
            method,
            route,
            sleep_time,
        )
        await asyncio.sleep(sleep_time)
        raise error.RateLimitedError(
            retry_after=retry_after,
            headers=response.headers,
            url=str(response.real_url),
            json=json,
        )

    @staticmethod
    @typing.final
    async def _handle_err(
        response: aiohttp.ClientResponse, msg: typing.Optional[str] = None
    ) -> typing.NoReturn:
        raise await handle_errors(response, msg)

    def static_request(
        self,
        method: typing.Union[RequestMethod, str],
        path: aiohttp_typedefs.StrOrURL,
        auth: typing.Optional[str] = None,
        **kwargs: typing.Any,
    ) -> ResponseSig[typing.Any]:
        return self._request(method, path, auth=auth, **kwargs)

    def fetch_user(self, id: int) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, f"User/GetBungieNetUserById/{id}/")

    def fetch_user_themes(self) -> ResponseSig[typedefs.JsonArray]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, "User/GetAvailableThemes/")

    def fetch_membership_from_id(
        self,
        id: int,
        type: typedefs.IntAnd[enums.MembershipType] = enums.MembershipType.NONE,
        /,
    ) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET, f"User/GetMembershipsById/{id}/{int(type)}"
        )

    def fetch_player(
        self,
        name: str,
        type: typedefs.IntAnd[enums.MembershipType] = enums.MembershipType.ALL,
        /,
    ) -> ResponseSig[typedefs.JsonArray]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"Destiny2/SearchDestinyPlayer/{int(type)}/{parse.quote(name)}/",
        )

    def search_users(self, name: str, /) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, f"User/Search/Prefix/{name}/0")

    def fetch_clan_from_id(self, id: int, /) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, f"GroupV2/{id}")

    def fetch_clan(
        self,
        name: str,
        /,
        type: typedefs.IntAnd[enums.GroupType] = enums.GroupType.CLAN,
    ) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, f"GroupV2/Name/{name}/{int(type)}")

    def fetch_clan_admins(self, clan_id: int, /) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, f"GroupV2/{clan_id}/AdminsAndFounder/")

    def fetch_clan_conversations(
        self, clan_id: int, /
    ) -> ResponseSig[typedefs.JsonArray]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET, f"GroupV2/{clan_id}/OptionalConversations/"
        )

    def fetch_app(self, appid: int, /) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, f"App/Application/{appid}")

    def fetch_character(
        self, memberid: int, type: typedefs.IntAnd[enums.MembershipType], /
    ) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"Destiny2/{int(type)}/Profile/{memberid}/?components={int(enums.Component.CHARACTERS)}",
        )

    def fetch_activity(
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
            f"Destiny2/Vendors/?components={int(enums.Component.VENDOR_SALES)}",
        )

    def fetch_profile(
        self, memberid: int, type: typedefs.IntAnd[enums.MembershipType], /
    ) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"Destiny2/{int(type)}/Profile/{int(memberid)}/?components={int(enums.Component.PROFILE)}",
        )

    def fetch_entity(self, type: str, hash: int) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET, route=f"Destiny2/Manifest/{type}/{hash}"
        )

    def fetch_inventory_item(self, hash: int, /) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self.fetch_entity("DestinyInventoryItemDefinition", hash)

    def fetch_groups_for_member(
        self,
        member_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
        /,
        *,
        filter: int = 0,
        group_type: typedefs.IntAnd[enums.GroupType] = enums.GroupType.CLAN,
    ) -> ResponseSig[typedefs.JsonObject]:
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
    ) -> ResponseSig[typedefs.JsonObject]:
        return self._request(
            RequestMethod.GET,
            f"GroupV2/User/Potential/{int(member_type)}/{member_id}/{filter}/{int(group_type)}/",
        )

    def fetch_clan_members(
        self,
        id: int,
        type: typedefs.IntAnd[enums.MembershipType] = enums.MembershipType.NONE,
        name: typing.Optional[str] = None,
        /,
    ) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"/GroupV2/{id}/Members/?memberType={int(type)}&nameSearch={name if name else ''}&currentpage=1",
        )

    def fetch_hard_linked(
        self,
        credential: int,
        type: typedefs.IntAnd[enums.CredentialType] = enums.CredentialType.STADIAID,
        /,
    ) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"User/GetMembershipFromHardLinkedCredential/{int(type)}/{credential}/",
        )

    async def fetch_manifest_path(self) -> str:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        request = await self._request(RequestMethod.GET, "Destiny2/Manifest")
        return str(request["mobileWorldContentPaths"]["en"])

    async def fetch_manifest(self) -> bytes:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        content = await self.fetch_manifest_path()
        resp = await self._request(RequestMethod.GET, content, type="read", base=True)
        return bytes(resp)

    def fetch_linked_profiles(
        self,
        member_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
        /,
        *,
        all: bool = False,
    ) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            f"Destiny2/{int(member_type)}/Profile/{member_id}/LinkedProfiles/?getAllMemberships={all}",
        )

    def fetch_clan_banners(self) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, "Destiny2/Clan/ClanBannerDictionary/")

    def fetch_public_milestones(self) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(RequestMethod.GET, "Destiny2/Milestones/")

    def fetch_public_milestone_content(
        self, milestone_hash: int, /
    ) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET, f"Destiny2/Milestones/{milestone_hash}/Content/"
        )

    def fetch_own_bungie_user(
        self, access_token: str, /
    ) -> ResponseSig[typedefs.JsonObject]:
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
    ) -> ResponseSig[typedefs.JsonObject]:
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
        tags: typedefs.NoneOr[typing.Sequence[str]] = None,
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

    def fetch_friends(self, access_token: str, /) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            RequestMethod.GET,
            "Social/Friends/",
            auth=access_token,
        )

    def fetch_friend_requests(
        self, access_token: str, /
    ) -> ResponseSig[typedefs.JsonObject]:
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
    ) -> ResponseSig[typedefs.JsonObject]:
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
    ) -> ResponseSig[typedefs.JsonObject]:
        return self._request(
            RequestMethod.GET,
            f"Fireteam/Clan/{group_id}/Available/{int(platform)}/{int(activity_type)}/{int(date_range)}/{slots_filter}/{public_only}/{page}",  # noqa: E501
            json={"langFilter": str(language)},
            auth=access_token,
        )

    def fetch_clan_fireteam(
        self, access_token: str, fireteam_id: int, group_id: int
    ) -> ResponseSig[typedefs.JsonObject]:
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
    ) -> ResponseSig[typedefs.JsonObject]:
        payload = {"groupFilter": filtered, "langFilter": str(language)}
        return self._request(
            RequestMethod.GET,
            f"Fireteam/Clan/{group_id}/My/{int(platform)}/{include_closed}/{page}",
            json=payload,
            auth=access_token,
        )

    def fetch_private_clan_fireteams(
        self, access_token: str, group_id: int, /
    ) -> ResponseSig[int]:
        return self._request(
            RequestMethod.GET,
            f"Fireteam/Clan/{group_id}/ActiveCount",
            auth=access_token,
        )

    # * Not implemented yet.

    def fetch_item(
        self, member_id: int, item_id: int, /
    ) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        raise NotImplementedError

    def fetch_clan_weekly_rewards(
        self, clan_id: int, /
    ) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        raise NotImplementedError

    def fetch_weapon_history(
        self,
        character_id: int,
        member_id: int,
        member_type: typedefs.IntAnd[enums.MembershipType],
    ) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        raise NotImplementedError

    def fetch_post_activity(self, instance: int, /) -> ResponseSig[typedefs.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        # return self._request(RequestMethod.GET, f"Destiny2/Stats/PostGameCarnageReport/{instance}")
        raise NotImplementedError
