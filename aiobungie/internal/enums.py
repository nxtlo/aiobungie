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

"""Bungie enums implementation used within aiobungie."""


from __future__ import annotations

__all__: tuple[str, ...] = (
    "Enum",
    "Flag",
    "GameMode",
    "MembershipType",
    "Class",
    "MilestoneType",
    "Race",
    "Vendor",
    "Raid",
    "Dungeon",
    "Gender",
    "ComponentType",
    "Planet",
    "Stat",
    "WeaponType",
    "DamageType",
    "ItemType",
    "Place",
    "ItemTier",
    "AmmoType",
    "GroupType",
    "CredentialType",
    "Presence",
    "Relationship",
    "ClanMemberType",
    "MembershipOption",
    "ItemBindStatus",
    "ItemLocation",
    "TransferStatus",
    "ItemState",
    "PrivacySetting",
    "ClosedReasons",
    "ItemSubType",
    "TierType",
)

import enum as __enum
import typing

_ITERABLE = (set, list, tuple)


class Enum(__enum.Enum):
    """Builtin Python enum with extra handlings."""

    @property
    def name(self) -> str:  # type: ignore[override]
        return self._name_

    @property
    def value(self) -> typing.Any:  # type: ignore[override]
        return self._value_

    def __str__(self) -> str:
        return self._name_

    def __repr__(self) -> str:
        return f"<{type(self).__name__}.{self._name_}: {self._value_!s}>"

    def __int__(self) -> int:
        if isinstance(self.value, _ITERABLE):
            raise TypeError(
                f"Can't overload {self.value} in {type(self).__name__}, Please use `.value` attribute.",
            )
        return int(self.value)


class Flag(__enum.Flag):
    """Builtin Python enum flag with extra handlings."""

    # Needs to type this here for mypy
    _value_: int

    @property
    def name(self) -> str:  # type: ignore[override]
        if self._name_ is None:
            self._name_ = f"UNKNOWN {self._value_}"

        return self._name_

    @property
    def value(self) -> int:  # type: ignore[override]
        return self._value_

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<{type(self).__name__}.{self.name}: {self._value_!s}>"

    def __int__(self) -> int:
        if isinstance(self.value, _ITERABLE):
            raise TypeError(
                f"Can't overload {self.value} in {type(self).__name__}, Please use `.value` attribute.",
            )
        return int(self.value)

    def __or__(self, other: typing.Union[Flag, int]) -> Flag:
        return self.__class__(self._value_ | int(other))

    def __xor__(self, other: typing.Union[Flag, int]) -> Flag:
        return self.__class__(self._value_ ^ int(other))

    def __and__(self, other: typing.Union[Flag, int]) -> Flag:
        return self.__class__(other & int(other))

    def __invert__(self) -> Flag:
        return self.__class__(~self._value_)

    def __contains__(self, other: typing.Union[Flag, int]) -> bool:
        return self.value & int(other) == int(other)


@typing.final
class Raid(int, Enum):
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
class Dungeon(int, Enum):
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

    GOA_LEGEND = 4078656646
    """Grasp of Avarice legend."""

    GOA_MASTER = 3774021532
    """Grasp of Avarice master."""


@typing.final
class Planet(int, Enum):
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
class Place(int, Enum):
    """An Enum for Destiny 2 Places and NOT Planets"""

    ORBIT = 2961497387
    SOCIAL = 4151112093
    LIGHT_HOUSE = 4276116472
    EXPLORE = 3497767639


@typing.final
class Vendor(int, Enum):
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
class GameMode(int, Enum):
    """An Enum for all available gamemodes in Destiny 2."""

    NONE = 0
    STORY = 2
    STRIKE = 3
    RAID = 4
    ALLPVP = 5
    PATROL = 6
    ALLPVE = 7
    RESERVED9 = 9
    CONTROL = 10
    RESERVED11 = 11
    CLASH = 12
    RESERVED13 = 13
    CRIMSONDOUBLES = 15
    NIGHTFALL = 16
    HEROICNIGHTFALL = 17
    ALLSTRIKES = 18
    IRONBANNER = 19
    RESERVED20 = 20
    RESERVED21 = 21
    RESERVED22 = 22
    RESERVED24 = 24
    ALLMAYHEM = 25
    RESERVED26 = 26
    RESERVED27 = 27
    RESERVED28 = 28
    RESERVED29 = 29
    RESERVED30 = 30
    SUPREMACY = 31
    PRIVATEMATCHESALL = 32
    SURVIVAL = 37
    COUNTDOWN = 38
    TRIALSOFTHENINE = 39
    SOCIAL = 40
    TRIALSCOUNTDOWN = 41
    TRIALSSURVIVAL = 42
    IRONBANNERCONTROL = 43
    IRONBANNERCLASH = 44
    IRONBANNERSUPREMACY = 45
    SCOREDNIGHTFALL = 46
    SCOREDHEROICNIGHTFALL = 47
    RUMBLE = 48
    ALLDOUBLES = 49
    DOUBLES = 50
    PRIVATEMATCHESCLASH = 51
    PRIVATEMATCHESCONTROL = 52
    PRIVATEMATCHESSUPREMACY = 53
    PRIVATEMATCHESCOUNTDOWN = 54
    PRIVATEMATCHESSURVIVAL = 55
    PRIVATEMATCHESMAYHEM = 56
    PRIVATEMATCHESRUMBLE = 57
    HEROICADVENTURE = 58
    SHOWDOWN = 59
    LOCKDOWN = 60
    SCORCHED = 61
    SCORCHEDTEAM = 62
    GAMBIT = 63
    ALLPVECOMPETITIVE = 64
    BREAKTHROUGH = 65
    BLACKARMORYRUN = 66
    SALVAGE = 67
    IRONBANNERSALVAGE = 68
    PVPCOMPETITIVE = 69
    PVPQUICKPLAY = 70
    CLASHQUICKPLAY = 71
    CLASHCOMPETITIVE = 72
    CONTROLQUICKPLAY = 73
    CONTROLCOMPETITIVE = 74
    GAMBITPRIME = 75
    RECKONING = 76
    MENAGERIE = 77
    VEXOFFENSIVE = 78
    NIGHTMAREHUNT = 79
    ELIMINATION = 80
    MOMENTUM = 81
    DUNGEON = 82
    SUNDIAL = 83
    TRIALS_OF_OSIRIS = 84
    DARES = 85
    OFFENSIVE = 86
    LOSTSECTOR = 87
    RIFT = 88
    ZONECONTROL = 89
    IRONBANNERRIFT = 90


@typing.final
class ComponentType(Enum):
    """An Enum for Destiny 2 profile Components."""

    NONE = 0

    PROFILE = 100
    PROFILE_INVENTORIES = 102
    PROFILE_CURRENCIES = 103
    PROFILE_PROGRESSION = 104
    ALL_PROFILES = (
        PROFILE,
        PROFILE_INVENTORIES,
        PROFILE_CURRENCIES,
        PROFILE_PROGRESSION,
    )
    """All profile components."""

    VENDORS = 400
    VENDOR_SALES = 402
    VENDOR_RECEIPTS = 101
    ALL_VENDORS = (VENDORS, VENDOR_RECEIPTS, VENDOR_SALES)
    """All vendor components."""

    # Items
    ITEM_INSTANCES = 300
    ITEM_OBJECTIVES = 301
    ITEM_PERKS = 302
    ITEM_RENDER_DATA = 303
    ITEM_STATS = 304
    ITEM_SOCKETS = 305
    ITEM_TALENT_GRINDS = 306
    ITEM_PLUG_STATES = 308
    ITEM_PLUG_OBJECTIVES = 309
    ITEM_REUSABLE_PLUGS = 310

    ALL_ITEMS = (
        ITEM_PLUG_OBJECTIVES,
        ITEM_PLUG_STATES,
        ITEM_SOCKETS,
        ITEM_INSTANCES,
        ITEM_OBJECTIVES,
        ITEM_PERKS,
        ITEM_RENDER_DATA,
        ITEM_STATS,
        ITEM_TALENT_GRINDS,
        ITEM_REUSABLE_PLUGS,
    )
    """All item components."""

    PLATFORM_SILVER = 105
    KIOSKS = 500
    CURRENCY_LOOKUPS = 600
    PRESENTATION_NODES = 700
    COLLECTIBLES = 800
    RECORDS = 900
    TRANSITORY = 1000
    METRICS = 1100
    INVENTORIES = 102
    STRING_VARIABLES = 1200
    CRAFTABLES = 1300

    CHARACTERS = 200
    CHARACTER_INVENTORY = 201
    CHARECTER_PROGRESSION = 202
    CHARACTER_RENDER_DATA = 203
    CHARACTER_ACTIVITIES = 204
    CHARACTER_EQUIPMENT = 205

    ALL_CHARACTERS = (
        CHARACTERS,
        CHARACTER_INVENTORY,
        CHARECTER_PROGRESSION,
        CHARACTER_RENDER_DATA,
        CHARACTER_ACTIVITIES,
        CHARACTER_EQUIPMENT,
        RECORDS,
    )
    """All character components."""

    ALL = (
        *ALL_PROFILES,  # type: ignore
        *ALL_CHARACTERS,  # type: ignore
        *ALL_VENDORS,  # type: ignore
        *ALL_ITEMS,  # type: ignore
        RECORDS,
        CURRENCY_LOOKUPS,
        PRESENTATION_NODES,
        COLLECTIBLES,
        KIOSKS,
        METRICS,
        PLATFORM_SILVER,
        INVENTORIES,
        STRING_VARIABLES,
        TRANSITORY,
        CRAFTABLES,
    )
    """ALl components included."""


@typing.final
class MembershipType(int, Enum):
    """An Enum for Bungie membership types."""

    NONE = 0
    XBOX = 1
    PSN = 2
    STEAM = 3
    BLIZZARD = 4
    STADIA = 5
    EPIC_GAMES_STORE = 6
    DEMON = 10
    BUNGIE = 254
    ALL = -1


@typing.final
class Class(int, Enum):
    """An Enum for Destiny character classes."""

    TITAN = 0
    HUNTER = 1
    WARLOCK = 2
    UNKNOWN = 3


@typing.final
class Gender(int, Enum):
    """An Enum for Destiny Genders."""

    MALE = 0
    FEMALE = 1
    UNKNOWN = 2


@typing.final
class Race(int, Enum):
    """An Enum for Destiny races."""

    HUMAN = 0
    AWOKEN = 1
    EXO = 2
    UNKNOWN = 3


@typing.final
class MilestoneType(int, Enum):
    """An Enum for Destiny 2 milestone types."""

    UNKNOWN = 0
    TUTORIAL = 1
    ONETIME = 2
    WEEKLY = 3
    DAILY = 4
    SPECIAL = 5


@typing.final
class Stat(int, Enum):
    """An Enum for Destiny 2 character stats."""

    NONE = 0
    MOBILITY = 2996146975
    RESILIENCE = 392767087
    RECOVERY = 1943323491
    DISCIPLINE = 1735777505
    INTELLECT = 144602215
    STRENGTH = 4244567218
    LIGHT_POWER = 1935470627


@typing.final
class WeaponType(int, Enum):
    """Enums for The three Destiny Weapon Types"""

    NONE = 0
    KINETIC = 1498876634
    ENERGY = 2465295065
    POWER = 953998645


@typing.final
class DamageType(int, Enum):
    """Enums for Destiny Damage types"""

    NONE = 0
    KINETIC = 1
    ARC = 2
    SOLAR = 3
    VOID = 4
    RAID = 5
    """This is a special damage type reserved for some raid activity encounters."""
    STASIS = 6


@typing.final
class ItemType(int, Enum):
    """Enums for Destiny2's item types."""

    NONE = 0
    CURRENCY = 1
    ARMOR = 2
    WEAPON = 3
    MESSAGE = 7
    ENGRAM = 8
    CONSUMABLE = 9
    EXCHANGEMATERIAL = 10
    MISSIONREWARD = 11
    QUESTSTEP = 12
    QUESTSTEPCOMPLETE = 13
    EMBLEM = 14
    QUEST = 15
    SUBCLASS = 16
    CLANBANNER = 17
    AURA = 18
    MOD = 19
    DUMMY = 20
    SHIP = 21
    VEHICLE = 22
    EMOTE = 23
    GHOST = 24
    PACKAGE = 25
    BOUNTY = 26
    WRAPPER = 27
    SEASONALARTIFACT = 28
    FINISHER = 29


@typing.final
class ItemSubType(int, Enum):
    """An enum for Destiny 2 inventory items subtype."""

    NONE = 0
    AUTORIFLE = 6
    SHOTGUN = 7
    MACHINEGUN = 8
    HANDCANNON = 9
    ROCKETLAUNCHER = 10
    FUSIONRIFLE = 11
    SNIPERRIFLE = 12
    PULSERIFLE = 13
    SCOUTRIFLE = 14
    SIDEARM = 17
    SWORD = 18
    MASK = 19
    SHADER = 20
    ORNAMENT = 21
    FUSIONRIFLELINE = 22
    GRENADELAUNCHER = 23
    SUBMACHINEGUN = 24
    TRACERIFLE = 25
    HELMETARMOR = 26
    GAUNTLETSARMOR = 27
    CHESTARMOR = 28
    LEGARMOR = 29
    CLASSARMOR = 30
    BOW = 31
    DUMMYREPEATABLEBOUNTY = 32


@typing.final
class ItemTier(int, Enum):
    """An enum for a Destiny 2 item tier."""

    NONE = 0
    BASIC = 3340296461
    COMMON = 2395677314
    RARE = 2127292149
    LEGENDERY = 4008398120
    EXOTIC = 2759499571


@typing.final
class TierType(int, Enum):
    """An enum for a Destiny 2 item tier type."""

    UNKNOWN = 0
    CURRENCY = 1
    BASIC = 2
    COMMON = 3
    RARE = 4
    SUPERIOR = 5
    EXOTIC = 6


@typing.final
class AmmoType(int, Enum):
    """AN enum for Detyiny 2 ammo types."""

    NONE = 0
    PRIMARY = 1
    SPECIAL = 2
    HEAVY = 3


@typing.final
class GroupType(int, Enum):
    """An enums for the known bungie group types."""

    GENERAL = 0
    CLAN = 1


@typing.final
class CredentialType(int, Enum):
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
class Presence(int, Enum):
    """An enum for a bungie friend status."""

    OFFLINE_OR_UNKNOWN = 0
    ONLINE = 1


@typing.final
class Relationship(int, Enum):
    """An enum for bungie friends relationship types."""

    UNKNOWN = 0
    FRIEND = 1
    INCOMING_REQUEST = 2
    OUTGOING_REQUEST = 3


@typing.final
class ClanMemberType(int, Enum):
    """An enum for bungie clan member types."""

    NONE = 0
    BEGINNER = 1
    MEMBER = 2
    ADMIN = 3
    ACTING_FOUNDER = 4
    FOUNDER = 5


@typing.final
class MembershipOption(int, Enum):
    """A enum for GroupV2 membership options."""

    REVIEWD = 0
    OPEN = 1
    CLOSED = 2


@typing.final
class ItemBindStatus(int, Enum):
    """An enum for Destiny 2 items bind status."""

    NOT_BOUND = 0
    BOUND_TO_CHARACTER = 1
    BOUND_TO_ACCOUNT = 2
    BOUNT_TO_GUILD = 3


@typing.final
class ItemLocation(int, Enum):
    """An enum for Destiny 2 items location."""

    UNKNOWN = 0
    INVENTORY = 1
    VAULT = 2
    VENDOR = 3
    POSTMASTER = 4


@typing.final
class TransferStatus(Flag):
    """An enum for items transfer statuses."""

    CAN_TRANSFER = 0
    """The item can be transferred."""
    IS_EQUIPPED = 1 << 0
    """You can't transfer since the item is equipped."""
    NOT_TRASNFERRABLE = 1 << 1
    """This item can not be transferred."""
    COULD_BE_TRANSFERRED = 1 << 2
    """You can trasnfer the item. But the place you're trying to put it at has no space for it."""


@typing.final
class ItemState(Flag):
    """An enum for Destiny 2 item states."""

    NONE = 0
    LOCKED = 1 << 0
    TRACKED = 1 << 1
    MASTERWORKED = 1 << 2
    CRAFTED = 1 << 3
    """If this bit is set, the item has been 'crafted' by the player."""
    HIGHLITED_OBJECTIVE = 1 << 4
    """If this bit is set, the item is a 'highlighted' objective."""


@typing.final
class PrivacySetting(int, Enum):
    """An enum for players's privacy settings."""

    OPEN = 0
    CLAN_AND_FRIENDS = 1
    FRIENDS_ONLY = 2
    INVITE_ONLY = 3
    CLOSED = 4


@typing.final
class ClosedReasons(Flag):
    """A Flags enumeration representing the reasons why a person can't join this user's fireteam."""

    NONE = 0
    MATCHMAKING = 1 << 0
    LOADING = 1 << 1
    SOLO = 1 << 2
    """The activity is required to be played solo."""
    INTERNAL_REASONS = 1 << 3
    """
    The user can't be joined for one of a variety of internal reasons.
    Basically, the game can't let you join at this time,
    but for reasons that aren't under the control of this user
    """
    DISALLOWED_BY_GAME_STATE = 1 << 4
    """The user's current activity/quest/other transitory game state is preventing joining."""
    OFFLINE = 32768
    """The user appears offline."""


@typing.final
class StatsGroupType(int, Enum):
    """Bungie historical group stats type enum."""

    NONE = 0
    GENERAL = 1
    WEAPONS = 2
    MEDALS = 3
    REVERSED_GROUPS = 100
    """This is purely to serve as the dividing line between filterable and un-filterable groups.
    Below this number is a group you can pass as a filter.
    Above it are groups used in very specific circumstances and not relevant for filtering.
    """
    LEADERBOARDS = 101
    ACTIVITY = 102
    UNIQUE_WEAPON = 103
    INTERNAL = 104


@typing.final
class PeriodType(int, Enum):
    """Bungie historical group stats period type enum."""

    NONE = 0
    DAILY = 1
    ALL_TIME = 2
    ACTIVITY = 3
