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


class TestClanFeatures:
    @pytest.fixture()
    def obj(self):
        return crate.ClanFeatures(
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

    def test_clan_has_features(self, obj: crate.ClanFeatures):
        assert obj.invite_permissions is True
        assert obj.update_banner_permissions is True
        assert obj.update_culture_permissions is False
        assert obj.join_level >= 1

    def test_clan_max_members(self, obj: crate.ClanFeatures):
        assert obj.max_members == 200

    def test_clan_max_membership_types(self, obj: crate.ClanFeatures):
        assert obj.max_membership_types == 5

    def test_clan_capabilities(self, obj: crate.ClanFeatures):
        assert obj.capabilities == 3


class TestClanCoversation:
    @pytest.fixture()
    def model(self):
        return crate.ClanConversation(
            net=mock.Mock(),
            group_id=123,
            id=456,
            name="cool convo chat",
            chat_enabled=True,
            security=1,
        )

    def test___int__(self, model: crate.ClanConversation):
        assert int(model) == 456

    def test___str__(self, model: crate.ClanConversation):
        assert str(model) == "cool convo chat"

    @pytest.mark.asyncio()
    async def test_edit(self, model: crate.ClanConversation):
        model.net.request.rest.edit_optional_conversation = convo = mock.AsyncMock()

        await model.edit("token", name="new cool name", security=0, enable_chat=False)

        convo.assert_awaited_once_with(
            "token",
            model.group_id,
            model.id,
            name="new cool name",
            security=0,
            enable_chat=False,
        )


class TestClanBanner:
    @pytest.fixture()
    def model(self):
        return crate.ClanBanner(
            id=2934,
            foreground=assets.Image("brrr.png"),
            background=assets.Image("xo.jpg"),
        )

    def test___int__(self, model: crate.ClanBanner):
        assert int(model) == 2934

    def test_foreground(self, model: crate.ClanBanner):
        assert model.foreground.__str__() == assets.Image("brrr.png").url

    def test_background(self, model: crate.ClanBanner):
        assert model.background.__str__() == assets.Image("xo.jpg").url


class TestClanMember:
    @pytest.fixture()
    def obj(self):
        mock_bungie_user = mock.Mock(crate.PartialBungieUser)
        return crate.ClanMember(
            net=mock.Mock(),
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
            bungie=mock_bungie_user,
            crossave_override=1,
            member_type=aiobungie.ClanMemberType.ADMIN,
        )

    def test_clan_member___int__(self, obj: crate.ClanMember):
        assert int(obj) == 4432

    def test_clan_member___str__(self, obj: crate.ClanMember):
        assert str(obj) == "thom#5432"

    def test_clan_member___str__when_code_is_None(self, obj: crate.ClanMember):
        obj.code = None
        assert str(obj) == "thom#None"

    def test_clan_member___str__when_name_is_Undeined(self, obj: crate.ClanMember):
        obj.name = aiobungie.UNDEFINED
        assert str(obj) == "UNDEFINED#5432"

    def test_is_admin_property(self, obj: crate.ClanMember):
        assert obj.is_admin is True

    def test_is_founder_property(self, obj: crate.ClanMember):
        assert not obj.is_founder

    @pytest.mark.asyncio()
    async def test_fetch_clan(self, obj: crate.ClanMember):
        obj.net.request.fetch_clan_from_id = mock.AsyncMock()

        assert await obj.fetch_clan() is obj.net.request.fetch_clan_from_id.return_value

        assert obj.net.request.fetch_clan_from_id.call_count == 1

        obj.net.request.fetch_clan_from_id.assert_awaited_once_with(obj.group_id)

    @pytest.mark.asyncio()
    async def test_clan_member_ban(self, obj: crate.ClanMember):
        obj.net.request.rest.ban_clan_member = mock.AsyncMock()
        await obj.ban("token")

        obj.net.request.rest.ban_clan_member.assert_called_once_with(
            "token",
            obj.group_id,
            obj.id,
            obj.type,
            comment=aiobungie.UNDEFINED,
            length=0,
        )

    @pytest.mark.asyncio()
    async def test_clan_member_unban(self, obj: crate.ClanMember):
        obj.net.request.rest.unban_clan_member = mock.AsyncMock()
        await obj.unban("token")

        obj.net.request.rest.unban_clan_member.assert_awaited_once_with(
            "token",
            group_id=obj.group_id,
            membership_id=obj.id,
            membership_type=obj.type,
        )

    @pytest.mark.asyncio()
    async def test_clan_member_kick(self, obj: crate.ClanMember):
        obj.net.request.kick_clan_member = mock.AsyncMock()

        obj.net.request.kick_clan_member.return_value = clan = mock.Mock(crate.Clan)
        clan.id = obj.group_id

        kicked_clan = await obj.kick("token")

        assert kicked_clan.id == obj.group_id

        obj.net.request.kick_clan_member.assert_awaited_once_with(
            "token",
            group_id=obj.group_id,
            membership_id=obj.id,
            membership_type=obj.type,
        )


class TestGroupMember:
    @pytest.fixture()
    def obj(self):
        mock_membership = mock.Mock(crate.DestinyMembership)
        mock_group = mock.Mock(crate.Clan, id=1234)

        return crate.GroupMember(
            net=mock.Mock(),
            inactive_memberships=None,
            member_type=aiobungie.ClanMemberType.ADMIN,
            is_online=True,
            last_online=datetime.datetime(2021, 5, 1),
            member=mock_membership,
            group=mock_group,
            group_id=3342,
            join_date=datetime.datetime(2021, 9, 6),
        )

    def test_group_member___int__(self, obj: crate.GroupMember):
        assert obj.__int__() == 3342

    def test_group_id(self, obj: crate.GroupMember):
        assert obj.group.id == 1234

    @pytest.mark.asyncio()
    async def test_fetch_self_clan(self, obj: crate.GroupMember):
        obj.net.request.fetch_clan_from_id = mock.AsyncMock()

        assert (
            await obj.fetch_self_clan()
            is obj.net.request.fetch_clan_from_id.return_value
        )

        obj.net.request.fetch_clan_from_id.assert_awaited_once_with(obj.group_id)


class TestClan:
    @pytest.fixture()
    def obj(self):
        mock_owner = mock.Mock(spec_set=crate.ClanMember)
        mock_features = mock.Mock(spec_set=crate.clans.ClanFeatures)
        return crate.Clan(
            net=mock.Mock(),
            id=998271,
            type=aiobungie.GroupType.CLAN,
            name="Cool clan",
            created_at=datetime.datetime(2018, 9, 3, 11, 13, 12),
            member_count=2,
            motto="Cool motto",
            is_public=True,
            banner=assets.Image("xxx.jpg"),
            avatar=assets.Image("zzz.jpg"),
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
            current_user_membership=mock.Mock({"Steam": mock.Mock(crate.ClanMember)}),
        )

    def test_clan___int__(self, obj: crate.Clan):
        assert int(obj) == obj.id

    def test_clan___str__(self, obj: crate.Clan):
        assert str(obj) == obj.name

    def test_clan_tags(self, obj: crate.Clan):
        assert obj.tags == ["Raids", "Tag", "Another tag"]

    def test_clan_member_count(self, obj: crate.Clan):
        assert obj.member_count == 2

    def test_clan_about(self, obj: crate.Clan):
        assert obj.about == "A cool clan."

    def test_clan_owner_is_None(self, obj: crate.Clan):
        assert obj.owner is not None
        obj.owner = None
        assert obj.owner is None

    @pytest.mark.asyncio()
    async def test_edit_options(self, obj: crate.Clan):
        obj.net.request.rest.edit_clan_options = mock.AsyncMock()

        await obj.edit_options(
            "token",
            invite_permissions_override=True,
            update_banner_permission_override=None,
            host_guided_game_permission_override=1,
            update_culture_permissionOverride=False,
            join_level=aiobungie.ClanMemberType.BEGINNER,
        )

        obj.net.request.rest.edit_clan_options.assert_awaited_once_with(
            "token",
            group_id=obj.id,
            invite_permissions_override=True,
            update_banner_permission_override=None,
            host_guided_game_permission_override=1,
            update_culture_permissionOverride=False,
            join_level=aiobungie.ClanMemberType.BEGINNER,
        )

    @pytest.mark.asyncio()
    async def test_edit(self, obj: crate.Clan):
        obj.net.request.rest.edit_clan = mock.AsyncMock()

        await obj.edit(
            "token",
            name="big name",
            motto="big motto",
            about="big about",
            tags=["fool", "jim"],
            theme="big theme",
            locale="EU",
        )

        obj.net.request.rest.edit_clan.assert_awaited_once_with(
            "token",
            group_id=998271,
            name="big name",
            about="big about",
            motto="big motto",
            theme="big theme",
            tags=["fool", "jim"],
            is_public=None,
            locale="EU",
            avatar_image_index=None,
            membership_option=None,
            allow_chat=None,
            chat_security=None,
            call_sign=None,
            homepage=None,
            enable_invite_messaging_for_admins=None,
            default_publicity=None,
            is_public_topic_admin=None,
        )

    @pytest.mark.asyncio()
    async def test_fetch_available_fireteams(self, obj: crate.Clan):
        obj.net.request.fetch_available_clan_fireteams = fts = mock.AsyncMock(
            [crate.Fireteam]
        )
        fts.return_value = [mock.Mock(crate.Fireteam), mock.Mock(crate.Fireteam)]

        fts.return_value[0].activity_type = aiobungie.FireteamActivity.RAID_DSC

        fireteams = await obj.fetch_available_fireteams(
            "token",
            activity_type=aiobungie.FireteamActivity.RAID_DSC,
            platform=aiobungie.FireteamPlatform.ANY,
            language=aiobungie.FireteamLanguage.JAPANESE,
        )
        assert fireteams is not None

        assert len(fireteams) == 2
        assert fireteams[0].activity_type == aiobungie.FireteamActivity.RAID_DSC
        fts.assert_awaited_once_with(
            "token",
            998271,
            aiobungie.FireteamActivity.RAID_DSC,
            platform=aiobungie.FireteamPlatform.ANY,
            language="ja",
            date_range=aiobungie.FireteamDate.ALL,
            page=0,
            public_only=False,
            slots_filter=0,
        )

    @pytest.mark.asyncio()
    async def test_fetch_fireteams(self, obj: crate.Clan):
        obj.net.request.fetch_my_clan_fireteams = fts = mock.AsyncMock([crate.Fireteam])

        await obj.fetch_fireteams(
            "token",
            platform=aiobungie.FireteamPlatform.STEAM,
            language=aiobungie.FireteamLanguage.ENGLISH,
        )

        fts.assert_awaited_once_with(
            "token",
            998271,
            include_closed=True,
            platform=aiobungie.FireteamPlatform.STEAM,
            language="en",
            filtered=True,
            page=0,
        )

    @pytest.mark.asyncio()
    async def test_fetch_conversations(self, obj: crate.Clan):
        obj.net.request.fetch_clan_conversations = mock.AsyncMock(
            [crate.ClanConversation]
        )

        convos = await obj.fetch_conversations()

        obj.net.request.fetch_clan_conversations.assert_awaited_once_with(obj.id)
        assert convos is obj.net.request.fetch_clan_conversations.return_value

    @pytest.mark.asyncio()
    async def test_add_optional_conversation(self, obj: crate.Clan):
        obj.net.request.rest.add_optional_conversation = mock.AsyncMock()

        await obj.add_optional_conversation("token", name="new chat", security=1)
        obj.net.request.rest.add_optional_conversation.assert_awaited_once_with(
            "token",
            obj.id,
            name="new chat",
            security=1,
        )

    @pytest.mark.asyncio()
    async def test_approve_pending_members(self, obj: crate.Clan):
        obj.net.request.rest.approve_all_pending_group_users = mock.AsyncMock()

        await obj.approve_pending_members(
            "token", message="You have been approved as a jim"
        )
        obj.net.request.rest.approve_all_pending_group_users.assert_awaited_once_with(
            "token", obj.id, message="You have been approved as a jim"
        )

    @pytest.mark.asyncio()
    async def test_deny_pending_members(self, obj: crate.Clan):
        obj.net.request.rest.deny_all_pending_group_users = mock.AsyncMock()

        await obj.deny_pending_members("token")
        obj.net.request.rest.deny_all_pending_group_users.assert_awaited_once_with(
            "token", obj.id, message=aiobungie.UNDEFINED
        )

    @pytest.mark.asyncio()
    async def test_fetch_clan_members(self, obj: crate.Clan):
        first_member = mock.Mock(spec_set=crate.ClanMember)
        first_member.type = aiobungie.MembershipType.XBOX

        another_member = mock.Mock(spec_set=crate.ClanMember)
        another_member.type = aiobungie.MembershipType.STEAM

        mock_members = mock.Mock(spec_set=[first_member, another_member])
        obj.net.request.fetch_clan_members = mock.AsyncMock(return_value=mock_members)
        members = await obj.fetch_members()

        obj.net.request.fetch_clan_members.assert_awaited_once_with(
            obj.id, type=aiobungie.MembershipType.NONE, name=None
        )
        assert members is obj.net.request.fetch_clan_members.return_value

    # These are never implemented.
    @pytest.mark.asyncio()
    async def test_fetch_banned_clan_member(self, obj: crate.Clan):
        ...

    @pytest.mark.asyncio()
    async def test_fetch_pending_clan_member(self, obj: crate.Clan):
        ...

    @pytest.mark.asyncio()
    async def test_fetch_invited_clan_member(self, obj: crate.Clan):
        ...
