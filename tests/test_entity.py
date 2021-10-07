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

import mock
import pytest

import aiobungie
from aiobungie import crate
from aiobungie.internal import helpers, assets


class TestEntity:
    # ABCs not being tested currently.
    @pytest.fixture()
    def entity(self):
        assert lambda: None


class TestInventoryItemEntity:
    @pytest.fixture()
    def item(self):
        return crate.InventoryEntity(
            net=mock.Mock(),
            hash=182371221,
            index=1223,
            name="Midnight Coup",
            description=helpers.Undefined,
            icon=None,
            has_icon=False,
            type=aiobungie.Item.WEAPON,
            sub_type=aiobungie.Item.HANDCANNON,
            type_name="Hand Cannon",
            water_mark=None,
            tier=aiobungie.ItemTier.LEGENDERY,
            tier_name="Legendery",
            bucket_type=aiobungie.Item.KINETIC,
            stats={},
            ammo_type=aiobungie.AmmoType.PRIMARY,
            lore_hash=123230123,
            item_class=aiobungie.Class.UNKNOWN,
            is_equippable=True,
            summary_hash=190230123,
            damage=aiobungie.DamageType.KINETIC,
            about="Best hand cannon in the game. :p",
            banner=assets.Image("someImagePath.jpg"),
        )

    def test_item_description_is_undefined(self, item) -> None:
        assert item.description is helpers.Undefined

    def test_item_types(self, item):
        assert item.sub_type is aiobungie.Item.HANDCANNON
        assert item.damage is aiobungie.DamageType.KINETIC
        assert item.item_class is aiobungie.Class.UNKNOWN
        assert item.tier is aiobungie.ItemTier.LEGENDERY
        assert item.bucket_type is aiobungie.Item.KINETIC

    def test_item_numbers(self, item):
        assert item.lore_hash == 123230123
        assert isinstance(item.hash, int) and item.hash == 182371221
        assert isinstance(item.index, int) and item.index == 1223

    def test_item_bool_stuff(self, item):
        assert item.is_equippable is True
        assert item.has_icon is False

    def test_int_over(self, item):
        assert int(item) == item.hash

    def test_str_over(self, item):
        assert str(item) == item.name
