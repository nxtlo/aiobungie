<div align="center">
    <h1>aiobungie</h1>
    <p>An asynchronous statically typed API wrapper for the Bungie API written in Python.</p>
    <a href="https://codeclimate.com/github/nxtlo/aiobungie/maintainability">
    <img src="https://api.codeclimate.com/v1/badges/09e71a0374875d4594f4/maintainability"/>
    </a>
    <a href="https://github.com/nxtlo/aiobungie/issues">
    <img src="https://img.shields.io/github/issues/nxtlo/aiobungie"/>
    </a>
    <a href="http://python.org">
    <img src="https://img.shields.io/badge/python-3.9%20%7C%203.10-blue"/>
    </a>
    <a href="https://pypi.org/project/aiobungie/">
    <img src="https://img.shields.io/pypi/v/aiobungie?color=green"/>
    </a>
    <a href="https://github.com/nxtlo/aiobungie/blob/master/LICENSE">
    <img src="https://img.shields.io/pypi/l/aiobungie"/>
    </a>
    <a href="https://github.com/nxtlo/aiobungie/actions/workflows/ci.yml">
    <img src="https://github.com/nxtlo/aiobungie/actions/workflows/ci.yml/badge.svg?branch=master">
    </a>
    <a href="https://pepy.tech/project/aiobungie">
    <img src="https://pepy.tech/badge/aiobungie">
    </a>
</div>

# Installing

_IT IS recommended_ to use the latest pre-release from master
since `0.2.4` is missing features from `0.2.5`.


PyPI stable release. __Not Recommended Currently__.

```sh
$ pip install aiobungie
```

From master __Recommended Currently__.

```sh
$ pip install git+https://github.com/nxtlo/aiobungie
```

## Quick Example

See [Examples for advance usage.](https://github.com/nxtlo/aiobungie/tree/master/examples)

```python
import aiobungie

# crates in aiobungie are implementations
# of Bungie's objects to provide
# more functionality.

client = aiobungie.Client('YOUR_API_KEY')

async def main() -> None:

    # fetch a clan
    clan: aiobungie.crate.Clan = await client.fetch_clan("Nuanceㅤ")
    print(clan.name, clan.id)

    # Clan owner.
    if owner := clan.owner:

        # Fetch a profile.
        profile: aiobungie.crate.Component = await client.fetch_profile(
            owner.id,
            owner.type,
            # Return All profile components and character components.
            aiobungie.ComponentType.CHARACTERS,
            *aiobungie.ComponentType.ALL_PROFILES.value
            # If a method requires OAuth2 you may wanna pass an auth token as a kwarg.
            auth="access_token"
        )

        # A profile characters component as a mapping from each character id to a character object.
        if owner_characters := profile.characters:
            for character_id, character in owner_characters.items():
                print(f"ID: {character_id}: Character {character}")

                # Check if warlock
                if character.class_type is aiobungie.Class.WARLOCK:
                    # Do something with the warlock
                    ...

# You can either run it using the client or just `asyncio.run(main())`
client.run(main())
```

## RESTful client
Alternatively, You can use `RESTClient` which's designed to only make HTTP requests and return JSON objects.

### Quick Example
```py
import aiobungie
import asyncio

async def main(access_token: str) -> None:
    # Max retries is the maximum retries to backoff when you hit 5xx error codes.
    # It defaults to 4 retries.
    async with aiobungie.RESTClient("TOKEN", max_retries=5) as rest:
        # Passing the player's name and code -> 'Fate怒#4275'
        fetch_player = await rest.fetch_player('Fate怒', 4275)
        print(*fetch_player) # A JSON array of dict object
        for player in fetch_player: # Iterate through the array.
            print(player['membershipId'], player['iconPath']) # The player id and icon path.
            for k, v in player.items():
                print(k, v)

            # You can also send your own requests.
            await rest.static_request("POST", "Need/OAuth2", headers={"A-HEADER": f"A-Value"}, auth=access_token)
            # Defined methods.
            await rest.send_friend_request(access_token, member_id=1234)

asyncio.run(main("DB_ACCESS_TOKEN"))
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
