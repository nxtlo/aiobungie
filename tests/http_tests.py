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

"""This file is for real api tests."""

import asyncio
import os
from typing import Sequence

import pytest
try:
    from dotenv import load_dotenv
    load_dotenv()
    token = os.environ['TOKEN']
except (ImportError, KeyError):
    # if you don't have a .env file nor want to install
    # dotenv you can just put your token down here.
    token = ""

import aiobungie
from aiobungie import crate


client = aiobungie.Client(token)
MID = 4611686018484639825


@pytest.mark.asyncio()
async def test_users() -> crate.User:
    u = await client.fetch_user(20315338)
    return u


@pytest.mark.asyncio()
async def test_user_themese() -> Sequence[crate.user.UserThemes]:
    ut = await client.fetch_user_themes()
    return ut


@pytest.mark.asyncio()
async def test_hard_types() -> crate.user.HardLinkedMembership:
    uht = await client.fetch_hard_types(76561198141430157)
    return uht


@pytest.mark.asyncio()
async def test_clan_from_id() -> crate.Clan:
    c = await client.fetch_clan_from_id(4389205)
    members = await c.fetch_members()
    member = await c.fetch_member("Fate")
    print(members, member)
    return c


@pytest.mark.asyncio()
async def test_clan() -> crate.Clan:
    c = await client.fetch_clan("Fast")
    members = await c.fetch_members()
    member = await c.fetch_member("Bj")
    print(members, member)
    return c


@pytest.mark.asyncio()
async def test_fetch_clan_member() -> crate.ClanMember:
    m = await client.fetch_clan_member(4389205, "Fate")
    return m


@pytest.mark.asyncio()
async def test_fetch_clan_members() -> Sequence[crate.ClanMember]:
    ms = await client.fetch_clan_members(4389205)
    return ms


@pytest.mark.asyncio()
async def test_fetch_inventory_item() -> crate.InventoryEntity:
    i = await client.fetch_inventory_item(1397707366)
    print(i.about, i.damage, i.description, i.icon)
    return i


@pytest.mark.asyncio()
async def test_fetch_app() -> crate.Application:
    a = await client.fetch_app(33226)
    return a


@pytest.mark.asyncio()
async def test_profile() -> crate.Profile:
    pf = await client.fetch_profile(MID, aiobungie.MembershipType.STEAM)
    warlock = await pf.warlock()
    titan = await pf.titan()
    hunter = await pf.hunter()
    print(warlock, titan, hunter)
    return pf


@pytest.mark.asyncio()
async def test_player() -> crate.Player:
    p = await client.fetch_player("Fate怒#4275")
    return p


@pytest.mark.asyncio()
async def test_char() -> crate.Character:
    c = await client.fetch_character(
        MID, aiobungie.MembershipType.STEAM, aiobungie.Class.WARLOCK
    )
    return c


@pytest.mark.asyncio()
async def main():
    coros = [
        test_users(),
        test_user_themese(),
        test_hard_types(),
        test_clan_from_id(),
        test_clan(),
        test_fetch_clan_member(),
        test_fetch_clan_members(),
        test_profile(),
        test_fetch_app(),
        test_fetch_inventory_item(),
        test_char(),
    ]
    print(await asyncio.gather(*coros))


if __name__ == "__main__":
    client.run(main(), True)
