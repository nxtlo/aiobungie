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

    # Fetch a clan
    clan = await client.fetch_clan("Nuanceㅤ")

    # Fetch the clan members.
    members = await clan.fetch_members()

    # Take the first 2 members.
    for member in members.take(2):
        # Get the profile for this clan member.
        profile = await member.fetch_self_profile(
            # Passing profile components as a list.
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

async def main(token: str) -> None:
    # Single REST client.
    async with aiobungie.RESTClient("TOKEN") as rest_client:
        response = await rest_client.fetch_clan_members(4389205)
        raw_members_payload = response['results']

        for member in raw_members_payload:
            print(member)

asyncio.run(main("some token"))
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
