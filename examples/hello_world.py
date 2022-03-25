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

            # We store the membership to be able to use it in the future without having to fetch it again.
            client.metadata['membership'] = fate[0]

            # Fetch this membership's profile with all components.
            profile = await membership.fetch_self_profile(
                components=[aiobungie.ComponentType.ALL]
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
                    f"Last time you played it was {character.last_played}"
                )

async def fetch_my_equipments() -> None:

    # How to fetch your characters equipments.
    # This will fetch equipped weapons, ships, sparrows, emblems, etc.

    my_membership: aiobungie.crate.DestinyMembership = client.metadata['membership']

    # Fetch the profile bound to this membership.
    my_profile = await my_membership.fetch_self_profile(components=[aiobungie.ComponentType.CHARACTER_EQUIPMENT])

    assert my_profile.character_equipments is not None

    equipments = my_profile.character_equipments.values()

    for items in equipments:
        for equipment in items:
            print(
                f"Found item ID: {equipment.instance_id} "
                f"And its location is: {equipment.location} "
                f"And the item {'Can be transferred' if equipment.is_transferable else 'Cannot be transferred'}"
            )

async def main() -> None:
    await fetch_me()
    await fetch_my_equipments()

if __name__ == '__main__':
    client.run(main())
