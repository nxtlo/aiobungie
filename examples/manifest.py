"""A basic example on how to use Destiny's manifest."""
# aiobungie's REST client provides 5 methods to interact with the manifest.
#
# * fetch_manifest_path
# This fetch the manifest path calling `Destiny2/Manifest` endpoint and return
# JSON response contains all available paths.
#
# * read_manifest_bytes
# This can be used to read the raw bytes of the SQLite version manifest.
# Its a lower level method that allows you to read and write the bytes yourself.
#
# * download_manifest
# This is the standard method to download the SQLite manifest.
# It will read, write, zip, unzip and prepare the manifest file to be used.
#
# * download_json_manifest
# Same as download_manifest but it will download the JSON manifest instead of SQLite.
#
# * fetch_manifest_version
# Performs an HTTP request fetching the latest version of the manifest.

import asyncio
import json
import random
import sqlite3
import concurrent.futures as concurrent

import aiobungie

# The reason we're using REST client here is because we're working with raw data directly.
# So we don't need the Base client impl.

# NOTE: Interacting with manifest doesn't requires a token. So we can leave this as an empty string.
client = aiobungie.RESTClient("...")


async def sqlite_manifest() -> None:
    # Download the SQLite manifest.
    manifest_path = await client.download_sqlite_manifest(
        # optionally, you can give the manifest file a name. It defaults to just `manifest`
        name="2024.0.0-manifest",
        # The path that the manifest will be downloaded into.
        # It default to the relative path `.`, So the final path will be like
        # ./2024.0.0-manifest.sqlite3
        path=".",
        # The manifest supports multiple languages, It default to `en` which is english.
        language="ko",
        # The force flag will force the download even if the file exists. the old one gets unlinked
        # and get replaced with an up to date version.
        force=True,
        # The manifest bytes gets written asynchronously via executors, you have multiple executor options.
        # - ThreadPoolExecutor, The asynchronous execution can be performed with threads.
        # - ProcessPoolExecutor, a pool of processes to execute calls asynchronously which uses the multiprocessing module
        executor=concurrent.ThreadPoolExecutor(),
    )

    # The manifest version.
    manifest_version = await client.fetch_manifest_version()
    print(manifest_version)

    # Connect to the manifest database.
    # `download_sqlite_manifest` returns a Python `Path` object
    # of the manifest, so we can safely directly pass it to the connection constructor.
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
