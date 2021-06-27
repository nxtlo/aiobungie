## aiobungie

An Asynchronous API wrapper for the bungie API witten in Python.


## Installing

```
pip install aiobungie
```

## Quick Example

```python
import aiobungie

client = aiobungie.Client(key='YOUR_API_KEY')

async def main() -> None:

    clan = await client.get_clan(1234)
    print(f'{clan.id}, {clan.name}, {clan.owner}, {clan.created_at}, {clan.about}')

    player = await client.get_player('Fate怒')
    print(f'{player.name}, {player.id[0]}, {player.icon}, {player.type}')

    char = await client.get_character(player.id[0], aiobungie.MembershipType.STEAM, aiobungie.DestinyCharacter.WARLOCK)
    print(f'{char.emblem}, {char.light}, {char.id}, {char.race}, {char.gender}, {char._class}')

    activ = await client.get_activity_stats(player.id[0], char.id, aiobungie.MembershipType.STEAM, aiobungie.GameMode.RAID)
    print(
        f'''{activ.mode}, {activ.kills}, {activ.player_count}, 
        {activ.duration}, {activ.when}, {activ.kd}, {activ.deaths},
        {activ.assists}, {activ.hash} -> raids only {activ.raw_hash} -> Any
        ''')

    # Raw search
    print(await client.from_path('User/.../.../'))


# OAuth2 is not fully implemented yet.

from aiobungie.experiements import OAuth2, refresh

auth_client = OAuth2(token='', secret='')

# Use the refresh decorator to automatically refresh the tokens
# The cls param is required to get the client secret and pass it to the POST request.
@refresh(every=3600, cls=auth_client)
async def auth_stuff() -> None:
    await auth_client.do_auth() # Creates sqlite db, Open a page get the code param then paste it in the pormpt.
                                # You will only do this one, after it will auto_refresh the tokens for you.
    print(await auth_client.get_current_user())

client.loop.run_until_complete(main())
client.loop.run_until_complete(auth_stuff())
```

### Requirements
>= Python3.8 <= 4.0
* httpx

### OAuth and Dev
* requests_oauthlib
* aiosqlite
* aiofiles
* python-dotenv
