"""A simple example on how aiobungie functions."""

import aiobungie

client = aiobungie.Client("...")


async def fetch_me() -> None:
    # fetch a Destiny 2 membership.

    # returns all Destiny 2 available memberships for the player.
    async with client.rest:
        memberships = await client.fetch_player("Fate怒", 4275)

        # Iterate over all memberships.
        for membership in memberships:
            print(membership)

            # A player cant have multiple memberships, Check if the membership is steam.
            if membership.type is aiobungie.MembershipType.STEAM:
                print(f"Found steam membership! {membership}")


if __name__ == "__main__":
    client.run(fetch_me())
