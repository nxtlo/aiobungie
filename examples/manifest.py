"""An example on how to download and use Destiny2 Manifest.

aiobungie's REST interface provides 5 methods to interact with the manifest.

* fetch_manifest_path
This fetch the manifest path calling `Destiny2/Manifest` endpoint and return
JSON response contains all available data.

* read_manifest_bytes
This can be used to read the raw bytes of the SQLite version manifest.
Its a low-levelish method to read and write the bytes yourself.

* download_manifest
This is the standard method to download the SQLite manifest.
It will read, write, zip, unzip and prepare the manifest file to be used.

* download_json_manifest
Same as download_manifest but it will download the JSON manifest instead of SQLite.

* fetch_manifest_version
Lookups the current manifest version.
"""

import asyncio
import json
import random
import sqlite3

import aiobungie

# The reason we're using REST client here is because we're working with raw data directly.
# So we don't need the Base client impl.

# NOTE: Interacting with manifest doesn't requires a token. So we can leave this as an empty string.
client = aiobungie.RESTClient("...")


async def sqlite_manifest() -> None:
    # Download the SQLite manifest.
    # The force parameter will force the download even if the file exists.
    manifest_path = await client.download_sqlite_manifest(force=True)

    # The manifest version.
    manifest_version = await client.fetch_manifest_version()
    print(manifest_version)

    # Connect to the manifest database.
    # The default path is `manifest.sqlite3`.
    manifest = sqlite3.connect(manifest_path)
    manifest.row_factory = sqlite3.Row

    # Select an inventory item from the manifest and return the object if it matches the given id.
    levante_prize_json = (
        manifest.cursor()
        .execute(
            "SELECT json FROM DestinyInventoryItemDefinition WHERE id = -757221402"
        )
        .fetchone()
    )
    print(levante_prize_json[0])


async def json_manifest() -> None:
    # Download the JSON manifest.
    manifest = await client.download_json_manifest()

    with manifest.open("r") as file:
        manifest_json = json.loads(file.read())
        random_item = random.choice(
            list(manifest_json["DestinyInventoryItemDefinition"].values())
        )
        print(random_item)


async def main():
    async with client:
        await json_manifest()
        # await sqlite_manifest()


if __name__ == "__main__":
    asyncio.run(main())
