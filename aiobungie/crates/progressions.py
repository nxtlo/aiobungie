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

"""Basic implementation of Bungie progression resources."""

from __future__ import annotations

__all__ = ("Progression", "Factions")

import attrs


@attrs.frozen(kw_only=True)
class Progression:
    """The base progression class that all progression objects must inherit from."""

    hash: int
    """The progression's hash."""

    level: int
    """The level of the progression."""

    cap: int
    """The cap number of this progression."""

    daily_limit: int
    """The limit of the daily earned progress."""

    weekly_limit: int
    """The limit of the weekly earned progress."""

    current_progress: int
    """The current progress of this progression."""

    daily_progress: int
    """The number of the daily progress."""

    needed: int
    """The needed progress to earn the next level."""

    next_level: int
    """The progression's next level at."""


@attrs.frozen(kw_only=True)
class Factions(Progression):
    """Represent a Bungie progression faction found in a character progressions component."""

    faction_hash: int
    """The faction's hash related to this progression."""

    faction_vendor_hash: int
    """The index of the Faction vendor that is currently available. Will be set to -1 if no vendors are available."""
