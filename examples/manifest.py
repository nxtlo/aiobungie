"""An example on how to download and use Destiny2 Manifest."""

import json

import aiobungie

client = aiobungie.Client("TOKEN")


async def main():
    try:
        # Download the manifest.
        await client.rest.download_manifest()
    except FileExistsError:
        # If this file exists just pass.
        pass

    # Connect to the manifest database.
    # A path parameter is optional if your manifest file has been downloaded somewhere else
    # or with a different name.
    manifest = client.rest.connect_manifest()

    # Select an inventory item from the manifest and return the object if it matches the given id.
    levante_prize_json = manifest.execute(
        "SELECT json FROM DestinyInventoryItemDefinition WHERE id = -757221402"
    ).fetchone()

    # Load the JSON string to a JSON object.
    loaded_json: aiobungie.typedefs.JSONObject = json.loads(levante_prize_json[0])

    # Deserialize the JSON object into an inventory item.
    levante_prize = client.factory.deserialize_inventory_entity(loaded_json)

    print(
        repr(levante_prize)
    )  # InventoryEntity(hash=3537745894, index=10835, name='The Levante Prize', description=UNDEFINED, type=<Item.EMBLEM: 14>, type_and_tier_name='Legendary Emblem')

    # You can also fetch an up-to-date object given its hash.
    up_to_date_levante_prize = await client.fetch_inventory_item(levante_prize.hash)
    print(repr(up_to_date_levante_prize))


client.run(main())
