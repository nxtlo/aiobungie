# aiobungie
A statically typed API wrapper for the Bungie's REST API written in Python3 and Asyncio.

# Installing

PyPI stable release.

```sh
$ pip install aiobungie
```

Development
```sh
$ pip install git+https://github.com/nxtlo/aiobungie@master
```

## Quick Example

See [Examples for advance usage.](https://github.com/nxtlo/aiobungie/tree/master/examples)

```python
import aiobungie

client = aiobungie.Client('YOUR_API_KEY')

async def main() -> None:

    # fetch a clan
    clan = await client.fetch_clan("Nuanceㅤ")

    # Fetch the clan members.
    members = await clan.fetch_members()

    # Filter the results to return only steam members from the clan.
    for member in members.filter(lambda m: m.type is aiobungie.MembershipType.STEAM):
        # Get the profile for this clan member.
        profile = await member.fetch_self_profile(
            components=[aiobungie.ComponentType.CHARACTERS]
        )

        print(profile.characters)

# You can either run it using the client or just `asyncio.run(main())`
client.run(main())
```

## RESTful clients
Alternatively, You can use `RESTClient` which's designed to only make HTTP requests and return JSON objects.

### Example
```py
import aiobungie
import asyncio

async def main(access_token: str) -> None:
    # Single REST client.
    async with aiobungie.RESTClient("TOKEN") as rest_client:
        response = await rest_client.fetch_clan_members(4389205)
        raw_members_payload = response['results']

        for member in raw_members_payload:
            print(member)

        # Methods only exposed through the REST API.
        await rest.refresh_access_token('a token')

asyncio.run(main("DB_ACCESS_TOKEN"))
```

## REST client pooling.

A REST client pool allows you to acquire multiple `RESTClient`
instances that shares the same connection.

### Example
```py
import aiobungie
import asyncio

pool = aiobungie.RESTPool("token")

async def func1() -> None:
    async with pool.acquire() as instance:
        tokens = await instance.fetch_oauth2_tokens('code')
        pool.metadata['tokens'] = tokens

async def func2() -> None:
    async with pool.acquire() as instance:
        tokens = pool.metadata['tokens']
        await instance.refresh_access_token(tokens.refresh_token)

async def main() -> None:
    await asyncio.gather(func1(), func2())

asyncio.run(main())
```

### Requirements
* Python 3.9 or higher
* aiohttp
* attrs

## Contributing
Please read this [manual](https://github.com/nxtlo/aiobungie/blob/master/CONTRIBUTING.md)

### Getting Help
* Discord: `Fate 怒#0008` | `350750086357057537`
* Docs: [Here](https://nxtlo.github.io/aiobungie/).
