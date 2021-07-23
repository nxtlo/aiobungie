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

"""User and entities releated to a Bungie user."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional, TypedDict, Union

from ..internal import Image
from ..internal.enums import MembershipType


class UserCard(TypedDict):
    iconPath: Image
    isPublic: bool
    displayName: str
    applicableMembershipTypes: List[int]
    membershipType: MembershipType
    membershipId: int


class UserImpl(UserCard, total=False):
    isDeleted: bool
    about: Optional[str]
    firstAccess: str
    lastUpdate: str
    psnDisplayName: Optional[str]
    locale: str
    profilePicturePath: Optional[Image]
    statusText: Optional[str]
    blizzardDisplayName: Optional[str]
    steamDisplayName: Optional[str]
    twitchDisplayName: Optional[str]
