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

"""A basic REST only client to interact with Bungie's REST API."""

from __future__ import annotations

__all__: tuple[str, ...] = ("RESTClient",)

import asyncio
import http
import logging
import sys
import types
import typing
from urllib.parse import quote

import aiohttp

from aiobungie import _info as info
from aiobungie import error
from aiobungie import interfaces
from aiobungie import url
from aiobungie.internal import enums
from aiobungie.internal import helpers

ResponseSigT = typing.TypeVar("ResponseSigT")
"""The type of the response signature."""

ResponseSig = typing.Coroutine[typing.Any, typing.Any, ResponseSigT]
"""A type hint for a general coro method that returns a type
that's mostly going to be on of `aiobungie.internal.helpers.JsonObject`
or `aiobungie.internal.helpers.JsonArray`
"""

_LOG: typing.Final[logging.Logger] = logging.getLogger("aiobungie.rest")


async def handle_errors(
    response: aiohttp.ClientResponse, msg: str, long: str
) -> error.AiobungieError:
    from_json = await response.json()
    data = [str(response.real_url), from_json, msg]

    if response.status == http.HTTPStatus.NOT_FOUND:
        return error.NotFound(*data)
    elif response.status == http.HTTPStatus.FORBIDDEN:
        return error.Forbidden(*data)
    elif response.status == http.HTTPStatus.UNAUTHORIZED:
        return error.Unauthorized(*data)

    status = http.HTTPStatus(response.status)
    why = [msg, long]

    if 400 <= status < 500:
        return error.ResponseError(*data, status)
    elif 500 <= status < 600:
        # High order errors.
        if msg == "ClanNotFound":
            return error.ClanNotFound(*why)
        elif msg == "NotFound":
            return error.NotFound(*why)
        elif msg == "DestinyInvalidMembershipType":
            return error.MembershipTypeError(*why)
        elif msg == "GroupNotFound":
            return error.ClanNotFound(*why)
        elif msg == "UserCannotFindRequestedUser":
            return error.UserNotFound(*why)
        else:
            return error.AiobungieError(*why)
    else:
        return error.HTTPException(*why)


class PreLock:
    __slots__ = ("_lock",)

    def __init__(self) -> None:
        self._lock = asyncio.Lock()

    async def __aenter__(self) -> None:
        await self.acquire()

    async def __aexit__(
        self,
        _: typing.Optional[BaseException],
        __: typing.Optional[BaseException],
        ___: typing.Optional[types.TracebackType],
    ) -> None:
        self._lock.release()

    async def acquire(self) -> None:
        if not self._lock.locked():
            await self._lock.acquire()


class RESTClient(interfaces.RESTInterface):
    """A REST only client implementation for interacting with Bungie's REST API.

    Attributes
    ----------
    token : `builtins.str`
        A valid application token from Bungie's developer portal.
    """

    __slots__: typing.Sequence[str] = ("_token", "_kwargs")

    def __init__(self, token: str, /, **kwargs: typing.Any) -> None:
        self._kwargs = kwargs
        self._token: str = token

    @typing.final
    async def _fetch(
        self,
        method: str,
        route: str,
        base: bool = False,
        type: typing.Literal["json", "read"] = "json",
        **kwargs: typing.Any,
    ) -> typing.Any:

        user_agent: typing.Final[
            str
        ] = f"AiobungieClient/{info.__version__} ({info.__url__}) Python/{sys.version_info}"

        if isinstance(self._token, str) and self._token is not None:
            kwargs["headers"] = headers = {}
            headers["X-API-KEY"] = self._token
            headers["User-Agent"] = user_agent
        else:
            raise ValueError("No API KEY was passed.")

        while True:
            async with PreLock():
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.request(
                            method=method,
                            url=f"{url.REST_EP if base is False else url.BASE}/{route}",
                            **kwargs,
                        ) as response:

                            data = await response.json()
                            msg: str = data["ErrorStatus"]

                            # There's no point of making requests here.
                            # A VERY LITTLE amount of endpoints does not
                            # require the API to be up and running, Which are
                            # The themes afaik. Not making any difference though so
                            # Just to be careful we raise this here.

                            if msg == "SystemDisabled":
                                raise OSError("API IS DOWN!", data["Message"])

                            if 300 > response.status >= 200:
                                if type == "read":
                                    # We want to read the bytes for the manifest response.
                                    data = await response.read()
                                    return data

                                _LOG.debug(
                                    "{} Request success from {} with status {}".format(
                                        method,
                                        f"{url.REST_EP}/{route}",
                                        response.status,
                                    )
                                )
                                try:
                                    return data["Response"]

                                # In case we didn't find the Response key
                                # its safer to just return the data.
                                except KeyError:
                                    return data

                            await self._handle_err(response, msg, data["Message"])

                except aiohttp.ContentTypeError:
                    raise error.HTTPException(
                        f"Expected json content but got {response.content_type=}, {response.real_url=!r}"
                    ) from None

    @staticmethod
    @typing.final
    async def _handle_err(
        response: aiohttp.ClientResponse, msg: str, long: str
    ) -> typing.NoReturn:
        raise await handle_errors(response, msg, long)

    def fetch_user(self, id: int) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._fetch("GET", f"User/GetBungieNetUserById/{id}/")

    def fetch_user_themes(self) -> ResponseSig[helpers.JsonArray]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._fetch("GET", "User/GetAvailableThemes/")

    def fetch_membership_from_id(
        self, id: int, type: enums.MembershipType = enums.MembershipType.NONE, /
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._fetch("GET", f"User/GetMembershipsById/{id}/{type}")

    def static_search(self, path: str, **kwargs: typing.Any) -> ResponseSig[typing.Any]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._fetch("GET", path, **kwargs)

    def fetch_player(
        self, name: str, type: enums.MembershipType = enums.MembershipType.ALL, /
    ) -> ResponseSig[helpers.JsonArray]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._fetch(
            "GET", f"Destiny2/SearchDestinyPlayer/{int(type)}/{quote(name)}/"
        )

    def search_users(self, name: str, /) -> ResponseSig[helpers.JsonArray]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._fetch("GET", f"User/Search/Prefix/{name}/0")

    def fetch_clan_from_id(self, id: int) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._fetch("GET", f"GroupV2/{id}")

    def fetch_clan(
        self, name: str, type: enums.GroupType = enums.GroupType.CLAN
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._fetch("GET", f"GroupV2/Name/{name}/{int(type)}")

    def fetch_clan_conversations(
        self, clan_id: int, /
    ) -> ResponseSig[helpers.JsonArray]:
        return self._fetch("GET", f"GroupV2/{clan_id}/OptionalConversations/")

    def fetch_app(self, appid: int, /) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._fetch("GET", f"App/Application/{appid}")

    def fetch_character(
        self, memberid: int, type: enums.MembershipType, /
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._fetch(
            "GET",
            f"Destiny2/{int(type)}/Profile/{memberid}/?components={int(enums.Component.CHARACTERS)}",
        )

    def fetch_activity(
        self,
        member_id: int,
        character_id: int,
        mode: enums.GameMode,
        membership_type: enums.MembershipType,
        *,
        page: typing.Optional[int] = 0,
        limit: typing.Optional[int] = 1,
    ) -> ResponseSig[typing.Any]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._fetch(
            "GET",
            f"Destiny2/{int(membership_type)}/Account/"
            f"{member_id}/Character/{character_id}/Stats/Activities"
            f"/?mode={int(mode)}&count={limit}&page={page}",
        )

    def fetch_post_activity(self, instance: int, /) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        # return self._fetch("GET", f"Destiny2/Stats/PostGameCarnageReport/{instance}")
        raise NotImplementedError

    def fetch_vendor_sales(self) -> ResponseSig[typing.Any]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._fetch(
            "GET", f"Destiny2/Vendors/?components={int(enums.Component.VENDOR_SALES)}"
        )

    def fetch_profile(
        self, memberid: int, type: enums.MembershipType, /
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._fetch(
            "GET",
            f"Destiny2/{int(type)}/Profile/{int(memberid)}/?components={int(enums.Component.PROFILE)}",
        )

    def fetch_entity(self, type: str, hash: int) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._fetch("GET", route=f"Destiny2/Manifest/{type}/{hash}")

    def fetch_inventory_item(self, hash: int) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self.fetch_entity("DestinyInventoryItemDefinition", hash)

    def fetch_clan_members(
        self,
        id: int,
        type: enums.MembershipType = enums.MembershipType.NONE,
        name: typing.Optional[str] = None,
        /,
    ) -> ResponseSig[helpers.JsonArray]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._fetch(
            "GET",
            f"/GroupV2/{id}/Members/?memberType={int(type)}&nameSearch={name if name else ''}&currentpage=1",
        )

    def fetch_hard_linked(
        self,
        credential: int,
        type: enums.CredentialType = enums.CredentialType.STADIAID,
        /,
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._fetch(
            "GET",
            f"User/GetMembershipFromHardLinkedCredential/{int(type)}/{credential}/",
        )

    async def fetch_manifest_path(self) -> str:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        request = await self._fetch("GET", "Destiny2/Manifest")
        return request["mobileWorldContentPaths"]["en"]

    async def fetch_manifest(self) -> bytes:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        content = await self.fetch_manifest_path()
        resp = await self._fetch("GET", content, type="read", base=True)
        return resp
