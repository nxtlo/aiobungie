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

"""A basic implementations of stuff that a Destiny 2 season contains.

This includes all season that can be found in a regular season i.e,
season artifact, season content, season pass, etc.
"""

from __future__ import annotations

# Since this is still being implemented
# We let pdoc3 not generate pages for this.

__pdoc__: dict[str, bool] = {}
__all__: list[str] = ["Artifact", "PowerBonus"]

for _cls in __all__:
    __pdoc__[_cls] = False

import typing

import attr

from aiobungie.crate import entity

if typing.TYPE_CHECKING:
    from aiobungie.internal import assets
    from aiobungie.internal import traits

    # The artifact tires.
    Tiers: list[dict[int, dict[str, typing.Any]]]


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class PowerBonus:
    """Represents a Destiny 2 artifact power bonus information."""

    progression_hash: int = attr.field(repr=False)
    """The hash of the power bonus."""

    level: int = attr.field(repr=True)
    """Power bonus's current level aka The total earned bonus."""

    cap: int = attr.field(repr=False)
    """The cap of the power bonus."""

    daily_limit: int = attr.field(repr=False)
    """Power bonus's daily limit."""

    weekly_limit: int = attr.field(repr=False)
    """Power bonus's weekly limit."""

    current_progress: int = attr.field(repr=True)
    """Power bonus's current progress."""

    daily_progress: int = attr.field(repr=False)
    """Power bonus's daily progress."""

    needed: int = attr.field(repr=True)
    """The needed progress to earn the next level."""

    next_level: int = attr.field(repr=True)
    """Power bonus's next level at."""


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class ArtifactPoint:
    """Represents a Destiny 2 artifact points information."""

    progression_hash: int = attr.field(repr=False)
    """The hash of the power bonus."""

    level: int = attr.field(repr=True)
    """Power bonus's current level aka The total earned bonus."""

    cap: int = attr.field(repr=False)
    """The cap of the power bonus."""

    daily_limit: int = attr.field(repr=False)
    """Power bonus's daily limit."""

    weekly_limit: int = attr.field(repr=False)
    """Power bonus's weekly limit."""

    current_progress: int = attr.field(repr=True)
    """Power bonus's current progress."""

    daily_progress: int = attr.field(repr=False)
    """Power bonus's daily progress."""

    needed: int = attr.field(repr=True)
    """The needed progress to earn the next level."""

    next_level: int = attr.field(repr=True)
    """Power bonus's next level at."""


@attr.s(init=True, slots=True, weakref_slot=False, eq=True, hash=True, kw_only=True)
class FetchableArtifact(entity.InventoryEntity):
    """A interface for a Destiny 2 artifact entity the can be fetched.

    This derives from `DestinyArtifactDefinition` definition.

    The point of this is to return the artifact from the actual Definition.
    This will be part of `aiobungie.crate.Entity` and acts like an entity later.
    """

    hash: int = attr.field(repr=True, hash=True, eq=True)
    """Entity's hash."""

    index: int = attr.field(repr=True, hash=False, eq=False)
    """Entity's index."""

    app: traits.Netrunner = attr.field(repr=False, hash=False, eq=False)
    """A client that we may use to make rest calls."""

    name: str = attr.field(repr=True, hash=False, eq=False)
    """Entity's name"""

    icon: assets.MaybeImage = attr.field(repr=False, hash=False, eq=False)
    """Entity's icon"""

    has_icon: bool = attr.field(repr=False, hash=False, eq=False)
    """A boolean that returns True if the entity has an icon."""

    description: str = attr.field(repr=True)
    """Entity's description."""


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class Artifact:
    """Represents a Destiny 2 Season artifact."""

    net: traits.Netrunner = attr.field(repr=False, eq=False, hash=False)
    """A client app we may use to make external requests."""

    hash: int = attr.field(repr=True, hash=True)
    """The season artifact's hash."""

    power_bonus: int = attr.field(repr=True)
    """Season artifact's power bonus."""

    acquired_points: int = attr.field(repr=False)
    """The total acquired artifact points"""

    bonus: PowerBonus = attr.field(repr=False)
    """Information about the artifact's power bonus."""

    points: ArtifactPoint = attr.field(repr=False)
    """Information about the artifact's power points"""
