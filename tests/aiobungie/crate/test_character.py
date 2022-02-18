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

import datetime

import mock
import pytest

import aiobungie
from aiobungie import crate
from aiobungie.internal import assets
from aiobungie.internal import helpers


class TestDye:
    @pytest.fixture()
    def dye(self):
        return crate.Dye(channel_hash=123, dye_hash=321)

    def test_dye_hash(self, dye: crate.Dye):
        assert dye.dye_hash == 321

    def test_channel_hash(self, dye: crate.Dye):
        assert dye.channel_hash == 123


class TestCustomizationOptions:
    @pytest.fixture()
    def model(self) -> crate.CustomizationOptions:
        return crate.CustomizationOptions(
            personality=1,
            face=2,
            skin_color=3,
            lip_color=4,
            eye_color=5,
            hair_colors=[1, 2, 3, 4],
            feature_colors=[321, 345],
            decal_color=12445,
            wear_helmet=True,
            hair_index=2,
            feature_index=3,
            decal_index=4,
        )

    def test_personality(self, model: crate.CustomizationOptions):
        assert model.personality == 1

    def test_wears_helmet(self, model: crate.CustomizationOptions):
        assert model.wear_helmet

    def test_hair_colors(self, model: crate.CustomizationOptions):
        assert model.hair_colors == [1, 2, 3, 4]


class TestMinimalEquipments:
    @pytest.fixture()
    def equipment(self) -> crate.MinimalEquipments:
        return crate.MinimalEquipments(
            net=mock.Mock(),
            item_hash=123,
            dyes=[mock.Mock(spec_set=crate.Dye), mock.Mock(spec_set=crate.Dye)],
        )

    def test_item_hash(self, equipment: crate.MinimalEquipments):
        assert equipment.item_hash == 123

    def test_dyes(self, equipment: crate.MinimalEquipments):
        assert equipment.dyes

    @pytest.mark.asyncio()
    async def test_fetch_my_item(self, equipment: crate.MinimalEquipments) -> None:
        equipment.net.request.fetch_inventory_item = mock.AsyncMock()
        item = await equipment.fetch_my_item()

        equipment.net.request.fetch_inventory_item.assert_awaited_once_with(
            equipment.item_hash
        )
        assert item is equipment.net.request.fetch_inventory_item.return_value


class TestRenderedData:
    @pytest.fixture()
    def model(self) -> crate.RenderedData:
        return crate.RenderedData(
            net=mock.Mock(),
            custom_dyes=[mock.Mock(spec_set=crate.Dye), mock.Mock(spec_set=crate.Dye)],
            customization=mock.Mock(spec_set=crate.CustomizationOptions),
            equipment=[mock.Mock(item_hash=123), mock.Mock(item_hash=321)],
        )

    def test_custom_dyes(self, model: crate.RenderedData):
        assert model.custom_dyes

    @pytest.mark.asyncio()
    async def test_fetch_my_items(self, model: crate.RenderedData) -> None:
        model.net.request.fetch_inventory_item = mock.AsyncMock()
        helpers.awaits = mock.AsyncMock()

        items = await model.fetch_my_items()
        assert all(
            item is model.net.request.fetch_inventory_item.return_value
            for item in items
        )
        model.net.request.fetch_inventory_item.assert_has_calls([])


class TestCharacterProgression:
    @pytest.fixture()
    def model(self) -> crate.CharacterProgression:
        return crate.CharacterProgression(
            progressions={0: mock.Mock()},
            factions={1: mock.Mock()},
            milestones={2: mock.Mock()},
            checklists={3: mock.Mock()},
            seasonal_artifact=mock.Mock(spec=crate.CharacterScopedArtifact),
            uninstanced_item_objectives={4: [mock.Mock()]},
        )

    def test_progressions(self, model: crate.CharacterProgression) -> None:
        with mock.patch.object(model, "progressions", new={0: mock.Mock()}) as progress:
            assert model.progressions == progress

    def test_factions(self, model: crate.CharacterProgression) -> None:
        with mock.patch.object(model, "factions", new={1: mock.Mock()}) as factions:
            assert model.factions == factions

    def test_milestones(self, model: crate.CharacterProgression) -> None:
        with mock.patch.object(model, "milestones", new={2: mock.Mock()}) as milestone:
            assert model.milestones == milestone

    def test_checklists(self, model: crate.CharacterProgression) -> None:
        with mock.patch.object(model, "checklists", new={3: mock.Mock()}) as checklist:
            assert model.checklists == checklist


class TestCharacter:
    @pytest.fixture()
    def model(self) -> crate.Character:
        return crate.Character(
            net=mock.Mock(),
            id=2110,
            member_id=4321,
            member_type=aiobungie.MembershipType.STEAM,
            light=1310,
            gender=aiobungie.Gender.MALE,
            race=aiobungie.Race.EXO,
            emblem=assets.Image("emblempath.jpg"),
            emblem_icon=assets.Image("emblemiconpath.jpg"),
            emblem_hash=998877,
            last_played=datetime.datetime(2021, 9, 1),
            total_played_time="1100 hours and 9 seconds.",
            class_type=aiobungie.Class.TITAN,
            title_hash=None,
            level=50,
            stats={
                aiobungie.Stat.MOBILITY: 100,
                aiobungie.Stat.RECOVERY: 100,
                aiobungie.Stat.RESILIENCE: 23,
                aiobungie.Stat.INTELLECT: 29,
                aiobungie.Stat.STRENGTH: 78,
                aiobungie.Stat.DISCIPLINE: 67,
            },
        )

    def test___int__(self, model: crate.Character) -> None:
        assert int(model) == model.id

    def test_url(self, model: crate.Character) -> None:
        assert (
            model.url
            == f"{aiobungie.url.BASE}/en/Gear/{int(model.member_type)}/{model.member_id}/{model.id}"
        )

    def test_stats(self, model: crate.Character) -> None:
        assert (
            aiobungie.Stat.MOBILITY in model.stats
            and model.stats[aiobungie.Stat.RECOVERY] == 100
        )

    def test_title_hash(self, model: crate.Character) -> None:
        assert model.title_hash is None

    def test_emblem(self, model: crate.Character) -> None:
        assert model.emblem.url == assets.Image("emblempath.jpg").url

    def test_emblem___str__(self, model: crate.Character) -> None:
        assert str(model.emblem) == str(assets.Image("emblempath.jpg"))

    def test_emblem_icon(self, model: crate.Character) -> None:
        assert model.emblem_icon.url == assets.Image("emblemiconpath.jpg").url

    @pytest.mark.asyncio()
    async def test_fetch_activities(self, model: crate.Character) -> None:
        model.net.request.fetch_activities = mock.AsyncMock()
        activities = await model.fetch_activities(aiobungie.GameMode.RAID)
        model.net.request.fetch_activities.assert_called_once_with(
            model.member_id,
            model.id,
            aiobungie.GameMode.RAID,
            membership_type=model.member_type,
            limit=250,
            page=0,
        )
        assert activities is model.net.request.fetch_activities.return_value

    @pytest.mark.asyncio()
    async def test_transfer_item(self, model: crate.Character) -> None:
        model.net.request.rest.transfer_item = mock.AsyncMock()
        await model.transfer_item(
            "token",
            item_id=123,
            item_hash=293,
        )
        model.net.request.rest.transfer_item.assert_called_once_with(
            "token",
            item_id=123,
            character_id=model.id,
            item_hash=293,
            member_type=model.member_type,
            vault=False,
            stack_size=1,
        )

    @pytest.mark.asyncio()
    async def test_pull_item(self, model: crate.Character) -> None:
        model.net.request.rest.pull_item = mock.AsyncMock()
        await model.pull_item(
            "token",
            item_id=123,
            item_hash=293,
        )
        model.net.request.rest.pull_item.assert_called_once_with(
            "token",
            item_id=123,
            character_id=model.id,
            item_hash=293,
            member_type=model.member_type,
            vault=False,
            stack_size=1,
        )

    @pytest.mark.asyncio()
    async def test_equip_item(self, model: crate.Character) -> None:
        model.net.request.rest.equip_item = mock.AsyncMock()
        await model.equip_item(
            "token",
            123,
        )
        model.net.request.rest.equip_item.assert_called_once_with(
            "token",
            item_id=123,
            character_id=model.id,
            membership_type=model.member_type,
        )

    @pytest.mark.asyncio()
    async def test_equip_items(self, model: crate.Character) -> None:
        model.net.request.rest.equip_items = mock.AsyncMock()
        await model.equip_items(
            "token",
            [123, 234],
        )
        model.net.request.rest.equip_items.assert_called_once_with(
            "token",
            item_ids=[123, 234],
            character_id=model.id,
            membership_type=model.member_type,
        )
