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
import logging
import os
import sys

import aiobungie

# NOTE: If you're on unix based system make sure to run this
# in your terminal. export CLIENT_TOKEN='TOKEN'

CID = 2305843009444904605
MID = 4611686018484639825
STEAM = aiobungie.MembershipType.STEAM
_LOG = logging.getLogger("test_client")


def __build_client() -> aiobungie.Client:
    token = os.environ["CLIENT_TOKEN"]
    client = aiobungie.Client(token, max_retries=0)
    client.rest.enable_debugging(True)
    return client


client = __build_client()


async def test_users():
    u = await client.fetch_bungie_user(20315338)
    assert isinstance(u, aiobungie.crate.BungieUser)


async def test_user_themes():
    ut = await client.fetch_user_themes()
    assert isinstance(ut, list)
    assert isinstance(ut[0], aiobungie.crate.UserThemes)


async def test_hard_types():
    uht = await client.fetch_hard_types(76561198141430157)
    assert isinstance(uht, aiobungie.crate.HardLinkedMembership)


async def test_clan_from_id():
    c = await client.fetch_clan_from_id(4389205)
    members = await c.fetch_members()
    for member in members:
        assert isinstance(member, aiobungie.crate.ClanMember)


async def test_clan():
    c = await client.fetch_clan("Nuanceㅤ ")
    members = await c.fetch_members()

    for member in members.filter(lambda member: not member.is_online):
        assert isinstance(member, aiobungie.crate.ClanMember)


async def test_fetch_clan_members():
    ms = await client.fetch_clan_members(4389205, name="Fate")
    assert len(ms) == 1
    for member in ms:
        assert isinstance(member, aiobungie.crate.ClanMember)
        assert isinstance(member.bungie_user, aiobungie.crate.PartialBungieUser)
        assert member.bungie_user.name == "Fate怒"


async def test_fetch_inventory_item():
    i = await client.fetch_inventory_item(1216319404)
    assert isinstance(i, aiobungie.crate.InventoryEntity)


async def test_fetch_app():
    a = await client.fetch_application(33226)
    assert isinstance(a, aiobungie.crate.Application)


async def test_player():
    p = await client.fetch_membership("Fate怒", 4275)
    profile = await p[0].fetch_self_profile([aiobungie.ComponentType.PROFILE])
    assert isinstance(profile, aiobungie.crate.Component)
    assert isinstance(profile.profiles, aiobungie.crate.Profile)


async def test_fetch_character():
    c = await client.fetch_character(
        MID,
        STEAM,
        CID,
        [aiobungie.ComponentType.ALL],
    )
    assert isinstance(c, aiobungie.crate.CharacterComponent)
    assert c.activities
    assert c.character
    assert c.character_records
    assert c.equipment
    assert c.inventory
    assert c.render_data
    assert c.progressions
    assert c.profile_records is None
    assert c.item_components


async def test_profile():
    pf = await client.fetch_profile(MID, STEAM, [aiobungie.ComponentType.ALL])
    assert isinstance(pf, aiobungie.crate.Component)

    assert pf.profiles
    assert isinstance(pf.profile_progression, aiobungie.crate.ProfileProgression)

    assert pf.characters
    for cid, character in pf.characters.items():
        assert isinstance(cid, int)
        assert isinstance(character, aiobungie.crate.Character)
        assert cid in pf.profiles.character_ids

    assert pf.profile_records
    for _, prec in pf.profile_records.items():
        assert isinstance(prec, aiobungie.crate.Record)

    assert pf.character_records
    for _, record in pf.character_records.items():
        assert isinstance(record, aiobungie.crate.CharacterRecord)

    assert pf.character_equipments
    for cid, items in pf.character_equipments.items():
        assert isinstance(cid, int)
        for item in items:
            assert isinstance(item, aiobungie.crate.ProfileItemImpl)

    assert pf.character_activities
    for char_id, act in pf.character_activities.items():
        assert isinstance(char_id, int)
        assert isinstance(act, aiobungie.crate.activity.CharacterActivity)

    assert pf.character_render_data
    for char_id_, data in pf.character_render_data.items():
        assert isinstance(char_id_, int)
        assert isinstance(data, aiobungie.crate.RenderedData)
        items_ = await data.fetch_my_items(limit=2)
        assert len(items_) == 2
        for item_ in items_:
            assert isinstance(item_, aiobungie.crate.InventoryEntity)

    assert pf.character_progressions
    for cid, prog in pf.character_progressions.items():
        assert isinstance(cid, int)
        assert isinstance(prog, aiobungie.crate.CharacterProgression)

    assert pf.profile_string_variables
    assert pf.character_string_variables
    assert isinstance(pf.profile_string_variables, dict)
    assert isinstance(pf.character_string_variables, dict)

    assert pf.metrics
    for met in pf.metrics:
        for met_id, met_ in met.items():
            assert isinstance(met_id, int)
            inv, _ = met_
            assert isinstance(inv, bool)

            assert any(o is not None for o in met_)

    if pf.transitory:
        assert isinstance(pf.transitory, aiobungie.crate.FireteamParty)
    if pf.item_components:
        assert isinstance(pf.item_components, aiobungie.crate.ItemsComponent)

    if pf.character_craftables:
        for craftable_item_hash, craftable_item in pf.character_craftables.items():
            assert isinstance(craftable_item_hash, int)
            for item in craftable_item.craftables.values():
                if item:
                    assert isinstance(item, aiobungie.crate.CraftableItem)


async def test_membership_types_from_id():
    u = await client.fetch_membership_from_id(MID)
    assert isinstance(u, aiobungie.crate.User)
    assert isinstance(u.bungie_user, aiobungie.crate.BungieUser)
    for mem in u.memberships:
        assert isinstance(mem, aiobungie.crate.DestinyMembership)


async def test_search_users():
    x = await client.search_users("Fate")
    # assert isinstance(x, list)
    for u in x:
        assert isinstance(u, aiobungie.crate.SearchableDestinyUser)
        for membership in u.memberships:
            assert isinstance(membership, aiobungie.crate.DestinyMembership)


async def test_clan_conversations():
    x = await client.fetch_clan_conversations(881267)
    assert isinstance(x, list)
    for c in x:
        assert isinstance(c, aiobungie.crate.ClanConversation)


async def test_clan_admins():
    ca = await client.fetch_clan_admins(4389205)
    assert any(member.is_admin or member.is_founder for member in ca)
    assert all(isinstance(admin, aiobungie.crate.ClanMember) for admin in ca)


async def test_groups_for_member():
    obj = await client.fetch_groups_for_member(4611686018475612431, STEAM)
    assert obj
    up_to_date_clan_obj = await obj[0].fetch_self_clan()
    assert isinstance(up_to_date_clan_obj, aiobungie.crate.Clan)


async def test_potential_groups_for_member():
    obj = await client.fetch_potential_groups_for_member(MID, STEAM)
    assert not obj


async def test_linked_profiles():
    obj = await client.fetch_linked_profiles(
        MID, aiobungie.MembershipType.ALL, all=True
    )
    assert isinstance(obj, aiobungie.crate.LinkedProfile)
    user = obj.profiles[0]
    assert isinstance(user, aiobungie.crate.DestinyMembership)
    transform_profile = await user.fetch_self_profile([aiobungie.ComponentType.PROFILE])
    assert transform_profile.profiles
    assert isinstance(transform_profile, aiobungie.crate.Component)


async def test_clan_banners():
    cb = await client.fetch_clan_banners()
    for b in cb:
        assert isinstance(b, aiobungie.crate.ClanBanner)


async def test_public_milestones_content():
    cb = await client.fetch_public_milestone_content(4253138191)
    assert isinstance(cb, aiobungie.crate.MilestoneContent)


async def test_static_request():
    r = await client.rest.static_request(
        "GET",
        f"Destiny2/3/Profile/{MID}/?components={aiobungie.ComponentType.CHARACTER_EQUIPMENT.value}",
    )
    assert isinstance(r, dict)


async def test_fetch_fireteam():
    f = await client.fetch_fireteams(aiobungie.FireteamActivity.NIGHTFALL)
    if f:
        assert isinstance(f[0].url, str)

    f2 = await client.fetch_fireteams(
        aiobungie.FireteamActivity.ANY,
        platform=aiobungie.FireteamPlatform.ANY,
        language=aiobungie.FireteamLanguage.ENGLISH,
        date_range=1,
    )
    if f2:
        for ft in f2:
            assert isinstance(ft, aiobungie.crate.Fireteam)


async def test_fetch_activities():
    a = await client.fetch_activities(MID, CID, aiobungie.GameMode.RAID)
    post = await a.first().fetch_post()
    assert isinstance(post, aiobungie.crate.PostActivity)
    assert a.any(lambda act: act.is_flawless)

    for act in a:
        assert isinstance(act, aiobungie.crate.Activity)
        if act.hash == aiobungie.Raid.DSC.value:
            assert aiobungie.GameMode.RAID in act.modes


async def test_post_activity():
    a = await client.fetch_post_activity(9538108571)
    assert a.mode is aiobungie.GameMode.RAID
    assert a.hash == aiobungie.Raid.DSC.value
    assert not a.is_flawless
    assert not a.is_solo
    assert not a.is_solo_flawless
    for player in a.players:
        assert isinstance(player, aiobungie.crate.activity.PostActivityPlayer)
        assert isinstance(
            player.extended_values, aiobungie.crate.activity.ExtendedValues
        )
        if weapons := player.extended_values.weapons:
            for weapon in weapons:
                assert isinstance(weapon, aiobungie.crate.activity.ExtendedWeaponValues)


async def test_activity_flawless():
    a = await client.fetch_post_activity(9710513682)
    assert a.is_flawless
    assert a.is_solo
    assert a.is_solo_flawless
    a2 = await client.fetch_post_activity(9711329560)
    assert a2.is_solo and not a2.is_flawless


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


# FIXME: There's currently a problem with this API route from Bungie's side.
# async def test_set_item_lock_state():
#     try:
#         await client.rest.set_item_lock_state("my-token", True, 123, 123, 1)
#     # This will fail due to OAuth2
#     except aiobungie.Unauthorized:
#         pass


async def test_search_entities():
    e = await client.search_entities("Parallel", "DestinyInventoryItemDefinition")

    acts = await client.search_entities("Scourge", "DestinyActivityDefinition")

    assert acts.any(lambda act: act.name in "Scourge of the Past")

    for i in e:
        assert isinstance(i, aiobungie.crate.SearchableEntity)


async def test_unique_weapon_history():
    w = await client.fetch_unique_weapon_history(MID, CID, STEAM)
    for weapon in w:
        assert isinstance(weapon, aiobungie.crate.ExtendedWeaponValues)


async def test_client_metadata():
    client.metadata["pepe"] = "laugh"
    clan = await client.fetch_clan("Math Class")
    assert clan.net.request.metadata["pepe"] == "laugh"


async def test_clan_weekly_rewards():
    r = await client.fetch_clan_weekly_rewards(4389205)
    assert isinstance(r, aiobungie.crate.Milestone)


async def test_aggregated_activity():
    a = await client.fetch_aggregated_activity_stats(CID, MID, STEAM)
    for act in a.sort(key=lambda act: act.values.fastest_completion_time[1]):
        assert isinstance(act, aiobungie.crate.AggregatedActivity)


async def main() -> None:
    from aiobungie.internal import helpers

    coros = []
    for n, coro in inspect.getmembers(
        sys.modules[__name__], inspect.iscoroutinefunction
    ):
        if n == "main" or not n.startswith("test_"):
            continue

        coros.append(coro())

    async with client.rest:
        await helpers.awaits(*coros)

    _LOG.info(
        "Asserted %i functions out of %i excluding main.",
        len(coros),
        len(inspect.getmembers(sys.modules[__name__], inspect.iscoroutinefunction)),
    )


if __name__ == "__main__":
    client.run(main())
