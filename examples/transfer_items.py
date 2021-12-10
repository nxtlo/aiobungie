# -*- coding: utf-8 -*-

"""An example on fetching a titan character, inventory and try to transfer an item to a hunter."""

import aiobungie
from aiobungie.internal import helpers


class ClientAware:
    def __init__(self) -> None:
        self.client = aiobungie.Client("TOKEN")
        self.membership_type = aiobungie.MembershipType.STEAM
        # Those are dummy ids, You should put yours here.
        self.membership_id = 4401
        self.titan_id = 2234
        self.hunter_id = 2235

    async def titan_worker(self) -> None:
        """A method that fetch the titan character and transfer an item to the hunter."""
        try:
            character_request = await self.client.fetch_character(
                self.membership_id,
                self.membership_type,
                self.titan_id,
                # Character component
                aiobungie.ComponentType.CHARACTERS,
                # Character's inventory component.
                aiobungie.ComponentType.CHARACTER_INVENTORY,
            )

            # Check if the titan character component is not None
            if titan := character_request.character:
                print(titan.emblem, titan.id, titan.class_type)

                # Check if the titan inventory component is not None.
                if inventory := character_request.inventory:
                    for item in inventory:
                        # Try to transfer an item.
                        if (
                            # Check if the item is One thousand Voices in our titan inventory.
                            item.hash == 2069224589
                            # Check if the item can be transferred.
                            and item.is_transferable
                        ):
                            assert item.instance_id is not None
                            # Try to transfer the item to hunter through the rest.
                            try:
                                # A bearer access token must be provided to be able to
                                # make OAuth2 requests otherwise this will not work.

                                # To ensure items are transferred to your character
                                # you must first transfer it to vault then from vault to character.

                                # You can either use `asyncio.create_task(...)` or
                                # builtin `helpers.awaits(...)` function to transfer items concurrently
                                # to ensure you don't get ratelimited assuming You're serving hundereds of requests a minute.

                                await helpers.awaits(
                                    self.client.rest.transfer_item(
                                        "BEARER_TOKEN",
                                        item.instance_id,
                                        item.hash,
                                        # From titan to vault.
                                        titan.id,
                                        titan.member_type,
                                        vault=True,
                                    ),
                                    self.client.rest.transfer_item(
                                        "BEARER_TOKEN",
                                        item.instance_id,
                                        item.hash,
                                        # From vault to hunter.
                                        self.hunter_id,
                                        self.membership_type,
                                    ),
                                )
                                print("Transferred item success!.")
                            except aiobungie.Unauthorized as err:
                                print("Can't tranfer item for unautorized users.", err)
                                pass

        except aiobungie.CharacterError:
            print(f"Couldn't find the titan for player id {self.membership_id}.")

    def run_it(self) -> None:
        """A method to run our titan worker."""
        self.client.run(self.titan_worker())


client = ClientAware()
client.run_it()
