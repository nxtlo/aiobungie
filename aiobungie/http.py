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

__all__ = ("HTTPClient",)

from typing import TYPE_CHECKING, Any, Coroutine, Final, Optional, TypeVar

import aiohttp

from . import url
from .error import ClanNotFound, HTTPException, NotFound
from .internal import helpers
from .internal.enums import Class, Component, GameMode, MembershipType

if TYPE_CHECKING:
    from .types import character, profile

    T = TypeVar("T")
    Response = Coroutine[Any, Any, T]

import asyncio
import logging

log: Final[logging.Logger] = logging.getLogger(__name__)
log.setLevel("DEBUG")


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

    async def fetch(
        self,
        method: str,
        route: str,
        base: bool = False,
        type: str = "json",
        **kwargs: Any,
    ) -> Any:

        if (token := self.key) is not None:
            kwargs["headers"] = {"X-API-KEY": token}
        else:
            raise ValueError("No API KEY was passed.")

        for tries in range(5):
            try:
                async with aiohttp.ClientSession(
                    loop=self.loop, connector=self.connector
                ) as session:
                    async with session.request(
                        method=method,
                        url=f"{url.REST_EP if not base else url.BASE}/{route}",
                        **kwargs,
                    ) as response:

                        if 300 > response.status >= 200:
                            if (
                                type == "read"
                            ):  # We want to read the bytes for the manifest response.
                                return await response.read()

                            data = await response.json()
                            log.debug(
                                "{} Request success from {} with status {}".format(
                                    method, f"{url.REST_EP}/{route}", data["Message"]
                                )
                            )
                            try:
                                return data[
                                    "Response"
                                ]  # Almost all bungie json objects are
                                # wrapped inside a dict[Response=...], but
                                # sometimes it returns a List so this check
                                # is needed
                            except (AttributeError, TypeError):
                                return data

                        if response.status in {500, 502}:
                            if data["ErrorStatus"] == "ClanNotFound":  # type: ignore
                                raise ClanNotFound(
                                    "The clan you're looking for was not found."
                                )
                            log.error(
                                f"Error making the request: code {response.status}, {data['Message']}"  # type: ignore
                            )
                            await asyncio.sleep(tries + 1 * 2)
                            continue

            except aiohttp.ContentTypeError:
                if response.status == 404:
                    raise NotFound(
                        "Method {} from {} returned {}".format(
                            response.method, response.url, response.status
                        )
                    )
                else:
                    raise HTTPException(data, response)  # type: ignore

            except aiohttp.ClientError:
                raise

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
    ) -> Response[character.CharacterImpl]:
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
        self, memberid: int, type: MembershipType, *, component: Component
    ) -> Response[profile.ProfileImpl]:
        return self.fetch(
            "GET",
            f"Destiny2/{int(type)}/Profile/{int(memberid)}/?components={int(component)}",
        )
