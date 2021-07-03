'''
MIT License

Copyright (c) 2020 = Present nxtlo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import httpx
from .error import JsonError
from typing import Optional, Sequence, Any, Union, TYPE_CHECKING, TypeVar, Coroutine
from .types import player, clans
from .utils.enums import MembershipType

# if TYPE_CHECKING:
T = TypeVar('T')
Response = Coroutine[Any, Any, T]

__all__ = (
    'HTTPClient',
)
class HTTPClient:
    BASE: str = 'https://www.bungie.net/Platform'
    __slots__: Sequence[str] = ('session', 'key')

    def __init__(self, key: str, session = None) -> None:
        self.session: httpx.AsyncClient = session
        self.key  = key

    async def create_session(self) -> None:
        """Creates a new aiohttp Client Session"""
        self.session = httpx.AsyncClient()

    async def close(self) -> None:
        if not self.session.is_closed:
            try:
                return await self.session.aclose()
            except httpx.CloseError:
                raise
            self.session = None

    async def fetch(self, url: str) -> Any:
        if not self.session:
            await self.create_session()

        async with self.session as client:
            data = await client.get(url, headers={'X-API-KEY': self.key})
            if data.status_code == 200:
                try:
                    data = data.json()
                except httpx.DecodingError as e:
                    raise JsonError(f'Falied decoding json, See: {e!r}') from e
            return data

    def get_player(self, name: str, type: Union[MembershipType, int]) -> Response[player.Player]:
        return self.fetch(f'{self.BASE}/Destiny2/SearchDestinyPlayer/{type}/{name}')

    def get_clan(self, id: int) -> Response[clans.Clan]:
        return self.fetch(f'{self.BASE}/GroupV2/{id}')