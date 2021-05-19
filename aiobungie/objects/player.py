'''
MIT License

Copyright (c) 2020 - Present nxtlo

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

from typing import Optional, Sequence, List, Union
from ..utils import MembershipType as mbs, ImageProtocol
from ..error import PlayerNotFound

class Player:
    __slots__ = ("response",)
    def __init__(self, data) -> None:
        self.response = data.get("Response")

    @property
    def icon(self) -> Optional[Union[ImageProtocol, str]]:
        for item in self.response:
            return ImageProtocol(item['iconPath'])

    @property
    def name(self) -> Optional[str]:
        for item in self.response:
            return item['displayName']

    @property
    def type(self) -> Optional[mbs]:
        for item in self.response:
            try:
                _type = item['membershipType']
                if _type == mbs.NONE:
                    _type = None
                elif _type == mbs.XBOX:
                    _type = 'Xbox'
                elif _type == mbs.BLIZZARD:
                    _type = 'Blizzard'
                elif _type == mbs.PSN:
                    _type = 'PSN'
                elif _type == mbs.STEAM:
                    _type = 'Steam'
                else:
                    _type = mbs.ALL
                return _type
            except UnboundLocalError:
                _type = None
                return None

    @property
    def id(self) -> Optional[List[int]]:
        return [item['membershipId'] for item in self.response]
