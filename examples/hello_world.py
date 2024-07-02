"""A simple example on how aiobungie functions."""

import aiobungie
import asyncio

client = aiobungie.Client("...")


async def fetch_me() -> None:
    # Fetch all Destiny 2 available memberships bound to a player.
    async with client.rest:
        memberships = await client.fetch_membership("Fate怒", 4275)

        # Iterate over all memberships.
        for membership in memberships:
            print(membership)

            # A player may have multiple memberships, check if the membership is steam.
            if membership.type is aiobungie.MembershipType.STEAM:
                print(f"Found steam membership! {membership!s}")


if __name__ == "__main__":
    asyncio.run(fetch_me())
