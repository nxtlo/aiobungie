"""A simple example on how aiobungie functions."""

import aiobungie

client = aiobungie.Client("TOKEN")


async def fetch_me() -> None:

    # fetch a Destiny 2 Player.

    # NOTE that the name has to be the new bungie name
    # With the code as well like this one.

    # returns all Destiny 2 available memberships for the player.
    fate = await client.fetch_player("Fate怒", 4275)

    for member_ship in fate:
        # Check if the membership is Steam.
        if member_ship.type is aiobungie.MembershipType.STEAM:
            print(member_ship.name, member_ship.unique_name, member_ship.type)

    # Fetch a BungieNet user.
    user = await client.fetch_bungie_user(20315338)
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

    # Fetch a Destiny 1/2 clan.
    clan = await client.fetch_clan("Math Class")
    # You can use the from_id(1234) to fetch the clan givin an id.

    # Fetch the clan members's steam memberships.
    members = await clan.fetch_members()
    for m in members:
        print(m.unique_name, m.id, m.type)

    # Clan owner.
    if clan.owner:
        print(clan.owner.unique_name)

        datto = clan.owner

        # Fetch datto's profile.
        profile = await client.fetch_profile(
            datto.id,
            datto.type,
            # Return All profile components and all character components.
            *aiobungie.ComponentType.ALL_PROFILES.value,
            *aiobungie.ComponentType.ALL_CHARACTERS.value,
        )

        # A Mapping from each character id to a character object.
        if datto_characters := profile.characters:
            for character_id, character in datto_characters.items():
                print(f"ID: {character_id}: Character {character}")

                # Check if warlock
                if character.class_type is aiobungie.Class.WARLOCK:
                    # Do something with the warlock
                    ...


client.run(fetch_me())
