from aiobungie import Client

client = Client('')

async def player_test():
    guardian = await client.get_player("DeeJ")
    
    attrs = f'''
            {guardian.name},
            {guardian.id},
            {guardian.icon_path},
            {guardian.type}
            '''
    print(attrs)


async def clan_test():
    clan = await client.get_clan(4389205)
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

client.loop.run_until_complete(main())
