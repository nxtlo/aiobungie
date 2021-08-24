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

"""A Pythonic `async`/`await` framework / wrapper for interacting with the Bungie API."""


from __future__ import annotations

__all__: tuple[str, ...] = (
    # __init__.py
    "__about__",
    "__author__",
    "__version__",
    "__url__",
    "__email__",
    "__docs__",
    "__license__",
    # client.py
    "Client",
    # error.py
    "PlayerNotFound",
    "ActivityNotFound",
    "ClanNotFound",
    "NotFound",
    "HTTPException",
    "UserNotFound",
    "ResponseError",
    "Unauthorized",
    "Forbidden",
    "MembershipTypeError",
    # enums.py
    "GameMode",
    "MembershipType",
    "Class",
    "MilestoneType",
    "Race",
    "Vendor",
    "Raid",
    "Dungeon",
    "Gender",
    "Component",
    "Planet",
    "Stat",
    "WeaponType",
    "DamageType",
    "Item",
    "Place",
    "CredentialType",
)

from .client import Client
from .error import *
from .internal.enums import *

__version__ = "0.2.5b5"
__about__ = "A Pythonic `async`/`await` framework / wrapper for interacting with the Bungie API."
__author__ = "nxtlo"
__docs__ = "https://nxtlo.github.io/aiobungie/"
__license__ = "MIT"
__url__ = "https://github.com/nxtlo/aiobungie"
__email__ = "dhmony-99@hotmail.com"
