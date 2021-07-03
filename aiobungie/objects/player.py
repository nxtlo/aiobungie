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

from typing import Optional, Sequence, List, Union, Dict, Any, TYPE_CHECKING
from ..error import PlayerNotFound

# if TYPE_CHECKING:
from ..types.player import Player as PlayerPayload
from ..utils.enums import MembershipType
from ..utils import ImageProtocol

class Player:
    __slots__: Sequence[str] = (
        'icon', 'id', 'name', 'type', 'is_public'
    )
    if TYPE_CHECKING:
        icon: ImageProtocol
        id: int
        name: str
        is_public: bool
        type: Union[MembershipType, int]

    def __init__(self, data: PlayerPayload) -> None:
        self._update(data)

    def _update(self, data: PlayerPayload) -> None:
        new_data = data['Response'][0]
        self.is_public: bool = new_data['isPublic']
        self.icon: ImageProtocol = ImageProtocol(str(new_data['iconPath']))
        self.id: Optional[int] = new_data['membershipId']
        self.type: Union[MembershipType, int] = MembershipType(data=new_data['membershipType'])
        self.name: str = new_data['displayName']

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return (
            f'Player name={self.name} id={self.id}'
            f' type={self.type} icon={self.icon} is_public={self.is_public}'
        )

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Player) and other.id == self.id

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.id)

    def __int__(self) -> int:
        return int(self.id)