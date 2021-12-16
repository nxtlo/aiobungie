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
import inspect
import logging
import os
import sys
import typing

import aiobungie

if typing.TYPE_CHECKING:
    import types

# NOTE: If you're on unix based system make sure to run this
# in your terminal. export CLIENT_TOKEN='TOKEN'

CID = 2305843009444904605
MID = 4611686018484639825
_LOG = logging.getLogger("test_client")
logging.basicConfig(level=logging.DEBUG)


def __build_client() -> aiobungie.Client:
    token = os.environ["CLIENT_TOKEN"]
    rest = aiobungie.RESTClient(token, max_retries=2)
    client = aiobungie.Client(token, rest_client=rest)
    return client


client = __build_client()


async def test_users():
    u = await client.fetch_user(20315338)
    assert isinstance(u, aiobungie.crate.BungieUser)


async def test_user_themese():
    ut = await client.fetch_user_themes()
    assert isinstance(ut, list)
    assert isinstance(ut[0], aiobungie.crate.UserThemes)


async def test_hard_types():
    uht = await client.fetch_hard_types(76561198141430157)
    assert isinstance(uht, aiobungie.crate.HardLinkedMembership)


async def test_clan_from_id():
    c = await client.fetch_clan_from_id(4389205)
    members = await c.fetch_members()
    member = await c.fetch_member("Fate")
    assert isinstance(members, list)
    assert isinstance(members[0], aiobungie.crate.ClanMember)
    assert isinstance(member, aiobungie.crate.ClanMember)


async def test_clan():
    c = await client.fetch_clan("Nuanceㅤ ")
    members = await c.fetch_members()
    member = await c.fetch_member("Hizxr")
    assert isinstance(members, list)
    assert isinstance(members[0], aiobungie.crate.ClanMember)
    assert isinstance(member, aiobungie.crate.ClanMember)


async def test_fetch_clan_member():
    m = await client.fetch_clan_member(4389205, "Fate")
    assert isinstance(m, aiobungie.crate.ClanMember)


async def test_fetch_clan_members():
    ms = await client.fetch_clan_members(4389205)
    assert isinstance(ms, list)
    for member in ms:
        assert isinstance(member, aiobungie.crate.ClanMember)
        assert isinstance(member.bungie, aiobungie.crate.PartialBungieUser)
        if member.bungie.name == "Fate":
            fetched_user = await member.bungie.fetch_self()
            assert isinstance(fetched_user, aiobungie.crate.BungieUser)


async def test_fetch_inventory_item():
    i = await client.fetch_inventory_item(1216319404)
    assert isinstance(i, aiobungie.crate.InventoryEntity)


async def test_fetch_app():
    a = await client.fetch_app(33226)
    assert isinstance(a, aiobungie.crate.Application)
    fetched_user = await a.owner.fetch_self()
    assert isinstance(fetched_user, aiobungie.crate.BungieUser)


async def test_player():
    p = await client.fetch_player("Fate怒", 4275)
    profile = await p[0].fetch_self_profile(aiobungie.ComponentType.PROFILE)
    assert isinstance(profile, aiobungie.crate.Component)
    assert isinstance(profile.profiles, aiobungie.crate.Profile)

    components = aiobungie.ComponentType.ALL_CHARACTERS
    profiles = profile.profiles.collect_characters(*components.value)
    for char in await profiles:
        assert isinstance(char, aiobungie.crate.CharacterComponent)
        assert (
            char.activities,
            char.character,
            char.character_records,
            char.equipment,
            char.inventory,
            char.render_data,
            char.progressions,
        ) is not None


async def test_char():
    c = await client.fetch_character(
        MID,
        aiobungie.MembershipType.STEAM,
        CID,
        aiobungie.ComponentType.CHARACTER_ACTIVITIES,
        aiobungie.ComponentType.CHARACTERS,
    )
    assert isinstance(c, aiobungie.crate.CharacterComponent)
    assert c.activities
    assert c.character
    assert c.character_records is None
    assert c.equipment is None
    assert c.inventory is None
    assert c.profile_records is None
    assert c.render_data is None
    assert c.progressions is None
    acts = await c.character.fetch_activities(aiobungie.GameMode.RAID, limit=10)
    assert len(acts) == 10
    for act in acts:
        assert isinstance(act, aiobungie.crate.Activity)


async def test_profile():
    pf = await client.fetch_profile(
        MID,
        aiobungie.MembershipType.STEAM,
        *aiobungie.ComponentType.ALL.value,  # type: ignore
    )
    assert isinstance(pf, aiobungie.crate.Component)

    assert pf.profiles
    for pfile_char in await pf.profiles.collect_characters(
        *aiobungie.ComponentType.ALL_CHARACTERS.value
    ):
        assert isinstance(pfile_char, aiobungie.crate.CharacterComponent)
        assert (
            pfile_char.profile_records is None
        )  # Always None or a character component.
        assert pfile_char.activities
        assert pfile_char.character
        assert pfile_char.character_records
        assert pfile_char.equipment
        assert pfile_char.inventory
        assert pfile_char.render_data
        assert pfile_char.progressions

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
        items = await data.fetch_my_items(limit=2)
        assert len(items) == 2
        for item in items:
            assert isinstance(item, aiobungie.crate.InventoryEntity)

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
            inv, obj = met_
            assert isinstance(inv, bool)
            assert isinstance(obj, aiobungie.crate.Objective)


async def test_membership_types_from_id():
    u = await client.fetch_membership_from_id(MID)
    assert isinstance(u, aiobungie.crate.User)
    assert isinstance(u.bungie, aiobungie.crate.BungieUser)
    for du in u.destiny:
        assert isinstance(du, aiobungie.crate.DestinyUser)


async def test_search_users():
    x = await client.search_users("Fate怒")
    assert isinstance(x, list)
    for u in x:
        assert isinstance(u, aiobungie.crate.DestinyUser)


async def test_clan_conves():
    x = await client.fetch_clan_conversations(881267)
    assert isinstance(x, list)
    for c in x:
        assert isinstance(c, aiobungie.crate.ClanConversation)


async def test_clan_admins():
    ca = await client.fetch_clan_admins(4389205)
    assert any(
        not isinstance(c.name, aiobungie.UndefinedType) and "Karlz" or "Crit" == c.name
        for c in ca
    )
    for ad in ca:
        assert isinstance(ad, aiobungie.crate.ClanAdmin)


async def test_groups_for_member():
    obj = await client.fetch_groups_for_member(MID, aiobungie.MembershipType.STEAM)
    assert obj
    up_to_date_clan_obj = await obj.fetch_self_clan()
    assert isinstance(up_to_date_clan_obj, aiobungie.crate.Clan)


async def test_potential_groups_for_member():
    obj = await client.fetch_potential_groups_for_member(
        MID, aiobungie.MembershipType.STEAM
    )
    assert obj is None


async def test_linked_profiles():
    obj = await client.fetch_linked_profiles(
        MID, aiobungie.MembershipType.ALL, all=True
    )
    assert isinstance(obj, aiobungie.crate.LinkedProfile)
    try:
        async for user in obj:
            assert isinstance(user, aiobungie.crate.DestinyUser)
            transform_profile = await user.fetch_self_profile(
                aiobungie.ComponentType.PROFILE
            )
            assert transform_profile.profiles
            assert isinstance(transform_profile, aiobungie.crate.Component)
    # This originally should be StopIteration exception
    # But client.run throws RuntimeError
    # TODO: raise the actual exception instead of RuntimeError in client.run?
    except RuntimeError:
        pass


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
    f = await client.fetch_fireteams(aiobungie.FireteamActivity.ALL)
    if f:
        assert isinstance(f[0].url, str)

    f2 = await client.fetch_fireteams(
        aiobungie.FireteamActivity.ALL or 4,
        platform=aiobungie.FireteamPlatform.ANY or 4,
        language=aiobungie.FireteamLanguage.ENGLISH,
        date_range=1,
    )
    if f2:
        for ft in f2:
            assert isinstance(ft, aiobungie.crate.Fireteam)


async def test_fetch_activities():
    a = await client.fetch_activities(MID, CID, aiobungie.GameMode.RAID)
    assert any(_.is_flawless for _ in a)
    for act in a:
        assert isinstance(act, aiobungie.crate.Activity)
        if act.hash == aiobungie.Raid.DSC.value:
            assert aiobungie.GameMode.RAID in act.modes
    post = await a[0].fetch_post()
    assert isinstance(post, aiobungie.crate.PostActivity)


async def test_post_activity():
    a = await client.fetch_post_activity(9538108571)
    assert a.mode is aiobungie.GameMode.RAID
    assert a.hash == aiobungie.Raid.DSC.value
    assert not a.is_flawless
    assert not a.is_solo
    assert not a.is_solo_flawless
    for player in a.players:
        assert isinstance(player, aiobungie.crate.activity.PostActivityPlayer)
        assert isinstance(player.extended_values, aiobungie.crate.activity.ExtendedValues)
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


async def main() -> None:
    coro: types.FunctionType
    coros: typing.MutableSequence[asyncio.Future[types.FunctionType]] = []
    for n, coro in inspect.getmembers(
        sys.modules[__name__], inspect.iscoroutinefunction
    ):
        if n == "main" or not n.startswith("test_"):
            continue
        coros.append(coro())
    await asyncio.gather(*coros)
    _LOG.info(
        "Asserted %i functions out of %i excluding main.",
        len(coros),
        len(inspect.getmembers(sys.modules[__name__], inspect.iscoroutinefunction)),
    )


if __name__ == "__main__":
    client.run(main())
