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

    # Fetch a charatcer with all its components.
    # This includes Equimpents, Inventory, Records, etc.
    async with client.rest:
        my_warlock = await client.fetch_character(
            membership_id,
            aiobungie.MembershipType.STEAM,
            character_id,
            components=[aiobungie.Component.ALL_CHARACTERS]
        )

        for activity in my_warlock.activities:
            # Check if activity is a raid.
            if activity.current_mode and activity.current_mode is aiobungie.GameMode.RAID:
                print(activity.avaliable_activities) # All raids for this character.

# You can either run it using the client or just asyncio.run(main())
client.run(main())
```

## RESTful clients
Alternatively, You can use `RESTClient` which's designed to only make HTTP requests and return JSON objects.
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

### Requirements
* Python 3.9 or higher
* aiohttp
* attrs

## Contributing
Please read this [manual](https://github.com/nxtlo/aiobungie/blob/master/CONTRIBUTING.md)

### Getting Help
* Discord: `Fate 怒#0008` | `350750086357057537`
* Docs: [Here](https://nxtlo.github.io/aiobungie/).
