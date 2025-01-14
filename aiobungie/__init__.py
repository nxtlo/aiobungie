# MIT License
# ruff: noqa: F401
# ruff: noqa: F403
# ruff: noqa: F405
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

"""A statically typed, asynchronous API wrapper for building clients for Bungie's API in Python.

### Getting Started

aiobungie provides 3 different client interfaces to get started with, each serve a different purpose.

* `Client`: is probably what you want to get started with first. It provides minimal abstraction for the REST api. Is [Pythonic](https://stackoverflow.com/questions/84102/what-is-idiomatic-code#84270).
* `RESTClient`: When you're building a light-weight REST backend. You can use this one. It returns `JSON` objects instead of `dataclasses`, as well `OAuth2` API.
This is considered lower-level version of `Client`.
* `RESTPool`: when you're serving a large amount of users and want to spawn a session for each. each instance of this pool returns a `RESTClient`.

Check either the examples or each of those objects's documentation for more information about the usage.
"""

from __future__ import annotations

from aiobungie import api, builders, crates, framework, traits, typedefs, url
from aiobungie.client import Client
from aiobungie.error import *
from aiobungie.internal.enums import *
from aiobungie.rest import *

# Activity enums
from .crates.activity import Difficulty

# Clans enums
from .crates.clans import GroupDate

# Components enums
from .crates.components import ComponentPrivacy

# Entity enums
from .crates.entity import GatingScope, ObjectiveUIStyle, ValueUIStyle

# Fireteam enums.
from .crates.fireteams import (
    FireteamActivity,
    FireteamDate,
    FireteamLanguage,
    FireteamPlatform,
)

# Records enums
from .crates.records import RecordState

# Package metadata
from .metadata import (
    __about__,
    __author__,
    __docs__,
    __email__,
    __license__,
    __url__,
    __version__,
)

__all__ = [mod for mod in dir() if not mod.startswith("_")]  # type: ignore
