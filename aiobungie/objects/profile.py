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

"""Implementation for a Bungie a Profile."""

from __future__ import annotations

__all__: typing.Sequence[str] = ("Profile",)

import typing
import traceback
import logging
import datetime
from .character import Character
from aiobungie.internal import enums, Image, Time

if typing.TYPE_CHECKING:
    from ..types.profile import ProfileImpl, PartialProfile
    from ..types.character import CharacterImpl

log: typing.Final[logging.Logger] = logging.getLogger(__name__)


class Profile:
    """Represents a Bungie member Profile.

    A bungie profile have components, each component has different data,
    for an example, The profile component returns the a `aiobungie.objects.Profile`
    object which's this class, the character component returns `aiobungie.objects.Character` object, etc.
    See `aiobungie.internal.enums.Component` to see the current available components.

    Attributes
    ----------
    id: `builtins.int`
            Profile's id
    name: `builtins.str`
            Profile's name
    type: `aiobungie.internal.enums.MembershipType`
            The profile's membership type.
    last_played: `datetime.datetime`
            The profile owner's last played date in UTC
    character_ids: `typing.List[builtins.int]`
            A list of the profile's character ids.
    character: `aiobungie.objects.Character`
            A character thats only accessiable if the component was set
            to CHARACTERS from`aiobungie.internal.enums.Component`.
    power_cap: `builtins.int`
            The profile's current season power cap.
    """

    __slots__: typing.Sequence[str] = (
        "id",
        "name",
        "type",
        "last_played",
        "character_ids",
        "character",
        "is_public",
        "power_cap",
        "_character",
        "_component",
    )

    id: int
    name: str
    type: enums.MembershipType
    is_public: bool
    last_played: datetime.datetime
    character_ids: typing.List[int]
    character: Character
    power_cap: int

    def __init__(
        self,
        *,
        data: ProfileImpl,
        component: enums.Component,
        character: typing.Optional[enums.Class] = None,
    ) -> None:
        self._component = component
        self._character = character
        self.update(data)

    def __repr__(self) -> str:
        return (
            f"Profile name={self.name} id={self.id} type={self.type}"
            f" is_public={self.is_public} last_played={self.last_played}"
        )

    def __str__(self) -> str:
        return self.name

    def __eq__(self, o: typing.Any) -> bool:
        return isinstance(o, Profile) and o.id == self.id

    def __ne__(self, o: typing.Any) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        return hash(self.id)

    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """Returns a dict object of the profile,
        This function is useful if you're binding to other REST apis.
        """
        return dict(
            id=self.id,
            name=self.name,
            type=self.type,
            is_public=self.is_public,
            last_played=self.last_played,
            character_ids=self.character_ids,
            power_cap=self.power_cap,
            character=self.character if self._character else None,
        )

    @property
    def delta_last_played(self) -> str:
        """Returns last_played attr but in human delta date."""
        return Time.human_timedelta(self.last_played)

    def predicate(self, data: ProfileImpl) -> PartialProfile:
        try:
            inject = data["profile"]["data"]
        except KeyError:
            inject = data
        return inject

    def _factor_character(self, data: CharacterImpl) -> None:
        if not self._component == enums.Component.CHARECTERS:
            raise Warning from None

        if not self._character:
            raise ValueError(
                f"Expected aiobungie.Class in character parameter, Got {self._character}"
            )

        self.character = Character(char=self._character, data=data)

    def _factor_profile(self, data: ProfileImpl) -> None:

        if self._component != enums.Component.PROFILE:
            raise TypeError(
                "You must select the profile component to return a profile."
            )
            traceback.print_exc()

        if self._component == enums.Component.PROFILE and self._character:
            log.warning(
                f"WARNING: The character paramater is not needed for {self._component} component"
            )

        data = self.predicate(data)  # type: ignore

        self.id = int(data["userInfo"]["membershipId"])
        self.name = data["userInfo"]["displayName"]
        self.is_public = data["userInfo"]["isPublic"]
        self.type = enums.MembershipType(data["userInfo"]["membershipType"])
        self.last_played = Time.clean_date(str(data["dateLastPlayed"]))
        self.character_ids = data["characterIds"]
        self.power_cap = data["currentSeasonRewardPowerCap"]

    def update(self, data: ProfileImpl) -> None:
        data = self.predicate(data)  # type: ignore
        if self._component is enums.Component.PROFILE:
            self._factor_profile(data)

        elif self._component is enums.Component.CHARECTERS:
            self._factor_character(data)  # type: ignore
