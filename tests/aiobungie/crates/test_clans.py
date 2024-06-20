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
from aiobungie import crates
from aiobungie.internal import assets


class TestClanFeatures:
    @pytest.fixture()
    def obj(self):
        return crates.ClanFeatures(
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

    def test_clan_has_features(self, obj: crates.ClanFeatures):
        assert obj.invite_permissions is True
        assert obj.update_banner_permissions is True
        assert obj.update_culture_permissions is False
        assert obj.join_level >= 1

    def test_clan_max_members(self, obj: crates.ClanFeatures):
        assert obj.max_members == 200

    def test_clan_max_membership_types(self, obj: crates.ClanFeatures):
        assert obj.max_membership_types == 5

    def test_clan_capabilities(self, obj: crates.ClanFeatures):
        assert obj.capabilities == 3


class TestClanConversation:
    @pytest.fixture()
    def model(self):
        return crates.ClanConversation(
            group_id=123,
            id=456,
            name="cool convo chat",
            chat_enabled=True,
            security=1,
        )


class TestClanBanner:
    @pytest.fixture()
    def model(self):
        return crates.ClanBanner(
            id=2934,
            foreground=assets.Image(path="brrr.png"),
            background=assets.Image(path="xo.jpg"),
        )

    def test_foreground(self, model: crates.ClanBanner):
        assert model.foreground.__str__() == assets.Image(path="brrr.png").url

    def test_background(self, model: crates.ClanBanner):
        assert model.background.__str__() == assets.Image(path="xo.jpg").url


class TestClanMember:
    @pytest.fixture()
    def obj(self):
        mock_bungie_user = mock.Mock(crates.PartialBungieUser)
        return crates.ClanMember(
            app=mock.Mock(),
            id=4432,
            name="thom",
            type=aiobungie.MembershipType.STEAM,
            icon=assets.Image(path="someIconPath.jpg"),
            is_public=True,
            group_id=998271,
            is_online=True,
            joined_at=datetime.datetime(2021, 9, 6),
            last_online=datetime.datetime(2021, 5, 1),
            code=None,
            types=[aiobungie.MembershipType.STEAM, aiobungie.MembershipType.STADIA],
            last_seen_name="YOYONAME",
            bungie_user=mock_bungie_user,
            crossave_override=aiobungie.MembershipType.STADIA,
            member_type=aiobungie.ClanMemberType.ADMIN,
        )

    def test_is_admin_property(self, obj: crates.ClanMember):
        assert obj.is_admin is True

    def test_is_founder_property(self, obj: crates.ClanMember):
        assert not obj.is_founder

    @pytest.mark.asyncio()
    async def test_fetch_clan(self, obj: crates.ClanMember):
        obj.app.request.fetch_clan_from_id = mock.AsyncMock()

        assert await obj.fetch_clan() is obj.app.request.fetch_clan_from_id.return_value

        assert obj.app.request.fetch_clan_from_id.call_count == 1

        obj.app.request.fetch_clan_from_id.assert_awaited_once_with(obj.group_id)

    @pytest.mark.asyncio()
    async def test_clan_member_ban(self, obj: crates.ClanMember): ...

    @pytest.mark.asyncio()
    async def test_clan_member_unban(self, obj: crates.ClanMember): ...

    @pytest.mark.asyncio()
    async def test_clan_member_kick(self, obj: crates.ClanMember): ...


class TestGroupMember:
    @pytest.fixture()
    def obj(self):
        mock_membership = mock.Mock(crates.DestinyMembership)
        mock_group = mock.Mock(crates.Clan, id=1234)

        return crates.GroupMember(
            inactive_memberships=None,
            member_type=aiobungie.ClanMemberType.ADMIN,
            is_online=True,
            last_online=datetime.datetime(2021, 5, 1),
            member=mock_membership,
            group=mock_group,
            group_id=3342,
            join_date=datetime.datetime(2021, 9, 6),
        )

    def test_group_id(self, obj: crates.GroupMember):
        assert obj.group.id == 1234

    @pytest.mark.asyncio()
    async def test_fetch_self_clan(self, obj: crates.GroupMember): ...


class TestClan:
    @pytest.fixture()
    def obj(self):
        mock_owner = mock.Mock(spec_set=crates.ClanMember)
        mock_features = mock.Mock(spec_set=crates.clans.ClanFeatures)
        return crates.Clan(
            app=mock.Mock(),
            id=998271,
            type=aiobungie.GroupType.CLAN,
            name="Cool clan",
            created_at=datetime.datetime(2018, 9, 3, 11, 13, 12),
            member_count=2,
            motto="Cool motto",
            is_public=True,
            banner=assets.Image(path="xxx.jpg"),
            avatar=assets.Image(path="zzz.jpg"),
            about="A cool clan.",
            tags=["Raids", "Tag", "Another tag"],
            owner=mock_owner,
            features=mock_features,
            theme="SomeClanTheme",
            allow_chat=True,
            chat_security=1,
            conversation_id=12345,
            progressions={},
            banner_data={},
            call_sign="C",
            current_user_membership=mock.Mock({"Steam": mock.Mock(crates.ClanMember)}),
        )

    def test_clan_tags(self, obj: crates.Clan):
        assert obj.tags == ["Raids", "Tag", "Another tag"]

    def test_clan_member_count(self, obj: crates.Clan):
        assert obj.member_count == 2

    def test_clan_about(self, obj: crates.Clan):
        assert obj.about == "A cool clan."

    @pytest.mark.asyncio()
    async def test_fetch_clan_members(self, obj: crates.Clan):
        first_member = mock.Mock(spec_set=crates.ClanMember)
        first_member.type = aiobungie.MembershipType.XBOX

        another_member = mock.Mock(spec_set=crates.ClanMember)
        another_member.type = aiobungie.MembershipType.STEAM

        mock_members = mock.Mock(spec_set=[first_member, another_member])
        obj.app.request.fetch_clan_members = mock.AsyncMock(return_value=mock_members)
        members = await obj.fetch_members()

        obj.app.request.fetch_clan_members.assert_awaited_once_with(
            obj.id, type=aiobungie.MembershipType.NONE, name=None
        )
        assert members is obj.app.request.fetch_clan_members.return_value
