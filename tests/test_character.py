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
from aiobungie import url
from aiobungie.internal import assets


@pytest.fixture()
def mock_client():
    return mock.Mock(spec_set=aiobungie.Client)


class TestCharacterComponent:
    # ABCs are not being tested right now.
    @pytest.fixture()
    def obj(self):
        assert lambda: None


def init_titan_char():
    return crate.Character(
        net=mock_client,
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
        # TODO: Maybe return a dict like this during
        # Serielizing the data.
        stats={
            aiobungie.Stat.MOBILITY: 100,
            aiobungie.Stat.RECOVERY: 100,
            aiobungie.Stat.RESILIENCE: 23,
            aiobungie.Stat.INTELLECT: 29,
            aiobungie.Stat.STRENGTH: 78,
            aiobungie.Stat.DISCIPLINE: 67,
        },
    )


def init_hunter_char():
    return crate.Character(
        net=mock_client,
        id=2111,
        member_id=4321,
        member_type=aiobungie.MembershipType.STEAM,
        light=1260,
        gender=aiobungie.Gender.FEMALE,
        race=aiobungie.Race.HUMAN,
        emblem=assets.Image("emblempath.jpg"),
        emblem_icon=assets.Image("emblemiconpath.jpg"),
        emblem_hash=998877,
        last_played=datetime.datetime(2021, 8, 3),
        total_played_time="990 hours and 20 seconds.",
        class_type=aiobungie.Class.HUNTER,
        title_hash=None,
        level=50,
        stats={
            aiobungie.Stat.MOBILITY: 90,
            aiobungie.Stat.RECOVERY: 78,
            aiobungie.Stat.RESILIENCE: 63,
            aiobungie.Stat.INTELLECT: 70,
            aiobungie.Stat.STRENGTH: 50,
            aiobungie.Stat.DISCIPLINE: 40,
        },
    )


def init_warlock_char():
    return crate.Character(
        net=mock_client,
        id=2112,
        member_id=4321,
        member_type=aiobungie.MembershipType.STEAM,
        light=1320,
        gender=aiobungie.Gender.FEMALE,
        race=aiobungie.Race.AWOKEN,
        emblem=assets.Image("emblempath.jpg"),
        emblem_icon=assets.Image("emblemiconpath.jpg"),
        emblem_hash=998877,
        last_played=datetime.datetime(2021, 4, 6),
        total_played_time="1151 hours and 13 seconds.",
        class_type=aiobungie.Class.WARLOCK,
        title_hash=None,
        level=50,
        stats={
            aiobungie.Stat.MOBILITY: 100,
            aiobungie.Stat.RECOVERY: 88,
            aiobungie.Stat.RESILIENCE: 63,
            aiobungie.Stat.INTELLECT: 78,
            aiobungie.Stat.STRENGTH: 32,
            aiobungie.Stat.DISCIPLINE: 40,
        },
    )


class TestCharacter:
    @pytest.fixture()
    def obj(self):
        return init_warlock_char()

    def test_character_stats(self, obj):
        assert isinstance(obj.stats, dict) and obj.stats[aiobungie.Stat.MOBILITY] >= 100

    def test_char_meta(self, obj):
        assert isinstance(obj.emblem, assets.Image)
        assert (
            isinstance(obj.gender, aiobungie.Gender)
            and obj.gender is aiobungie.Gender.FEMALE
        )
        assert obj.race is aiobungie.Race.AWOKEN
        assert obj.light > 1300
        assert obj.member_type is aiobungie.MembershipType.STEAM
        assert obj.level == 50

    def test_char_times(self, obj):
        assert isinstance(obj.last_played, datetime.datetime)
        assert obj.last_played.year >= 2020 and obj.last_played.hour == 0
        assert "1151 hours" in obj.total_played_time


class TestProfile:
    # The reason im doing this because we're testing
    # The profile character here as well since some
    # methods requires a character object
    @pytest.fixture()
    def obj(self, mock_client):
        p = crate.Profile(
            id=4321,
            net=mock_client,
            name="Crit",
            type=aiobungie.MembershipType.STEAM,
            is_public=True,
            last_played=datetime.datetime(2021, 3, 8, 9, 20),
            # Order in the list is always TITAN, HUNTER, WARLOCk
            character_ids=[2110, 2111, 2112],
            power_cap=1360,
        )
        return p

    # TODO: implement this.
    @pytest.mark.asyncio()
    async def test_when_this_player_doesnt_have_a_titan(self, obj):
        ...

    @pytest.mark.asyncio()
    async def test_when_this_player_doesnt_have_a_hunter(self, obj):
        ...

    @pytest.mark.asyncio()
    async def test_when_this_player_doesnt_have_a_warlock(self, obj):
        ...

    @pytest.mark.asyncio()
    async def test_equip_item(self, obj):
        ...

    @pytest.mark.asyncio()
    async def test_equip_items(self, obj):
        ...

    def test_profile_meta(self, obj):
        assert obj.id == 4321
        assert obj.name == "Crit"
        assert obj.is_public is True
        assert isinstance(obj.character_ids, list)
        assert obj.character_ids is not None
