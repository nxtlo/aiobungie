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
    "DestinyClass",
    "DestinyMilestoneType",
    "DestinyRace",
    "Vendor",
    "Raid",
    "Dungeon",
    "DestinyGender",
    "Component",
    "Planet",
    "Stat",
)

import typing
import enum


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

    ORBIT = 2961497387
    """The Orbit"""

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
    ALL = -1

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)


@typing.final
class DestinyClass(enum.Enum):
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
class DestinyGender(enum.Enum):
    """An Enum for Destiny Genders."""

    MALE = 0
    FEMALE = 1
    UNKNOWN = 2

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)


@typing.final
class DestinyRace(enum.Enum):
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
class DestinyMilestoneType(enum.Enum):
    """An Enum for Destiny 2 milestone types."""

    UNKNOWN = 0
    TUTORIAL = 1
    ONETIME = 2
    WEEKLY = 3
    DAILY = 4
    SPECIAL = 5


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
