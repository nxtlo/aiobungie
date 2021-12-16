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

"""Standard implementation of Bungie activity and entities."""

from __future__ import annotations

__all__: tuple[str, ...] = (
    "Activity",
    "PostActivity",
    "ActivityValues",
    "ExtendedValues",
    "ExtendedWeaponValues",
    "PostActivityPlayer",
    "PostActivityTeam",
    "AvailableActivity",
    "Diffculity",
    "Rewards",
    "Challenges",
    "Matchmaking",
    "GuidedGame",
    "Location",
    "CharacterActivity",
)

import typing

import attr

from aiobungie.internal import enums

if typing.TYPE_CHECKING:
    import collections.abc as collections
    import datetime

    from aiobungie import traits
    from aiobungie import typedefs
    from aiobungie.crate import entity
    from aiobungie.crate import user


@typing.final
class Diffculity(enums.IntEnum):
    """An enum for activities diffculities."""

    TRIVIAL = 0
    EASY = 1
    NORMAL = 2
    CHALLENGING = 3
    HARD = 4
    BRAVE = 5
    ALMOST_IMPOSSIBLE = 6
    IMPOSSIBLE = 7


@attr.define(kw_only=True, weakref_slot=False)
class Rewards:
    """Represents awards achieved from activities."""

    hash: int = attr.field()
    """Reward's hash."""

    instance_id: typing.Optional[int] = attr.field()
    """An optional instance id for this reward. `None` if not found."""

    quantity: int = attr.field(repr=False)
    """Reward's quantity."""

    has_conditional_visibility: bool = attr.field(repr=False)
    """???"""

    async def fetch_self(self) -> entity.InventoryEntity:
        """Fetch the definition of this reward."""
        raise NotImplementedError


@attr.define(kw_only=True, weakref_slot=False)
class Challenges:
    """Represents challenges found in activities."""

    net: traits.Netrunner = attr.field(repr=False)

    objective_hash: int = attr.field()
    """The challenge's objetive hash."""

    dummy_rewards: collections.Sequence[Rewards] = attr.field(repr=False)
    """A sequence of the challenge rewards as they're represented in the UI."""

    async def fetch_objective(self) -> entity.ObjectiveEntity:
        """Fetch the objective of this challenge."""
        raise NotImplementedError


@attr.define(kw_only=True, weakref_slot=False)
class Matchmaking:
    """Represents activity's matchmaking information."""

    is_matchmaking: bool = attr.field()
    """Whether the activity is matchmaking or not."""

    min_party: int = attr.field()
    """The minimum number of how many player can join this activity as a party."""

    max_party: int = attr.field()
    """The maximum number of how many player can join this activity as a party."""

    max_player: int = attr.field()
    """The maximum number of how many player can join this activity."""

    requires_guardian_oath: bool = attr.field(repr=False)
    """If true, you have to Solemnly Swear to be up to Nothing But Good(tm) to play."""


@attr.define(kw_only=True, weakref_slot=False)
class GuidedGame:
    """Represents information about a guided game activity."""

    max_loby_size: int = attr.field()
    """The max amount of people that can be in the lobby."""

    min_lobby_size: int = attr.field()
    """The minimum amount of people that can be in the lobby."""

    disband_count: int = attr.field()
    """If 1, the guided group cannot be disbanded.
    Otherwise, take the total number of players in the activity and subtract this number

    That is the total number of votes needed for the guided group to disband.
    """


@attr.define(kw_only=True, weakref_slot=False)
class Location:
    """Represents information about an activity location."""

    hash: typing.Union[
        typedefs.IntAnd[enums.Place], typedefs.IntAnd[enums.Planet]
    ] = attr.field()
    """Location hash."""

    activition_source: str = attr.field()
    """A hint that the UI uses to figure out how this location is activated by the player."""

    item_hash: typing.Optional[int] = attr.field(repr=False)
    """The items hash if poulated."""

    objective_hash: typing.Optional[int] = attr.field(repr=False)
    """The objecitve hash if populated."""

    activity_hash: typing.Optional[int] = attr.field(repr=False)
    """The activity hash if populated."""


@attr.define(kw_only=True, weakref_slot=False)
class CharacterActivity:
    """Represents a character activity profile component."""

    date_started: datetime.datetime = attr.field()
    """The start datetime of the activity."""

    current_hash: int = attr.field()
    """The current activity hash that the player is now playing."""

    current_mode_hash: int = attr.field(repr=False)
    """The current activity mode hash that the player is now playing."""

    current_mode: typing.Optional[typedefs.IntAnd[enums.GameMode]] = attr.field()
    """The current activity mode presented an an enum."""

    current_mode_types: typing.Optional[
        collections.Sequence[typedefs.IntAnd[enums.GameMode]]
    ] = attr.field(repr=False)
    """A sequence of the current activity game-mode types presented as an enum."""

    current_mode_hashes: typing.Optional[collections.Sequence[int]] = attr.field(
        repr=False
    )
    """A sequence of the current activity's mode hashes."""

    current_playlist_hash: typing.Optional[int] = attr.field(repr=False)
    """The current activity playlist hash."""

    last_story_hash: int = attr.field(repr=False)
    """The last completed story hash."""

    available_activities: collections.Sequence[AvailableActivity] = attr.field(
        repr=False
    )
    """A sequence of the available activities associated with this character."""


@attr.define(kw_only=True, weakref_slot=False)
class AvailableActivity:
    """Represents an available activity that can be found in character activities profile component."""

    hash: int = attr.field()
    """Activity's hash."""

    is_new: bool = attr.field(repr=False)
    """Whether the activity is new or not."""

    can_lead: bool = attr.field(repr=False)
    """Whether the character can lead this activity or not."""

    can_join: bool = attr.field(repr=False)
    """Whether the character can join this activity or not."""

    is_completed: bool = attr.field()
    """Whether the character completed this acvitivy before or not."""

    is_visible: bool = attr.field(repr=False)
    """Whether the activity is visible to this character or not."""

    display_level: typing.Optional[int] = attr.field(repr=False)
    """The activity's display leve."""

    recommended_light: typing.Optional[int] = attr.field()
    """The recommended light power to enter this activity."""

    diffculity: typedefs.IntAnd[Diffculity] = attr.field()
    """Activity's diffculity tier."""

    async def fetch_self(self) -> entity.ActivityEntity:
        """Fetch the definition of this activity."""
        raise NotImplementedError


@attr.define(kw_only=True, weakref_slot=False)
class ActivityValues:
    """Information about values found in an activity.

    fields here include kills, deaths, K/D, assists, completion time, etc.
    """

    assists: int = attr.field(repr=False)
    """Activity's assists"""

    is_completed: bool = attr.field()
    """Whether the activity was completed or no."""

    kills: int = attr.field(repr=False)
    """Activity's kills."""

    deaths: int = attr.field(repr=False)
    """Activity's deaths."""

    opponents_defeated: int = attr.field(repr=False)
    """The amount of opponents killed in this activity."""

    efficiency: float = attr.field(repr=False)
    """Activity's efficienty."""

    kd_ratio: float = attr.field(repr=False)
    """Activity's kill/death ratio."""

    kd_assists: float = attr.field(repr=False)
    """Activity's Kill/Death/Assists."""

    score: int = attr.field(repr=False)
    """If the activity has a score, This will be available otherwise 0."""

    played_time: tuple[int, str] = attr.field()
    """The total time the player was in this activity represented as a tuple of int, str."""

    team: typing.Optional[int] = attr.field(repr=False)
    """???"""

    completion_reason: str = attr.field(repr=False)
    """The reason why the activity was completed. usually its Unknown."""

    fireteam_id: int = attr.field(repr=False)
    """The fireteam id associated with this activity."""

    player_count: int = attr.field()
    """Activity's player count."""

    start_seconds: tuple[int, str] = attr.field(repr=False)
    """A tuple of int and str of when did the player start the activity in seconds."""

    duration: tuple[int, str] = attr.field()
    """A tuple of int, string of The activity's duration, Example int, string format `1845`, `30m 45s`"""

    # activity_id: typing.Optional[int] = attr.field(repr=False)
    # """When a stat represents the best, most, longest, fastest or some other personal best,
    # the actual activity ID where that personal best was established is available on this property.
    # """

    team_score: int = attr.field(repr=False)
    """???"""


@attr.define(kw_only=True, weakref_slot=False)
class ExtendedWeaponValues:
    """Information about post activity extended player's weapon values data."""

    reference_id: int = attr.field()
    """Weapon's hash or reference id."""

    kills: int = attr.field()
    """Weapon's total kills."""

    precision_kills: int = attr.field()
    """Weapon's total precision kills."""

    precision_kills_percentage: tuple[int, str] = attr.field()
    """A tuple of weapon's precision kills percentage as an int and a str.

    A string version will be formatted as: `100%`
    and the int version will be formatted as: `1`
    """


@attr.define(kw_only=True, weakref_slot=False)
class ExtendedValues:
    """Information about post activity extended player values data."""

    precision_kills: int = attr.field()
    """Player preci kills."""

    grenade_kills: int = attr.field()
    """Player grenade kills."""

    melee_kills: int = attr.field()
    """Player mele kills."""

    super_kills: int = attr.field()
    """Player super kills."""

    ability_kills: int = attr.field()
    """Player ability kills."""

    weapons: typing.Optional[
        collections.Collection[ExtendedWeaponValues]
    ] = attr.field()
    """Collection of unique player per-weapons used in this activity. if no weapons found None will be returned."""


@attr.define(kw_only=True, weakref_slot=False)
class PostActivityTeam:
    """Represents a post activity team information.

    Teams will be available in PvP gamemodes, e.g., Gambit, Crucible, Iron Banner. etc.
    """

    id: int = attr.field(hash=True)
    """Team id."""

    name: str = attr.field()
    """Team name."""

    is_defeated: bool = attr.field()
    """Whether the team has been defeated or won."""

    score: int = attr.field()
    """Team score"""


@attr.define(kw_only=True, weakref_slot=False)
class PostActivityPlayer:
    """Represents a post activity Destiny 2 player."""

    standing: int = attr.field(repr=False)
    """Sanding of the player."""

    destiny_user: user.DestinyUser = attr.field(repr=False)
    """An object of the destiny membership bound to this player."""

    score: int = attr.field(repr=False)
    """Score of the player."""

    character_id: int = attr.field(hash=True)
    """The id of the character the player finished this activity with."""

    character_class: str = attr.field()
    """A string of the character class the player finished this activity with."""

    class_hash: int = attr.field(repr=False)
    """The hash of the player's character class."""

    race_hash: int = attr.field(repr=False)
    """The hash of the player's character race."""

    gender_hash: int = attr.field(repr=False)
    """The hash of the player's character gender."""

    character_level: int = attr.field(repr=False)
    """The player's character's level."""

    light_level: int = attr.field(repr=False)
    """The light level of the player's character."""

    emblem_hash: int = attr.field(repr=False, hash=True)
    """The embelem hash of the player's character."""

    values: ActivityValues = attr.field(repr=False, eq=False, hash=False)
    """Player's information that occurred in this activity."""

    extended_values: ExtendedValues = attr.field(repr=False)
    """Extended player information occurred in this activity.

    This include weapon, super, grenade kills and more.
    """


@attr.define(kw_only=True, weakref_slot=False)
class PostActivity:
    """Represents a Destiny 2 post activity details."""

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    starting_phase: int = attr.field(repr=False)
    """If this activity has "phases", this is the phase at which the activity was started."""

    hash: int = attr.field(hash=True)
    """The activity's reference id or hash."""

    membership_type: enums.MembershipType = attr.field(repr=False, hash=False)
    """The activity player's membership type."""

    instance_id: int = attr.field(repr=True, hash=True)
    """The activity's instance id."""

    mode: enums.GameMode = attr.field(hash=False)
    """The activity mode or type."""

    modes: collections.Sequence[enums.GameMode] = attr.field(
        eq=False, hash=False, repr=False
    )
    """A sequence of the activity's gamemodes."""

    is_private: bool = attr.field(repr=False)
    """Whether this activity is private or not."""

    occurred_at: datetime.datetime = attr.field(eq=False, hash=False)
    """A datetime of when did this activity occurred."""

    players: collections.Collection[PostActivityPlayer] = attr.field(repr=False)
    """Collection of players that were in the activity."""

    teams: typing.Optional[collections.Collection[PostActivityTeam]] = attr.field()
    """Collections the teams that were playing against each other.

    This field is optional and will be `None` if the activity don't have teams.
    """

    @property
    def is_flawless(self) -> bool:
        """Whether this activity was a flawless run or not."""
        return all(player.values.deaths == 0 for player in self.players)

    @property
    def is_solo(self) -> bool:
        """Whether this activity was completed solo or not."""
        return len(self.players) == 1

    @property
    def is_solo_flawless(self) -> bool:
        """Whether this activity was completed solo and flawless."""
        return self.is_solo & self.is_flawless

    @property
    def refrence_id(self) -> int:
        """An alias to the activity's hash"""
        return self.hash

    def __int__(self) -> int:
        return self.hash


@attr.define(kw_only=True, weakref_slot=False)
class Activity:
    """Represents a Bungie Activity."""

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    hash: int = attr.field(hash=True)
    """The activity's reference id or hash."""

    membership_type: enums.MembershipType = attr.field(repr=False, hash=False)
    """The activity player's membership type."""

    instance_id: int = attr.field(repr=True, hash=True)
    """The activity's instance id."""

    mode: enums.GameMode = attr.field(hash=False)
    """The activity mode or type."""

    modes: collections.Sequence[enums.GameMode] = attr.field(
        eq=False, hash=False, repr=False
    )
    """Sequence of the activity's gamemodes."""

    is_private: bool = attr.field(repr=False)
    """Whether this activity is private or not."""

    occurred_at: datetime.datetime = attr.field(eq=False, hash=False)
    """A datetime of when did this activity occurred."""

    values: ActivityValues = attr.field(repr=False, eq=False, hash=False)
    """Information occurred in this activity."""

    @property
    def is_flawless(self) -> bool:
        """Whether this activity was a flawless run or not."""
        return self.values.deaths == 0 and self.values.is_completed is True

    @property
    def is_solo(self) -> bool:
        """Whether this activity was completed solo or not."""
        return self.values.player_count == 1 and self.values.is_completed

    @property
    def is_solo_flawless(self) -> bool:
        """Whether this activity was completed solo and flawless."""
        return self.is_solo & self.is_flawless

    @property
    def refrence_id(self) -> int:
        """An alias to the activity's hash"""
        return self.hash

    async def fetch_post(self) -> PostActivity:
        """Fetch this activity's data after was finished.

        Returns
        -------
        `PostActivity`
            A post activity object.
        """
        return await self.net.request.fetch_post_activity(self.instance_id)

    def __int__(self) -> int:
        return self.instance_id
