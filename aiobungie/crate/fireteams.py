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
    "FireteamLanguage",
    "FireteamPlatform",
    "FireteamActivity",
    "FireteamDate",
    "AvalaibleFireteam",
    "FireteamUser",
    "FireteamMember",
)

import typing

import attrs

from aiobungie import url
from aiobungie.crate import user
from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    import collections.abc as collections
    import datetime

    from aiobungie import undefined


@typing.final
class FireteamPlatform(enums.IntEnum):
    """An enum for fireteam related to bungie fireteams.
    This is different from the normal `aiobungie.MembershipType`.
    """

    ANY = 0
    PSN_NETWORK = 1
    XBOX_LIVE = 2
    STEAM = 4
    STADIA = 5


@typing.final
class FireteamActivity(enums.IntEnum):
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
    DOE = 36
    """Dares of Eterinity."""
    DUNGEON_GOA = 37
    """Grasp of Avarice."""


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
class FireteamDate(enums.IntEnum):
    """An enum for fireteam date ranges."""

    ALL = 0
    NOW = 1
    TODAY = 2
    TWO_DAYS = 3
    THIS_WEEK = 4


@attrs.define(kw_only=True, weakref_slot=True, hash=False)
class FireteamUser(user.DestinyUser):
    """Represents a Bungie fireteam user info."""

    fireteam_display_name: str = attrs.field(repr=True)
    """The fireteam display name."""

    fireteam_membership_id: enums.MembershipType = attrs.field(repr=True)
    """The fireteam's membership type."""


@attrs.define(kw_only=True, weakref_slot=True, hash=False)
class FireteamMember(user.PartialBungieUser):
    """Represents a Bungie fireteam member."""

    destiny_user: FireteamUser = attrs.field(repr=True)
    """The destiny user info related to this fireteam member."""

    character_id: int = attrs.field(repr=True)
    """Fireteam member's character id."""

    date_joined: datetime.datetime = attrs.field(repr=False)
    """Fireteam member's join date."""

    has_microphone: bool = attrs.field(repr=False)
    """Whether the fireteam member has a mic or not."""

    last_platform_invite_date: datetime.datetime = attrs.field(repr=False)
    """"""

    last_platform_invite_result: int = attrs.field(repr=False)
    """"""


@attrs.define(kw_only=True, weakref_slot=True, hash=False)
class Fireteam:
    """A representation of a Bungie fireteam."""

    id: int = attrs.field(hash=True)
    """The fireteam id."""

    group_id: int = attrs.field(hash=True, repr=False)
    """The fireteam group id."""

    platform: FireteamPlatform = attrs.field(repr=False)
    """The fireteam platform."""

    activity_type: FireteamActivity = attrs.field()
    """The activity this fireteam is planning to run."""

    is_immediate: bool = attrs.field(repr=False)
    """Whether the fireteam activity is immediate or not."""

    owner_id: int = attrs.field(hash=True, repr=False)
    """The fireteam owner id."""

    player_slot_count: int = attrs.field(repr=False)
    """The needed player count in this fireteam."""

    available_player_slots: int = attrs.field()
    """The available player slots in this fireteam."""

    available_alternate_slots: int = attrs.field(repr=False)
    """The alternate available player slots in this fireteam."""

    title: undefined.UndefinedOr[str] = attrs.field()
    """The fireteam title. Could be `UNDEFINED` if not set."""

    date_created: datetime.datetime = attrs.field(repr=False)
    """A datetime of when was this fireteam created."""

    is_public: bool = attrs.field(repr=False)
    """Whether the fireteam is public or not."""

    locale: FireteamLanguage = attrs.field(repr=False)
    """The selected locale language for this fireteam."""

    is_valid: bool = attrs.field(repr=False)
    """Whether this fireteam is valid or not."""

    last_modified: datetime.datetime = attrs.field(repr=False)
    """A datetime of when was this fireteam created."""

    total_results: int = attrs.field(repr=False)
    """The total results of the found activities."""

    @property
    def url(self) -> str:
        """The activity url at Bungie.net."""
        return f"{url.BASE}/en/ClanV2/PublicFireteam?groupId={self.group_id}&fireteamId={self.id}"  # noqa: E501


@attrs.define(kw_only=True, weakref_slot=True, hash=False)
class AvalaibleFireteam(Fireteam):
    """Represents an available clan fireteam. This includes the members and alternative members."""

    members: typing.Optional[collections.Sequence[FireteamMember]] = attrs.field(
        repr=True
    )
    """A sequence of the fireteam members."""

    alternatives: typing.Optional[collections.Sequence[FireteamMember]] = attrs.field(
        repr=True
    )
    """A sequence of the fireteam alternative members."""
