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

import aiobungie
import os
import sys
import typing
import inspect
import logging
import asyncio

try:
    import dotenv

    dotenv.load_dotenv(verbose=True)
except ImportError:
    pass

# NOTE: If you're on unix based system make sure to run this
# in your terminal. export CLIENT_TOKEN='TOKEN'

client = aiobungie.Client(os.environ["CLIENT_TOKEN"])
MID = 4611686018484639825
_LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


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
    print(members, member)
    print(c.owner)
    return c


async def test_clan() -> aiobungie.crate.Clan:
    c = await client.fetch_clan("Nuanceㅤ ")
    members = await c.fetch_members()
    member = await c.fetch_member("Hizxr")
    print(members, member)
    print(c.owner)
    return c


async def test_fetch_clan_member() -> aiobungie.crate.ClanMember:
    m = await client.fetch_clan_member(4389205, "Fate")
    return m


async def test_fetch_clan_members() -> typing.Sequence[aiobungie.crate.ClanMember]:
    ms = await client.fetch_clan_members(4389205)
    for member in ms:
        if member.bungie.name == "Cosmic":
            fetched_user = await member.bungie.fetch_self()
            print(repr(fetched_user))
    return ms


async def test_fetch_inventory_item() -> aiobungie.crate.InventoryEntity:
    i = await client.fetch_inventory_item(1397707366)
    print(i.about, i.damage, i.description, i.icon)
    return i


async def test_fetch_app() -> aiobungie.crate.Application:
    a = await client.fetch_app(33226)
    fetched_user = await a.owner.fetch_self()
    print(fetched_user)
    return a


async def test_profile() -> aiobungie.crate.Profile:
    pf = await client.fetch_profile(MID, aiobungie.MembershipType.STEAM)
    warlock = await pf.warlock()
    titan = await pf.titan()
    hunter = await pf.hunter()
    print(warlock, titan, hunter)
    return pf


async def test_player() -> typing.Sequence[
    typing.Optional[aiobungie.crate.DestinyUser]
]:
    p = await client.fetch_player("Datto#6446")
    profile = await p[0].fetch_self_profile()
    print(repr(profile))
    print(repr(await profile.titan()))
    return p


async def test_char() -> aiobungie.crate.Character:
    c = await client.fetch_character(
        MID, aiobungie.MembershipType.STEAM, aiobungie.Class.WARLOCK
    )
    return c


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
    print(repr(up_to_date_clan_obj))
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
    print(repr(up_to_date_clan_obj))
    return obj


async def test_linked_profiles() -> None:
    obj = await client.fetch_linked_profiles(
        4611686018468008855, aiobungie.MembershipType.ALL, all=True
    )
    print(repr(obj.profiles_with_errors), repr(obj.bungie))
    try:
        async for profile in obj:
            print(repr(profile))
            transform_profile = await profile.fetch_self_profile()
            print(repr(transform_profile))
    except RuntimeError:
        pass


async def test_clan_banners() -> typing.Sequence[aiobungie.crate.ClanBanner]:
    cb = await client.fetch_clan_banners()
    return cb


async def test_public_milestones_content() -> aiobungie.crate.Milestone:
    cb = await client.fetch_public_milestone_content(4253138191)
    return cb


async def test_static_request() -> None:
    return await client.rest.static_request(
        "GET",
        f"Destiny2/3/Profile/{MID}/?components={aiobungie.Component.EQUIPED_ITEMS.value}",
    )


async def main() -> None:
    coros: typing.MutableSequence[asyncio.Future] = []
    for n, coro in inspect.getmembers(
        sys.modules[__name__], inspect.iscoroutinefunction
    ):
        if n == "main" or not n.startswith("test_"):
            continue
        coros.append(coro())
    print(await asyncio.gather(*coros))


if __name__ == "__main__":
    raise SystemExit(client.run(main()))
