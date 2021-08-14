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

"""Non manifest aiobungie tests."""


import asyncio
import os
import time

import aiobungie
from aiobungie import crate
from tests.config import TOKEN
from tests.config import data

# Using uvloop for speedups.
if os.name != "nt":
    try:
        import uvloop
    except ImportError:
        pass
    else:
        uvloop.install()


class ClientTest(aiobungie.Client):
    def __init__(self, token: str) -> None:
        super().__init__(token=token)

    async def app_test(self):
        app: crate.Application = await self.fetch_app(data["app"])
        print(app.as_dict)

    async def player_test(self) -> None:
        player: crate.Player = await self.fetch_player(
            data["me"], aiobungie.MembershipType.ALL
        )
        print(player.as_dict)

    async def vendor_test(self):
        resp = await self.fetch_vendor_sales(
            vendor=data["vendor"],
            memberid=data["memid"],
            charid=data["charid"],
            type=data["memtype"],
        )
        print(resp)

    async def with_enter(self) -> None:
        async with self as resp:
            player = await resp.fetch_player("Fate", aiobungie.MembershipType.STEAM)
            print(player.id)

    async def activity_test(self):
        # char = await self.fetch_charecter(data['memid'], data['memtype'], data['char'])
        act: crate.Activity = await self.fetch_activity(
            data["memid"],
            data["charid"],
            aiobungie.GameMode.RAID,
            membership_type=data["memtype"],
            page=25,
        )
        print(act.as_dict)

    async def char_test(self):
        char: crate.Character = await self.fetch_character(
            data["memid"], data["memtype"], data["char"]
        )
        print(char.as_dict)

    async def clan_id_test(self):
        clan: crate.Clan = await self.fetch_clan_from_id(data["clanid"])
        members = await clan.fetch_members()
        print(members)

    async def clan_test(self):
        clan: crate.Clan = await self.fetch_clan("Nuanceㅤ")
        member: ClanMember = await clan.fetch_member("Fate")
        print(clan.as_dict)
        print(member.as_dict)

    async def user_test(self):
        user: crate.User = await self.fetch_user("Fate", position=24)
        print(user.as_dict)

    async def user_id_test(self):
        user: crate.User = await self.fetch_user_from_id(data["id"])
        print(user.as_dict)

    async def profile_test(self) -> None:
        profile: crate.Profile = await self.fetch_profile(
            data["memid"],
            aiobungie.MembershipType.STEAM,
        )
        print(profile.warlock_id, profile.titan_id, profile.hunter_id)
        print(profile.as_dict)

    async def titan_test(self) -> None:
        profile: crate.Profile = await self.fetch_profile(
            data["memid"], aiobungie.MembershipType.STEAM
        )
        char: crate.Character = await profile.titan()
        print(char.as_dict)

    async def hunter_test(self) -> None:
        profile: crate.Profile = await self.fetch_profile(
            data["memid"], aiobungie.MembershipType.STEAM
        )
        char: crate.Character = await profile.hunter()
        print(char.as_dict)

    async def warlock_test(self) -> None:
        profile: crate.Profile = await self.fetch_profile(
            data["memid"], aiobungie.MembershipType.STEAM
        )
        char: crate.Character = await profile.warlock()
        print(char.as_dict)

    async def hard_linked_test(self) -> None:
        user: crate.HardLinkedMembership = await self.fetch_hard_types(
            76561198141430157, aiobungie.CredentialType.STEAMID
        )
        print(user.id, user.cross_save_type, user.type)


client = ClientTest(TOKEN)


async def main() -> None:
    before = time.time()
    coros = [
        client.activity_test(),
        client.hard_linked_test(),
        client.warlock_test(),
        client.hunter_test(),
        client.titan_test(),
        client.char_test(),
        client.user_id_test(),
        client.user_test(),
        client.clan_id_test(),
        client.clan_test(),
        client.app_test(),
        client.player_test(),
        client.profile_test(),
    ]
    await asyncio.gather(*coros)
    full = before - time.time()
    print(f"Full test TOOK {1000 * full:,.0f} ms")


if __name__ == "__main__":
    client.run(main(), debug=True)
