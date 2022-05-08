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

"""A Pythonic `async`/`await` wrapper for interacting with the Bungie API.

Base client.

Example
-------
```py
import aiobungie

client = aiobungie.Client('YOUR_API_KEY')

# Search for Destiny2 users.
async def main() -> None:
    users = await client.search_users('Crit')

    # Iterate over the users and take the first 5 results.
    for user in users.take(5):
        print(f'{user.name} ({user.code})')

        # Iterate through the users memberships.
        for membership in user.memberships:
            print(membership.type, membership.id)

client.run(main()) # or asyncio.run(main())
```

Single RESTClient instance.

The difference between base client and the REST clients:

* No Hight-Level concepts.
* All returned data are pure JSON objects from the API.
* No object creation.

Example
-------
```py
import aiobungie

async def main() -> None:
    # Using `async with` context manager to close the session properly.
    async with aiobungie.RESTClient("TOKEN") as rest:
        payload = await rest.fetch_player('Fate怒', 4275)

        for membership in payload:
            print(membership['membershipId'], membership['iconPath'])

import asyncio
asyncio.run(main())
```

REST client pool.

A REST client pool allows you to acquire multiple `RESTClient` instances that shares the same connection.

Example
-------
```py
import aiobungie
import asyncio

pool = aiobungie.RESTPool("token")

async def func1() -> None:
    async with pool.acquire() as instance:
        tokens = await instance.fetch_oauth2_tokens('code')
        pool.metadata['tokens'] = tokens

# Other instance may access the tokens from pool since its shared.

async def func2() -> None:
    async with pool.acquire() as instance:
        tokens = pool.metadata['tokens']
        tokens = await instance.refresh_access_token(tokens.refresh_token)

async def main() -> None:
    await asyncio.gather(func1(), func2())

asyncio.run(main())
```

Should you use the base client or the REST client?
This returns to you. For an example if you're building a website.

You can use python as a REST API in the backend with the RESTClient since all returned object are JSON objects.
Which gives you the freedom to deserialize it and implement your own logic in the front-end.

Or of you're building a Discord bot for an example or something simple. The base client is the way to go.
"""


from __future__ import annotations

from aiobungie import builders
from aiobungie import crates
from aiobungie import interfaces
from aiobungie import traits
from aiobungie import typedefs
from aiobungie import url
from aiobungie.client import Client
from aiobungie.error import *
from aiobungie.internal import iterators
from aiobungie.internal.assets import Image
from aiobungie.internal.enums import *
from aiobungie.internal.factory import Factory
from aiobungie.internal.iterators import *
from aiobungie.rest import *
from aiobungie.undefined import Undefined
from aiobungie.undefined import UndefinedOr
from aiobungie.undefined import UndefinedType

from ._info import __about__
from ._info import __author__
from ._info import __docs__
from ._info import __email__
from ._info import __license__
from ._info import __url__
from ._info import __version__

# Alias for crate for backwards compatibility.
crate = crates

# Activity enums
from .crates.activity import Difficulty

# Components enums
from .crates.components import ComponentFields
from .crates.components import ComponentPrivacy

# Entity enums
from .crates.entity import GatingScope
from .crates.entity import ObjectiveUIStyle
from .crates.entity import ValueUIStyle

# Fireteam enums.
from .crates.fireteams import FireteamActivity
from .crates.fireteams import FireteamDate
from .crates.fireteams import FireteamLanguage
from .crates.fireteams import FireteamPlatform

# Records enums
from .crates.records import RecordState

__all__ = [mod for mod in dir() if not mod.startswith("_")]  # type: ignore
