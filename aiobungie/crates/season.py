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

__all__: tuple[str, ...] = (
    "Artifact",
    "ArtifactTier",
    "ArtifactTierItem",
    "CharacterScopedArtifact",
)

import typing

import attrs

if typing.TYPE_CHECKING:
    import collections.abc as colelctions

    from aiobungie import traits
    from aiobungie.crates import progressions


@attrs.define(kw_only=True)
class ArtifactTierItem:

    hash: int

    is_active: bool


@attrs.define(kw_only=True)
class ArtifactTier:

    hash: int

    is_unlocked: bool

    points_to_unlock: int

    items: colelctions.Sequence[ArtifactTierItem]


@attrs.define(kw_only=True)
class CharacterScopedArtifact:
    """Represetns per-character artifact data."""

    hash: int

    points_used: int

    reset_count: int

    tiers: colelctions.Sequence[ArtifactTier]


@attrs.define(kw_only=True)
class Artifact:
    """Represents a Destiny 2 Season artifact."""

    net: traits.Netrunner = attrs.field(repr=False, eq=False, hash=False)
    """A client app we may use to make external requests."""

    hash: int
    """The season artifact's hash."""

    power_bonus: int
    """Season artifact's power bonus."""

    acquired_points: int
    """The total acquired artifact points"""

    bonus: progressions.Progression
    """Information about the artifact's power bonus progression."""

    points: progressions.Progression
    """Information about the artifact's power point progression."""
