# MIT License
#
# Copyright (c) 2020 - Present nxtlo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""A simple example with error handle."""

import asyncio
import logging

import aiobungie
from aiobungie.crate import Character


class HandleMyErrors:
    def __init__(self) -> None:
        self.type = aiobungie.MembershipType.STEAM
        self.id = 4611686018484639825

    async def my_titan(self) -> Character:
        try:
            async with aiobungie.Client("YOUR_TOKEN_HERE") as client:
                titan: Character = await client.fetch_character(
                    self.id, self.type, aiobungie.Class.TITAN
                )

        except aiobungie.CharacterError:
            logging.warn(f"Couldn't find the titan for player id {self.id}")

        return titan


handler = HandleMyErrors()
if __name__ == "__main__":
    loop = asyncio.get_event_loop().run_until_complete
    print(loop(handler.my_titan()))
