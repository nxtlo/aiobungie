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

"""Basic aiobungie objects implementation."""


from __future__ import annotations

__all__: Seq[str] = [
    "Application",
    "Clan",
    "Player",
    "Character",
    "CharacterComponent",
    "Activity",
    "User",
    "ClanOwner",
    "ClanMember",
    "ApplicationOwner",
    "Profile",
    "InventoryEntity",
    "UserLike",
    "ProfileComponentImpl",
    "Entity",
]

from typing import Sequence as Seq

from .activity import Activity
from .application import Application
from .application import ApplicationOwner
from .character import Character
from .character import CharacterComponent
from .clans import Clan
from .clans import ClanMember
from .clans import ClanOwner
from .entity import Entity
from .entity import InventoryEntity
from .player import Player
from .profile import Profile
from .profile import ProfileComponentImpl
from .user import User
from .user import UserLike
