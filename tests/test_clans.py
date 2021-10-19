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

from __future__ import annotations
import datetime

import mock
import pytest
from pytest import fixture

import aiobungie
from aiobungie import crate
from aiobungie.internal import helpers, assets


@fixture()
def mock_client():
    return mock.Mock(spec_set=aiobungie.Client)


class TestClanFeatures:
    @fixture()
    def obj(self):
        return crate.clans.ClanFeatures(
            max_members=200,
            max_membership_types=5,
            capabilities=3,
            membership_types=[
                aiobungie.MembershipType.STEAM,
                aiobungie.MembershipType.XBOX,
            ],
            invite_permissions=True,
            update_banner_permissions=True,
            update_culture_permissions=False,
            join_level=1,
        )

    def test_clan_has_features(self, obj):
        assert obj.invite_permissions is True
        assert obj.update_banner_permissions is True
        assert obj.update_culture_permissions is False
        assert obj.join_level >= 1

    def test_clan_meta(self, obj):
        assert obj.max_members >= 200
        assert obj.max_membership_types == 5
        assert (
            isinstance(obj.membership_types, list)
            and aiobungie.MembershipType.STEAM in obj.membership_types
        )
        assert obj.capabilities == 3

@fixture()
def mock_bungie_user() -> crate.user.PartialBungieUser:
    return mock.Mock(spec_set=crate.user.PartialBungieUser)

class TestClanMember:
    @fixture()
    def obj(self):
        return crate.ClanMember(
            net=mock_client,
            id=4432,
            name="thom",
            type=aiobungie.MembershipType.STEAM,
            icon=assets.Image("someIconPath.jpg"),
            is_public=True,
            group_id=998271,
            is_online=True,
            joined_at=datetime.datetime(2021, 9, 6),
            last_online=datetime.datetime(2021, 5, 1),
            code=5432,
            types=[aiobungie.MembershipType.STEAM, aiobungie.MembershipType.STADIA],
            last_seen_name="YOYONAME",
            bungie=mock_bungie_user
        )

    def test_clan_member_link(self, obj):
        # Need the enum type value here.
        assert obj.id, int(obj.type) in obj.link

    # Methods under always raises NotImplementedError
    # Since they requires OAuth2. I will probably implement them later.
    @pytest.mark.asyncio()
    async def test_clan_member_ban(self, obj):
        with pytest.raises(NotImplementedError):
            await obj.ban()

    @pytest.mark.asyncio()
    async def test_clan_member_unban(self, obj):
        with pytest.raises(NotImplementedError):
            await obj.unban()

    @pytest.mark.asyncio()
    async def test_clan_member_kick(self, obj):
        with pytest.raises(NotImplementedError):
            await obj.kick()

    def test_clan_member_meta(self, obj):
        assert (
            isinstance(obj.type, aiobungie.MembershipType)
            and obj.type == aiobungie.MembershipType.STEAM
        )


class TestClanOwner:
    types = [
        aiobungie.MembershipType.STADIA,
        aiobungie.MembershipType.STEAM,
        aiobungie.MembershipType.XBOX,
    ]

    @fixture()
    def obj(self):
        return crate.ClanMember(
            net=mock_client,
            group_id=123,
            id=2938,
            name="DiggaD",
            type=aiobungie.MembershipType.STEAM,
            icon=assets.Image("someIconPath.jpg"),
            is_public=True,
            joined_at=datetime.datetime(2021, 9, 6),
            last_online=datetime.datetime(2021, 5, 1),
            types=self.types,
            code=5432,
            last_seen_name="Some name",
            bungie=mock_bungie_user
        )

    def test_clan_owner_is_userlike(self, obj):
        assert issubclass(obj.__class__, crate.user.UserLike)

    def test_clan_owner_meta(self, obj):
        assert obj.id == 2938
        assert obj.type is aiobungie.MembershipType.STEAM
        assert all(types in obj.types for types in self.types)

    def test_clan_owner_int_over(self, obj):
        assert int(obj) == obj.id

    def test_clan_owner_str_over(self, obj):
        assert str(obj) == obj.last_seen_name

    def test_clan_owner_link(self, obj):
        assert obj.id, int(obj.type) in obj.link


class TestClan:
    @fixture()
    def obj(self, mock_client):
        mock_owner = mock.Mock(spec_set=crate.ClanMember)
        mock_features = mock.Mock(spec_set=crate.clans.ClanFeatures)
        return crate.Clan(
            net=mock_client,
            id=998271,
            type=aiobungie.GroupType.CLAN,
            name="Cool clan",
            created_at=datetime.datetime(2018, 9, 3, 11, 13, 12),
            member_count=2,
            motto=str(helpers.Undefined),
            is_public=True,
            banner=assets.Image("xxx.jpg"),
            avatar=assets.Image("zzz.jpg"),
            about="A cool clan.",
            tags=["Raids", "Tag", "Another tag"],
            owner=mock_owner,
            features=mock_features,
        )

    @pytest.mark.asyncio()
    def test_clan_owner_is_None(self, obj: crate.Clan):
        assert obj.owner is not None and isinstance(obj.owner, crate.ClanMember)
        obj.owner = None
        assert obj.owner is None

    @pytest.mark.asyncio()
    async def test_fetch_clan_member(self, obj):
        mock_member = mock.Mock(spec_set=crate.ClanMember)
        obj.net.request.fetch_clan_member = mock.AsyncMock(return_value=mock_member)
        member = await obj.fetch_member("DiggaD", aiobungie.MembershipType.STEAM)
        obj.net.request.fetch_clan_member.assert_awaited_once_with(
            obj.id, "DiggaD", aiobungie.MembershipType.STEAM
        )
        assert member is obj.net.request.fetch_clan_member.return_value

    @pytest.mark.asyncio()
    async def test_fetch_clan_members(self, obj):
        first_member = crate.ClanMember
        first_member.type = aiobungie.MembershipType.XBOX

        another_member = crate.ClanMember
        another_member.type = aiobungie.MembershipType.STEAM

        mock_members = mock.Mock(spec_set=[first_member, another_member])
        obj.net.request.fetch_clan_members = mock.AsyncMock(return_value=mock_members)
        members = await obj.fetch_members()

        assert members is not None
        assert obj.member_count == 2

        obj.net.request.fetch_clan_members.assert_awaited_once_with(
            obj.id, aiobungie.MembershipType.NONE
        )
        assert members is obj.net.request.fetch_clan_members.return_value

    @pytest.mark.asyncio()
    async def test_fetch_banned_clan_member(self, obj):
        with pytest.raises(NotImplementedError):
            await obj.fetch_banned_members()

    @pytest.mark.asyncio()
    async def test_fetch_pending_clan_member(self, obj):
        with pytest.raises(NotImplementedError):
            await obj.fetch_pending_members()

    @pytest.mark.asyncio()
    async def test_fetch_invited_clan_member(self, obj):
        with pytest.raises(NotImplementedError):
            await obj.fetch_invited_members()

    def test_clan_int_over(self, obj):
        assert int(obj) == obj.id

    def test_clan_str_over(self, obj):
        assert str(obj) == obj.name
