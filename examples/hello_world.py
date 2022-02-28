"""A simple example on how aiobungie functions."""

import aiobungie

client = aiobungie.Client("TOKEN")


async def fetch_me() -> None:

    # fetch a Destiny 2 Player.

    # NOTE that the name has to be the new bungie name
    # With the code as well like this one.

    # returns all Destiny 2 available memberships for the player.
    fate = await client.fetch_player("Fate怒", 4275)

    for membership in fate:
        print(membership)

        if membership.type is aiobungie.MembershipType.STEAM:
            print("Found steam membership!", membership)

            # Fetch this membership's profile with all components.
            profile = await membership.fetch_self_profile(
                components=[aiobungie.ComponentType.ALL]
            )

            # Print the profile characters component for this membership.
            print(profile.characters)


client.run(fetch_me())
