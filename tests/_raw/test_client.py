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
"""Base client tests."""

from __future__ import annotations

import asyncio
import os
import typing

try:
    from dotenv import load_dotenv
    load_dotenv()
    token = os.environ['TOKEN']
except (ImportError, KeyError):
    token = ""  # <-- TOKEN GOES HERE

import aiobungie
from aiobungie import crate

client = aiobungie.Client(token)
MID = 4611686018484639825

def view(func: typing.Callable[[], typing.Any]) -> typing.Callable[..., typing.Any]:
    import logging
    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    log.debug(
        f"Func {func.__name__} Returns {func.__annotations__.get('return', 'Undefined')} Passed."
    )
    return lambda *args, **kwargs: func(*args, **kwargs)

@view
async def test_users() -> crate.user.BungieUser:
    u = await client.fetch_user(20315338)
    return u


@view
async def test_user_themese() -> typing.Sequence[crate.user.UserThemes]:
    ut = await client.fetch_user_themes()
    return ut


@view
async def test_hard_types() -> crate.user.HardLinkedMembership:
    uht = await client.fetch_hard_types(76561198141430157)
    return uht


@view
async def test_clan_from_id() -> crate.Clan:
    c = await client.fetch_clan_from_id(4389205)
    members = await c.fetch_members()
    member = await c.fetch_member("Fate")
    print(members, member)
    print(c.owner)
    return c


@view
async def test_clan() -> crate.Clan:
    c = await client.fetch_clan("Nuanceㅤ ")
    members = await c.fetch_members()
    member = await c.fetch_member("Hizxr")
    print(members, member)
    print(c.owner)
    return c


@view
async def test_fetch_clan_member() -> crate.ClanMember:
    m = await client.fetch_clan_member(4389205, "Fate")
    return m


@view
async def test_fetch_clan_members() -> typing.Sequence[crate.ClanMember]:
    ms = await client.fetch_clan_members(4389205)
    for member in ms:
        if member.bungie.name == "Cosmic":
            fetched_user = await member.bungie.fetch_self()
            print(repr(fetched_user))
    return ms

@view
async def test_fetch_inventory_item() -> crate.InventoryEntity:
    i = await client.fetch_inventory_item(1397707366)
    print(i.about, i.damage, i.description, i.icon)
    return i


@view
async def test_fetch_app() -> crate.Application:
    a = await client.fetch_app(33226)
    fetched_user = await a.owner.fetch_self()
    print(fetched_user)
    return a


@view
async def test_profile() -> crate.Profile:
    pf = await client.fetch_profile(MID, aiobungie.MembershipType.STEAM)
    warlock = await pf.warlock()
    titan = await pf.titan()
    hunter = await pf.hunter()
    print(warlock, titan, hunter)
    return pf


@view
async def test_player() -> typing.Sequence[typing.Optional[crate.DestinyUser]]:
    p = await client.fetch_player("Datto#6446")
    profile = await p[0].fetch_self_profile()
    print(repr(profile))
    print(repr(await profile.titan()))
    return p


@view
async def test_char() -> crate.Character:
    c = await client.fetch_character(
        MID, aiobungie.MembershipType.STEAM, aiobungie.Class.WARLOCK
    )
    return c

@view
async def test_membership_types_from_id() -> crate.User:
    u = await client.fetch_membership_from_id(MID)
    return u

@view
async def test_search_users() -> typing.Any:
    x = await client.search_users("Fate怒")
    return x

@view
async def test_clan_conves():
    return await client.fetch_clan_conversations(881267)

@view
async def test_clan_admins():
    return await client.fetch_clan_admins(4389205)

@view
async def test_groups_for_member():
    obj = await client.fetch_groups_for_member(MID, aiobungie.MembershipType.STEAM)
    if obj is None:
        return None
    up_to_date_clan_obj = await obj.fetch_self_clan()
    print(repr(up_to_date_clan_obj))
    return obj

@view
async def test_potential_groups_for_member():
    obj = await client.fetch_potential_groups_for_member(MID, aiobungie.MembershipType.STEAM)
    if obj is None:
        return None
    up_to_date_clan_obj = await obj.fetch_self_clan()
    print(repr(up_to_date_clan_obj))
    return obj

@view
async def test_linked_profiles():
    obj = await client.fetch_linked_profiles(4611686018468008855, aiobungie.MembershipType.ALL, all=True)
    print(repr(obj.profiles_with_errors), repr(obj.bungie))
    try:
        async for profile in obj:
            print(repr(profile))
            transform_profile = await profile.fetch_self_profile()
            print(repr(transform_profile))
    except StopIteration:
        pass

@view
async def test_clan_banners():
    cb = await client.fetch_clan_banners()
    for banner in cb:
        print(repr(banner))

@view
async def test_public_milestones_content():
    cb = await client.fetch_public_milestone_content(4253138191)
    print(repr(cb))

async def main() -> None:
    coros = [
        test_clan_banners(),
        test_linked_profiles(),
        test_clan_admins(),
        test_player(),
        test_users(),
        test_user_themese(),
        test_hard_types(),
        test_clan(),
        test_clan_from_id(),
        test_fetch_clan_member(),
        test_fetch_inventory_item(),
        test_profile(),
        test_char(),
        test_membership_types_from_id(),
        test_search_users(),
        test_fetch_app(),
        test_clan_conves(),
        test_groups_for_member(),
        test_potential_groups_for_member(),
        test_public_milestones_content()
    ]
    print(await asyncio.gather(*coros))
    await client.rest.close()

if __name__ == '__main__':
    raise SystemExit(client.run(main()))
