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

import aiobungie
import os
import sys
import typing
import inspect
import logging
import asyncio

if typing.TYPE_CHECKING:
    import types
    
# NOTE: If you're on unix based system make sure to run this
# in your terminal. export CLIENT_TOKEN='TOKEN'

CID = 2305843009444904605
MID = 4611686018484639825
_LOG = logging.getLogger("test_client")
logging.basicConfig(level=logging.DEBUG)

def build_client() -> aiobungie.Client:
    token = os.environ['CLIENT_TOKEN']
    rest = aiobungie.RESTClient(token, max_retries=2)
    client = aiobungie.Client(token, rest_client=rest)
    return client


client = build_client()

async def test_users() -> aiobungie.crate.user.BungieUser:
    u = await client.fetch_user(20315338)
    return u

async def test_user_themese() -> typing.Sequence[aiobungie.crate.user.UserThemes]:
    ut = await client.fetch_user_themes()
    return ut

async def test_hard_types() -> aiobungie.crate.user.HardLinkedMembership:
    uht = await client.fetch_hard_types(76561198141430157)
    return uht


async def test_clan_from_id() -> aiobungie.crate.Clan:
    c = await client.fetch_clan_from_id(4389205)
    members = await c.fetch_members()
    member = await c.fetch_member("Fate")
    print(members.__repr__(), member.__repr__())
    print(c.owner.__repr__())
    return c

async def test_clan() -> aiobungie.crate.Clan:
    c = await client.fetch_clan("Nuanceㅤ ")
    members = await c.fetch_members()
    member = await c.fetch_member("Hizxr")
    print(members.__repr__(), member.__repr__())
    print(c.owner.__repr__())
    return c

async def test_fetch_clan_member() -> aiobungie.crate.ClanMember:
    m = await client.fetch_clan_member(4389205, "Fate")
    return m


async def test_fetch_clan_members() -> typing.Sequence[aiobungie.crate.ClanMember]:
    ms = await client.fetch_clan_members(4389205)
    for member in ms:
        if member.bungie.name == "Cosmic":
            fetched_user = await member.bungie.fetch_self()
            _LOG.debug(fetched_user)
    return ms

async def test_fetch_inventory_item() -> aiobungie.crate.InventoryEntity:
    i = await client.fetch_inventory_item(1216319404)
    _LOG.debug(repr(i))
    return i

async def test_fetch_app() -> aiobungie.crate.Application:
    a = await client.fetch_app(33226)
    fetched_user = await a.owner.fetch_self()
    _LOG.debug(fetched_user)
    return a

async def test_player() -> typing.Sequence[typing.Optional[aiobungie.crate.DestinyUser]]:
    p = await client.fetch_player("Crit#0495")
    profile = await p[0].fetch_self_profile(aiobungie.ComponentType.PROFILE)
    _LOG.debug(profile)
    components = aiobungie.ComponentType.ALL_CHARACTERS
    if profile.profiles:
        for char in await profile.profiles.collect(
            *components.value
        ):
            _LOG.debug(f"{char}")
    return p

async def test_char() -> aiobungie.crate.CharacterComponent:
    c = await client.fetch_character(
        MID,
        aiobungie.MembershipType.STEAM,
        CID,
        *aiobungie.ComponentType.ALL_CHARACTERS.value
    )
    _LOG.debug(c)
    return c

async def test_profile() -> None:
    pf = await client.fetch_profile(
        MID,
        aiobungie.MembershipType.STEAM,
        *aiobungie.ComponentType.ALL.value  # type: ignore
    )

    if (profile := pf.profiles):
        _LOG.debug(profile)
        try:
            for pfile_char in await profile.collect(*aiobungie.ComponentType.ALL_CHARACTERS.value):
                _LOG.debug(pfile_char.character)
        except RuntimeError:
            pass

    if (profile_progression := pf.profile_progression):
        _LOG.debug(profile_progression)
        _LOG.debug(profile_progression.checklist)

    if (characters := pf.characters):
        for _, character in characters.items():
            _LOG.debug(f'{character.class_type}, {character.emblem}, {character.light}')
            if profile and character.id in profile.character_ids:
                _LOG.debug(True)

    if pf_records := pf.profile_records:
        for _, prec in pf_records.items():
            if prec.objectives:
                fetched_obj = await prec.objectives[0].fetch_self()
                _LOG.info(repr(fetched_obj))
            _LOG.info(prec)
            break

    if char_records := pf.character_records:
        for char_id, record in char_records.items():
            _LOG.info(f"{char_id}")
            if record.objectives:
                fetched_char_obj = await record.objectives[0].fetch_self()
                _LOG.info(repr(fetched_char_obj))
            _LOG.info(
                f'{char_id}::{record}'
            )
            break

    if char_equips := pf.character_equipments:
        for _, items in char_equips.items():
            _LOG.info(items)
            _LOG.debug(repr(await items[0].fetch_self()))

    if char_acts := pf.character_activities:
        for char_id, act in char_acts.items():
            _LOG.info(f'{char_id, act.available_activities}')

    if char_render_data := pf.character_render_data:
        for char_id_, data in char_render_data.items():
            _LOG.info(f'{char_id_} | {repr(data)}')
            items = await data.fetch_my_items(limit=2)
            for item in items:
                _LOG.info(repr(item))

    if char_progrs := pf.character_progressions:
        for cid, prog in char_progrs.items():
            _LOG.debug(f"{cid} | {prog}")

    if (strs := pf.profile_string_variables) and (chr_strs := pf.character_string_variables):
        _LOG.debug(f'{strs} | {chr_strs}')
    
    if metrics := pf.metrics:
        _LOG.debug(metrics)

async def test_membership_types_from_id() -> aiobungie.crate.User:
    u = await client.fetch_membership_from_id(MID)
    return u


async def test_search_users() -> typing.Any:
    x = await client.search_users("Fate怒")
    return x


async def test_clan_conves() -> typing.Sequence[aiobungie.crate.clans.ClanConversation]:
    return await client.fetch_clan_conversations(881267)


async def test_clan_admins() -> typing.Sequence[aiobungie.crate.clans.ClanAdmin]:
    return await client.fetch_clan_admins(4389205)


async def test_groups_for_member() -> typing.Optional[
    aiobungie.crate.clans.GroupMember
]:
    obj = await client.fetch_groups_for_member(MID, aiobungie.MembershipType.STEAM)
    if obj is None:
        return None
    up_to_date_clan_obj = await obj.fetch_self_clan()
    _LOG.debug(up_to_date_clan_obj)
    return obj


async def test_potential_groups_for_member() -> typing.Optional[
    aiobungie.crate.GroupMember
]:
    obj = await client.fetch_potential_groups_for_member(
        MID, aiobungie.MembershipType.STEAM
    )
    if obj is None:
        return None
    up_to_date_clan_obj = await obj.fetch_self_clan()
    _LOG.debug(up_to_date_clan_obj)
    return obj


async def test_linked_profiles() -> None:
    obj = await client.fetch_linked_profiles(
        4611686018468008855, aiobungie.MembershipType.ALL, all=True
    )
    print(obj.profiles_with_errors.__repr__(), obj.bungie.__repr__())
    try:
        async for profile in obj:
            print(profile.__repr__())
            transform_profile = await profile.fetch_self_profile(aiobungie.ComponentType.PROFILE)
            print(transform_profile.__repr__())
    # This originally should be StopIteration exception
    # But client.run throws RuntimeError
    # TODO: raise the actual exception instead of RuntimeError in client.run?
    except RuntimeError:
        pass


async def test_clan_banners() -> typing.Sequence[aiobungie.crate.ClanBanner]:
    cb = await client.fetch_clan_banners()
    return cb


async def test_public_milestones_content() -> aiobungie.crate.MilestoneContent:
    cb = await client.fetch_public_milestone_content(4253138191)
    return cb


async def test_static_request() -> None:
    r = await client.rest.static_request(
        "GET",
        f"Destiny2/3/Profile/{MID}/?components={aiobungie.ComponentType.CHARACTER_EQUIPMENT.value}",
    )
    assert r is not None and isinstance(r, dict)

async def test_fetch_fireteam():
    f = await client.fetch_fireteams(aiobungie.FireteamActivity.ALL)
    _LOG.debug(f)
    if f:
        _LOG.debug(f[0].url)

    f2 = await client.fetch_fireteams(
        aiobungie.FireteamActivity.ALL or 4,
        platform=aiobungie.FireteamPlatform.ANY or 4,
        language=aiobungie.FireteamLanguage.ENGLISH,
        date_range=1,
    )
    _LOG.debug(repr(f2))
    if f2:
        _LOG.debug(f2[0].url)

async def main() -> None:
    coro: types.FunctionType
    coros: typing.MutableSequence[asyncio.Future[types.FunctionType]] = []
    for n, coro in inspect.getmembers(
        sys.modules[__name__], inspect.iscoroutinefunction
    ):
        if n == "main" or not n.startswith("test_"):
            continue
        coros.append(coro())
    _LOG.debug(await asyncio.gather(*coros))
    _LOG.info(
        "Ran %i functions out of %i excluding main.",
        len(coros), len(inspect.getmembers(sys.modules[__name__], inspect.iscoroutinefunction))
    )

if __name__ == "__main__":
    client.run(main())
