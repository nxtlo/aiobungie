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

import inspect
import os
import sys

import aiobungie
from tests import config

# NOTE: If you're on unix based system make sure to run this
# in your terminal. export CLIENT_TOKEN='TOKEN'


def __build_client() -> aiobungie.Client:
    token = os.environ["CLIENT_TOKEN"]
    client = aiobungie.Client(token, max_retries=0, debug="TRACE")
    return client


client = __build_client()


# *->> Users tests <<-*
class TestUser:
    @staticmethod
    async def test_users():
        u = await client.fetch_bungie_user(config.PRIMARY_BUNGIE_ID)
        assert isinstance(u, aiobungie.crates.BungieUser)

    @staticmethod
    async def test_user_themes():
        ut = await client.fetch_user_themes()
        assert isinstance(ut, tuple)
        assert isinstance(ut[0], aiobungie.crates.UserThemes)

    if config.PRIMARY_STEAM_ID is not None:
        # This method only uses STEAM IDs.
        @staticmethod
        async def test_hard_types():
            uht = await client.fetch_hard_types(config.PRIMARY_STEAM_ID)
            assert isinstance(uht, aiobungie.crates.HardLinkedMembership)

    @staticmethod
    async def test_membership():
        p = await client.fetch_membership(config.PRIMARY_USERNAME, config.PRIMARY_CODE)
        profile = await p[0].fetch_self_profile([])
        assert isinstance(profile, aiobungie.crates.Component)

    @staticmethod
    async def test_membership_types_from_id():
        u = await client.fetch_membership_from_id(config.PRIMARY_MEMBERSHIP_ID)
        assert isinstance(u, aiobungie.crates.User)
        assert isinstance(u.bungie_user, aiobungie.crates.BungieUser)

    @staticmethod
    async def test_search_users():
        x = await client.search_users("Fate")
        assert isinstance(x.next(), aiobungie.crates.SearchableDestinyUser)


# *->> Activities tests <<-*
class TestActivities:
    @staticmethod
    async def test_fetch_activities():
        a = await client.fetch_activities(
            config.PRIMARY_MEMBERSHIP_ID,
            config.PRIMARY_CHARACTER_ID,
            aiobungie.GameMode.RAID,
        )
        post = await a.next().fetch_post()
        assert isinstance(post, aiobungie.crates.PostActivity)

        for act in a:
            assert isinstance(act, aiobungie.crates.Activity)

    @staticmethod
    async def test_post_activity():
        a = await client.fetch_post_activity(9538108571)
        assert isinstance(a, aiobungie.crates.PostActivity)
        assert len(a.players) >= 1

    @staticmethod
    async def test_activity_is_flawless():
        a = await client.fetch_post_activity(9710513682)
        assert a.is_flawless
        assert a.is_solo
        assert a.is_solo_flawless

    @staticmethod
    async def test_aggregated_activity():
        a = await client.fetch_aggregated_activity_stats(
            config.PRIMARY_CHARACTER_ID,
            config.PRIMARY_MEMBERSHIP_ID,
            config.PRIMARY_MEMBERSHIP_TYPE,
        )
        assert isinstance(a.next(), aiobungie.crates.AggregatedActivity)


# *->> Clan tests <<-*
class TestClans:
    @staticmethod
    async def test_clan_from_id():
        c = await client.fetch_clan_from_id(config.PRIMARY_CLAN_ID)
        members = await c.fetch_members()
        for member in members:
            assert isinstance(member, aiobungie.crates.ClanMember)

    @staticmethod
    async def test_clan():
        c = await client.fetch_clan(config.PRIMARY_CLAN_NAME)
        members = await c.fetch_members()

        assert isinstance(members.next(), aiobungie.crates.ClanMember)

    @staticmethod
    async def test_fetch_clan_members():
        ms = await client.fetch_clan_members(
            config.PRIMARY_CLAN_ID, name=config.PRIMARY_USERNAME
        )
        assert any(
            member.bungie_user and member.bungie_user.name == config.PRIMARY_USERNAME
            for member in ms
        )

    @staticmethod
    async def test_clan_conversations():
        x = await client.fetch_clan_conversations(881267)
        for c in x:
            assert isinstance(c, aiobungie.crates.ClanConversation)

    @staticmethod
    async def test_clan_admins():
        ca = await client.fetch_clan_admins(4389205)
        ca.any(lambda member: member.is_admin or member.is_founder)

    @staticmethod
    async def test_groups_for_member():
        obj = await client.fetch_groups_for_member(
            4611686018475612431, config.PRIMARY_MEMBERSHIP_TYPE
        )
        assert obj
        up_to_date_clan_obj = await obj[0].fetch_self_clan()
        assert isinstance(up_to_date_clan_obj, aiobungie.crates.Clan)

    @staticmethod
    async def test_potential_groups_for_member():
        obj = await client.fetch_potential_groups_for_member(
            config.PRIMARY_MEMBERSHIP_ID, config.PRIMARY_MEMBERSHIP_TYPE
        )
        assert not obj

    @staticmethod
    async def test_clan_banners():
        cb = await client.fetch_clan_banners()
        for b in cb:
            assert isinstance(b, aiobungie.crates.ClanBanner)

    @staticmethod
    async def test_clan_weekly_rewards():
        r = await client.fetch_clan_weekly_rewards(4389205)
        assert isinstance(r, aiobungie.crates.Milestone)


# *->> Application tests <<-*
class TestApplication:
    @staticmethod
    async def test_fetch_app():
        a = await client.fetch_application(config.APP_ID)
        assert isinstance(a, aiobungie.crates.Application)


# *->> Character components tests <<-*
class TestCharacter:
    # TODO: Separate each character component type to its own method?
    @staticmethod
    async def test_fetch_character():
        c = await client.fetch_character(
            config.PRIMARY_MEMBERSHIP_ID,
            config.PRIMARY_MEMBERSHIP_TYPE,
            config.PRIMARY_CHARACTER_ID,
            [aiobungie.ComponentType.ALL],
        )
        assert isinstance(c, aiobungie.crates.CharacterComponent)
        assert c.activities
        assert c.character
        assert c.character_records
        assert c.equipment
        assert c.inventory
        assert c.render_data
        assert c.progressions
        assert c.profile_records is None
        assert c.item_components


# *->> Profile components tests <<-*
class TestProfile:
    # TODO: Separate each profile component type to its own method?
    @staticmethod
    async def test_profile():
        pf = await client.fetch_profile(
            config.PRIMARY_MEMBERSHIP_ID,
            config.PRIMARY_MEMBERSHIP_TYPE,
            [aiobungie.ComponentType.ALL],
        )
        assert isinstance(pf, aiobungie.crates.Component)

        assert pf.profiles
        assert isinstance(pf.profile_progression, aiobungie.crates.ProfileProgression)

        assert pf.characters
        for config.PRIMARY_CHARACTER_ID, character in pf.characters.items():
            assert isinstance(config.PRIMARY_CHARACTER_ID, int)
            assert isinstance(character, aiobungie.crates.Character)
            assert config.PRIMARY_CHARACTER_ID in pf.profiles.character_ids

        assert pf.profile_records
        for _, prec in pf.profile_records.items():
            assert isinstance(prec, aiobungie.crates.Record)

        assert pf.character_records
        for _, record in pf.character_records.items():
            assert isinstance(record, aiobungie.crates.CharacterRecord)

        assert pf.character_equipments
        for config.PRIMARY_CHARACTER_ID, items in pf.character_equipments.items():
            assert isinstance(config.PRIMARY_CHARACTER_ID, int)
            for item in items:
                assert isinstance(item, aiobungie.crates.ProfileItemImpl)

        assert pf.character_activities
        for char_id, act in pf.character_activities.items():
            assert isinstance(char_id, int)
            assert isinstance(act, aiobungie.crates.activity.CharacterActivity)

        assert pf.character_render_data
        for _, data in pf.character_render_data.items():
            assert isinstance(data, aiobungie.crates.RenderedData)
            items_ = await data.fetch_my_items(limit=2)
            assert len(items_) == 2

        assert pf.character_progressions
        for config.PRIMARY_CHARACTER_ID, prog in pf.character_progressions.items():
            assert isinstance(config.PRIMARY_CHARACTER_ID, int)
            assert isinstance(prog, aiobungie.crates.CharacterProgression)

        assert pf.profile_string_variables
        assert pf.character_string_variables
        assert isinstance(pf.profile_string_variables, dict)
        assert isinstance(pf.character_string_variables, dict)
        assert pf.metrics
        assert isinstance(pf.item_components, aiobungie.crates.ItemsComponent)
        assert pf.character_craftables

    @staticmethod
    async def test_linked_profiles():
        obj = await client.fetch_linked_profiles(
            config.PRIMARY_MEMBERSHIP_ID, config.PRIMARY_MEMBERSHIP_TYPE
        )
        assert isinstance(obj, aiobungie.crates.LinkedProfile)
        user = obj.profiles[0]
        assert isinstance(user, aiobungie.crates.DestinyMembership)


# *->> Entities tests <<-*
class TestEntities:
    @staticmethod
    async def test_fetch_inventory_item():
        i = await client.fetch_inventory_item(1216319404)
        assert isinstance(i, aiobungie.crates.InventoryEntity)

    @staticmethod
    async def test_search_entities():
        acts = await client.search_entities("Scourge", "DestinyActivityDefinition")
        assert "Scourge of the Past" in acts.next().name


# *->> Functions that doesn't fall under any of the above <<-*
class TestMeta:
    # * Special REST methods. Those that don't fit under other categories.
    @staticmethod
    async def test_static_request():
        r = await client.rest.static_request(
            "GET",
            (
                f"Destiny2/3/Profile/{config.PRIMARY_MEMBERSHIP_ID}"
                f"/?components={int(aiobungie.ComponentType.CHARACTER_EQUIPMENT)}"
            ),
        )
        assert isinstance(r, dict)

    @staticmethod
    async def test_insert_plug_free():
        p = (
            aiobungie.builders.PlugSocketBuilder()
            .set_socket_array(0)
            .set_socket_index(0)
            .set_plug_item(3000)
            .collect()
        )
        try:
            await client.rest.insert_socket_plug_free("", 619, p, 1234, 3)
        # This will always fail due to OAuth2
        except aiobungie.Unauthorized:
            pass

    @staticmethod
    async def test_unique_weapon_history():
        w = await client.fetch_unique_weapon_history(
            config.PRIMARY_MEMBERSHIP_ID,
            config.PRIMARY_CHARACTER_ID,
            config.PRIMARY_MEMBERSHIP_TYPE,
        )
        for weapon in w:
            assert isinstance(weapon, aiobungie.crates.ExtendedWeaponValues)

    @staticmethod
    async def test_client_metadata():
        client.metadata[0] = None
        clan = await client.fetch_clan("Math Class")
        assert clan.net.request.metadata[0] is None

    # FIXME: There's currently a problem with this API route from Bungie's side
    # where it returns an HTML not found page.
    # async def test_set_item_lock_state():
    #     try:
    #         await client.rest.set_item_lock_state("my-token", True, 123, 123, 1)
    #     # This will fail due to OAuth2
    #     except aiobungie.Unauthorized:
    #         pass

    # * Milestone methods
    # FIXME: Uncomment this when it get stabilized.
    # @staticmethod
    # async def test_public_milestones_content():
    #     cb = await client.fetch_public_milestone_content(4253138191)
    #     assert isinstance(cb, aiobungie.crates.MilestoneContent)

    # * Fireteam methods.
    @staticmethod
    async def test_fetch_fireteam():
        f2 = await client.fetch_fireteams(
            aiobungie.FireteamActivity.ANY,
            platform=aiobungie.FireteamPlatform.ANY,
            language=aiobungie.FireteamLanguage.ENGLISH,
            date_range=1,
        )
        assert f2
        for ft in f2:
            assert isinstance(ft, aiobungie.crates.Fireteam)


async def main() -> None:
    from aiobungie.internal import helpers

    tasks = []
    for cls in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if cls[0].startswith("Test"):
            for name in dir(cls[1]):
                if name.startswith("test_"):
                    print("Tested: ", name)
                    coro = getattr(cls[1], name)()
                    assert inspect.iscoroutine(coro)
                    tasks.append(coro)

    async with client.rest:
        await helpers.awaits(*tasks)


if __name__ == "__main__":
    client.run(main())
