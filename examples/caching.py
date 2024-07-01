"""A basic example on how to cache objects in memory to avoid making HTTP requests."""

import aiobungie
import asyncio

client = aiobungie.Client("TOKEN")


# Setup some global map locations in the client metadata.
# This function usually will run once at the start of your program.
def setup_cache():
    client.metadata["items"] = {}


async def get_item(item_id: int) -> aiobungie.crates.InventoryEntity:
    items: dict[int, aiobungie.crates.InventoryEntity] = client.metadata["items"]

    # Check if the item is cached in our client metadata.
    # Returns the item if it was cached otherwise perform an HTTP request fetching it.
    if (item := items.get(item_id)) is not None:
        return item

    # fetch and store the item for later access
    item = await client.fetch_inventory_item(item_id)
    items[item_id] = item
    return item


async def main() -> None:
    setup_cache()

    # We call this `get_item` 5 times concurrently, The first call will be an HTTP request,
    # The rest will be retrieved from the cache.
    item_tasks = asyncio.create_task(*(get_item(2203) for _ in range(5)))
    items = await asyncio.gather(*item_tasks)
    for item in items:
        ...

    for item_id, item in client.metadata["items"].items():
        print(item_id, item)


if __name__ == "__main__":
    asyncio.run(main())
