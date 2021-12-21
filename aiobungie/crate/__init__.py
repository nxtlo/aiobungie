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

__all__: tuple[str, ...] = (
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
    "ProfileProgression",
    "ProfileComponent",
    "CharacterComponent",
    "LinkedProfile",
    "ClanBanner",
    "FriendRequestView",
    "Fireteam",
    "FireteamMember",
    "FireteamUser",
    "AvalaibleFireteam",
    "Component",
    "ComponentFields",
    "ComponentPrivacy",
    "Artifact",
    "ArtifactTier",
    "ArtifactTierItem",
    "CharacterScopedArtifact",
    "CharacterProgression",
    "ProfileItem",
    "ProfileItemImpl",
    "Record",
    "CharacterRecord",
    "Objective",
    "ObjectiveEntity",
    "BaseEntity",
    "AvailableActivity",
    "Location",
    "Rewards",
    "GuidedGame",
    "Challenges",
    "Matchmaking",
    "ActivityEntity",
    "PlaylistActivityEntity",
    "RecordScores",
    "MilestoneContent",
    "MilestoneItems",
    "Milestone",
    "MilestoneReward",
    "MilestoneRewardEntry",
    "MilestoneActivity",
    "MilestoneQuest",
    "MilestoneVendor",
    "MilestoneActivityPhase",
    "QuestStatus",
    "Progression",
    "Factions",
    "ArtifactTier",
    "ArtifactTierItem",
    "CharacterScopedArtifact",
    "CharacterComponent",
    "ProfileComponent",
    "RecordsComponent",
    "ItemsComponent",
    "VendorsComponent",
    "ActivityValues",
    "PostActivityPlayer",
    "PostActivityTeam",
    "ExtendedValues",
    "ExtendedWeaponValues",
    "UserCredentials",
    "SearchableEntity",
)

from .activity import Activity
from .activity import ActivityValues
from .activity import AvailableActivity
from .activity import Challenges
from .activity import ExtendedValues
from .activity import ExtendedWeaponValues
from .activity import GuidedGame
from .activity import Location
from .activity import Matchmaking
from .activity import PostActivity
from .activity import PostActivityPlayer
from .activity import PostActivityTeam
from .activity import Rewards
from .application import *
from .character import *
from .clans import *
from .components import *
from .entity import ActivityEntity
from .entity import BaseEntity
from .entity import Entity
from .entity import InventoryEntity
from .entity import ObjectiveEntity
from .entity import PlaylistActivityEntity
from .entity import SearchableEntity
from .fireteams import AvalaibleFireteam
from .fireteams import Fireteam
from .fireteams import FireteamMember
from .fireteams import FireteamUser
from .friends import *
from .milestones import *
from .profile import *
from .progressions import *
from .records import CharacterRecord
from .records import Objective
from .records import Record
from .records import RecordScores
from .season import *
from .user import *
