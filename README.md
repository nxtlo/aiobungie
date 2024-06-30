# aiobungie

A statically typed, asynchronous API wrapper that supports Bungie's REST API for Python 3.

## Installing

Currently Python 3.10, 3.11 and 3.12 are supported.

Latest Release using `pip`.

```sh
pip install aiobungie
```

Development via github master.

```sh
pip install git+https://github.com/nxtlo/aiobungie@master
```

## Quick Example

See [Examples for advance usage](https://github.com/nxtlo/aiobungie/tree/master/examples)

```py
import aiobungie
import asyncio

client = aiobungie.Client('YOUR_API_KEY')

async def main() -> None:
    # Search for Destiny 2 players.
    async with client.rest:
        users = await client.search_users("Fate")
        for user in users:
            # Print all Destiny 2 memberships for this user.
            print(user.memberships)
            

asyncio.run(main())
```

## RESTful clients

aiobungie also provides a stand-alone `RESTClient` / `RESTPool` which's what `Client` built on top of, These clients just provide a lower-level abstraction.

A key note is that any `Client` based user can access the `RESTClient` instance bound to it with `.rest` property.

### Key features

* Lower level, allows to read and deserialize the JSON objects yourself.
* `RESTClient`s do not turn response payloads into one of `aiobungie.crates` object.
* RESTful, You can use this as your REST API client in backend directly.
* Both manifest and OAuth2 methods are usable directly.

### Example

```py
import aiobungie
import asyncio

# Single REST client connection.
client = aiobungie.RESTClient("YOUR_API_KEY")

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

## Dependencies

* aiohttp
* attrs
* [`sain`](https://github.com/nxtlo/sain), this is a dependency free package.
* `backports.datetime_fromisoformat`, required for `Python 3.10` only.

### Features

aiobungie features are extra dependencies that replaces the standard library with either faster/neater pkgs.

* `speedup`
This will include and uses [orjson](https://github.com/ijl/orjson) or [ujson](https://github.com/ultrajson/ultrajson)
as the default `json` parser. They provide faster json serialization and de-serialization than the standard Python JSON pkg.
* `full`: This will include all of the features above.

For installing the specified feature, type `pip install aiobungie[feature-name]`

## Contributing

Please read this [manual](https://github.com/nxtlo/aiobungie/blob/master/CONTRIBUTING.md)

## Related Projects

If you have used aiobungie and want to show your work, Feel free to Open a PR including it.

* [Fated](https://github.com/nxtlo/Fated/blob/master/core/components/destiny.py): A Discord BOT that uses aiobungie.

## Useful Resources

* Discord Username: `vfate`
* aiobungie Documentation: [Here](https://nxtlo.github.io/aiobungie/).
* BungieAPI Discord: [Here](https://discord.gg/vP7VC7TKUG)
* Official Bungie Documentation: [Here](https://bungie-net.github.io/multi/index.html)
* Bungie Developer Portal: [Here](https://www.bungie.net/en/Application)

## Additional information

If you have any question you can either open a blank issue, open a new github discussion, or just tag me in BungieAPI discord server.
