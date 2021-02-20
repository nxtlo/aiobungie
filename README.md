## aiobungie

An Asynchronous API wrapper for the bungie API witten in Python.


## Installing

```
pip install aiobungie
```

## Quick Example

```python
import aiobungie

# Without classes.

client = aiobungie.Client(key={'X-API-KEY': 'YOUR_API_KEY'})

async def player(name):
    _player = await client.get_player(name)
    print(_player.name)
    print(_player.icon_path)
    print(_player.id)
    print(_player.type)

client.loop.run_until_complete(player("Sweatcicle"))

# With classes

class PlayerTest(aiobungie.Client):
    def __init__(self):
        super().__init__(key={'X-API-KEY': 'YOUR_API_KEY'})

    async def player_data(self, player_name: str):
        player = await self.get_player(player_name)

        try:
            print(player.name)
            print(player.type)
            print(player.id)
            print(player.icon_path)
        except:
            pass

if __name__ == '__main__':
    plr = PlayerTest()
    plr.loop.run_until_complete(plr.player_data("DeeJ"))
```

### Requirements
* aiohttp
