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
    "AvaliableActivity",
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

    quantity: int = attr.field()
    """Reward's quantity."""

    has_conditional_visibility: bool = attr.field()
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

    dummy_rewards: collections.Sequence[Rewards]
    """A sequence of the challenge rewards as they're represented in the UI."""

    async def fetch_objective(self) -> entity.ObjectiveEntity:
        """Fetch the objective of this challenge."""


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

    requires_guardian_oath: bool = attr.field()
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

    item_hash: typing.Optional[int] = attr.field()
    """The items hash if poulated."""

    objective_hash: typing.Optional[int] = attr.field()
    """The objecitve hash if populated."""

    activity_hash: typing.Optional[int] = attr.field()
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

    available_activities: collections.Sequence[AvaliableActivity] = attr.field(
        repr=False
    )
    """A sequence of the available activities associated with this character."""


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class AvaliableActivity:
    """Represents an available activity that can be found in character activities profile component."""

    hash: int = attr.field()
    """Activity's hash."""

    is_new: bool = attr.field()
    """Whether the activity is new or not."""

    can_lead: bool = attr.field()
    """Whether the character can lead this activity or not."""

    can_join: bool = attr.field()
    """Whether the character can join this activity or not."""

    is_completed: bool = attr.field()
    """Whether the character completed this acvitivy before or not."""

    is_visible: bool = attr.field()
    """Whether the activity is visible to this character or not."""

    display_level: typing.Optional[int] = attr.field()
    """The activity's display leve."""

    recommended_light: typing.Optional[int] = attr.field()
    """The recommended light power to enter this activity."""

    diffculity: typedefs.IntAnd[Diffculity] = attr.field()
    """Activity's diffculity tier."""

    async def fetch_self(self) -> entity.ActivityEntity:
        """Fetch the definition of this activity."""


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class PostActivity:
    """Represents a Destiny 2 post activity details."""

    period: datetime.datetime = attr.field(repr=True, eq=False, hash=False)
    """The post activity's period utc date."""

    starting_phase: int = attr.field(repr=False, eq=False, hash=False)
    """The postt activity starting phase index.
    For an example if it was 0 that means it's a fresh run"""

    reference_id: int = attr.field(repr=True, eq=False, hash=False)
    """The post activity reference id. AKA the activity hash."""

    mode: typing.Optional[enums.GameMode] = attr.field(repr=True, eq=False, hash=False)
    """The post activity's game mode, Can be `Undefined` if unknown."""

    modes: typing.List[enums.GameMode] = attr.field(repr=False, eq=False, hash=False)
    """A list of the post activity's game mode."""

    membership_type: enums.MembershipType = attr.field(repr=True, eq=False, hash=False)
    """The post activity's membership type."""

    players: typing.Sequence[typing.Dict[str, typing.Any]] = attr.field(repr=False)

    # def get_players(self) -> typing.Sequence[player.Player]:
    #     """Returns a sequence of the players that were in this activity.

    #     Returns
    #     -------
    #     `typing.Sequence[aiobungie.crate.Player]`
    #         the players that were in this activity.
    #     """

    #     players_entries: typing.List[player.Player] = [
    #         isplayer["player"]["destinyUserInfo"] for isplayer in self.players
    #     ]

    #     for raw_player in players_entries:
    #         players_entries.append(raw_player)

    #     return players_entries

    @property
    def is_fresh(self) -> bool:
        """Determines if the activity was fresh or no."""
        return self.starting_phase == 0

    def __int__(self) -> int:
        return self.reference_id


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class Activity:
    """Represents a Bungie Activity."""

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    is_completed: str = attr.field(repr=False, hash=False, eq=False)
    """Check if the activity was completed or no."""

    hash: int = attr.field(hash=True, repr=True, eq=False)
    """The activity's hash."""

    instance_id: int = attr.field(repr=True)
    """The activity's instance id."""

    mode: enums.GameMode = attr.field(hash=False, repr=True)
    """The activity mode or type."""

    kills: int = attr.field(repr=False, eq=False, hash=False)
    """Activity's kills."""

    deaths: int = attr.field(repr=False, eq=False, hash=False)
    """Activity's deaths."""

    period: datetime.datetime = attr.field(repr=True, eq=False, hash=False)
    """When did the activity occurred in UTC datetime."""

    assists: int = attr.field(repr=False, eq=False, hash=False)
    """Activity's assists"""

    duration: str = attr.field(repr=True, eq=False, hash=False)
    """A string of The activity's duration, Example format `7m 42s`"""

    player_count: int = attr.field(repr=False, eq=False, hash=False)
    """Activity's player count."""

    member_type: enums.MembershipType = attr.field(repr=False, eq=False, hash=False)
    """The activity player's membership type."""

    kd: float = attr.field(repr=True, eq=False, hash=False)
    """Activity's kill/death ratio."""

    modes: typing.List[enums.GameMode] = attr.field(repr=False, eq=False, hash=False)
    """A list of the post activity's game mode."""

    opponents_defeated: int = attr.field(repr=False)
    """Activity's opponents kills."""

    efficiency: float = attr.field(repr=False)
    """Activity's efficienty."""

    score: int = attr.field(repr=False)
    """Activity's score."""

    completion_reason: str = attr.field(repr=False)
    """The reason why the activity was completed. usually its Unknown."""

    async def post_report(self) -> PostActivity:
        """Get activity's data after its finished.

        Returns
        -------
        `.PostActivity`
        """
        return await self.net.request.fetch_post_activity(self.instance_id)

    def __int__(self) -> int:
        return self.instance_id
