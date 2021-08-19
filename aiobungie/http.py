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

"""An HTTPClient for sending requests to the Bungie API
and Where all the magic happenes.
"""

from __future__ import annotations

from aiobungie.internal.helpers import JsonDict

__all__ = ("HTTPClient",)

import http
import types
import typing

import aiohttp

from aiobungie import error
from aiobungie import url
from aiobungie.internal import enums
from aiobungie.internal import helpers

if typing.TYPE_CHECKING:
    T = typing.TypeVar("T")
    Response = typing.Coroutine[typing.Any, typing.Any, T]

import asyncio
import logging

_LOG: typing.Final[logging.Logger] = logging.getLogger("aiobungie.http")


async def handle_errors(
    response: aiohttp.ClientResponse, msg: str
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

    if 400 <= status < 500:
        return error.ResponseError(*data, status)
    elif 500 <= status < 600:
        # High order errors
        if msg == "ClanNotFound":
            return error.ClanNotFound(msg)
        elif msg == "DestinyInvalidMembershipType":
            return error.MembershipTypeError(msg)
        elif msg == "GroupNotFound":
            return error.ClanNotFound(msg)
        else:
            return error.AiobungieError(msg)
    else:
        return error.HTTPException(msg)


class PreLock:

    __slots__: typing.Sequence[str] = ("_lock",)

    def __init__(self, locker: asyncio.Lock) -> None:
        self._lock: asyncio.Lock = locker

    async def __aenter__(self) -> None:
        await self.acquire()

    async def __aexit__(
        self,
        ext_type: typing.Optional[BaseException],
        exc: typing.Optional[BaseException],
        exc_tb: typing.Optional[types.TracebackType],
    ) -> None:
        self._lock.release()

    async def acquire(self) -> None:
        if not self._lock.locked():
            await self._lock.acquire()


class HTTPClient:
    """An HTTP Client for sending http requests to the Bungie API"""

    def __init__(
        self,
        key: str,
        connector: typing.Optional[aiohttp.BaseConnector] = None,
        *,
        loop: asyncio.AbstractEventLoop = None,
    ) -> None:
        self.key: str = key
        self.connector = connector
        self.loop = loop or asyncio.get_event_loop()

    @typing.final
    async def fetch(
        self,
        method: str,
        route: str,
        base: bool = False,
        type: str = "json",
        **kwargs: typing.Any,
    ) -> typing.Any:

        locker = asyncio.Lock()
        if isinstance(self.key, str) and self.key is not None:
            kwargs["headers"] = {"X-API-KEY": self.key}
        else:
            raise ValueError("No API KEY was passed.")

        if "json" in kwargs:
            kwargs["Content-Type"] = "application/json"

        for tries in range(5):
            async with PreLock(locker):
                try:
                    async with aiohttp.ClientSession(
                        loop=self.loop, connector=self.connector
                    ) as session:
                        async with session.request(
                            method=method,
                            url=f"{url.REST_EP if not base else url.BASE}/{route}",
                            **kwargs,
                        ) as response:

                            data = await response.json()
                            msg: str = data["ErrorStatus"]
                            if 300 > response.status >= 200:
                                if (
                                    type == "read"
                                ):  # We want to read the bytes for the manifest response.
                                    data = await response.read()
                                    return data

                                _LOG.debug(
                                    "{} Request success from {} with status {}".format(
                                        method,
                                        f"{url.REST_EP}/{route}",
                                        data["Message"],
                                    )
                                )
                                try:
                                    # Almost all bungie json objects are
                                    # wrapped inside a dict[Response=...], but
                                    # sometimes it returns a List so this check
                                    # is needed
                                    return data["Response"]
                                except KeyError:
                                    return data

                            # We continue here.
                            if response.status in {500, 502, 504}:
                                await self._handle_err(response, msg)

                                await asyncio.sleep(tries + 0x01 * 0x02)
                                continue

                except aiohttp.ContentTypeError:
                    return await response.text(encoding="utf-8")

                except aiohttp.ClientError:
                    raise

    @staticmethod
    @typing.final
    async def _handle_err(
        response: aiohttp.ClientResponse, msg: str
    ) -> typing.NoReturn:
        raise await handle_errors(response, msg)

    def fetch_user(self, name: str) -> Response[helpers.JsonList]:
        return self.fetch("GET", f"User/SearchUsers/?q={name}")

    def fetch_user_from_id(self, id: int) -> Response[helpers.JsonDict]:
        return self.fetch("GET", f"User/GetBungieNetUserById/{id}/")

    def fetch_manifest(self) -> Response[typing.Any]:
        return self.fetch("GET", "Destiny2/Manifest/")

    def static_search(self, path: str) -> Response[typing.Any]:
        return self.fetch("GET", path)

    def fetch_player(
        self, name: str, type: enums.MembershipType
    ) -> Response[helpers.JsonDict]:
        return self.fetch("GET", f"Destiny2/SearchDestinyPlayer/{int(type)}/{name}")

    def fetch_clan_from_id(self, id: int) -> Response[helpers.JsonDict]:
        return self.fetch("GET", f"GroupV2/{id}")

    def fetch_clan(self, name: str, type: int = 1) -> Response[helpers.JsonDict]:
        return self.fetch("GET", f"GroupV2/Name/{name}/{type}")

    def fetch_app(self, appid: int, /) -> Response[helpers.JsonDict]:
        return self.fetch("GET", f"App/Application/{appid}")

    def fetch_character(
        self, memberid: int, type: enums.MembershipType, character: enums.Class
    ) -> Response[helpers.JsonDict]:
        return self.fetch(
            "GET",
            f"Destiny2/{int(type)}/Profile/{memberid}/?components={int(enums.Component.CHARECTERS)}",
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
    ) -> Response[typing.Any]:
        return self.fetch(
            "GET",
            f"Destiny2/{int(membership_type)}/Account/"
            f"{member_id}/Character/{character_id}/Stats/Activities"
            f"/?mode={int(mode)}&count={limit}&page={page}",
        )

    def fetch_post_activity(self, instance: int, /) -> Response[helpers.JsonDict]:
        return self.fetch("GET", f"Destiny2/Stats/PostGameCarnageReport/{instance}")

    def fetch_vendor_sales(self) -> Response[typing.Any]:
        return self.fetch(
            "GET", f"Destiny2/Vendors/?components={int(enums.Component.VENDOR_SALES)}"
        )

    def fetch_profile(
        self, memberid: int, type: enums.MembershipType, /
    ) -> Response[helpers.JsonDict]:
        return self.fetch(
            "GET",
            f"Destiny2/{int(type)}/Profile/{int(memberid)}/?components={int(enums.Component.PROFILE)}",
        )

    def fetch_entity(self, type: str, hash: int) -> Response[helpers.JsonDict]:
        return self.fetch("GET", route=f"Destiny2/Manifest/{type}/{hash}")

    def fetch_inventory_item(self, hash: int) -> Response[helpers.JsonDict]:
        return self.fetch_entity("DestinyInventoryItemDefinition", hash)

    def fetch_clan_members(
        self,
        id: int,
        type: enums.MembershipType = enums.MembershipType.NONE,
        name: typing.Optional[str] = None,
        /,
        *,
        page: int = 1,
    ) -> Response[helpers.JsonDict]:
        return self.fetch(
            "GET",
            f"/GroupV2/{id}/Members/?memberType={int(type)}&nameSearch={name if name else ''}&currentpage={page}",
        )

    def fetch_hard_linked(
        self,
        credential: int,
        type: enums.CredentialType = enums.CredentialType.STADIAID,
        /,
    ) -> Response[JsonDict]:
        return self.fetch(
            "GET",
            f"User/GetMembershipFromHardLinkedCredential/{int(type)}/{credential}/",
        )
