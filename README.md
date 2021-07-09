# aiobungie

An Asynchronous statically typed API wrapper for the bungie API written in Python.

# Features

* Fully Asynchronous.
* Easy to use.
* Statically typings and annotations.
* All endpoints will be implemented.

# Installing

Official release.

```s
$ pip install aiobungie
```

Development

```s
$ pip install git+https://github.com/nxtlo/aiobungie
```

## Quick Example

```python
import aiobungie

client = aiobungie.Client(key='YOUR_API_KEY')

async def main() -> None:

    # fetch a clan.
    clan = await client.fetch_clan(1234)
    print(f'{clan.id}, {clan.name}, {clan.owner}, {clan.created_at}, {clan.about}')

    # fetch a bungie user.
    player = await client.fetch_player('Fate怒')
    print(f'{player.name}, {player.id[0]}, {player.icon}, {player.type}')

    # fetch a specific character.
    char = await client.fetch_character(player.id[0], aiobungie.MembershipType.STEAM, aiobungie.DestinyCharacter.WARLOCK)
    print(f'{char.emblem}, {char.light}, {char.id}, {char.race}, {char.gender}, {char._class}')

    # fetch activities.
    activ = await client.fetch_activity(player.id[0], char.id, aiobungie.MembershipType.STEAM, aiobungie.GameMode.RAID)
    print(
        f'''{activ.mode}, {activ.kills}, {activ.player_count}, 
        {activ.duration}, {activ.when}, {activ.kd}, {activ.deaths},
        {activ.assists}, {activ.hash} -> raids only {activ.raw_hash} -> Any
        ''')

    # Raw search
    endpoint = await client.from_path('User/.../.../')
    print(endpoint)

client.loop.run_until_complete(main())
```

## OAuth2

```py
# OAuth2 is not fully implemented yet.

from aiobungie.ext import OAuth2, refresh

client = OAuth2(token='', secret='')

# Use the refresh decorator to automatically refresh the tokens
# The cls param is required to get the client secret and pass it to the POST request.

@refresh(hours=1, cls=client)
async def auth_stuff() -> None:
    await client.do_auth()
    print(await client.get_current_user())

client.loop.run_until_complete(auth_stuff())
```

### Requirements
* Python >=3.8
* aiohttp

### OAuth2 and Dev
* cryptography
* requests_oauthlib
* aiosqlite
* aiofiles
* python-dotenv


### Getting Help
* Discord: `Fate 怒#0008`
* Docs: Soon.