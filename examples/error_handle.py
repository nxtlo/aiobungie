import asyncio
import logging

import aiobungie
from aiobungie.crate import Character


class HandleMyErrors:
    def __init__(self) -> None:
        self.type = aiobungie.MembershipType.STEAM
        self.id = 4611686018484639825
        self.client = aiobungie.Client("YOUR_TOKEN_HERE")

    async def my_titan(self) -> Character:
        try:
            titan: Character = await self.client.fetch_character(
                self.id, self.type, aiobungie.Class.TITAN
            )
        except aiobungie.CharacterError:
            logging.warn(f"Couldn't find the titan for player id {self.id}")

        return titan


handler = HandleMyErrors()
if __name__ == "__main__":
    loop = asyncio.get_event_loop().run_until_complete
    print(loop(handler.my_titan()))
