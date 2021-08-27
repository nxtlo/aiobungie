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

from typing import Sequence

import aiobungie
from aiobungie import crate

# crates in aiobungie are used to organaize
# The flow and how aiobungie is structured
# for simplecity and performance


client = aiobungie.Client("YOUR_TOKEN_HERE")


async def fetch_me() -> None:

    # fetch a Destiny 2 Player.

    # NOTE that the name has to be the new bungie name
    # With the code as well like this one.
    fate: crate.Player = await client.fetch_player(
        "Fate怒#4275"
    )  # returns a Destiny 2 Player crate.

    print(fate.name, fate.type, fate.id)

    fate_warlock: crate.Character = await client.fetch_character(  # returns a Destiny 2 player character crate.
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
    user: crate.User = await client.fetch_user(20315338)  # Returns a Bungie user crate.
    print(
        user.name,
        user.about,
        user.id,
        user.human_timedelta,
        user.steam_name,  # You can get the steam name if it exists.
    )

    clan: crate.Clan = await client.fetch_clan(
        "Fast"
    )  # returns a Destiny 1/2 clan crate.
    # You can use the from_id(1234) to fetch the clan givin an id.

    # Fetching the members is kinda expensive operation
    # since they're http requests. You can implement your own cache
    # strategy to cache the members instead of making an http request
    # every time.

    members: Sequence[
        crate.ClanMember
    ] = await clan.fetch_members()  # get the clan members.
    for m in members:
        print(m.unique_name, m.code, m.id, m.type)

    specific_member: crate.ClanMember = await clan.fetch_member(
        "Bj"
    )  # get a player name starts with or has Bj.
    print(specific_member.name, specific_member.id)

    # You can also fetch a profile then get the exact character.

    profile: crate.Profile = await client.fetch_profile(
        4611686018484639825, aiobungie.MembershipType.STEAM
    )
    # Hunter
    hunter: crate.Character = await profile.hunter()

    # Warlock
    # warlock: Character = await profile.warlock()

    # Titan
    # titan: Character = await profile.titan()

    print(hunter.id, hunter.light, hunter.gender, hunter.race is aiobungie.Race.HUMAN)


client.run(fetch_me())
