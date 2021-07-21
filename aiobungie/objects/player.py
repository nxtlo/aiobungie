# MIT License
#
# Copyright (c) 2020 - Present nxtlo
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

"""Basic implementation for a Bungie a player."""


from __future__ import annotations

__all__: Sequence[str] = ["Player"]

from typing import TYPE_CHECKING, Any, Dict, Optional, Sequence, Union
from ..error import PlayerNotFound
from ..internal import Image
from ..internal.enums import MembershipType

if TYPE_CHECKING:
    from ..types.player import PlayerImpl


class Player:
    """Represents a Bungie Destiny 2 Players.

    Attributes
    ----------
    icon: `aiobungie.internal.Image`
        The player's icon.
    id: `builtins.int`
        The player's id.
    name: `builtins.str`
        The player's name.
    is_public: `builtins.bool`
        A boolean True if the user's profile is public and False if not.
    type: `aiobungie.internal.enums.MembershipType`
        The player's membership type.
    """

    __slots__: Sequence[str] = (
        "icon",
        "id",
        "name",
        "type",
        "is_public",
    )

    icon: Image
    id: int
    name: str
    is_public: bool
    type: Union[MembershipType, int]

    def __init__(self, data: PlayerImpl, *, position: int = None) -> None:
        self._update(data, position=position)

    def as_dict(self) -> Dict[str, Any]:
        """Returns a dict object of the player,
        This function is useful if you're binding to other REST apis.
        """
        return dict(
            id=self.id,
            name=self.name,
            is_public=self.is_public,
            icon=self.icon,
            type=self.type,
        )

    def _update(self, data: PlayerImpl, *, position: int = None) -> None:
        try:
            data = data[0] if not position else data[position]  # type: ignore
        except IndexError:
            return data[0]  # type: ignore
        self.is_public = data["isPublic"]
        self.icon = Image(str(data["iconPath"]))
        self.id = data["membershipId"]
        self.type = MembershipType(data["membershipType"])
        self.name = data["displayName"]

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return (
            f"Player name={self.name} id={self.id}"
            f" type={self.type} icon={self.icon} is_public={self.is_public}"
        )

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Player) and other.id == self.id

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.id)

    def __int__(self) -> int:
        return int(self.id)
