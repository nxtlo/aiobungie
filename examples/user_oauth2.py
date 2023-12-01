"""An example on how to use Bungie OAuth2 purely using aiobungie and aiohttp.web only."""

import ssl

from aiohttp import web

import aiobungie

# Web router.
router = web.RouteTableDef()


# Home page where we will be redirected to login.
@router.get("/")
async def home(request: web.Request) -> web.Response:
    # Build the OAuth2 url, Make sure the client id and secret are set in the client
    # constructor.
    client: aiobungie.RESTPool = request.app["client"]

    # Acquire a new RESTClient instance.
    async with client.acquire() as rest:
        oauth_url = rest.build_oauth2_url()

    if oauth_url is None:
        return web.json_response(
            {
                "error": "Couldn't generate OAuth2 URL.",
                "hint": "Make sure the client IDs are set.",
            },
            status=400,
        )
    raise web.HTTPFound(location=oauth_url.url)


# After logging in we will be redirected from our Bungie app to this location.
# This "/redirect" route is configured in your Bungie Application at the developer portal.
@router.get("/redirect")
async def redirect(request: web.Request) -> web.Response:
    # Check if the code parameter is in the redirect URL.
    client: aiobungie.RESTPool = request.app["client"]

    if code := request.query.get("code"):
        async with client.acquire() as rest:
            # Make the request and fetch the OAuth2 tokens.

            tokens = await rest.fetch_oauth2_tokens(code)
            # Store the access token in the pool metadata.
            client.metadata["token"] = tokens.access_token
            print(f"Member {tokens.membership_id} has been authenticated!")

        # Redirect to "/me" route with the access token.
        raise web.HTTPFound(location="/me", reason="OAuth2 success")
    else:
        # Otherwise return 404 and couldn't authenticate.
        return web.json_response(
            {"error": "code not found and couldn't authenticate."}, status=400
        )


# Our own authenticated user route.
@router.get("/me")
async def my_user(request: web.Request) -> web.Response:
    client: aiobungie.RESTPool = request.app["client"]
    # Check our pool storage if it has the tokens stored.
    if access_token := client.metadata.get("token"):
        # Fetch our current Bungie.net user.
        async with client.acquire() as rest:
            my_user = await rest.fetch_current_user_memberships(access_token)

        # Return a JSON response.
        return web.json_response(my_user)
    else:
        # Otherwise return unauthorized if no access token found.
        return web.json_response({"No access token found, Unauthorized."}, status=401)


# When the app start, We initialize our rest pool and add it to the app storage.
async def on_start_up(app: web.Application) -> None:
    client = aiobungie.RESTPool(
        "CLIENT_TOKEN",
        client_secret="CLIENT_SECRET",
        client_id=0000,  # client ID.
    )
    app["client"] = client


async def on_shutdown(app: web.Application) -> None:
    # Called when the app shuts down.
    # You can close servers, cleanup database, etc.
    ...


def main() -> None:
    # The application itself.
    app = web.Application()

    # Add the routes.
    app.add_routes(router)

    # Add on start and close callbacks
    app.on_startup.append(on_start_up)
    app.on_shutdown.append(on_shutdown)

    # Bungie doesn't allow redirecting to http and requires https,
    # So we need to generate ssl certifications to allow our server
    # run on https.
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    # You should generate cert and private key files and place their path here.
    ctx.load_cert_chain("CERT.pem", "KEY.pem")

    # Run the app.
    web.run_app(app, host="localhost", port=8000, ssl_context=ctx)


if __name__ == "__main__":
    main()
