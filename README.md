# aiobungie
A statically typed, asynchronous API wrapper for building clients for Bungie's API in Python.

# Installing

Currently Python 3.10, 3.11 and 3.12 are supported.

Stable release.

```sh
$ pip install aiobungie
```

Development via github master.
```sh
$ pip install git+https://github.com/nxtlo/aiobungie@master
```

## Quick Example

See [Examples for advance usage.](https://github.com/nxtlo/aiobungie/tree/master/examples)

```py
import aiobungie

client = aiobungie.Client('YOUR_API_KEY')

async def main() -> None:
    # Fetch a Destiny 2 character passing a component.
    # This includes Equipments, Inventory, Records, etc.
    async with client.rest:
        my_warlock = await client.fetch_character(
            member_id=4611686018484639825,
            membership_type=aiobungie.MembershipType.STEAM,
            character_id=2305843009444904605,
            components=[aiobungie.ComponentType.CHARACTER_EQUIPMENT],
        )
        # Other components will be populated when passed to `components=[...]`
        # Otherwise will be `None`

        # Make sure the component is fetched.
        assert my_warlock.equipment is not None

        # Get the first item equipped on this character.
        item = my_warlock.equipment[0]
        print(item.hash, item.location, item)

        # Fetch this item, Note that this performs an HTTP request.
        # Alternatively, You can use the manifest here instead.
        # See examples folder for more information.
        item = await my_warlock.equipment[0].fetch_self()
        print(item.name, item.type_and_tier_name)
        # Prints: Izanagi's Burden Exotic Sniper Rifle

# You can either run it using the client or just asyncio.run(main())
client.run(main())
```

## RESTful clients
Alternatively, You can use `RESTClient` or `RESTPool` which're designed to only make HTTP requests and return JSON objects.
and to interact with the manifest.

### Example
```py
import aiobungie
import asyncio

# Single REST client connection.
client = aiobungie.RESTClient("...")

async def main() -> None:
    async with client:
        # SQLite manifest.
        await client.download_manifest()

        # OAuth2 API.
        tokens = await client.fetch_oauth2_tokens('code')

asyncio.run(main())
```

## Requirements
* Python 3.10 or higher is required.
* aiohttp
* attrs

### Speed-ups - Optional
Additionally, If you have [orjson](https://github.com/ijl/orjson) or [ujson](https://github.com/ultrajson/ultrajson)
installed they will be used as the default JSON parser.

Just install `pip install aiobungie[speedup]` like this.

They provide faster json serialization and de-serialization than the standard Python JSON pkg.

## Contributing
Please read this [manual](https://github.com/nxtlo/aiobungie/blob/master/CONTRIBUTING.md)

## Related Projects
If you have used aiobungie and want to show your work, Feel free to Open a PR including it.

* [Fated](https://github.com/nxtlo/Fated/blob/master/core/components/destiny.py): My Discord BOT for testing purposes.

## Getting Help
* Discord Username: `fateq`
* BungieAPI Discord: [Here](https://discord.gg/vP7VC7TKUG)
* Docs: [Here](https://nxtlo.github.io/aiobungie/).
