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

"""Basic implementations of bungie fireteams and entities."""

from __future__ import annotations

__all__: tuple[str, ...] = (
    "Fireteam",
    "AvailableFireteam",
    "FireteamUser",
    "FireteamMember",
    "FireteamPartySettings",
    "FireteamPartyMember",
    "FireteamPartyCurrentActivity",
    "FireteamParty",
)

import typing

import attrs

from aiobungie import url
from aiobungie.crates import user
from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    import collections.abc as collections
    import datetime

    from aiobungie import undefined


@typing.final
class FireteamPlatform(int, enums.Enum):
    """An enum for fireteam related to bungie fireteams.
    This is different from the normal `aiobungie.MembershipType`.
    """

    ANY = 0
    PSN_NETWORK = 1
    XBOX_LIVE = 2
    STEAM = 4
    STADIA = 5


@typing.final
class FireteamActivity(int, enums.Enum):
    """An enum for the fireteam activities."""

    ALL = 0
    CRUCIBLE = 2
    TRIALS_OF_OSIRIS = 3
    NIGHTFALL = 4
    ANY = 5
    GAMBIT = 6
    BLIND_WELL = 7
    NIGHTMARE_HUNTS = 12
    ALTARS_OF_SORROWS = 14
    DUNGEON = 15
    RAID_LW = 20
    RAID_GOS = 21
    RAID_DSC = 22
    EXO_CHALLENGE = 23
    S12_WRATHBORN = 24
    EMPIRE_HUNTS = 25
    S13_BATTLEGROUNDS = 26
    EXOTIC_QUEST = 27
    RAID_VOG = 28
    S14_EXPUNGE = 30
    S15_ASTRAL_ALIGNMENT = 31
    S15_SHATTERED_RELAM = 32
    SHATTERED_THRONE = 33
    PROPHECY = 34
    PIT_OF_HERESY = 35
    DOE = 36
    """Dares of Eternity."""
    DUNGEON_GOA = 37
    """Grasp of Avarice."""
    VOW_OF_THE_DISCPILE = 38
    CAMPAIGN = 39
    WELLSPRING = 40
    S16_BATTLEGROUNDS = 41
    S17_NIGHTMARE_CONTAINMENT = 44
    S17_SEVER = 45


@typing.final
class FireteamLanguage(str, enums.Enum):
    """An enum for fireteams languages filters."""

    ALL = ""
    ENGLISH = "en"
    FRENCH = "fr"
    ESPANOL = "es"
    DEUTSCH = "de"
    ITALIAN = "it"
    JAPANESE = "ja"
    PORTUGUESE = "pt-br"
    RUSSIAN = "ru"
    POLISH = "pl"
    KOREAN = "ko"
    # ? China
    ZH_CHT = "zh-cht"
    ZH_CHS = "zh-chs"

    def __str__(self) -> str:
        return str(self.value)


@typing.final
class FireteamDate(int, enums.Enum):
    """An enum for fireteam date ranges."""

    ALL = 0
    NOW = 1
    TODAY = 2
    TWO_DAYS = 3
    THIS_WEEK = 4


@typing.final
class FireteamPartyMemberState(enums.Flag):
    """An enum flag represents a fireteam party member status."""

    NONE = 0
    """???"""
    MEMBER = 1 << 0
    """A stanard member in the fireteam."""
    POSSE_MEMBER = 1 << 1
    """???"""
    GROUP_MEMBER = 1 << 2
    """???"""
    PARTY_LEADER = 1 << 3
    """Fireteam party member leader."""


@attrs.define(kw_only=True)
class FireteamPartyMember:
    """Minimal information about a party member in a fireteam."""

    membership_id: int
    """Party member's membership id."""

    emblem_hash: int
    """Party member's emblem hash."""

    display_name: undefined.UndefinedOr[str]
    """Party member's display name. `UNDEFINED` if not set."""

    status: FireteamPartyMemberState
    """A Flags Enumeration value indicating the states that the player is in relevant to being on a fireteam."""

    def __str__(self) -> str:
        return str(self.display_name)

    def __int__(self) -> int:
        return self.membership_id


@attrs.define(kw_only=True)
class FireteamPartyCurrentActivity:
    """Represents information about a fireteam party's current activity."""

    start_time: typing.Optional[datetime.datetime]
    """An optional datetime of when was this activity started."""

    end_time: typing.Optional[datetime.datetime]
    """An optional datetime of when was this activity ended."""

    score: float
    """This is the total score of the activity."""

    highest_opposing_score: float
    """If the activity was against humans, This will be their highest score."""

    opponenst_count: int
    """How many human opponents were playing against this fireteam."""

    player_count: int
    """How many human players were playing in this fireteam."""


@attrs.define(kw_only=True)
class FireteamPartySettings:
    """Represents information about a fireteam's joinability settngs."""

    open_slots: int
    """The number of open slots this fireteam has."""

    privacy_setting: enums.PrivacySetting
    """Fireteam leader's fireteam privacy setting."""

    closed_reasons: enums.ClosedReasons
    """Reasons why a person can't join this person's fireteam."""


@attrs.define(kw_only=True)
class FireteamParty:
    """Represents a fireteam party. This information found in profile transitory component."""

    members: collections.Sequence[FireteamPartyMember]
    """The party members currently in this fireteam."""

    activity: FireteamPartyCurrentActivity
    """The current activity this fireteam is in."""

    settings: FireteamPartySettings
    """Information about the fireteam joinability settings, e.g. Privacy, Open slots."""

    last_destination_hash: typing.Optional[int]
    """The hash identifier for the destination of the last location you were orbiting when in orbit."""

    tracking: list[dict[str, typing.Any]]
    """???"""


@attrs.define(kw_only=True)
class FireteamUser(user.DestinyMembership):
    """Represents a Bungie fireteam user info."""

    fireteam_display_name: str
    """The fireteam display name."""

    fireteam_membership_id: enums.MembershipType
    """The fireteam's membership type."""


@attrs.define(kw_only=True)
class FireteamMember(user.PartialBungieUser):
    """Represents a Bungie fireteam member."""

    destiny_user: FireteamUser
    """The destiny user info related to this fireteam member."""

    character_id: int
    """Fireteam member's character id."""

    date_joined: datetime.datetime
    """Fireteam member's join date."""

    has_microphone: bool
    """Whether the fireteam member has a mic or not."""

    last_platform_invite_date: datetime.datetime
    """"""

    last_platform_invite_result: int
    """"""


@attrs.define(kw_only=True)
class Fireteam:
    """A representation of a Bungie fireteam."""

    id: int
    """The fireteam id."""

    group_id: int
    """The fireteam group id."""

    platform: FireteamPlatform
    """The fireteam platform."""

    activity_type: FireteamActivity
    """The activity this fireteam is planning to run."""

    is_immediate: bool
    """Whether the fireteam activity is immediate or not."""

    owner_id: int
    """The fireteam owner id."""

    player_slot_count: int
    """The needed player count in this fireteam."""

    available_player_slots: int
    """The available player slots in this fireteam."""

    available_alternate_slots: int
    """The alternate available player slots in this fireteam."""

    title: undefined.UndefinedOr[str]
    """The fireteam title. Could be `UNDEFINED` if not set."""

    date_created: datetime.datetime
    """A datetime of when was this fireteam created."""

    is_public: bool
    """Whether the fireteam is public or not."""

    locale: FireteamLanguage
    """The selected locale language for this fireteam."""

    is_valid: bool
    """Whether this fireteam is valid or not."""

    last_modified: datetime.datetime
    """A datetime of when was this fireteam created."""

    total_results: int
    """The total results of the found activities."""

    @property
    def url(self) -> str:
        """The activity url at Bungie.net."""
        return f"{url.BASE}/en/ClanV2/PublicFireteam?groupId={self.group_id}&fireteamId={self.id}"  # noqa: E501

    def __int__(self) -> int:
        return self.id

    def __str__(self) -> str:
        return str(self.title)


@attrs.define(kw_only=True)
class AvailableFireteam(Fireteam):
    """Represents an available clan fireteam. This includes the members and alternative members."""

    members: typing.Optional[collections.Sequence[FireteamMember]]
    """A sequence of the fireteam members."""

    alternatives: typing.Optional[collections.Sequence[FireteamMember]]
    """A sequence of the fireteam alternative members."""
