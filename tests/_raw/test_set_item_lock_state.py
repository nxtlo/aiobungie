import os
import aiobungie


def __build_client() -> aiobungie.Client:
    token = os.environ["CLIENT_TOKEN"]
    client = aiobungie.Client(token, max_retries=0)
    client.rest.enable_debugging(True)
    return client


client = __build_client()


async def test_set_item_lock_state():
    try:
        await client.rest.set_item_lock_state(
            "my-token",
            True,
            123,
            123,
            1
        )
    # This will fail due to OAuth2
    # But the body sent in the function was "membership_type" and must be "membershipType"
    except aiobungie.Unauthorized:
        pass
