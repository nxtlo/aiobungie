"""An example on how to handle errors with aiobungie."""

import aiobungie
import asyncio

client = aiobungie.Client("TOKEN")
CHAR_ID = 0  # You character ID
MEMBER_ID = 1  # Your membership ID


async def fetch_character_component(
    membership: aiobungie.MembershipType = aiobungie.MembershipType.STADIA,
) -> aiobungie.crates.CharacterComponent:
    return await client.fetch_character(
        MEMBER_ID, membership, CHAR_ID, components=[aiobungie.ComponentType.CHARACTERS]
    )


async def main() -> None:
    async with client.rest:
        # Lets assume you made a request with the incorrect membership type.
        # In this case we don't have a Stadia membership.
        try:
            component = await fetch_character_component()

        # Since any request that requires a membership type might raise this error.
        # It can be handled easily with this exception.
        except aiobungie.MembershipTypeError as err:
            # If this gets raised. The API will return the required membership which can
            # be used to re-make the request. You can call the `into_membership` method to like this.
            component = await fetch_character_component(
                membership=err.into_membership()
            )

        # This is a subclass of HTTPError but include more data like headers, response body, etc.
        # You might use it for debugging purposes.
        except aiobungie.HTTPException as err:
            print(f"HTTPException Endpoint {err.url} Data: {err.body}")

        # First level, All of the above inherit from this one.
        # This catch any aiobungie error raised while performing an HTTP request to the API.
        # It includes minimal information like HTTP status code and The Bungie error message.
        except aiobungie.HTTPError as err:
            print(err.message, err.http_status)

        # No errors.
        else:
            print(component.character)


if __name__ == "__main__":
    asyncio.run(main())
