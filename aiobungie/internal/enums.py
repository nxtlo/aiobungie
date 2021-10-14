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

"""Bungie enums impl for aiobungie."""


from __future__ import annotations

__all__: tuple[str, ...] = (
    "GameMode",
    "MembershipType",
    "Class",
    "MilestoneType",
    "Race",
    "Vendor",
    "Raid",
    "Dungeon",
    "Gender",
    "Component",
    "Planet",
    "Stat",
    "WeaponType",
    "DamageType",
    "Item",
    "Place",
    "ItemTier",
    "AmmoType",
    "GroupType",
    "CredentialType",
    "Presence",
    "Relationship",
    "ClanMemberType",
    "MembershipOption",
)

import enum as __enum
import typing


class IntEnum(__enum.IntEnum):
    """An int only enum."""

    def __int__(self) -> int:
        return int(self.value)

    def __str__(self) -> str:
        return self.name


class Enum(__enum.Enum):
    """An enum that can be an int or a string."""

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return int(self.value)


@typing.final
class Raid(IntEnum):
    """An Enum for all available raids in Destiny 2."""

    DSC = 910380154
    """Deep Stone Crypt"""

    LW = 2122313384
    """Last Wish"""

    VOG = 3881495763
    """Normal Valut of Glass"""

    GOS = 3458480158
    """Garden Of Salvation"""


@typing.final
class Dungeon(IntEnum):
    """An Enum for all available Dungeon/Like missions in Destiny 2."""

    NORMAL_PRESAGE = 2124066889
    """Normal Presage"""

    MASTER_PRESAGE = 4212753278
    """Master Presage"""

    HARBINGER = 1738383283
    """Harbinger"""

    PROPHECY = 4148187374
    """Prophecy"""

    MASTER_POH = 785700673
    """Master Pit of Heresy?"""

    LEGEND_POH = 785700678
    """Legend Pit of Heresy?"""

    POH = 1375089621
    """Normal Pit of Heresy."""

    SHATTERED = 2032534090
    """Shattered Throne"""


@typing.final
class Planet(IntEnum):
    """An Enum for all available planets in Destiny 2."""

    UNKNOWN = 0
    """Unknown space"""

    EARTH = 3747705955
    """Earth"""

    DREAMING_CITY = 2877881518
    """The Dreaming city."""

    NESSUS = 3526908984
    """Nessus"""

    MOON = 3325508439
    """The Moon"""

    COSMODROME = 3990611421
    """The Cosmodrome"""

    TANGLED_SHORE = 3821439926
    """The Tangled Shore"""

    VENUS = 3871070152
    """Venus"""

    EAZ = 541863059  # Exclusive event.
    """European Aerial Zone"""

    EUROPA = 1729879943
    """Europa"""


@typing.final
class Place(IntEnum):
    """An Enum for Destiny 2 Places and NOT Planets"""

    ORBIT = 2961497387
    SOCIAL = 4151112093
    LIGHT_HOUSE = 4276116472
    EXPLORE = 3497767639


@typing.final
class Vendor(IntEnum):
    """An Enum for all available vendors in Destiny 2."""

    ZAVALA = 69482069
    XUR = 2190858386
    BANSHE = 672118013
    SPIDER = 863940356
    SHAXX = 3603221665
    KADI = 529635856
    """Postmaster exo."""
    YUNA = 1796504621
    """Asia servers only."""
    EVERVERSE = 3361454721
    AMANDA = 460529231
    """Amanda holiday"""
    CROW = 3611983588
    HAWTHORNE = 3347378076
    ADA1 = 350061650
    DRIFTER = 248695599
    IKORA = 1976548992
    SAINT = 765357505
    """Saint-14"""
    ERIS_MORN = 1616085565
    SHAW_HAWN = 1816541247
    """COSMODROME Guy"""
    VARIKS = 2531198101


@typing.final
class GameMode(IntEnum):
    """An Enum for all available gamemodes in Destiny 2."""

    NONE = 0
    STORY = 2
    STRIKE = 3
    RAID = 4
    ALLPVP = 5
    PATROL = 6
    ALLPVE = 7
    TOF = 14
    """Trials Of Osiris"""
    CONTROL = 10
    NIGHTFALL = 16
    IRONBANER = 19
    ALLSTRIKES = 18
    DUNGEON = 82
    GAMBIT = 63
    EMIPIRE_HUNT = 494260690
    RUMBLE = 964120289
    CLASSIC_MIX = 1472571612
    COUNTDOWN = 3956087078
    DOUBLES = 4288302346
    CLASH = 3954711135
    MAYHEM = 3517186939
    SURVIVAL = 2175955486


@typing.final
class Component(IntEnum):
    """An Enum for Destiny 2 Components."""

    NONE = 0
    PROFILE = 100
    SILVER = 105
    PROGRESSION = 104
    INVENTORIES = 102
    CHARACTERS = 200
    CHAR_INVENTORY = 201
    CHARECTER_PROGRESSION = 202
    EQUIPED_ITEMS = 205
    VENDORS = 400
    RECORDS = 900
    VENDOR_SALES = 402


@typing.final
class MembershipType(IntEnum):
    """An Enum for Bungie membership types."""

    NONE = 0
    XBOX = 1
    PSN = 2
    STEAM = 3
    BLIZZARD = 4
    STADIA = 5
    BUNGIE = 254
    ALL = -1


@typing.final
class Class(IntEnum):
    """An Enum for Destiny character classes."""

    TITAN = 0
    HUNTER = 1
    WARLOCK = 2
    UNKNOWN = 3


@typing.final
class Gender(IntEnum):
    """An Enum for Destiny Genders."""

    MALE = 0
    FEMALE = 1
    UNKNOWN = 2


@typing.final
class Race(IntEnum):
    """An Enum for Destiny races."""

    HUMAN = 0
    AWOKEN = 1
    EXO = 2
    UNKNOWN = 3


@typing.final
class MilestoneType(IntEnum):
    """An Enum for Destiny 2 milestone types."""

    UNKNOWN = 0
    TUTORIAL = 1
    ONETIME = 2
    WEEKLY = 3
    DAILY = 4
    SPECIAL = 5


@typing.final
class Stat(IntEnum):
    """An Enum for Destiny 2 character stats."""

    NONE = 0
    MOBILITY = 2996146975
    RESILIENCE = 392767087
    RECOVERY = 1943323491
    DISCIPLINE = 1735777505
    INTELLECT = 144602215
    STRENGTH = 4244567218


@typing.final
class WeaponType(IntEnum):
    """Enums for The three Destiny Weapon Types"""

    NONE = 0
    KINETIC = 1498876634
    ENERGY = 2465295065
    POWER = 953998645


@typing.final
class DamageType(IntEnum):
    """Enums for Destiny Damage types"""

    NONE = 0
    KINETIC = 3373582085
    SOLAR = 1847026933
    VOID = 3454344768
    ARC = 2303181850
    STASIS = 151347233
    RAID = 1067729826
    """This is a special damage type reserved for some raid activity encounters."""


@typing.final
class Item(IntEnum):
    """Enums for Destiny2's inventory bucket items"""

    NONE = 0
    ARMOR = 2
    WEAPON = 3
    AUTO_RIFLE = 6
    SHOTGUN = 7
    MACHINE_GUN = 8
    HANDCANNON = 9
    ROCKET_LAUNCHER = 10
    FUSION_RIFLE = 11
    SNIPER_RIFLE = 12
    PULSE_RIFLE = 13
    SCOUT_RIFLE = 14
    SIDEARM = 17
    SWORD = 18
    MASK = 19
    SHADER = 20
    ORNAMENT = 21
    FUSION_RIFLELINE = 22
    GRENADE_LAUNCHER = 23
    SUBMACHINE = 24
    TRACE_RIFLE = 25

    # the actual armor hash.
    HELMET_ARMOR = 26
    GAUNTLET_ARMOR = 27
    CHEST_ARMOR = 28
    LEG_ARMOR = 29
    CLASS_ARMOR = 30

    # Only for inventory item definitions.
    HELMET = 3448274439
    GAUNTLET = 3551918588
    CHEST = 14239492
    LEG = 20886954
    CLASS = 1585787867

    BOW = 31
    EMBLEMS = 4274335291
    LEGENDRY_SHARDS = 2689798309
    GHOST = 4023194814
    SUBCLASS = 3284755031
    SEASONAL_ARTIFACT = 1506418338
    EMOTES = 3054419239
    SYNTHWAEV_TEMPLATE = 4092644517

    # This is also required here since
    # All bungie items are entities.
    KINETIC = 1498876634
    ENERGY = 2465295065
    POWER = 953998645


@typing.final
class ItemTier(IntEnum):
    """An enum for a Destiny 2 item tier."""

    NONE = 0
    BASIC = 3340296461
    COMMON = 2395677314
    RARE = 2127292149
    LEGENDERY = 4008398120
    EXOTIC = 2759499571


@typing.final
class AmmoType(IntEnum):
    """AN enum for Detyiny 2 ammo types."""

    NONE = 0
    PRIMARY = 1
    SPECIAL = 2
    HEAVY = 3


@typing.final
class GroupType(IntEnum):
    """An enums for the known bungie group types."""

    GENERAL = 0
    CLAN = 1


@typing.final
class CredentialType(IntEnum):
    """The types of the accounts system supports at bungie."""

    NONE = 0
    XUID = 1
    PSNID = 2
    WILD = 3
    FAKE = 4
    FACEBOOK = 5
    GOOGLE = 8
    WINDOWS = 9
    DEMONID = 10
    STEAMID = 12
    BATTLENETID = 14
    STADIAID = 16
    TWITCHID = 18


@typing.final
class Presence(IntEnum):
    """An enum for a bungie friend status."""

    OFFLINE_OR_UNKNOWN = 0
    ONLINE = 1


@typing.final
class Relationship(IntEnum):
    """An enum for bungie friends relationship types."""

    UNKNOWN = 0
    FRIEND = 1
    INCOMING_REQUEST = 2
    OUTGOING_REQUEST = 3


@typing.final
class ClanMemberType(IntEnum):
    """An enum for bungie clan member types."""

    NONE = 0
    BEGINNER = 1
    MEMBER = 2
    ADMIN = 3
    ACTING_FOUNDER = 4
    FOUNDER = 5


@typing.final
class MembershipOption(IntEnum):
    """A enum for GroupV2 membership options."""

    REVIEWD = 0
    OPEN = 1
    CLOSED = 2
