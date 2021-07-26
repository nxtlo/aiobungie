![aiobungie open Issue](https://img.shields.io/github/issues/nxtlo/aiobungie)
![aiobungie Python Version Support](https://img.shields.io/pypi/pyversions/aiobungie)
![aiobungie PyPI last Version](https://img.shields.io/pypi/v/aiobungie?color=green)
![aiobungie LICENSE](https://img.shields.io/pypi/l/aiobungie)
[![CodeFactor](https://www.codefactor.io/repository/github/nxtlo/aiobungie/badge)](https://www.codefactor.io/repository/github/nxtlo/aiobungie)

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

See [Examples for more.](https://github.com/nxtlo/aiobungie/tree/master/examples)

```python
import aiobungie

client = aiobungie.Client(key='YOUR_API_KEY')

async def main() -> None:

    # fetch a clan from its id.
    clan = await client.fetch_clan_from_id(1234)
    # or fetch the clan by its name
    clan = await client.fetch_clan("Fast")
    print(f'{clan.id}, {clan.name}, {clan.owner}, {clan.created_at}, {clan.about}')

    # fetch a destiny 2 player.
    player = await client.fetch_player('Fate怒')
    print(f'{player.name}, {player.id[0]}, {player.icon}, {player.type}')

    # fetch a specific character.
    char = await client.fetch_character(player.id[0], aiobungie.MembershipType.STEAM, aiobungie.Class.WARLOCK)
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

### Requirements
* Python >=3.8 -> Required.
* aiohttp -> Required for http.
* aredis -> Optional for cache.
* aiosqlite -> Optional for Manifest db.

### Getting Help
* Discord: `Fate 怒#0008` | `350750086357057537`
* Docs: [Here](https://nxtlo.github.io/aiobungie/).