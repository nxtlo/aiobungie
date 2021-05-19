import aiobungie

with open('./.env') as env:
    token = env.read()

client = aiobungie.Client(token)
CLAN = 4389205
MEMID = 4611686018484639825
CHARID = 2305843009444904605
MEMTYPE = aiobungie.MembershipType.STEAM
VENDOR = aiobungie.Vendor.SPIDER

async def player_test():
    guardian = await client.get_player("Sweatcicle")
    
    attrs = f'''
            {guardian.name},
            {guardian.id},
            {guardian.icon},
            {guardian.type}
            '''
    print(attrs)


async def man_test():
    man = await client.get_manifest()
    print(await man.from_db())
    await man.download()

async def vendor_test():
    resp = await client.get_vendor_sales(vendor=VENDOR, memberid=MEMID, charid=CHARID, type=MEMTYPE)
    print(resp)

async def careers_test():
    car = await client.get_careers()
    print(car.categories)

async def activity_test():
    user = await client.get_clan_admins(CLAN)
    ...

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
    await clan_test()
    # await player_test()
    # await careers_test()
    # await man_test()
    # await vendor_test()
    # await activity_test()

client.loop.run_until_complete(main())
