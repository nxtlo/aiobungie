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
    "Rewards",
    "Challenges",
    "Matchmaking",
    "GuidedGame",
    "Location",
    "CharacterActivity",
    "AggregatedActivity",
    "AggregatedActivityValues",
)

import typing

import attrs

from aiobungie.internal import enums
from aiobungie.internal import helpers

if typing.TYPE_CHECKING:
    import collections.abc as collections
    import datetime

    from aiobungie import traits
    from aiobungie import undefined
    from aiobungie.crates import entity
    from aiobungie.crates import user


@typing.final
class Difficulty(int, enums.Enum):
    """An enum for activities difficulties."""

    TRIVIAL = 0
    EASY = 1
    NORMAL = 2
    CHALLENGING = 3
    HARD = 4
    BRAVE = 5
    ALMOST_IMPOSSIBLE = 6
    IMPOSSIBLE = 7


@attrs.define(kw_only=True)
class Rewards:
    """Represents rewards achieved from activities."""

    net: traits.Netrunner = attrs.field(repr=False, hash=False, eq=False)

    hash: int
    """Reward's hash."""

    instance_id: typing.Optional[int]
    """An optional instance id for this reward. `None` if not found."""

    quantity: int
    """Reward's quantity."""

    has_conditional_visibility: bool
    """???"""

    async def fetch_self(self) -> entity.InventoryEntity:
        """Fetch the definition of this reward.

        Returns
        -------
        `aiobungie.crates.InventoryEntity`
            An inventory item entity of the associated hash.
        """
        return await self.net.request.fetch_inventory_item(self.hash)


@attrs.define(kw_only=True)
class Challenges:
    """Represents challenges found in activities."""

    net: traits.Netrunner = attrs.field(repr=False, hash=False, eq=False)

    objective_hash: int
    """The challenge's objective hash."""

    dummy_rewards: collections.Sequence[Rewards]
    """A sequence of the challenge rewards as they're represented in the UI."""

    async def fetch_objective(self) -> entity.ObjectiveEntity:
        """Fetch the objective of this challenge."""
        return await self.net.request.fetch_objective_entity(self.objective_hash)


@attrs.define(kw_only=True)
class Matchmaking:
    """Represents activity's matchmaking information."""

    is_matchmaking: bool
    """Whether the activity is matchmaking or not."""

    min_party: int
    """The minimum number of how many player can join this activity as a party."""

    max_party: int
    """The maximum number of how many player can join this activity as a party."""

    max_player: int
    """The maximum number of how many player can join this activity."""

    requires_guardian_oath: bool
    """If true, you have to Solemnly Swear to be up to Nothing But Good(tm) to play."""


@attrs.define(kw_only=True)
class GuidedGame:
    """Represents information about a guided game activity."""

    max_lobby_size: int
    """The max amount of people that can be in the lobby."""

    min_lobby_size: int
    """The minimum amount of people that can be in the lobby."""

    disband_count: int
    """If 1, the guided group cannot be disbanded.
    Otherwise, take the total number of players in the activity and subtract this number

    That is the total number of votes needed for the guided group to disband.
    """


@attrs.define(kw_only=True)
class Location:
    """Represents information about an activity location."""

    hash: typing.Union[enums.Place, enums.Planet]
    """Location hash."""

    activision_source: str
    """A hint that the UI uses to figure out how this location is activated by the player."""

    item_hash: typing.Optional[int]
    """The items hash if populated."""

    objective_hash: typing.Optional[int]
    """The objective hash if populated."""

    activity_hash: typing.Optional[int]
    """The activity hash if populated."""


@attrs.define(kw_only=True)
class CharacterActivity:
    """Represents a character activity profile component."""

    date_started: datetime.datetime
    """The start datetime of the activity."""

    current_hash: int
    """The current activity hash that the player is now playing."""

    current_mode_hash: int
    """The current activity mode hash that the player is now playing."""

    current_mode: typing.Optional[enums.GameMode]
    """The current activity mode presented an an enum."""

    current_mode_types: typing.Optional[collections.Sequence[enums.GameMode]]
    """A sequence of the current activity game-mode types presented as an enum."""

    current_mode_hashes: typing.Optional[collections.Sequence[int]]
    """A sequence of the current activity's mode hashes."""

    current_playlist_hash: typing.Optional[int]
    """The current activity playlist hash."""

    last_story_hash: int
    """The last completed story hash."""

    available_activities: collections.Sequence[AvailableActivity]
    """A sequence of the available activities associated with this character."""


@attrs.define(kw_only=True)
class AvailableActivity:
    """Represents an available activity that can be found in character activities profile component."""

    hash: int
    """Activity's hash."""

    is_new: bool
    """Whether the activity is new or not."""

    can_lead: bool
    """Whether the character can lead this activity or not."""

    can_join: bool
    """Whether the character can join this activity or not."""

    is_completed: bool
    """Whether the character completed this activity before or not."""

    is_visible: bool
    """Whether the activity is visible to this character or not."""

    display_level: typing.Optional[int]
    """The activity's display level."""

    recommended_light: typing.Optional[int]
    """The recommended light power to enter this activity."""

    difficulty: Difficulty
    """Activity's difficulty tier."""

    @helpers.unimplemented()
    async def fetch_self(self) -> entity.ActivityEntity:
        """Fetch the definition of this activity."""
        ...


@attrs.define(kw_only=True)
class ActivityValues:
    """Information about values found in an activity.

    fields here include kills, deaths, K/D, assists, completion time, etc.
    """

    assists: int
    """Activity's assists"""

    is_completed: bool
    """Whether the activity was completed or no."""

    kills: int
    """Activity's kills."""

    deaths: int
    """Activity's deaths."""

    opponents_defeated: int
    """The amount of opponents killed in this activity."""

    efficiency: float
    """Activity's efficiently."""

    kd_ratio: float
    """Activity's kill/death ratio."""

    kd_assists: float
    """Activity's Kill/Death/Assists."""

    score: int
    """If the activity has a score, This will be available otherwise 0."""

    played_time: tuple[int, str]
    """The total time the player was in this activity represented as a tuple of int, str."""

    team: typing.Optional[int]
    """???"""

    completion_reason: str
    """The reason why the activity was completed. usually its Unknown."""

    fireteam_id: int
    """The fireteam id associated with this activity."""

    player_count: int
    """Activity's player count."""

    start_seconds: tuple[int, str]
    """A tuple of int and str of when did the player start the activity in seconds."""

    duration: tuple[int, str]
    """A tuple of int, string of The activity's duration, Example int, string format `1845`, `30m 45s`"""

    # activity_id: typing.Optional[int]
    # """When a stat represents the best, most, longest, fastest or some other personal best,
    # the actual activity ID where that personal best was established is available on this property.
    # """

    team_score: int
    """???"""


@attrs.define(kw_only=True)
class AggregatedActivityValues:
    """Information found in an aggregated activity stats."""

    id: int
    """Activity's id."""

    fastest_completion_time: tuple[int, str]
    """A tuple that contains a representation of the fastest completion for that activity in different data types.

    Order
    -----
    - `int`: The completion time in seconds.
    - `str`: The completion time in a readable format. i.e., `0:18.500`
    """

    completions: int
    """The amount of times the activity was completed."""

    kills: int
    """"The amount of kills the player has in this activity."""

    deaths: int
    """The amount of deaths the player has in this activity."""

    seconds_played: tuple[int, str]
    """A tuple that contains an int and a string representation of
    the total time the player has spent in this activity.
    """

    wins: int
    """The amount of wins the player has in this activity."""

    goals_missed: int
    """The amount of goals missed the player has in this activity."""

    special_actions: int
    """The amount of special actions the player has in this activity."""

    best_goals_hit: int
    """The amount of best goals hit the player has in this activity."""

    goals_hit: int

    special_score: int

    best_single_score: int

    kd_ratio: float

    kd_assists: int

    assists: int

    precision_kills: int


@attrs.define(kw_only=True)
class ExtendedWeaponValues:
    """Information about post activity extended player's weapon values data."""

    reference_id: int
    """Weapon's hash or reference id."""

    kills: int
    """Weapon's total kills."""

    precision_kills: int
    """Weapon's total precision kills."""

    assists: typing.Optional[int]
    """Optional weapon assists number."""

    assists_damage: typing.Optional[int]
    """Optional weapon assists damage number."""

    precision_kills_percentage: tuple[int, str]
    """A tuple of weapon's precision kills percentage as an int and a str.

    A string version will be formatted as: `100%`
    and the int version will be formatted as: `1`
    """


@attrs.define(kw_only=True)
class ExtendedValues:
    """Information about post activity extended player values data."""

    precision_kills: int
    """Player precision kills."""

    grenade_kills: int
    """Player grenade kills."""

    melee_kills: int
    """Player melee kills."""

    super_kills: int
    """Player super kills."""

    ability_kills: int
    """Player ability kills."""

    weapons: typing.Optional[collections.Collection[ExtendedWeaponValues]]
    """Collection of unique player weapons used in this activity. if no weapons found None will be returned."""


@attrs.define(kw_only=True)
class PostActivityTeam:
    """Represents a post activity team information.

    Teams will be available in PvP gamemodes, e.g., Gambit, Crucible, Iron Banner. etc.
    """

    id: int
    """Team id."""

    name: str
    """Team name."""

    is_defeated: bool
    """Whether the team has been defeated or won."""

    score: int
    """Team score"""


@attrs.define(kw_only=True)
class PostActivityPlayer:
    """Represents a post activity Destiny 2 player."""

    standing: int
    """Sanding of the player."""

    destiny_user: user.DestinyMembership
    """An object of the destiny membership bound to this player."""

    score: int
    """Score of the player."""

    character_id: int
    """The id of the character the player finished this activity with."""

    character_class: undefined.UndefinedOr[str]
    """A string of the character class the player finished this activity with."""

    class_hash: typing.Optional[int]
    """The hash of the player's character class."""

    race_hash: typing.Optional[int]
    """The hash of the player's character race."""

    gender_hash: typing.Optional[int]
    """The hash of the player's character gender."""

    character_level: typing.Optional[int]
    """The player's character's level."""

    light_level: int
    """The light level of the player's character."""

    emblem_hash: int
    """The emblem hash of the player's character."""

    values: ActivityValues
    """Player's information that occurred in this activity."""

    extended_values: ExtendedValues
    """Extended player information occurred in this activity.

    This include weapon, super, grenade kills and more.
    """


@attrs.define(kw_only=True)
class PostActivity:
    """Represents a Destiny 2 post activity details."""

    net: traits.Netrunner = attrs.field(repr=False, hash=False, eq=False)
    """A network state used for making external requests."""

    starting_phase: int
    """If this activity has "phases", this is the phase at which the activity was started."""

    hash: int
    """The activity's reference id or hash."""

    membership_type: enums.MembershipType
    """The activity player's membership type."""

    instance_id: int
    """The activity's instance id."""

    mode: enums.GameMode
    """The activity mode or type."""

    modes: collections.Sequence[enums.GameMode]
    """A sequence of the activity's gamemodes."""

    is_private: bool
    """Whether this activity is private or not."""

    occurred_at: datetime.datetime
    """A datetime of when did this activity occurred."""

    players: collections.Collection[PostActivityPlayer]
    """Collection of players that were in the activity."""

    teams: typing.Optional[collections.Collection[PostActivityTeam]]
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
    def reference_id(self) -> int:
        """An alias to the activity's hash"""
        return self.hash

    def __int__(self) -> int:
        return self.hash


@attrs.define(kw_only=True)
class Activity:
    """Represents a Bungie Activity."""

    net: traits.Netrunner = attrs.field(repr=False, hash=False, eq=False)
    """A network state used for making external requests."""

    hash: int
    """The activity's reference id or hash."""

    membership_type: enums.MembershipType
    """The activity player's membership type."""

    instance_id: int
    """The activity's instance id."""

    mode: enums.GameMode
    """The activity mode or type."""

    modes: collections.Sequence[enums.GameMode]
    """Sequence of the activity's gamemodes."""

    is_private: bool
    """Whether this activity is private or not."""

    occurred_at: datetime.datetime
    """A datetime of when did this activity occurred."""

    values: ActivityValues
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
    def reference_id(self) -> int:
        """An alias to the activity's hash"""
        return self.hash

    async def fetch_post(self) -> PostActivity:
        """Fetch this activity's data after it was finished.

        Returns
        -------
        `PostActivity`
            A post activity object.
        """
        return await self.net.request.fetch_post_activity(self.instance_id)

    def __int__(self) -> int:
        return self.instance_id


@attrs.define(kw_only=True)
class AggregatedActivity:
    """Represents aggergated activity data."""

    hash: int
    """The activity hash."""

    values: AggregatedActivityValues
    """Aggregated activity values. This contains kills, deaths, etc."""
