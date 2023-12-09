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

__all__ = (
    "PRIMARY_CHARACTER_ID",
    "PRIMARY_MEMBERSHIP_ID",
    "PRIMARY_MEMBERSHIP_TYPE",
    "PRIMARY_BUNGIE_ID",
    "PRIMARY_USERNAME",
    "PRIMARY_CLAN_NAME",
    "PRIMARY_CLAN_ID",
    "APP_ID",
    "PRIMARY_STEAM_ID",
    "PRIMARY_CODE",
)

import aiobungie

PRIMARY_CHARACTER_ID = 2305843009444904605
"""Your character ID"""
PRIMARY_MEMBERSHIP_ID = 4611686018484639825
"""Your membership ID"""
PRIMARY_MEMBERSHIP_TYPE = aiobungie.MembershipType.STEAM
"""Your main membership ID associated with the membership ID"""
PRIMARY_BUNGIE_ID = 20315338
"""Your Bungie profile ID."""
PRIMARY_USERNAME = "Fate怒"
"""Your in game name."""
PRIMARY_CODE = 4275
"""Your in game unique code. This is the code that follows your unique name"""
PRIMARY_CLAN_NAME = "Nuanceㅤ "
"""The clan name your membership is associated with."""
PRIMARY_CLAN_ID = 4389205
"""The clan ID."""
APP_ID = 33226
"""You application ID from bungie.net developer portal."""
PRIMARY_STEAM_ID: int | None = 76561198141430157
"""If you play on Steam, this is your Steam ID. otherwise set it to None."""
