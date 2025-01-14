# aiobungie

An ergonomic, statically typed, asynchronous API wrapper that supports Bungie's REST API for Python 3.

aiobungie is built to be extensible and reusable, allowing its users to freely switch parts of core implementations with their own incase of future circumstances.

## Installing

Currently Python 3.10, 3.11, 3.12 and 3.13 are supported.

Stable `pip`.

```sh
pip install aiobungie
```

unstable releases via GitHub master.

```sh
pip install git+https://github.com/nxtlo/aiobungie@master
```

## Quick Look

See [Examples](https://github.com/nxtlo/aiobungie/tree/master/examples) for advance usage.

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

aiobungie also provides a stand-alone [RESTClient](https://nxtlo.github.io/aiobungie/aiobungie/rest.html#RESTClient) / [RESTPool](https://nxtlo.github.io/aiobungie/aiobungie/rest.html#RESTPool) clients which are the foundation of [Client](https://nxtlo.github.io/aiobungie/aiobungie/client.html#Client), These clients just provide a lower-level abstraction.

a `Client` based user may access the `RESTClient` instance bound to it with `.rest` property.

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

        # two simple methods for fetching and refreshing tokens.
        tokens = await client.fetch_oauth2_tokens('code')
        refreshed_tokens = await client.refresh_access_token(tokens.refresh_token)

        # making your own requests.
        response = await client.static_request(
            "GET", # Method.
            "Destiny2/path/to/route", # Route.
            auth="optional_access_token", # If the method requires OAuth2.
            json={"some_key": "some_value"} # If you need to pass JSON data.
        )

asyncio.run(main())
```

## When to use which?

* Use `Client` when:
  * You want a high-level interface.
  * You're building a Bot, i.e, Discord Bot, Chat Bot.
  * You're building a CLI tool.
  * In a single script file.
* Use `RESTClient` when:
  * You want an interface similar to `Client` but with extra functionalities.
  * You want raw JSON responses instead of data-classes.
  * You want REST API functionalities.
  * You want full ownership of the requests/responses.
* Use `RESTPool` when:
  * everything `RESTClient` provides.
  * You want to spawn multiple `RESTClient`s.
  * You're building a distributed backend.

## Dependencies

* aiohttp
* attrs
* [`sain`](https://github.com/nxtlo/sain), this is a dependency free utility package.
* `backports.datetime_fromisoformat`, required for `Python 3.10` only.

### Features

aiobungie features are extra dependencies that replaces the standard library with either faster/neater pkgs.

* `speedup`
This will include and use [orjson](https://github.com/ijl/orjson)
as the default `json` parser. It provide faster JSON serialization and de-serialization than the standard Python JSON pkg.
* `full`: This will include all of the features above.

For installing the specified feature, type `pip install aiobungie[feature-name]`

## Optimizations

* runtime-assertion: You can disable runtime assertions by passing a `-O` flag `python app.py -O`,
the API responses won't get asserted at runtime which may boost the return speeds by a bit.
* [uvloop](https://github.com/MagicStack/uvloop) (unix systems only): uvloop is an _ultra-fast_ drop in replacement library for the built-in asyncio event loop.

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

## Notes

* If you need help with something related to this project: Consider opening a blank issue, discussion or checkout the `useful resources` above.
* `aiobungie` doesn't support `X` update, what now? `aiobungie`'s REST client has a method called `static_request` which allows you to make your own requests, check out `examples/custom_client` example.
* `aiobungie`'s release cycles are _slow_, It takes a couple of months between each release, Some features / routes may not be available on stable version, though, it is still possible to define your own routes on top of `aiobungie`'s clients foundation.
