"""A simple example on how aiobungie functions."""

import aiobungie

client = aiobungie.Client("...")

async def fetch_me() -> None:

    # fetch a Destiny 2 Player.

    # returns all Destiny 2 available memberships for the player.
    async with client.rest:
        fate = await client.fetch_player("Fate怒", 4275)

        # Iterate over all memberships.
        for membership in fate:
            print(membership)

            # A player cant have multiple memberships, Check if the membership is steam.
            if membership.type is aiobungie.MembershipType.STEAM:
                print("Found steam membership!", membership)

                # Fetch this membership's profile with all components.
                profile = await membership.fetch_self_profile(
                    components=[aiobungie.ComponentType.CHARACTERS]
                )

                assert profile.characters is not None

                # Print the profile characters component for this membership.
                for character in profile.characters.values():
                    print(
                        f"Found character ID: {character.id} "
                        f"Class {character.class_type} "
                        f"Race: {character.race} "
                        f"Gender: {character.gender} "
                        f"Light Power: {character.light} "
                        f"Last time you played it was: {character.last_played}"
                    )

if __name__ == '__main__':
    client.run(fetch_me())
