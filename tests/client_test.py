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


import aiobungie
import time
from aiobungie.objects import (
    Clan,
    Player,
    Character,
    User,
    Application,
    Activity,
    Profile,
)
from tests.config import data, TOKEN
import asyncio

class ClientTest(aiobungie.Client):
    def __init__(self, token: str) -> None:
        super().__init__(token=token)

    async def app_test(self):
        app: Application = await self.fetch_app(data["app"])
        print(
            app.human_timedelta,
            app.owner.link,
            app.id,
            app.published_at,
            app.as_dict,
            app.link,
            app.redirect_url
        )

    async def player_test(self) -> None:
        player: Player = await self.fetch_player(
            data["me"], aiobungie.MembershipType.ALL
        )
        print(
            player.name,
            player.id,
            player.is_public,
            player.icon,
            player.as_dict,
            player.type
        )

    #async def man_test(self):
        #man = await self.fetch_manifest()
        #await man.download()
        #print(await man.get_raid_image(raid=aiobungie.Raid.DSC))

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
        act: Activity = await self.fetch_activity(
            data["memid"],
            data["charid"],
            aiobungie.GameMode.RAID,
            memtype=data["memtype"],
            page=1,
            limit=1,
        )
        print(act.when)
        print(f"GameMode {act.mode}")
        print(f"Total Kills {act.kills}")
        print(f"Total assists {act.assists}")
        print(f"Total Players {act.player_count}")
        print(f"Total Deaths {act.deaths}")
        print(f"Duration {act.duration}")
        print(f"K/D {act.kd}")
        # print(f"Hash {act.hash}")
        print(f"Raw Hash {act.raw_hash}")
        print(f"is Completed {act.is_completed}")
        # print(f"Fastest: {act.fast}")s

    async def char_test(self):
        char: Character = await self.fetch_character(
            data["memid"], data["memtype"], data["char"]
        )
        print(repr(char))
        print(char.last_played_delta)
        print(char.member_id)
        print(char.member_type)
        print(char.last_played)
        print(char.emblem)
        print(char.emblem_hash)
        print(char.emblem_icon)
        print(char.level)
        print(char.light)
        print(char.stats)

    async def clan_id_test(self):
        clan: Clan = await self.fetch_clan_from_id(data["clanid"])
        print(
            clan.human_timedelta,
            repr(clan),
            clan.owner.link,
            clan.owner.as_dict,
            clan.owner.icon,
            clan.owner.joined_at,
            clan.owner.name,
            clan.owner.id,
            clan.about,
            clan.banner,
            clan.is_public,
            clan.member_count
        )

    async def clan_test(self):
        clan: Clan = await self.fetch_clan("Fast")
        print(
            clan.human_timedelta,
            repr(clan),
            clan.owner.link,
            clan.owner.as_dict,
            clan.owner.icon,
            clan.owner.joined_at,
            clan.owner.name,
            clan.owner.id,
            clan.about,
            clan.banner,
            clan.is_public,
            clan.member_count
        )

    async def user_test(self):
        user: User = await self.fetch_user("Fate", position=24)
        print(
            repr(user),
            user.human_timedelta,
            user.about,
            user.name,
            user.created_at,
            user.blizzard_name,
            user.status,
            user.steam_name,
            user.is_deleted,
            user.picture,
            user.psn_name,
            user.id,
        )

    async def user_id_test(self):
        user: User = await self.fetch_user_from_id(data['id'])
        print(
            print(repr(user)),
            user.human_timedelta,
            user.about,
            user.name,
            user.created_at,
            user.blizzard_name,
            user.status,
            user.steam_name,
            user.is_deleted,
            user.picture,
            user.psn_name,
            user.id,
        )

    async def profile_test(self) -> None:
        profile: Profile = await self.fetch_profile(
            data["memid"],
            aiobungie.MembershipType.STEAM,
            component=aiobungie.Component.PROFILE,
        )
        print(
            profile.name,
            profile.character_ids,
            profile.as_dict,
            profile.delta_last_played,
            profile.power_cap,
            profile.type,
        )

    async def profile_char_test(self) -> None:
        profile: Profile = await self.fetch_profile(
            data["memid"],
            aiobungie.MembershipType.STEAM,
            component=aiobungie.Component.CHARECTERS,
            character=aiobungie.Class.WARLOCK,
        )
        print(
            profile.character,
            profile.character.emblem,
            profile.character.last_played,
            profile.character.member_id,
            profile.character.light,
            profile.character.as_dict,
            profile.character.emblem_icon,
            profile.character.id,
            profile.character.gender,
            profile.character.race
        )


client = ClientTest(TOKEN)


async def main() -> None:
    before = time.time()
    coros = [
        client.clan_id_test(),
        client.clan_test(),
        client.app_test(),
        client.char_test(),
        client.profile_char_test(),
        client.profile_test(),
        client.player_test(),
        client.user_id_test(),
        client.user_test()
    ]
    await asyncio.gather(*coros)
    full = before - time.time()
    print(f"TOOK {1000 * full:,.0f} ms")
    # await client.man_test()
    # print(await client.fetch_vendor_sales())
    """Under is not working yet."""
    # await client.char_test()
    # await client.activity_test()

client.run(main(), debug=True)