"""The backend fastapi application."""

import contextlib
import logging

import aiohttp
import fastapi
import uvicorn
from backend import modules
from backend import rest

import aiobungie

logging.basicConfig(level=logging.INFO)
app = fastapi.FastAPI(debug=True)


@app.get("/", response_class=fastapi.responses.RedirectResponse, status_code=200)
async def home() -> str:
    # Just return the docs
    return "/docs"


# /user/1234/ -> {} JSON object.
@app.get(
    "/user/{id}",
    summary="Fetch a Bungie user and return it if exists.",
    status_code=200,
)
async def user_callback(id: int) -> aiobungie.typedefs.JsonObject:
    try:
        user = await rest.fetch_user(id)
    except aiobungie.NotFound as exc:
        raise fastapi.HTTPException(404, f"Player with id {id} was not found.") from exc
    return user


# /clan/Fast/ -> {} JSON object.
@app.get(
    "/clan/{name}",
    summary="Fetch a Bungie clan and return it if exists.",
    status_code=200,
)
async def clan_callback(name: str) -> aiobungie.typedefs.JsonObject:
    try:
        clan = await rest.fetch_clan(name)
    except aiobungie.NotFound as exc:
        raise fastapi.HTTPException(404, f"Clan with name {name} not found.") from exc
    return clan


# Here we make a POST method with JSON payload represents the player module we created.
# the payload should look like this {"name": "Fate#1234", type?: "Steam"}.
# The payload will be sent from the frontend to our API.
@app.post("/player", summary="Search for a Bungie player.", status_code=200)
async def player_callback(
    payload: modules.PlayerModule,
) -> aiobungie.typedefs.JsonArray:
    return await rest.fetch_player(payload.name, payload.type)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    # Close the client on shutdown.
    await rest.close()
    logging.info("Shutdown.")


@app.on_event("startup")
async def on_start() -> None:
    # Do some work when we run the app.
    import webbrowser

    try:
        webbrowser.open("http://localhost:8000/docs")
    except Exception:
        pass
    logging.info("App is running.")


def main() -> None:
    # Suppress Unclosed session warns.
    with contextlib.suppress(aiohttp.ClientError):
        uvicorn.run(app, host="localhost", port=8000)
