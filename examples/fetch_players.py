"""A simple example on how aiobungie functions."""

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

    # returns a Destiny user which includes all available memberships for the player.
    fate = await client.fetch_player("Fate怒#4275")

    for member_ship in fate:
        # You should always check if one of the memberships are not None
        # So you don't get NoneType errors thrown.
        if member_ship is not None:
            print(member_ship.name, member_ship.unique_name, member_ship.type, ...)

            # Check if the membership in the sequence is our steam membership and its not None.
            if member_ship.type is aiobungie.MembershipType.STEAM:
                fate_steam = member_ship

                fate_warlock: crate.Character = await client.fetch_character(  # returns a Destiny 2 player character.
                    fate_steam.id,
                    fate_steam.type,
                    character=aiobungie.Class.WARLOCK,  # The character we want to return is the warlock.
                )  # you can pass the data from the player's request to fetch the character.

    # Show the warlock data.
    print(
        fate_warlock.light,
        fate_warlock.id,
        fate_warlock.race,
        fate_warlock.emblem,
        fate_warlock.url,
    )

    # Fetch a bungie user.
    # A Bungie user id looks like this 20315338.
    user = await client.fetch_user(20315338)
    print(
        user.name,
        user.about,
        user.id,
        # Those fields may be None if the user doesn't have
        # The platforms.
        user.steam_name,
        user.stadia_name,
        user.blizzard_name,
        user.psn_name,
    )

    clan = await client.fetch_clan("Fast")  # returns a Destiny 1/2 clan.
    # You can use the from_id(1234) to fetch the clan givin an id.

    # Fetching the members is kinda expensive operation
    # since they're http requests. You can implement your own cache
    # strategy to cache the members instead of making an http request
    # every time.

    members = await clan.fetch_members()  # get the clan members.
    for m in members:
        print(m.unique_name, m.code, m.id, m.type)

    specific_member = await clan.fetch_member(
        "Bj"
    )  # get a player name starts with or has Bj.
    print(specific_member.name, specific_member.id)

    # You can also fetch a profile then get the exact character.

    profile = await client.fetch_profile(
        4611686018484639825, aiobungie.MembershipType.STEAM
    )
    # Hunter
    hunter = await profile.fetch_hunter()

    # Warlock
    # warlock = await profile.fetch_warlock()

    # Titan
    # titan = await profile.fetch_titan()

    print(hunter.id, hunter.light, hunter.gender, hunter.race is aiobungie.Race.HUMAN)


client.run(fetch_me())
