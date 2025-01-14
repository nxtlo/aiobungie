# MIT License
# ruff: noqa: F405
# ruff: noqa: F403
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

"""aiobungie crates are a collections of dataclasses which represents a fetched result from the API, specifically using `aiobungie.Client`.

This client uses the standard `aiobungie.Framework` entity framework which deserializes raw JSON payloads into a `crate`, aka a `dataclass` respectively.
"""

from __future__ import annotations

__all__ = (
    # activity.py
    "Activity",
    "PostActivity",
    "ActivityValues",
    "ExtendedValues",
    "ExtendedWeaponValues",
    "PostActivityPlayer",
    "PostActivityTeam",
    "AvailableActivity",
    "Rewards",
    "Challenges",
    "Matchmaking",
    "GuidedGame",
    "Location",
    "CharacterActivity",
    "AggregatedActivity",
    "AggregatedActivityValues",
    # application.py
    "Application",
    # character.py
    "Character",
    "Loadout",
    "LoadoutItem",
    "Dye",
    "MinimalEquipments",
    "RenderedData",
    "CustomizationOptions",
    "CharacterProgression",
    # clans.py
    "Clan",
    "Group",
    "ClanInfo",
    "GroupDate",
    "ClanMember",
    "ClanFeatures",
    "ClanConversation",
    "ClanBanner",
    "GroupMember",
    # components.py
    "Component",
    "CharacterComponent",
    "ProfileComponent",
    "RecordsComponent",
    "ItemsComponent",
    "VendorsComponent",
    "RecordsComponent",
    "UninstancedItemsComponent",
    "StringVariableComponent",
    "CraftablesComponent",
    # entity.py
    "InventoryEntity",
    "ActivityEntity",
    "PlaylistActivityEntity",
    "ObjectiveEntity",
    "SearchableEntity",
    "ActivityEntity",
    "PlaylistActivityEntity",
    # fireteams.py
    "Fireteam",
    "AvailableFireteam",
    "FireteamUser",
    "FireteamMember",
    "FireteamPartySettings",
    "FireteamPartyMember",
    "FireteamPartyCurrentActivity",
    "FireteamParty",
    # friends.py
    "Friend",
    "FriendRequestView",
    # milestones.py
    "MilestoneContent",
    "MilestoneItems",
    "Milestone",
    "MilestoneActivity",
    "MilestoneQuest",
    "MilestoneVendor",
    "MilestoneActivityPhase",
    "QuestStatus",
    "MilestoneReward",
    "MilestoneRewardEntry",
    # profile.py
    "Profile",
    "LinkedProfile",
    "ProfileProgression",
    "ProfileItemImpl",
    # progressions.py
    "Progression",
    "Factions",
    # records.py
    "Objective",
    "Record",
    "CharacterRecord",
    "RecordScores",
    "Node",
    # season.py
    "Artifact",
    "ArtifactTier",
    "ArtifactTierItem",
    "CharacterScopedArtifact",
    # user.py
    "User",
    "Unique",
    "HardLinkedMembership",
    "UserThemes",
    "BungieUser",
    "PartialBungieUser",
    "DestinyMembership",
    "UserCredentials",
    "SearchableDestinyUser",
    # items.py
    "ItemPerk",
    "ItemInstance",
    "ItemEnergy",
    "ItemStatsView",
    "PlugItemState",
    "ItemSocket",
    "ItemPerk",
    "Collectible",
    "Currency",
)

from .activity import *
from .application import *
from .character import *
from .clans import *
from .components import *
from .entity import *
from .fireteams import *
from .friends import *
from .items import *
from .milestones import *
from .profile import *
from .progressions import *
from .records import *
from .season import *
from .user import *
