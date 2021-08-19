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
    <img src="https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10dev-blue"/>
    </a>
    <a href="https://pypi.org/project/aiobungie/">
    <img src="https://img.shields.io/pypi/v/aiobungie?color=green"/>
    </a>
    <a href="https://github.com/nxtlo/aiobungie/blob/master/LICENSE">
    <img src="https://img.shields.io/pypi/l/aiobungie"/>
    </a>
    <a href="https://www.codefactor.io/repository/github/nxtlo/aiobungie/">
    <img src="https://www.codefactor.io/repository/github/nxtlo/aiobungie/badge">
    </a>
    <a href="https://github.com/nxtlo/aiobungie/actions/workflows/ci.yml">
    <img src="https://github.com/nxtlo/aiobungie/actions/workflows/ci.yml/badge.svg?branch=master">
    </a>
    <a href="https://codeclimate.com/github/nxtlo/aiobungie/test_coverage"><img src="https://api.codeclimate.com/v1/badges/09e71a0374875d4594f4/test_coverage" /></a>

</div>

# Installing

_IT IS recommended_ to use the latest release from master
since `0.2.4` is missing features from `0.2.5`.

Theoretically you probably will encounter breaking changes every `0.2.5x` release.

PyPI stable release.

```sh
$ pip install aiobungie
```

From master __Recommended Currently__.

```sh
$ pip install git+https://github.com/nxtlo/aiobungie
```

## Quick Example

See [Examples for more.](https://github.com/nxtlo/aiobungie/tree/master/examples)

```python
import aiobungie
from aiobungie import crate

# crates in aiobungie are implementations
# of Bungie's objects to provide
# more functionality.

client = aiobungie.Client(key='YOUR_API_KEY')

async def main() -> None:

    # fetch a clan
    clan: crate.Clan = await client.fetch_clan("Nuanceㅤ")
    print(clan.name, clan.id, clan.owner.name, clan.owner.id, ...)

    # fetch a member from the clan.
    member: crate.ClanMember = await clan.fetch_member("Fate怒")
    print(member.name, member.id, member.type, ...)

    # fetch the clan members and return only steam players
    members = await clan.fetch_members(aiobungie.MembershipType.STEAM)
    for member in members:
        if member.name == "Fate怒" or member.id == 4611686018484639825:
            print(...)
        else:
            print(member.name, member.id, member.type)

    # fetch my profile.
    profile: crate.Profile = await client.fetch_profile(member.id, member.type)
    print(profile.name, profile.id, profile.type, ...)

    # You can fetch a character in two ways.
    # Whether from the player's profile or
    # using `fetch_character()` method.

    # The profile way.
    warlock: crate.Character = await profile.warlock()
    print(warlock.light, warlock.id, warlock.gender, warlock.race, ...)

    # the fetch_character() way using the profile attrs.
    character: crate.Character = await client.fetch_character(profile.id, profile.type, profile.warlock_id)
    print(character.light, character.id, character.gender, character.race, ...)
```

### Requirements
* Python >=3.8 ,<=3.12
* aiohttp
* attrs.

### Optional Requirements for speedups.
* aiodns
* cchardet
* uvloop

### Getting Help
* Discord: `Fate 怒#0008` | `350750086357057537`
* Docs: [Here](https://nxtlo.github.io/aiobungie/).
