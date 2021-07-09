import aiobungie
import os

from aiobungie.objects.character import Character
from aiobungie.objects import Clan, Player

from asyncio import run
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv("./.env")
TOKEN = str(os.environ.get('TOKEN'))
SECRET = str(os.environ.get('SECRET'))

data: Dict[str, Any] = {
    'me': 'Fate怒',
    'clanid': 4389205,
    'memid': 4611686018484639825,
    'charid': 2305843009444904605,
    'char': aiobungie.DestinyCharecter.WARLOCK,
    'memtype': aiobungie.MembershipType.STEAM,
    'vendor': aiobungie.Vendor.SPIDER
}

class ClientTest(aiobungie.Client):
    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__(key=key)

    async def app_test(self) -> None:
        app = await self.fetch_app(33226)
        print(
            app.created_at, app.name, app.id, app.is_public, app.redirect_url
        )

    async def player_test(self) -> None:
        player: Player = await self.fetch_player(data['me'], data['memtype'])
        print(player.name, player.id, player.type, player.icon, player.is_public)
        print(repr(player))
        print(hash(player))
        print(int(player))

    
    async def man_test(self):
        man = await self.fetch_manifest()
        await man._dbinit()
        print(await man.get_raid_image(aiobungie.Raid.LW))

    async def vendor_test(self):
        resp = await self.fetch_vendor_sales(vendor=data['vendor'], memberid=data['memid'], charid=data['charid'], type=data['memtype'])
        print(resp)

    async def activity_test(self):
        person = await self.fetch_player(data['me'], data['memtype'])
        char = await self.fetch_charecter(data['memid'], data['memtype'], data['char'])
        act = await self.fetch_activity(
            data['memid'], char.id, aiobungie.GameMode.RAID, memtype=data['memtype'], page=1, limit=1
        )
        print(act.when)
        print(person.name)
        print(f'GameMode {act.mode}')
        print(f'Total Kills {act.kills}')
        print(f"Total assists {act.assists}")
        print(f"Total Players {act.player_count}")
        print(f"Total Deaths {act.deaths}")
        print(f"Duration {act.duration}")
        print(f"K/D {act.kd}")
        # print(f"Hash {act.hash}")
        print(f"Raw Hash {act.raw_hash}")
        print(f"is Completed {act.is_completed}")
        # print(f"Fastest: {act.fast}")

    async def char_test(self):
        player: Player = await self.fetch_player(data['me'], data['memtype'])
        char: Character = await self.fetch_charecter(data['memid'], data['memtype'], data['char'])
        #print(char._resp[1])
        print(player.name)
        print(char.emblem)
        print(char.total_played_time)
        print(char.gender)
        print(char.emblem_icon)
        print(char.light)
        print(char.id)
        print(char.race)
        print(char.last_played)
        print(char._class)

    async def clan_test(self):
        clan: Clan = await self.fetch_clan(data['clanid'])
        attrs = f'''
                {clan.id}
                {clan.about}
                {clan.name}
                {clan.member_count}
                {clan.avatar}
                {clan.banner}
                {clan.description}
                {clan.tags}
                {clan.owner.name}
                {clan.owner.last_online}
                {clan.owner.clan_id}
                '''
        print(attrs)


client = ClientTest(TOKEN)
async def main() -> None:
    # await client.app_test()
    # await client.player_test()
    # await client.char_test()
    await client.clan_test()
    # await client.activity_test()

client.loop.run_until_complete(main())