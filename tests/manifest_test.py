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

"""Bungie Manifest tests."""

import asyncio

import aiobungie
from aiobungie.ext import Manifest
from tests import config


class ClientTest(aiobungie.Client):
    def __init__(self, token: str) -> None:
        super().__init__(token=token)

    async def man_test(self) -> None:

        man: Manifest = await self.fetch_manifest()
        await man.download(force=True)

        print(
			man.get_raid_image(raid=aiobungie.Raid.DSC)
		)

client = ClientTest(config.TOKEN)

async def main() -> None:
	coros = [client.man_test()]
	await asyncio.gather(*coros)

if __name__ == "__main__":
	client.run(main())