from typing import Optional
import aiobungie
import json
import os

token: Optional[str]

try:
    from dotenv import load_dotenv
except (ImportError, ValueError):
    with open('./.env') as e:
        token = e.read()[4:]
else:
    load_dotenv("./.env")
    token = os.environ.get('TOKEN')

client = aiobungie.Client('e8ff97b63a444fe8a2f9fc36e9cdef19')
CLAN = 4389205
MEMID = 4611686018484639825
CHARID = 2305843009444904605
CHAR = aiobungie.DestinyCharecter.TITAN
MEMTYPE = aiobungie.MembershipType.STEAM
VENDOR = aiobungie.Vendor.SPIDER

async def player_test():
    guardian = await client.get_player("Granger", MEMTYPE)
    
    attrs = f'''
            {guardian.name},
            {guardian.id},
            {guardian.icon},
            {guardian.type}
            '''
    print(attrs)


async def man_test():
    man = await client.get_manifest()
    await man._dbinit()
    print(await man.get_raid_image(aiobungie.Raid.LW))

async def vendor_test():
    resp = await client.get_vendor_sales(vendor=VENDOR, memberid=MEMID, charid=CHARID, type=MEMTYPE)
    print(resp)

async def careers_test():
    car = await client.get_careers()
    print(car.categories)

async def activity_test():
    act: client.get_activity_stats() = await client.get_activity_stats(
        MEMID, CHARID, MEMTYPE, aiobungie.GameMode.IRONBANER
    )
    print(act.when)
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

async def char_test():
    player = await client.get_player('ItzKarlz')
    char: client.get_charecter() = await client.get_charecter(player.id[0], aiobungie.MembershipType.XBOX, 0)
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

async def clan_test():
    clan = await client.get_clan(CLAN)
    attrs = f'''
            {clan.id}, 
            {clan.name}, 
            {clan.about}, 
            {clan.description}, 
            {clan.created_at}, 
            {clan.edited_at}",
            {clan.avatar},
            {clan.banner},
            {clan.owner},
            {clan.tag}
            '''
    print(attrs)

async def main():
    # await clan_test()
    # await player_test()
    # await careers_test()
    # await man_test()
    # await vendor_test()
    # print(await client.from_path(f'/Destiny2/{MEMTYPE}/Profile/{MEMID}/?components={aiobungie.Component.CHARECTERS}'))
    await char_test()
    # await activity_test()

client.loop.run_until_complete(main())
