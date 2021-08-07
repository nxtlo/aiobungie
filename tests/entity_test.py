# -*- coding: utf-8 -*-
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

import asyncio

import pytest

import aiobungie
from aiobungie import objects
from tests.config import TOKEN
from tests.config import types


class EntityTest(aiobungie.Client):
    def __init__(self, token: str) -> None:
        super().__init__(token=token)

    #     @pytest.mark.asyncio()
    #     async def place_definition(self) -> None:
    #         earth: objects.Entity = await self.fetch_entity(types['place_def'], int(aiobungie.Planet.EARTH))
    #         assert earth.name == "Earth"
    #         assert earth.description == "Mankind's cradle, full of shattered glory, ready to be reclaimed."
    #         assert earth.hash == 3747705955
    #         assert earth.index == 0
    #

    @pytest.mark.asyncio()
    async def inventory_item_test(self) -> None:

        thunderlord: objects.InventoryEntity = await self.fetch_inventory_item(
            3325463374
        )

        print(thunderlord.name)
        print(thunderlord.description)
        print(thunderlord.about)
        print(thunderlord.hash)
        print(thunderlord.sub_type is aiobungie.Item.MACHINE_GUN)
        print(thunderlord.damage is aiobungie.DamageType.ARC)
        print(thunderlord.item_class is aiobungie.Class.UNKNOWN)
        print(thunderlord.tier is aiobungie.ItemTier.EXOTIC)
        print(thunderlord.index)
        print(thunderlord.is_equippable)
        print(thunderlord.has_icon)
        print(thunderlord.lore_hash)
        print(thunderlord.bucket_type)

    #  @pytest.mark.asyncio()
    #  async def activity_definition(self) -> None:
    #      scourge: objects.Entity = await self.fetch_entity(types['activity_def'], 548750096)
    #
    #      assert scourge.name == "Scourge of the Past"
    #      assert scourge.index == 501
    #      assert scourge.hash == 548750096
    #      assert scourge.description == "Beneath the ruins of the Last City lies the Black Armory's most precious vault, now under siege by Siviks and his crew, the Kell's Scourge."
    #      assert scourge.has_icon is True

    @pytest.mark.asyncio()
    async def activity_type_definition(self) -> None:
        ...

    @pytest.mark.asyncio()
    async def activity_mode_definition(self) -> None:
        ...

    @pytest.mark.asyncio()
    async def class_definition(self) -> None:
        ...

    @pytest.mark.asyncio()
    async def item_bucket_definition(self) -> None:
        ...

    @pytest.mark.asyncio()
    async def milestone_definition(self) -> None:
        ...


client = EntityTest(TOKEN)


async def main() -> None:
    coros = [client.inventory_item_test()]
    await asyncio.gather(*coros)


client.run(main())
