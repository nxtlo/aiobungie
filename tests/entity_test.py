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
import aiobungie
import pytest

from aiobungie import objects
from tests.config import TOKEN, types

class EntityTest(aiobungie.Client):
    def __init__(self, token: str) -> None:
        super().__init__(token=token)
    
    @pytest.mark.asyncio()
    async def place_definition(self) -> None:
        earth: objects.Entity = await self.fetch_entity(types['place_def'], int(aiobungie.Planet.EARTH))
        assert earth.name == "Earth"
        assert earth.description == "Mankind's cradle, full of shattered glory, ready to be reclaimed."
        assert earth.hash == 3747705955
        assert earth.index == 0


    @pytest.mark.asyncio()
    async def inventory_item_definition(self) -> None:

        thunderlord: objects.Entity = await self.fetch_entity(types['inventory_item_def'], 3325463374)

        assert thunderlord.name == "Thunderlord"
        assert thunderlord.description == "Undefined"
        assert thunderlord.about == "They return from fields afar. The eye has passed, the end nears. Do not fade quietly. Let thunder reign again."
        assert thunderlord.hash == 3325463374
        assert int(thunderlord.sub_type) == int(aiobungie.Item.MACHINE_GUN)
        assert int(thunderlord.damage) == int(aiobungie.DamageType.ARC)
        assert int(thunderlord.item_class) == int(aiobungie.Class.UNKNOWN)
        assert int(thunderlord.tier) == int(aiobungie.ItemTier.EXOTIC)
        assert thunderlord.index == 6472
        assert thunderlord.is_equippable is True
        assert thunderlord.has_icon is True
        assert thunderlord.lore_hash  == 3325463374
        assert thunderlord.bucket_type == int(aiobungie.Item.POWER)

        
    @pytest.mark.asyncio()
    async def activity_definition(self) -> None:
        scourge: objects.Entity = await self.fetch_entity(types['activity_def'], 548750096)
        
        assert scourge.name == "Scourge of the Past"
        assert scourge.index == 501
        assert scourge.hash == 548750096
        assert scourge.description == "Beneath the ruins of the Last City lies the Black Armory's most precious vault, now under siege by Siviks and his crew, the Kell's Scourge."
        assert scourge.has_icon is True
        
    
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
    coros = [client.inventory_item_definition(), client.place_definition()]
    await asyncio.gather(*coros)

client.run(main())