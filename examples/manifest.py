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

import json
import sqlite3
import random
import asyncio

import aiobungie

client = aiobungie.RESTClient("...")

async def main():

    async with client:
        # Download the SQLite manifest.
        # The force parameter will force the download even if the file exists.
        await client.download_manifest(force=True)

        # Download the JSON manifest.
        await client.download_json_manifest()

        with open("manifest.json", "r") as f:
            manifest_json = json.loads(f.read())
            random_item = random.choice(list(manifest_json['DestinyInventoryItemDefinition'].values()))
            print(random_item)

        # The manifest version.
        manifest_version = await client.fetch_manifest_version()
        print(manifest_version)

    # Connect to the manifest database.
    # The default path is `manifest.sqlite3`.
    manifest = sqlite3.connect("manifest.sqlite3")

    # Select an inventory item from the manifest and return the object if it matches the given id.
    levante_prize_json = manifest.cursor().execute(
        "SELECT json FROM DestinyInventoryItemDefinition WHERE id = -757221402"
    ).fetchone()
    print(levante_prize_json[0])

if __name__ == '__main__':
    asyncio.run(main())
