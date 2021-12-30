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

"""Standard implementation of Bungie items."""

from __future__ import annotations, print_function

__all__: tuple[str, ...] = ("Perk", "Item")

import typing
import attr

if typing.TYPE_CHECKING:
    import collections.abc as collections

    from aiobungie.internal import assets


@attr.define(kw_only=True, weakref_slot=False, hash=True)
class Perk:
    """Represents a Destiny 2 perk."""

    hash: int = attr.field(hash=True)
    """Perk's hash."""

    icon: assets.Image = attr.field()
    """Perk's icon."""

    is_active: bool = attr.field()
    """Either the perk is active or not."""

    is_visible: bool = attr.field()
    """Either the perk is visible or not."""

@attr.define(kw_only=True, weakref_slot=False, hash=True)
class Item:
    ...