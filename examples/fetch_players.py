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
from aiobungie.objects import Player, Profile, User

client = aiobungie.Client("YOUR_TOKEN_HERE")


async def fetch_me() -> None:

    # fetch a Destiny 2 Player and return the second player we find.

    fate: Player = await client.fetch_player(
        name="Fate",
        type=aiobungie.MembershipType.STEAM,  # Fetch only Steam players.
        position=3,
    )

    print(fate.name, fate.type, fate.id)

    fate_warlock: Profile = await client.fetch_profile(  # A Bungie user profile.
        fate.id,
        fate.type,
        component=aiobungie.Component.CHARECTERS,  # The component to return from the profile. We want the characters.
        character=aiobungie.Class.WARLOCK,  # The character we want to return is the warlock.
    )  # you can pass the data from the player's request to fetch the profile.
    # NOTE: you need to use the CHARACTERS component.

    print(
        fate_warlock.character.light,  # You'll actually need to access
        fate_warlock.character.id,  # The character from `character` variable.
        fate_warlock.character.race,
        fate_warlock.character.emblem,
        fate_warlock.character.url,
    )

    # Fetch a bungie user. its better to use the `from_id`
    # to fetch the exact profile since bungie doesn't
    # return all bungie users
    # a bungie user id looks like this 20315338
    user: User = await client.fetch_user_from_id(20315338)
    print(
        user.name,
        user.about,
        user.id,
        user.human_timedelta,
        user.steam_name,  # You can get the steam name if it exists.
    )


client.run(fetch_me())
