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

'''An HTTPClient for sending requests to the Bungie API
and Where all the magic happenes.
'''

from __future__ import annotations

__all__ = (
    'HTTPClient',
)

import aiohttp
from .error import NotFound, HTTPException, JsonError, ClanNotFound
from typing import (Optional
    , Any
    , Union
    , TypeVar
    , Coroutine
    , Dict
    , List
    , Final
    , TYPE_CHECKING
)

from .utils.enums import Component
if TYPE_CHECKING:
    from .types import player, clans, user, application as app
    from .utils.enums import MembershipType, DestinyClass, GameMode
    T = TypeVar('T')
    Response = Coroutine[Any, Any, T]

import logging
import warnings
import asyncio

log: Final[logging.Logger] = logging.getLogger(__name__)


class HTTPClient:
    """An HTTP Client for sending http requests to the Bungie API"""
    BASE: str = 'https://www.bungie.net/Platform'

    def __init__(self, key: str) -> None:
        self.key: str = key
        self.headers: Dict[str, str] = {'X-API-KEY': self.key} # had to do it this way due to Auth.

    async def fetch(self, method: str, route: str, **kwargs: Any) -> Any:
        if self.key is None:
            raise ValueError("No API KEY was passed.") 

        for tries in range(5):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.request(method=method, url=f'{self.BASE}/{route}', **kwargs) as response:
                        data = await response.json()

                        if 300 > response.status >= 200:
                            log.debug("{} Request success from {} with {}".format(method, self.BASE + route, data))
                            try:
                                return data['Response'] # Almost all bungie json objects are
                                                        # wrapped inside a dict[Response=...], but
                                                        # sometimes it returns a List so this check
                                                        # is needed
                            except (AttributeError, TypeError):
                                return data
                        
                        if response.status in {500, 502}:
                            if data['ErrorStatus'] == 'ClanNotFound':
                                raise ClanNotFound("The clan you're looking for was not found.")
                            warnings.warn("Got {} status {} Msg {}".format(data, response.status, data['Message']))
                            await asyncio.sleep(tries + 1 * 2)
                            continue

                        if response.status == 404:
                            raise NotFound(response, data)

            except aiohttp.ContentTypeError:
                text: str = await response.text()
                raise JsonError(f"Couldn't return json object: {text}")
        
            except aiohttp.ClientError:
                raise
    
    # Currently some of the funcs return Response[Any]
    # And not the actual type, The reason for that Character
    # And Activity objects are much complicated, so that'l
    # take Some time, but for Manifest and static search will
    # not return any types. So they will be Any.

    def fetch_user(self, name: str) -> Response[user.User]:
        return self.fetch('GET', f'User/SearchUsers/?q={name}', headers=self.headers)

    def fetch_user_from_id(self, id: int) -> Response[user.User]:
        return self.fetch("GET", f'User/GetBungieNetUserById/{id}/', headers=self.headers)

    def fetch_manifest(self) -> Response[Any]:
        return self.fetch('GET', 'Destin2/Manifest', headers=self.headers)

    def static_search(self, path: str) -> Response[Any]:
        return self.fetch('GET', path, headers=self.headers)

    def fetch_player(self, name: str, type: Union[MembershipType, int]) -> Response[player.Player]:
        return self.fetch('GET', f'Destiny2/SearchDestinyPlayer/{type}/{name}', headers=self.headers)

    def fetch_clan_from_id(self, id: int) -> Response[clans.Clan]:
        return self.fetch('GET' ,f'GroupV2/{id}', headers=self.headers)

    def fetch_clan(self, name: str, type: int = 1) -> Response[clans.Clan]:
        return self.fetch('GET', f'GroupV2/Name/{name}/{type}', headers=self.headers)

    def fetch_app(self, appid: int, /) -> Response[app.Application]:
        return self.fetch('GET' ,f'App/Application/{appid}', headers=self.headers)

    def fetch_character(self, 
            memberid: int, 
            type: MembershipType, 
            character: DestinyClass
            ) -> Response[Any]:
        return self.fetch('GET', 
                        f'Destiny2/{type.value}/Profile/{memberid}/ \
                          ?components={int(Component.CHARECTERS)}',
                          headers=self.headers
                        )

    def fetch_activity(
        self, 
        userid: int, 
        charid: int, 
        mode: Union[GameMode, int], 
        memtype: Union[int, MembershipType], 
        *,
        page: Optional[int] = 1, 
        limit: Optional[int] = 1
        ) -> Response[Any]:
        return self.fetch('GET', 
            f'Destiny2/{memtype}/Account/ \
            {userid}/Character/{charid}/Stats/ \
            Activities/?page={page}&count={limit} \
            &mode={mode}',
            headers=self.headers
        )

    def fetch_vendor_sales(self) -> Response[Any]:
        return self.fetch(
            'GET', 
            f'Destiny2/Vendors/?components={int(Component.VENDOR_SALES)}', 
            headers=self.headers)