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
from typing import Optional, Sequence, Dict, List, Union

class HTTPClient:
    __slots__: Sequence[str] = ('session', 'key')

    def __init__(self, key, session = None) -> None:
        self.session: httpx.AsyncClient = session
        self.key: Optional[str] = key

    async def create_session(self) -> Optional[httpx.AsyncClient]:
        """Creates a new aiohttp Client Session"""
        self.session = httpx.AsyncClient()

    async def close(self) -> None:
        if not self.session.is_closed:
            try:
                await self.session.aclose()
            except httpx.CloseError:
                raise
            self.session = None

    async def fetch(self ,url: str) -> Optional[httpx.Request]:
        if not self.session:
            await self.create_session()

        async with self.session as client:
            data = await client.get(url, headers={'X-API-KEY': self.key})
            if data.status_code == 200:
                try:
                    return data.json()
                except httpx.DecodingError:
                    return data.text
