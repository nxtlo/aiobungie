# -*- coding: utf-8 -*-

"""
An example on how to transfer items from a character to another.

This example must be used for an authorized membership. See user_oauth2 example.
"""

import aiobungie
import asyncio

client = aiobungie.Client("TOKEN")

HUNTER_ID = 4401
TITAN_ID = 4402
MEMBERSHIP_ID = 4403
MEMBERSHIP_TYPE = aiobungie.MembershipType.STEAM


async def fetch_my_titan_inventory():
    """A helper function to fetch our titan character and return both character and inventory components."""
    character = await client.fetch_character(
        MEMBERSHIP_ID,
        MEMBERSHIP_TYPE,
        TITAN_ID,
        # This component type will fetch our character inventory.
        [
            aiobungie.ComponentType.CHARACTER_INVENTORY,
        ],
    )
    # No reason to return the inventory if it was empty.
    if not character.inventory:
        raise Exception("Character inventory is empty...", character.inventory)

    return character.inventory


async def transfer() -> None:
    """A helper function to transfer our items from a character to another."""

    inventory = await fetch_my_titan_inventory()

    for item in inventory:
        # Try to transfer the item.
        if (
            # Check if the item is One thousand Voices in our titan inventory.
            item.hash == 2069224589
            # Check if the item can be transferred.
            and item.transfer_status == aiobungie.TransferStatus.CAN_TRANSFER
            and item.instance_id is not None
        ):
            # Transfer the item.
            try:
                # ! NOTES

                # * A bearer access token must be provided to be able to
                # * make OAuth2 requests otherwise this will not work.

                # * To ensure items are transferred to your character
                # * you must first transfer it to vault then from vault to character.
                # * CHAR_HAS_WEAPON -> VAULT -> CHAR_NEEDS_WEAPON.

                await client.rest.transfer_item(
                    "auth-token",
                    item.instance_id,
                    item.hash,
                    # From titan to vault.
                    TITAN_ID,
                    MEMBERSHIP_TYPE,
                    vault=True,
                )
                await client.rest.transfer_item(
                    "auth-token",
                    item.instance_id,
                    item.hash,
                    # From vault to hunter.
                    HUNTER_ID,
                    MEMBERSHIP_TYPE,
                )
                print("Transferred item success!.")

            # Handle the error.
            except aiobungie.HTTPError as err:
                print(f"Couldn't transfer item: {err.message}.")
                pass


async def main() -> None:
    async with client.rest:
        await transfer()


if __name__ == "__main__":
    asyncio.run(main())
