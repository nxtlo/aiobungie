"""A simple Python REST only API using the REST client.

All objects returned are JSON objects which we can view them in the frontend.
"""
import typing

import aiobungie

from backend import config

# The rest client.
rest = aiobungie.RESTClient(config.CLIENT_TOKEN)

# A helpers function to close the rest client.
async def close() -> None:
    await rest.close()


# Fetch some users from their id.
async def fetch_user(id: int) -> aiobungie.typedefs.JsonObject:
    return await rest.fetch_user(id)


# Fetch a clan.
async def fetch_clan(name_or_id: str) -> aiobungie.typedefs.JsonObject:
    return await rest.fetch_clan(name_or_id)


# Convert the user input membership type from string to an int.
def _convert_membership(type: typing.Optional[str] = None) -> aiobungie.MembershipType:
    convert: aiobungie.MembershipType
    if type is None:
        convert = aiobungie.MembershipType.ALL
    if type == "Steam":
        convert = aiobungie.MembershipType.STEAM
    elif type == "Xbox":
        convert = aiobungie.MembershipType.XBOX
    elif type == "PSN":
        convert = aiobungie.MembershipType.PSN
    elif type == "Stadia":
        convert = aiobungie.MembershipType.STADIA
    else:
        convert = aiobungie.MembershipType.ALL
    return convert


async def fetch_player(
    name: str, member_type: typing.Optional[str] = None
) -> aiobungie.typedefs.JsonArray:
    return await rest.fetch_player(name, _convert_membership(member_type))
