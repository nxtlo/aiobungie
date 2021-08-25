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

"""A simple example to fetch or search for destiny 2 players."""


# There're different types to fetch someone
# You can fetch the bungie profile, Destiny 2 player, Bungie user.

import aiobungie
from aiobungie.crate import Character
from aiobungie.crate import Player
from aiobungie.crate import Profile
from aiobungie.crate import User

client = aiobungie.Client("YOUR_TOKEN_HERE")


async def fetch_me() -> None:

    # fetch a Destiny 2 Player.

    fate: Player = await client.fetch_player("Fate怒#4275")

    print(fate.name, fate.type, fate.id)

    fate_warlock: Character = await client.fetch_character(  # A Destiny 2 player character.
        fate.id,
        fate.type,
        character=aiobungie.Class.WARLOCK,  # The character we want to return is the warlock.
    )  # you can pass the data from the player's request to fetch the character.

    print(
        fate_warlock.light,
        fate_warlock.id,
        fate_warlock.race,
        fate_warlock.emblem,
        fate_warlock.url,
    )

    # Fetch a bungie user. its better to use the `from_id`
    # to fetch the exact profile since bungie doesn't
    # return all bungie users
    # a bungie user id looks like this 20315338
    user: User = await client.fetch_user(20315338)
    print(
        user.name,
        user.about,
        user.id,
        user.human_timedelta,
        user.steam_name,  # You can get the steam name if it exists.
    )

    # You can also fetch a profile then get the exact character.

    profile: Profile = await client.fetch_profile(
        4611686018484639825, aiobungie.MembershipType.STEAM
    )
    # Hunter
    hunter: Character = await profile.hunter()

    # Warlock
    # warlock: Character = await profile.warlock()

    # Titan
    # titan: Character = await profile.titan()

    print(hunter.id, hunter.light, hunter.gender, hunter.race is aiobungie.Race.HUMAN)


client.run(fetch_me())
