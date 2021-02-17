from aiobungie import Client

client = Client(key={'X-API-KEY': ''})


async def tests():
    app = await client.get_app(38349)
    player = await client.get_player("DeeJ")

    print(player.id)
    print(player.type)
    print(player.name)
    print(player.icon_path)

    print(app.id)
    print(app.name)
    print(app.created_at)
    print(app.published_at)
    print(app.redirect_url)
    print(app.owner_id)
    print(app.owner_name)
    print(app.is_public)

def main():
    client.loop.run_until_complete(tests())

if __name__ == '__main__':
    main()
