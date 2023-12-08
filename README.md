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
aiobungie also provides a stand-alone `RESTClient` / `RESTPool` which's what `Client` built on top of, These clients just provide a lower-level abstraction.

A key note is that any `Client` based user can access the `RESTClient` instance bound to it with `.rest` property.

### Key Features
* Lower level, allows to read and deserialize the JSON objects yourself.
* `RESTClient`s do not turn response payloads into one of `aiobungie.crates` object.
* RESTful, You can use this as your REST API client in backend directly.
* Both `Manifest` and `OAuth` methods are usable directly.


### Example
```py
import aiobungie
import asyncio

# Single REST client connection.
client = aiobungie.RESTClient("...")

async def main() -> None:
    async with client:
        # Download and open the JSON manifest.
        manifest = await client.download_json_manifest(name="latest_manifest")
        with manifest.open("r") as file:
            data = file.read()

        # OAuth2 API. 2 simple methods for fetching and refreshing tokens.
        tokens = await client.fetch_oauth2_tokens('code')
        refreshed_tokens = await client.refresh_access_token(tokens.refresh_token)

        # Testing your own requests.
        response = await client.static_request(
            "GET", # Method.
            "Destiny2/path/to/route", # Route.
            auth="optional_access_token", # If the method requires OAuth2.
            json={"some_key": "some_value"} # If you need to pass JSON data.
        )

asyncio.run(main())
```

## Dependancies
* aiohttp
* attrs
* `backports.datetime_fromisoformat`, required for `Python 3.10` only.

### Speedups - Optional
Additionally, If you have [orjson](https://github.com/ijl/orjson) or [ujson](https://github.com/ultrajson/ultrajson)
installed they will be used as the default JSON parser.

Just install `pip install aiobungie[speedup]` like this.

They provide faster json serialization and de-serialization than the standard Python JSON pkg.

## Contributing
Please read this [manual](https://github.com/nxtlo/aiobungie/blob/master/CONTRIBUTING.md)

## Related Projects
If you have used aiobungie and want to show your work, Feel free to Open a PR including it.

* [Fated](https://github.com/nxtlo/Fated/blob/master/core/components/destiny.py): My Discord BOT for testing purposes.

## Useful Resources
* Discord Username: `fateq`
* aiobungie Documentation: [Here](https://nxtlo.github.io/aiobungie/).
* BungieAPI Discord: [Here](https://discord.gg/vP7VC7TKUG)
* Official Bungie Documentation: [Here](https://bungie-net.github.io/multi/index.html)
* Bungie Developer Portal: [Here](https://www.bungie.net/en/Application)

### Additional information
If you have any question you can either open a blank issue, open a new github discussion, or just tag me in BungieAPI discord server.
