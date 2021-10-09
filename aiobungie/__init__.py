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

"""A Pythonic `async`/`await` framework / wrapper for interacting with the Bungie API.

A basic client based example.

```py
import aiobungie

# crates in aiobungie are implementations
# of Bungie's objects to provide
# more functionality.
# See aiobungie.crate to view all the implemented objects.

client = aiobungie.Client('YOUR_API_KEY')

async def main() -> None:
    users = await client.search_users('Indica')
    for user in users:
        if user.type is aiobungie.MembershipType.STEAM and user.code == 868:
            print('Found the user', user.name, user.id, user.type)

        try:
            character: aiobungie.crate.Character = await client.fetch_character(
                user.id, user.type, aiobungie.Class.HUNTER)
        except aiobungie.CharacterError as exc:
            print(f'Couldn't get {user.name}'s hunter character. Due to: {exc}')
        else:
            print(character.light, character.id, character.emblem, character.class_type)

client.run(main()) # or asyncio.run(main())
```

A basic REST only client.

The difference between base client and the REST one are:

* No Hight-Level concepts. Just interact with Bungie's API.
* All returned data are pure JSON objects from Bungie's API.
* No runtime assertions.

Which lets you to implement your own logic, classes objects to get the desired results.

```py
import aiobungie

async def main() -> None:
    # First player in the array. Always returns one player.

    # Using `async with` context manager to close the session properly.
    async with aiobungie.RESTClient("TOKEN") as rest:
        fetch_player = await rest.fetch_player('Fate怒#4275')
        print(*fetch_player)  # A JSON array of dict object
        for player in fetch_player:  # Iterate through the array.
            print(player['membershipId'], player['iconPath']) # Print the player id and icon path.
            for k, v in player.items(): # Key, Value
                print(k, v)

import asyncio
asyncio.run(main())
```

Should you use the base client or the REST client?
This returns to you. For an example if you're building a website.

You can use python as a REST API in the backend with the RESTClient since all returned object are JSON objects.
Which gives you the freedom to deserialize it and implement you own logic in the front-end.

Or of you're building a Discord bot for an example or something simple. The base client is the way to go.
"""


from __future__ import annotations

from aiobungie import crate
from aiobungie import interfaces
from aiobungie.client import Client
from aiobungie.error import *
from aiobungie.internal.enums import *
from aiobungie.rest import RESTClient

from ._info import __about__
from ._info import __author__
from ._info import __docs__
from ._info import __email__
from ._info import __license__
from ._info import __url__
from ._info import __version__

__all__ = [mod for mod in dir() if not mod.startswith("_")]  # type: ignore
