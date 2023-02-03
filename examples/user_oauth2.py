"""An example on how to use Bungie OAuth2 purely using aiobungie and aiohttp.web only."""

import ssl
import urllib.parse

import aiohttp.web

import aiobungie

# Web router.
router = aiohttp.web.RouteTableDef()

client = aiobungie.RESTPool(
    "CLIENT_TOKEN", client_secret="CLIENT_SECRET", client_id=0000
)  # client ID.


def parse_url(url: str) -> str:
    """Parse the URL after we login and return the code parameter."""
    parser = urllib.parse.urlparse(url)
    return parser.query.removeprefix("code=")


# Home page where we will be redirected to login.
@router.get("/")
async def home(_: aiohttp.web.Request) -> aiohttp.web.Response:
    # Build the OAuth2 url, Make sure the client id and secret are set in the client
    # constructor.

    # Acquire a new RESTClient instance.
    async with client.acquire() as rest:
        oauth_url = rest.build_oauth2_url()

        assert oauth_url is not None, "Make sure client id and secret are set!"
        raise aiohttp.web.HTTPFound(location=oauth_url.url)


# After logging in we will be redirected from our Bungie app to this location.
# This "/redirect" route is configured in your Bungie Application at the developer portal.
@router.get("/redirect")
async def redirect(request: aiohttp.web.Request) -> aiohttp.web.Response:
    # Check if the code parameter is in the redirect URL.
    if code := parse_url(str(request.url)):

        async with client.acquire() as rest:
            # Make the request and fetch the OAuth2 tokens.

            tokens = await rest.fetch_oauth2_tokens(code)
            # Store the access token in the pool metadata.
            client.metadata["token"] = tokens.access_token

            # Redirect to "/me" route with the access token.
            raise aiohttp.web.HTTPFound(location="/me", reason="OAuth2 success")
    else:
        # Otherwise return 404 and couldn't authenticate.
        raise aiohttp.web.HTTPNotFound(text="Code not found and couldn't authinticate.")


# Our own authenticated user route.
@router.get("/me")
async def my_user(request: aiohttp.web.Request) -> aiohttp.web.Response:
    # Check our pool storage if it has the tokens stored.
    if access_token := client.metadata.get("token"):

        # Fetch our current Bungie.net user.
        async with client.acquire() as rest:
            my_user = await rest.fetch_current_user_memberships(access_token)

        # Return a JSON response.
        return aiohttp.web.json_response(my_user)
    else:
        # Otherwise return unauthorized if no access token found.
        raise aiohttp.web.HTTPUnauthorized(text="No access token found, Unauthorized.")


def main() -> None:

    # The application itself.
    app = aiohttp.web.Application()

    # Add the routes.
    app.add_routes(router)

    # Bungie doesn't allow redirecting to http and requires https,
    # So we need to generate ssl certifications to allow our server
    # run on https.
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    # You should generate cert and private key files and place their path here.
    ctx.load_cert_chain("CERTIFICATE_FILE_PATH", "PRIVATE_KEY_FILE_PATH")

    # Run the app.
    aiohttp.web.run_app(app, host="localhost", port=8000, ssl_context=ctx)


if __name__ == "__main__":
    main()
