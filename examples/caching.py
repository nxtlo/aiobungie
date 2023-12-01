"""A basic example on how to cache objects in memory to avoid making HTTP requests."""

import aiobungie
from aiobungie.internal import helpers

client = aiobungie.Client("TOKEN")

MEMBER_ID = 4611  # Sample member_ship id
CHAR_ID = 23019  # Sample character id
MEMBER_TYPE = aiobungie.MembershipType.STEAM


# Setup some map locations in the client metadata.
# This function usually will run once at the start of your program.
def setup_cache():
    client.metadata["items"] = {}


async def get_item(id: int) -> aiobungie.crates.InventoryEntity:
    items: dict[int, aiobungie.crates.InventoryEntity] = client.metadata["items"]

    # Check if the item is cached in our client metadata.
    # Returns the item if it was cached otherwise perform an HTTP request fetching it.
    if (item := items.get(id)) is not None:
        return item

    item = await client.fetch_inventory_item(id)
    items[id] = item
    return item


async def main() -> None:
    setup_cache()

    # We call this `get_item` 5 times concurrently, The first call will be an HTTP request,
    # The rest will be retrieved from the cache.
    items = await helpers.awaits(*(get_item(2203) for _ in range(5)))
    for item in items:
        ...

    for item_id, item in client.metadata["items"].items():
        print(item_id, item)


if __name__ == "__main__":
    client.run(main())
