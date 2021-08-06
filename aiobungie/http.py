# MIT License
#
# Copyright (c) 2020 = Present nxtlo
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

"""An HTTPClient for sending requests to the Bungie API
and Where all the magic happenes.
"""

from __future__ import annotations

import types
import typing

__all__ = ("HTTPClient",)

import http
from typing import (
    TYPE_CHECKING,
    Any,
    Coroutine,
    Final,
    NoReturn,
    Optional,
    TypeVar,
    Union,
    final,
)

import aiohttp

from . import error, url
from .internal import helpers
from .internal.enums import Class, Component, GameMode, MembershipType

if TYPE_CHECKING:
    T = TypeVar("T")
    Response = Coroutine[Any, Any, T]

import asyncio
import logging

_LOG: Final[logging.Logger] = logging.getLogger("aiobungie.http")


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
        ext_type: Optional[BaseException],
        exc: Optional[BaseException],
        exc_tb: Optional[types.TracebackType],
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
        connector: Optional[aiohttp.BaseConnector] = None,
        *,
        loop: asyncio.AbstractEventLoop = None,
    ) -> None:
        self.key: str = key
        self.connector = connector
        self.loop = loop or asyncio.get_event_loop()

    @final
    async def fetch(
        self,
        method: str,
        route: str,
        base: bool = False,
        type: str = "json",
        **kwargs: Any,
    ) -> Any:

        locker = asyncio.Lock()
        if isinstance(self.key, str) and self.key is not None:
            kwargs["headers"] = {"X-API-KEY": self.key}
        else:
            raise ValueError("No API KEY was passed.")

        if "json" in kwargs:
            kwargs["Content-Type"] = "application/json"

        while 1:
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

                                _LOG.info(
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
                                await asyncio.sleep(0x05)
                                continue

                            await self._handle_err(response, msg)

                except aiohttp.ContentTypeError:
                    return await response.text(encoding="utf-8")

                except aiohttp.ClientError:
                    raise

    @staticmethod
    @final
    async def _handle_err(response: aiohttp.ClientResponse, msg: str) -> NoReturn:
        raise await handle_errors(response, msg)

    # Currently some of the funcs return Response[Any]
    # And not the actual type, The reason for that Character
    # And Activity objects are much complicated, so that'l
    # take Some time, but for Manifest and static search will
    # not return any types. So they will be Any.

    def fetch_user(self, name: str) -> Response[helpers.JsonList]:
        return self.fetch("GET", f"User/SearchUsers/?q={name}")

    def fetch_user_from_id(self, id: int) -> Response[helpers.JsonDict]:
        return self.fetch("GET", f"User/GetBungieNetUserById/{id}/")

    def fetch_manifest(self) -> Response[Any]:
        return self.fetch("GET", "Destiny2/Manifest/")

    def static_search(self, path: str) -> Response[Any]:
        return self.fetch("GET", path)

    def fetch_player(
        self, name: str, type: MembershipType
    ) -> Response[helpers.JsonDict]:
        return self.fetch("GET", f"Destiny2/SearchDestinyPlayer/{int(type)}/{name}")

    def fetch_clan_from_id(self, id: int) -> Response[helpers.JsonDict]:
        return self.fetch("GET", f"GroupV2/{id}")

    def fetch_clan(self, name: str, type: int = 1) -> Response[helpers.JsonDict]:
        return self.fetch("GET", f"GroupV2/Name/{name}/{type}")

    def fetch_app(self, appid: int, /) -> Response[helpers.JsonDict]:
        return self.fetch("GET", f"App/Application/{appid}")

    def fetch_character(
        self, memberid: int, type: MembershipType, character: Class
    ) -> Response[helpers.JsonDict]:
        return self.fetch(
            "GET",
            f"Destiny2/{int(type)}/Profile/{memberid}/?components={int(Component.CHARECTERS)}",
        )

    def fetch_activity(
        self,
        userid: int,
        charid: int,
        mode: GameMode,
        memtype: MembershipType,
        *,
        page: Optional[int] = 1,
        limit: Optional[int] = 1,
    ) -> Response[Any]:
        return self.fetch(
            "GET",
            f"Destiny2/{int(memtype)}/Account/ \
            {userid}/Character/{charid}/Stats/ \
            Activities/?page={page}&count={limit} \
            &mode={int(mode)}",
        )

    def fetch_vendor_sales(self) -> Response[Any]:
        return self.fetch(
            "GET", f"Destiny2/Vendors/?components={int(Component.VENDOR_SALES)}"
        )

    def fetch_profile(
        self, memberid: int, type: MembershipType, /
    ) -> Response[helpers.JsonDict]:
        return self.fetch(
            "GET",
            f"Destiny2/{int(type)}/Profile/{int(memberid)}/?components={int(Component.PROFILE)}",
        )

    def fetch_entity(self, type: str, hash: int) -> Response[helpers.JsonDict]:
        return self.fetch("GET", route=f"Destiny2/Manifest/{type}/{hash}")
