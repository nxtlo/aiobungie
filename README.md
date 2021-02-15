## aiobungie

An Asynchronous API wrapper for the bungie API witten in Python.


## Installing

TODO

## Quick Example

```python
from aiobungie import Aiobungie
import asyncio

# You can inherit from the class it self.

class Example(Aiobungie):
    def __init__(self):
        # This will be formatted better later.
        super().__init__(key={'X-API-KEY': 'YOUR_API_KEY'})

    async def player(self):
        player = await self.get_player("Fate 怒")
        print(player.displayname)
        print(player.id)

if __name__ == '__main__':
    ex = Example()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ex.test())

```

### Requirements

* httpx
