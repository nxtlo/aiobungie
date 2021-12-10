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

import attr

if typing.TYPE_CHECKING:
    import collections.abc as colelctions

    from aiobungie import traits
    from aiobungie.crate import progressions


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class ArtifactTierItem:

    hash: int = attr.field()

    is_active: bool = attr.field()


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class ArtifactTier:

    hash: int = attr.field()

    is_unlocked: bool = attr.field()

    points_to_unlock: int = attr.field()

    items: colelctions.Sequence[ArtifactTierItem] = attr.field(repr=False)


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class CharacterScopedArtifact:
    """Represetns per-character artifact data."""

    hash: int = attr.field()

    points_used: int = attr.field()

    reset_count: int = attr.field()

    tiers: colelctions.Sequence[ArtifactTier] = attr.field(repr=False)


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class Artifact:
    """Represents a Destiny 2 Season artifact."""

    net: traits.Netrunner = attr.field(repr=False, eq=False, hash=False)
    """A client app we may use to make external requests."""

    hash: int = attr.field(hash=True)
    """The season artifact's hash."""

    power_bonus: int = attr.field()
    """Season artifact's power bonus."""

    acquired_points: int = attr.field()
    """The total acquired artifact points"""

    bonus: progressions.Progression = attr.field(repr=False)
    """Information about the artifact's power bonus progression."""

    points: progressions.Progression = attr.field(repr=False)
    """Information about the artifact's power point progression."""
