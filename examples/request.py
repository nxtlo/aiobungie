"""An example on how to solely use aiobungie's framework to deserialize objects directly.

In this example we will use a simple requests client to make the request and deserialize the object using aiobungie.
"""

import requests

import aiobungie


# Construct an empty framework. This will be used as a deserializer only.
framework = aiobungie.framework.Empty()
CLAN_TYPE = int(aiobungie.GroupType.CLAN)
CLAN_NAME = "Redeem"  # You can use your clan name.
TOKEN = "YOUR_TOKEN"  # This should be stored somewhere safe.


def main():
    # Make the request to the group endpoint.
    response = requests.get(
        f"https://www.bungie.net/Platform/GroupV2/Name/{CLAN_NAME}/{CLAN_TYPE}",
        headers={"X-API-KEY": TOKEN},
    )

    # Check if success.
    if response.status_code == 200:
        json_response = response.json()
        # Deserialize the JSON response into a Clan Python object.
        clan = framework.deserialize_clan(json_response["Response"])
        print(f"Clan: {clan}, Owner: {clan.owner}, Description: {clan.motto}")
    else:
        print(f"Encountered an error! {response.status_code}; {response.json()}")


if __name__ == "__main__":
    main()
