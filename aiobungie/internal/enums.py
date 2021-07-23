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

__all__: typing.Sequence[str] = (
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
)

import enum
import typing


@typing.final
class Raid(enum.Enum):
    """An Enum for all available raids in Destiny 2."""

    DSC = 910380154
    """Deep Stone Crypt"""

    LW = 2122313384
    """Last Wish"""

    VOG = 3881495763
    """Normal Valut of Glass"""

    GOS = 3458480158
    """Garden Of Salvation"""

    def __int__(self) -> int:
        return int(self.value)

    def __str__(self) -> str:
        return str(self.name)


@typing.final
class Dungeon(enum.Enum):
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

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)


@typing.final
class Planet(enum.Enum):
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

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)


@typing.final
class Place(enum.Enum):
    """An Enum for Destiny 2 Places and NOT Planets"""

    ORBIT = 2961497387
    SOCIAL = 4151112093
    LIGHT_HOUSE = 4276116472
    EXPLORE = 3497767639

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return int(self.value)


@typing.final
class Vendor(enum.Enum):
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

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)


@typing.final
class GameMode(enum.Enum):
    """An Enum for all available gamemodes in Destiny 2."""

    NOTHING = 0
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

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)


@typing.final
class Component(enum.Enum):
    """An Enum for Destiny 2 Components."""

    NOTHING = 0
    PROFILE = 100
    SILVER = 105
    PROGRESSION = 104
    INVENTORIES = 102
    CHARECTERS = 200
    CHAR_INVENTORY = 201
    CHARECTER_PROGRESSION = 202
    EQUIPED_ITEMS = 205
    VENDORS = 400
    RECORDS = 900
    VENDOR_SALES = 402

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)


@typing.final
class MembershipType(enum.Enum):
    """An Enum for Bungie membership types."""

    NONE = 0
    XBOX = 1
    PSN = 2
    STEAM = 3
    BLIZZARD = 4
    STADIA = 5
    ALL = -1

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)


@typing.final
class Class(enum.Enum):
    """An Enum for Destiny character classes."""

    TITAN = 0
    HUNTER = 1
    WARLOCK = 2
    UNKNOWN = 3

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)


@typing.final
class Gender(enum.Enum):
    """An Enum for Destiny Genders."""

    MALE = 0
    FEMALE = 1
    UNKNOWN = 2

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)


@typing.final
class Race(enum.Enum):
    """An Enum for Destiny races."""

    HUMAN = 0
    AWOKEN = 1
    EXO = 2
    UNKNOWN = 3

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)


@typing.final
class MilestoneType(enum.Enum):
    """An Enum for Destiny 2 milestone types."""

    UNKNOWN = 0
    TUTORIAL = 1
    ONETIME = 2
    WEEKLY = 3
    DAILY = 4
    SPECIAL = 5

    def __int__(self) -> int:
        return int(self.value)

    def __str__(self) -> str:
        return str(self.name)


@typing.final
class Stat(enum.Enum):
    """An Enum for Destiny 2 character stats."""

    MOBILITY = 2996146975
    RESILIENCE = 392767087
    RECOVERY = 1943323491
    DISCIPLINE = 1735777505
    INTELLECT = 144602215
    STRENGTH = 4244567218

    def __int__(self) -> int:
        return int(self.value)

    def __str__(self) -> str:
        return str(self.name)


@typing.final
class WeaponType(enum.Enum):
    """Enums for The three Destiny Weapon Types"""

    KINETIC = 1498876634
    ENERGY = 2465295065
    POWER = 953998645

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)


@typing.final
class DamageType(enum.Enum):
    """Enums for Destiny Damage types"""

    KINETIC = 3373582085
    SOLAR = 1847026933
    VOID = 3454344768
    ARC = 2303181850
    STASIS = 151347233
    RAID = 1067729826
    """This is a special damage type reserved for some raid activity encounters."""

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)


@typing.final
class Item(enum.Enum):
    """Enums for Destiny2's inventory bucket items"""

    NONE = 0
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
    HELMET = 26
    GAUNTLET = 27
    CHEST_ARMOR = 28
    LEG_ARMOR = 29
    CLASS_ARMOR = 30
    BOW = 31
    EMBLEMS = 4274335291
    LEGENDRY_SHARDS = 2689798309
    GHOST = 4023194814
    SUBCLASS = 3284755031
    SEASONAL_ARTIFACT = 1506418338
    EMOTES = 3054419239
    SYNTHWAEV_TEMPLATE = 4092644517

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)
