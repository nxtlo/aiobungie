"""An example on how to use Bungie OAuth2 purely using aiobungie and aiohttp.web only."""

import collections
import ssl
import urllib.parse

import aiohttp.web

import aiobungie

# Initilaize our client.
client = aiobungie.Client(
    "CLIENT_TOKEN",
    "CLIENT_SECRET",
    # Client ID placed here.
)

# Web router.
router = aiohttp.web.RouteTableDef()


def parse_url(url: str) -> str:
    """Parse the URL after we login and return the code parameter."""
    parser = urllib.parse.urlparse(url)
    return parser.query.removeprefix("code=")


# A Simple HTML page to show our information.
def user_html(user: aiobungie.crate.BungieUser) -> str:
    return f"""
<header>
    <a href="{aiobungie.url.BASE}">
    <img src="{user.picture}">
    </a>
    <h1>Welocme {user.name}!</h1>
    <h2>{user.id}</h2>
</header>

<div>
    <p>About: {user.about}</p>
</div>
"""


# Home page where we will be redirected to login.
@router.get("/")
async def home(_: aiohttp.web.Request) -> aiohttp.web.Response:
    # Build the OAuth2 url, Make sure the client id and secret are set in the client
    # constructor.
    oauth_url = client.rest.build_oauth2_url()
    assert oauth_url is not None, "Make sure client id and secret are set!"
    raise aiohttp.web.HTTPFound(location=oauth_url)


# After logging in we will be redirected from our Bungie app to this location.
# This "/redirect" route is configured in your Bungie Application at the developer portal.
@router.get("/redirect")
async def redirect(request: aiohttp.web.Request) -> aiohttp.web.Response:
    # Check if the code parameter is in the redirect URL.
    if code := parse_url(str(request.url)):

        # Make the request and fetch the OAuth2 tokens.
        tokens = await client.rest.fetch_oauth2_tokens(code)

        # This storage is a global dict where we can access the tokens object
        # from our app instance. -> request.app['storage']['me'].access_token
        request.app["storage"]["me"] = tokens

        # Redirect to "/me" route.
        raise aiohttp.web.HTTPFound(location="/me", reason="OAuth2 success")
    else:
        # Otherwise return 404 and couldn't authenticate.
        raise aiohttp.web.HTTPNotFound(text="Code not found and couldn't authinticate.")


# Our own authinticated user route.
@router.get("/me")
async def my_user(request: aiohttp.web.Request) -> aiohttp.web.Response:
    # Check our storage if it has the tokens stored.
    if my_tokens := request.app["storage"].get("me"):
        # Fetch our current Bungie.net user.
        my_user = await client.fetch_current_user_memberships(my_tokens.access_token)
        # Return an HTML response.
        return aiohttp.web.Response(
            text=user_html(my_user.bungie), content_type="text/html"
        )
    else:
        # Otherwise return unauthorized if no access token found.
        raise aiohttp.web.HTTPUnauthorized(text="No access token found, Unauthorized.")

# The application itself.
app = aiohttp.web.Application()

# Our global application storage.
app["storage"] = collections.defaultdict()

# Add the routes.
app.add_routes(router)

# Bungie doesn't allow redirecting to http and requires https,
# So we need to generate ssl certifacations to allow our server
# run on https.
ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

# You should generate cert and private key files and place their path here.
ctx.load_cert_chain("CERTIFICATE_FILE_PATH", "PRIFVATE_KEY_FILE_PATH")

# Run the app.
aiohttp.web.run_app(app, host="localhost", port=8000, ssl_context=ctx)
