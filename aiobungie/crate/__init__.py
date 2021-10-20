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

"""Basic implementations of aiobungie client crates.

These crates are used to organize the flow and how things stracture
for functional usage for the Bungie API objects.
"""


from __future__ import annotations

__all__ = (
    "Application",
    "PostActivity",
    "Clan",
    "Character",
    "Activity",
    "User",
    "ClanMember",
    "ApplicationOwner",
    "Profile",
    "InventoryEntity",
    "Entity",
    "HardLinkedMembership",
    "Friend",
    "UserThemes",
    "DestinyUser",
    "BungieUser",
    "ClanFeatures",
    "ClanAdmin",
    "GroupMember",
    "PartialBungieUser",
    "ProfileComponent",
    "CharacterComponent",
    "LinkedProfile",
    "ClanBanner",
    "Milestone",
    "MilestoneItems",
    "FriendRequestView",
)

from .activity import Activity
from .activity import PostActivity
from .application import Application
from .application import ApplicationOwner
from .character import Character
from .character import CharacterComponent
from .clans import Clan
from .clans import ClanAdmin
from .clans import ClanBanner
from .clans import ClanFeatures
from .clans import ClanMember
from .clans import GroupMember
from .entity import Entity
from .entity import InventoryEntity
from .friends import Friend
from .friends import FriendRequestView
from .milestones import Milestone
from .milestones import MilestoneItems
from .profile import LinkedProfile
from .profile import Profile
from .profile import ProfileComponent
from .user import BungieUser
from .user import DestinyUser
from .user import HardLinkedMembership
from .user import PartialBungieUser
from .user import User
from .user import UserThemes
