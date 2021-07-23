import aiobungie
import json
import os
from aiobungie.objects import (
    Clan,
    Player,
    Character,
    User,
    Application,
    Activity,
    Profile,
)

import asyncio
from dotenv import load_dotenv
from typing import Dict, Any, TYPE_CHECKING

load_dotenv("./.env")
TOKEN = str(os.environ.get("TOKEN"))
SECRET = str(os.environ.get("SECRET"))

data: Dict[str, Any] = {
    "me": "Fate怒",
    "id": 20315338,
    "app": 33226,
    "clanid": 4389205,
    "memid": 4611686018484639825,
    "charid": 2305843009444904605,
    "char": aiobungie.Class.WARLOCK,
    "memtype": aiobungie.MembershipType.STEAM,
    "vendor": aiobungie.Vendor.SPIDER,
}


class ClientTest(aiobungie.Client):
    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__(key=key)

    async def app_test(self):
        app: Application = await self.fetch_app(data["app"])
        print(repr(app), repr(app.owner))

    async def player_test(self) -> None:
        player: Player = await self.fetch_player(
            "Lukzy", aiobungie.MembershipType.STEAM, position=0
        )
        print(player.name, player.id, player.type, player.icon, player.is_public)
        print(repr(player))
        print(hash(player))
        print(int(player))

    async def man_test(self):
        man = await self.fetch_manifest()
        await man.download()
        print(await man.get_raid_image(raid=aiobungie.Raid.DSC))

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
        attrs = f"""
                {clan.name}
                {clan.id}
                {clan.member_count}
                {clan.about}
                {clan.tags}
                {clan.description}
                {clan.owner.type}
                {clan.owner.last_online}
                {clan.owner.joined_at}
                """
        print(attrs)

    async def clan_test(self):
        clan: Clan = await self.fetch_clan("Fast")
        attrs = f"""
                {clan.name}
                {clan.avatar}
                {clan.banner}
                {clan.id}
                {clan.member_count}
                {clan.about}
                {clan.tags}
                {clan.description}
                {clan.owner.type}
                {clan.owner.last_online}
                {clan.owner.joined_at}
                """
        print(attrs)

    async def user_test(self):
        user: User = await self.fetch_user("Fate")
        print(
            user.name,
            user.id,
            user.created_at,
            user.is_deleted,
            user.about,
            user.picture,
            user.blizzard_name,
            user.status,
            user.steam_name,
            user.psn_name,
            user.twitch_name,
            user.locale,
            user.human_time,
        )

    async def user_id_test(self):
        user: User = await self.fetch_user_from_id(data["id"])
        print(
            user.name,
            user.id,
            user.created_at,
            user.is_deleted,
            user.about,
            user.picture,
            user.blizzard_name,
            user.status,
            user.steam_name,
            user.psn_name,
            user.twitch_name,
            user.locale,
            user.human_time,
        )

    async def profile_test(self) -> None:
        profile: Profile = await self.fetch_profile(
            data["memid"],
            aiobungie.MembershipType.STEAM,
            component=aiobungie.Component.PROFILE,
        )
        print(repr(profile))

    async def profile_char_test(self) -> None:
        profile: Profile = await self.fetch_profile(
            data["memid"],
            aiobungie.MembershipType.STEAM,
            component=aiobungie.Component.CHARECTERS,
            character=aiobungie.Class.WARLOCK,
        )
        print(repr(profile.character))
        print(profile.character.emblem)
        print(profile.character.last_played)
        print(profile.character.member_id)
        print(profile.character.light)


client = ClientTest(TOKEN)


async def main() -> None:
    coros = [
        client.profile_test(),
        client.profile_char_test(),
        client.player_test(),
        client.char_test(),
        client.clan_test(),
        client.clan_id_test(),
        client.user_id_test(),
        client.user_test(),
        client.app_test(),
        client.with_enter()
    ]
    await asyncio.gather(*coros)
    await client.man_test()
    # print(await client.fetch_vendor_sales())
    """Under is not working yet."""
    # await client.char_test()
    # await client.activity_test()

client.run(main())