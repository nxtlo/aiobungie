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

"""Standard Bungie progression objects and entities."""

from __future__ import annotations

__all__: tuple[str, ...] = ("Progression", "Factions")

import attrs


@attrs.define(kw_only=True)
class Progression:
    """The base progression class that all progression objects must inherit from."""

    # net: traits.Netrunner = attrs.field(repr=False)

    hash: int
    """The progression's hash."""

    level: int
    """The level of the progression."""

    cap: int
    """The cap number of this progression."""
    # <<inherited docstring from aiobungie.crates.specials.Progression>>.

    daily_limit: int
    """The limit of the daily earned progress."""
    # <<inherited docstring from aiobungie.crates.specials.Progression>>.

    weekly_limit: int
    """The limit of the weekly earned progress."""
    # <<inherited docstring from aiobungie.crates.specials.Progression>>.

    current_progress: int
    """The current progress of this progression."""
    # <<inherited docstring from aiobungie.crates.specials.Progression>>.

    daily_progress: int
    """The number of the daily progress."""
    # <<inherited docstring from aiobungie.crates.specials.Progression>>.

    needed: int
    """The needed progress to earn the next level."""
    # <<inherited docstring from aiobungie.crates.specials.Progression>>.

    next_level: int
    """The progression's next level at."""
    # <<inherited docstring from aiobungie.crates.specials.Progression>>.


@attrs.define(kw_only=True)
class Factions(Progression):
    """Represent a Bungie progression faction found in a character progressions component."""

    faction_hash: int
    """The faction's hash related to this progression."""

    faction_vendor_hash: int
    """The index of the Faction vendor that is currently available. Will be set to -1 if no vendors are available."""
