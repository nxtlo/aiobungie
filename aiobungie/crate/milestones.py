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

from __future__ import annotations

__all__: tuple[str, ...] = ("Milestone", "MilestoneItems")

import typing

import attr

if typing.TYPE_CHECKING:
    from aiobungie.internal import helpers


@attr.define(hash=False, weakref_slot=False, kw_only=True)
class MilestoneItems:
    """Represents items the may be found inside a milestone."""

    title: helpers.UndefinedOr[str] = attr.field(repr=True)
    """The item title. This may be `UNDEFINED` if not specified."""

    hashes: typing.Sequence[int] = attr.field(repr=True)
    """The items hashes"""


@attr.define(hash=False, weakref_slot=False, kw_only=True, eq=False)
class Milestone:
    """Represents general information about a Destiny milestone."""

    about: helpers.UndefinedOr[str] = attr.field(repr=True)
    """About this milestone."""

    status: helpers.UndefinedOr[str] = attr.field(repr=True, eq=True)
    """The milestone's status. This field may be `UNDEFINED` if not specified."""

    tips: typing.Sequence[helpers.UndefinedOr[str]] = attr.field(repr=True)
    """A sequence of the milestone's tips. fields in the sequence may be `UNDEFINED` if not specified."""

    items: helpers.NoneOr[MilestoneItems] = attr.field(repr=True)
    """An optional items for this miletones. This may return `None` if nothing was found."""
