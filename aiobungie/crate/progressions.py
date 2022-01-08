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

import abc

import attrs


class BaseProgression(abc.ABC):
    """An interface for standard Bungie progressions objects."""

    @property
    @abc.abstractmethod
    def hash(self) -> int:
        """The progression's hash."""

    @property
    @abc.abstractmethod
    def level(self) -> int:
        """The level of the progression."""

    @property
    @abc.abstractmethod
    def cap(self) -> int:
        """The cap number of this progression."""

    @property
    @abc.abstractmethod
    def next_level(self) -> int:
        """The progression's next level at."""

    @property
    @abc.abstractmethod
    def needed(self) -> int:
        """The needed progress to earn the next level."""

    @property
    @abc.abstractmethod
    def current_progress(self) -> int:
        """The current progress of this progression."""

    @property
    @abc.abstractmethod
    def daily_limit(self) -> int:
        """The limit of the daily earned progress."""

    @property
    @abc.abstractmethod
    def daily_progress(self) -> int:
        """The number of the daily progress."""

    @property
    @abc.abstractmethod
    def weekly_limit(self) -> int:
        """The limit of the weekly earned progress."""


@attrs.define(kw_only=True)
class Progression(BaseProgression):
    """The base progression class that all progression objects must inherit from."""

    # net: traits.Netrunner = attrs.field(repr=False)

    hash: int
    # <<inherited docstring from aiobungie.crate.specials.Progression>>.

    level: int
    # <<inherited docstring from aiobungie.crate.specials.Progression>>.

    cap: int
    # <<inherited docstring from aiobungie.crate.specials.Progression>>.

    daily_limit: int
    # <<inherited docstring from aiobungie.crate.specials.Progression>>.

    weekly_limit: int
    # <<inherited docstring from aiobungie.crate.specials.Progression>>.

    current_progress: int
    # <<inherited docstring from aiobungie.crate.specials.Progression>>.

    daily_progress: int
    # <<inherited docstring from aiobungie.crate.specials.Progression>>.

    needed: int
    # <<inherited docstring from aiobungie.crate.specials.Progression>>.

    next_level: int
    # <<inherited docstring from aiobungie.crate.specials.Progression>>.


@attrs.define(kw_only=True)
class Factions(Progression, BaseProgression):
    """Represent a Bungie progression faction found in a character progressions component."""

    faction_hash: int
    """The faction's hash related to this progression."""

    faction_vendor_hash: int
    """The index of the Faction vendor that is currently available. Will be set to -1 if no vendors are available."""
