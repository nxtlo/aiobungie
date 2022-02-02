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

Example
-------
A Basic aiobungie API client.

```py
import aiobungie

# crates in aiobungie are implementations
# of Bungie's objects to provide
# more functionality.
# See aiobungie.crate to view all the implemented objects.

client = aiobungie.Client('YOUR_API_KEY')

# An example on how to search for Destiny 2 users/memberships and get their characters.
async def main() -> None:
    users = await client.search_users('Fate')
    for user in users:
        if user.code == 868:
            print('Found the desired user!', user.name, user.bungie_id)

            # Iterate through the user's memberships.
            for membership in user.memberships:
                if membership.type is aiobungie.MembershipType.STEAM:
                    try:
                        # Fetch the membership's profile and get characters component.
                        my_profile = await membership.fetch_self_profile(aiobungie.ComponentType.CHARACTERS)

                    # Handle the error.
                    except aiobungie.CharacterError as exc:
                        print(f'Couldn't get {user.name}'s characters. Due to: {exc.message}')
                        return

                    else:
                        # Will return a Mapping from the character's id to `aiobungie.crate.Character` object.
                        for character_id, character in my_profile.characters.items():
                            print(character_id, character)

client.run(main()) # or asyncio.run(main())
```

A basic RESTful client.

The difference between base client and the REST one are:

* No Hight-Level concepts. Just interact with the API.
* All returned data are pure JSON objects from Bungie's API.
* No runtime assertions.

Which lets you to implement your own logic, classes objects to get the desired results.

```py
import aiobungie

async def main() -> None:
    # Using `async with` context manager to close the session properly.
    async with aiobungie.RESTClient("TOKEN") as rest:
        # Fetch the memberships of a Destiny 2 player.
        payload = await rest.fetch_player('Fate怒', 4275)
        print(*payload)  # A JSON array of dict objects of our memberships.

        for membership in payload:
            # Print the ID and icon path of each membership.
            print(membership['membershipId'], membership['iconPath'])

            # Printing the icon URL.
            icon_url = aiobungie.Image(membership['iconPath'])
            print(icon_url)

            for k, v in membership.items(): # key, value
                print(k, v)

import asyncio
asyncio.run(main())
```

Should you use the base client or the REST client?
This returns to you. For an example if you're building a website.

You can use python as a REST API in the backend with the RESTClient since all returned object are JSON objects.
Which gives you the freedom to deserialize it and implement your own logic in the front-end.

Or of you're building a Discord bot for an example or something simple. The base client is the way to go.
"""


from __future__ import annotations

from aiobungie import crate
from aiobungie import interfaces
from aiobungie import traits
from aiobungie import typedefs
from aiobungie import url
from aiobungie.client import Client
from aiobungie.error import *
from aiobungie.internal.assets import Image
from aiobungie.internal.enums import *
from aiobungie.internal.factory import Factory
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

# Activity enums
from .crate.activity import Diffculity

# Components enums
from .crate.components import ComponentFields
from .crate.components import ComponentPrivacy

# Entity enums
from .crate.entity import GatingScope
from .crate.entity import ValueUIStyle

# Fireteam enums.
from .crate.fireteams import FireteamActivity
from .crate.fireteams import FireteamDate
from .crate.fireteams import FireteamLanguage
from .crate.fireteams import FireteamPlatform

# Records enums
from .crate.records import RecordState

__all__ = [mod for mod in dir() if not mod.startswith("_")]  # type: ignore
