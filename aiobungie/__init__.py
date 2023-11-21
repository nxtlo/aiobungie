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

"""A statically typed, asynchronous API wrapper for building clients for Bungie's API in Python.

Getting Started
---------------

This is the basic client you probably want you start with.

```py
import aiobungie

client = aiobungie.Client('YOUR_API_KEY', client_secret='KEY', client_id=0)

async def main() -> None:
    async with client.rest:
        # Search for Destiny 2 memberships.
        users = await client.search_users('Crit')

        # Iterate over the users and take the first 5 results.
        for user in users.take(5):
            # Print the user name and their code.
            print(f'{user.name} {user.code}')

# aiobungie provides an internal function to run async functions.
# It's equivalent to asyncio.run()
client.run(main()) # or asyncio.run(main())
```

RESTClient
----------

aiobungie provides a second way to use Bungie's API,

a single `RESTClient` allows you to make requests and return JSON objects immediately.

This bypasses the need to deserialize and create objects. It also exposes all `OAuth2` and `manifest` methods.
This can be faster for `REST` apis.

This is considered the core client since `aiobungie.Client` is built on top of it.
Using the `.rest` property allows direct access to the raw REST client instance.


```py
import aiobungie
import asyncio

client = aiobungie.RESTClient("TOKEN")

async def main() -> None:
    async with client as rest:
        payload = await rest.fetch_player('Fate怒', 4275)

        for membership in payload:
            print(membership['membershipId'])

asyncio.run(main())
```

RESTPool
--------

A REST client pool allows you to acquire multiple `RESTClient` that share the same state.

This is useful when you want to spawn an instance for each client which shared the same state.

```py
import aiobungie
import asyncio

pool = aiobungie.RESTPool("token")

async def set() -> None:
    # Set your ID to access it from other places.
    pool.metadata['my_id'] = 4401
    async with pool.acquire() as instance:
        ...

async def fetch() -> None:
    my_id: int = pool.metadata['my_id']
    async with pool.acquire() as instance: # A different client instance.
        my_user = instance.fetch_bungie_user(my_id)

await asyncio.gather(set(), fetch())
```

## When should you use which client?
* Use `Client` when you want to build a Chat Bot, Discord Bot, access data as Python classes.
* Use `RESTClient` when you want one TCP session for all clients, access data as JSON payloads.
* Use `RESTPool` when you're serving a large amount of connections and want to spawn a session for each,
access data as JSON payloads.
Note that setting up multiple TCP connections can be expensive.
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
from aiobungie.undefined import UNDEFINED
from aiobungie.undefined import UndefinedOr
from aiobungie.undefined import UndefinedType

from .metadata import __about__
from .metadata import __author__
from .metadata import __docs__
from .metadata import __email__
from .metadata import __license__
from .metadata import __url__
from .metadata import __version__

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
