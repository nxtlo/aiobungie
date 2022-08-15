# -*- coding: utf-8 -*-

"""An example on how to transfer items from a character to another."""

import aiobungie
from aiobungie.internal import helpers

client = aiobungie.Client("TOKEN")

HUNTER_ID = 4401
TITAN_ID = 4402
MEMBERSHIP_ID = 4403
MEMBERSHIP_TYPE = aiobungie.MembershipType.STEAM


async def fetch_my_titan() -> aiobungie.crate.CharacterComponent:
    """A helper function to fetch our titan character and return both character and inventory components."""
    return await client.fetch_character(
        MEMBERSHIP_ID,
        MEMBERSHIP_TYPE,
        TITAN_ID,
        # Titian character component and inventory component.
        [
            aiobungie.ComponentType.CHARACTERS,
            aiobungie.ComponentType.CHARACTER_INVENTORY,
        ],
    )


async def transfer() -> None:
    """A helper function to transfer our items from a character to another."""

    async with client.rest:
        my_titan = await fetch_my_titan()

        # Check if the inventory component is not empty.
        if inventory := my_titan.inventory:
            for item in inventory:
                # Try to transfer an item.
                if (
                    # Check if the item is One thousand Voices in our titan inventory.
                    item.hash == 2069224589
                    # Check if the item can be transferred.
                    and item.is_transferable
                ):
                    assert item.instance_id is not None

                    # Transfer the item.
                    try:
                        # ! Notes

                        # * A bearer access token must be provided to be able to
                        # * make OAuth2 requests otherwise this will not work.

                        # * To ensure items are transferred to your character
                        # * you must first transfer it to vault then from vault to character.

                        # * You can either use `asyncio.create_task(...)` or
                        # * builtin `helpers.awaits(...)` function to transfer items concurrently
                        # * to ensure you don't get ratelimited assuming You're serving hundereds of requests a minute.

                        await helpers.awaits(
                            client.rest.transfer_item(
                                "BEARER_TOKEN",
                                item.instance_id,
                                item.hash,
                                # From titan to vault.
                                TITAN_ID,
                                MEMBERSHIP_TYPE,
                                vault=True,
                            ),
                            client.rest.transfer_item(
                                "BEARER_TOKEN",
                                item.instance_id,
                                item.hash,
                                # From vault to hunter.
                                HUNTER_ID,
                                MEMBERSHIP_TYPE,
                            ),
                        )
                        print("Transferred item success!.")

                    # Handle the error.
                    except aiobungie.HTTPError as err:
                        print(f"Couldn't transfer item due to {err.message}.")
                        return

if __name__ == '__main__':
    client.run(transfer())
