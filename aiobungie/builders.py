# MIT License
#
# Copyright (c) 2020 = Present nxtlo
#
# Permission is hereby granted, free of charge, to typing.Any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF typing.Any KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR typing.Any CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Utilities for building entities to be sent/received to/from the API."""

from __future__ import annotations

__all__ = ("OAuth2Response", "PlugSocketBuilder", "OAuthURL", "Image", "Settings")

import asyncio
import datetime
import functools
import pathlib
import typing
import uuid

import aiohttp
import attrs

from . import error, url
from .internal import enums, helpers

if typing.TYPE_CHECKING:
    import collections.abc as collections
    import concurrent.futures
    import os
    import ssl
    import types

    from typing_extensions import Required, Self

    from aiobungie import traits, typedefs

    class _FinderListingValue(typing.TypedDict):
        valueType: Required[int]
        values: Required[collections.Sequence[int]]

    class _ListingFilter(typing.TypedDict):
        listingValue: Required[_FinderListingValue]
        rangeType: int
        matchType: int


@typing.final
@attrs.define(kw_only=True)
class Settings:
    """Basic settings used within aiobungie HTTP clients."""

    http_timeout: aiohttp.ClientTimeout = attrs.field(
        default=aiohttp.ClientTimeout(30.0)
    )
    """Setting to control HTTP request timeouts, This includes
    the time it takes to acquire the client,
    timeout for connecting and reading the socket, and more.

    Defaults to total of `30.0` seconds.
    """

    trust_env: bool = attrs.field(default=False)
    """Trust environment settings for proxy configuration.

    Gets proxy credentials from `~/.netrc` file if present or
    Gets HTTP Basic Auth credentials from `~/.netrc` file if present.

    If `NETRC` environment variable is set, read from file specified 
    there rather than from `~/.netrc`.
    """

    auth: aiohttp.BasicAuth | None = attrs.field(default=None)
    """an object that represents HTTP Basic Authorization, Defaults to `None`."""

    headers: collections.Mapping[str, typing.Any] | None = attrs.field(default=None)
    """Default HTTP headers to send the request with, Defaults to `None`."""

    use_dns_cache: bool = attrs.field(default=True)
    """References [use_dns_cache](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.TCPConnector)"""
    ttl_dns_cache: int = attrs.field(default=10)
    """References [ttl_dns_cache](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.TCPConnector)"""
    verify_ssl: bool = attrs.field(default=True)
    """References [verify_ssl](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.TCPConnector)"""
    ssl_context: ssl.SSLContext | None = attrs.field(default=None)
    """References [ssl_context](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.TCPConnector)"""
    ssl: bool | aiohttp.Fingerprint | ssl.SSLContext = attrs.field(default=True)
    """References [ssl](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.TCPConnector)"""


@typing.final
class MimeType(str, enums.Enum):
    """Image mime types enum."""

    JPEG = "jpeg"
    PNG = "png"
    WEBP = "webp"
    JPG = "jpg"
    GIF = "gif"

    def __str__(self) -> str:
        return self.value


def _open_write_path(path: pathlib.Path) -> typing.BinaryIO:
    return path.open("wb")


@typing.final
class Image:
    """A streamable Bungie resource.

    Images are _lazy_, which mean they do nothing unless you `await` or poll them.

    Example
    -------
    ```py
    from aiobungie import Image
    img = Image("img/destiny_content/pgcr/raid_eclipse.jpg")
    print(img)
    # https://www.bungie.net/img/destiny_content/pgcr/raid_eclipse.jpg

    # Save the image to a file.
    async with img:
        await img.save(
            "file_name",
            "/my/path/to/save/to",
            mime_type="png"
        )
    ```

    Parameters
    ----------
    path : `str | None`
        A valid Bungie resource path. if left `None`, `Image.DEFAULT_PATH` will be used.
    """

    __slots__ = ("path", "_client_session", "_call")
    DEFAULT_PATH: typing.ClassVar[str] = "/img/misc/missing_icon_d2.png"
    """Returns the path to the missing Bungie image.

    This returns the path only, If you want an actual image object use `Image.default()`
    """

    def __init__(self, path: str | None = None) -> None:
        self.path = self.DEFAULT_PATH if not path else path
        self._client_session: aiohttp.ClientSession = NotImplemented
        self._call: aiohttp.ClientResponse = NotImplemented

    @property
    def is_missing(self) -> bool:
        """Returns `True` if the path of this image is missing.

        Example
        -------
        ```py
        # default returns a missing destiny 2 icon.
        image = Image.default()
        assert image.is_missing

        # applies to empty strings as well
        image = Image("")
        assert image.is_missing
        ```
        """
        return not self.path or self.path == self.DEFAULT_PATH

    @staticmethod
    def default() -> Image:
        """Return the default image.

        Some Bungie resources can be nullable, aiobungie usually replaces them with this instance.
        but not always, they might be `Image | None` in certain cases.

        Example
        -------
        ```py
        missing = Image.default()
        print(missing.create_url()) # https://www.bungie.net/img/misc/missing_icon_d2.png
        ```
        """
        return _DEFAULT_IMAGE

    def create_url(self) -> str:
        """Creates a full URL to the image path.

        Example
        -------
        ```py
        img = Image("img/destiny_content/pgcr/raid_eclipse.jpg")
        print(img.create_url())
        # https://www.bungie.net/img/destiny_content/pgcr/raid_eclipse.jpg
        ```

        Returns
        -------
        `str`
            The URL to the image.
        """
        return url.BASE + "/" + self.path

    async def _static_request(self) -> aiohttp.ClientResponse:
        client_session = aiohttp.ClientSession()
        request = client_session.request(
            "GET", self.create_url(), raise_for_status=False
        )
        try:
            await client_session.__aenter__()
            response = await request.__aenter__()
            try:
                if 300 >= response.status >= 200:
                    self._client_session = client_session
                    self._call = response
                    return response
                else:
                    raise await error.panic(response)

            except Exception as e:
                await response.__aexit__(type(e), e, e.__traceback__)
                raise

        except Exception:
            await client_session.close()
            raise

    async def save(
        self,
        file_name: str,
        path: str | os.PathLike[str],
        *,
        mime_type: MimeType | str = MimeType.PNG,
        executor: concurrent.futures.Executor | None = None,
    ) -> None:
        """Saves this image to a file.

        Parameters
        ----------
        file_name : `str`
            A name for the file to save the image to.
        path : `PathLike[str] | str`
            A path to save the image to.

        Other Parameters
        ----------------
        mime_type : `MimeType | str`
            MIME type of the image. Defaults to JPEG.
        executor : `concurrent.futures.Executor | None`
            An optional executor to use for writing the bytes of this image.

        Raises
        ------
        `FileNotFoundError`
            If the path provided does not exist.
        `PermissionError`
            If the path provided is not writable or does not have write permissions.
        `RuntimeError`
            If the image could not be saved for some other reason.
        """
        if isinstance(path, pathlib.Path) and not path.exists():
            raise FileNotFoundError(f"File does not exist: {path!r}")

        # empty str, nothing to do here.
        if self.is_missing and self.path != self.DEFAULT_PATH:
            return

        path = pathlib.Path(path) / f"{file_name}.{mime_type}"
        loop = helpers.get_or_make_loop()
        file = await loop.run_in_executor(executor, _open_write_path, path)

        reader = await self._static_request()
        try:
            async for chunk in reader.content:
                await loop.run_in_executor(executor, file.write, chunk)

        except asyncio.CancelledError:
            pass

        except Exception as err:
            raise RuntimeError("Encountered an error while saving image.") from err

    async def read(self) -> bytes:
        """Perform an HTTP call reading this image's entire bytes into memory.

        Example
        -------
        ```py
        image = Image.default()
        # you can fetch the bytes in two different ways
        # they do the exact same thing.
        async with image:
            buffer = await image.read() or await image
        ```

        Returns
        -------
        `bytes`:
            The bytes of this image.
        """
        return await (await self._static_request()).read()

    async def stream(self) -> aiohttp.streams.AsyncStreamIterator[bytes]:
        """Stream this image's data.

        Example
        -------
        ```py
        image = Image.default()
        async with image:
            stream = await image.stream()
            async for byte in stream:
                # write chunk to file
            ...
        ```

        Returns
        -------
        `AsyncStreamIterator[bytes]`:
            A streaming iterator of this image bytes, yielding the entire data as soon as its received.
        """
        return (await self._static_request()).content.iter_any()

    async def chunks(self, n: int) -> aiohttp.streams.AsyncStreamIterator[bytes]:
        """Stream the bytes of this image in `n` chunks.

        Example
        -------
        ```py
        buffer_size = 1024
        image = Image.default()

        async with image:
            chunks = await image.chunks(buffer_size)
            while True:
                next_chunk = await anext(chunks)
                if not next_chunk:
                    break
                # write chunk to file
        ```

        Returns
        -------
        `AsyncStreamIterator[bytes]`:
            A chunking stream of bytes.
        """
        return (await self._static_request()).content.iter_chunked(n)

    async def iter(self) -> collections.AsyncGenerator[bytes, None]:
        """Yield each byte in this image from start to end.

        Example
        -------
        ```py
        resource = Image.default()
        async with resource:
            async for byte in resource.iter():
                print(byte)
        ```

        Returns
        -------
        `collections.AsyncGenerator[bytes, None]`
            An async generator that yields this image's bytes from start to end.
        """

        reader = await self.chunks(1024)
        async for chunk in reader:
            yield chunk

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None:
        await self._client_session.close()
        await self._call.__aexit__(exc_type, exc, exc_tb)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.path == other
        elif isinstance(other, Image):
            return self.path == other.path

        return NotImplemented

    def __ne__(self, value: object, /) -> bool:
        return not self.__eq__(value)

    def __hash__(self) -> int:
        return hash(self.path)

    def __repr__(self) -> str:
        return f"Image({self.create_url()})"

    def __str__(self) -> str:
        return self.create_url()

    def __await__(self) -> collections.Generator[None, None, bytes]:
        return self.read().__await__()


_DEFAULT_IMAGE: typing.Final[Image] = Image(Image.DEFAULT_PATH)
"""A const default image.

This is always returned by calling `Image.default()`
"""


@typing.final
@attrs.frozen(kw_only=True, repr=False)
class OAuth2Response:
    """The result of fetching or refreshing an OAuth2 token."""

    access_token: str
    """The returned OAuth2 `access_token` field."""

    refresh_token: str
    """The returned OAuth2 `refresh_token` field."""

    expires_in: int
    """The returned OAuth2 `expires_in` field."""

    token_type: str
    """The returned OAuth2 `token_type` field. This is usually just `Bearer`"""

    refresh_expires_in: int
    """The returned OAuth2 `refresh_expires_in` field."""

    membership_id: int
    """The returned BungieNet membership id for the authorized user."""

    @classmethod
    def build_response(cls, payload: typedefs.JSONObject, /) -> OAuth2Response:
        """Deserialize and builds the JSON object into this object."""
        return OAuth2Response(
            access_token=payload["access_token"],
            refresh_token=payload["refresh_token"],
            expires_in=int(payload["expires_in"]),
            token_type=payload["token_type"],
            refresh_expires_in=payload["refresh_expires_in"],
            membership_id=int(payload["membership_id"]),
        )


# To be able to cache the result of the compiled URL, We disable the slots here.
@typing.final
@attrs.frozen(kw_only=True, slots=False)
class OAuthURL:
    """The result of calling `aiobungie.RESTClient.build_oauth2_url`.

    Example
    -------
    ```py
    url = aiobungie.builders.OAuthURL(client_id=1234)
    print(url.compile()) # Full URL to make an OAuth2 request.
    print(url.state)  # The UUID state to be used in the OAuth2 request.
    ```
    """

    state: uuid.UUID = attrs.field(factory=uuid.uuid4)
    """The state parameter for the URL."""

    client_id: int
    """The client id for that's making the request."""

    @functools.cached_property
    def url(self) -> str:
        """The cached result of calling `OAuthURL.compile`.

        This allow for a faster access for the compiled URL.

        Example
        -------
        ```py
        url = OAuthURL(client_id=0000)
        first_compile = url.url
        cached_url = url.url
        ```
        """
        return self.compile()

    def compile(self) -> str:
        """Compiles the fields to finalize the result of the URL."""
        return (
            url.OAUTH_EP
            + f"?client_id={self.client_id}&response_type=code&state={self.state}"  # noqa: W503
        )

    def __str__(self) -> str:
        return self.compile()


@typing.final
@attrs.frozen(kw_only=True)
class PlugSocketBuilder:
    """A helper class for quickly building socket plugs.

    Example
    -------
    ```py
    import aiobungie

    rest = aiobungie.RESTClient(...)
    plug = (
        aiobungie.builders.PlugSocketBuilder()
        .set_socket_array(0)
        .set_socket_index(0)
        .set_plug_item(3023847)
        .collect()
    )
    await rest.insert_socket_plug_free(..., plug=plug)
    ```
    """

    _map: collections.MutableMapping[str, int] = attrs.field(factory=dict)

    def set_socket_array(self, socket_type: typing.Literal[0, 1], /) -> Self:
        """Set the array socket type.

        Parameters
        ----------
        socket_type : `typing.Literal[0, 1]`
            Either 0, or 1. If set to 0 it will be the default,
            Otherwise if 1 it will be Intrinsic.

        Returns
        -------
        `Self`
            The class itself to allow chained methods.
        """
        self._map["socketArrayType"] = socket_type
        return self

    def set_socket_index(self, index: int, /) -> Self:
        """Set the socket index into the array.

        Parameters
        ----------
        index : `int`
            The socket index.

        Returns
        -------
        `Self`
            The class itself to allow chained methods.
        """
        self._map["socketIndex"] = index
        return self

    def set_plug_item(self, item_hash: int, /) -> Self:
        """Set the socket index into the array.

        Parameters
        ----------
        item_hash : `int`
            The hash of the item to plug.

        Returns
        -------
        `Self`
            The class itself to allow chained methods.
        """
        self._map["plugItemHash"] = item_hash
        return self

    def collect(self) -> collections.Mapping[str, int]:
        """Collect the set values and return its map to be passed to the request.

        Returns
        -------
        `Mapping[str, int]`
            The built map.
        """
        return self._map


@typing.final
@attrs.frozen(weakref_slot=False)
class FireteamBuilder:
    """A helper class that exposes all of `FireteamFinder` methods.

    This is the result of calling `RESTClient.build_fireteam_finder()`.

    Note
    ----
    All methods in this class require an `access token` for authentication.

    Example
    -------
    ```py
    client = aiobungie.Client("token")
    fireteam_finder = client.rest.build_fireteam_finder(
        member_id,
        char_id,
        member_type
    ) # All methods are available via `fireteam_finder`
    application = await fireteam_finder.fetch_application('token', app_id)
    ```
    """

    rest: traits.RESTful
    """A reference to the `RESTful` client interface that is performing the requests."""
    membership_id: int
    """The membership ID that will be used to perform the requests with."""
    character_id: int
    """The character ID that will be used to perform the requests with."""
    membership_type: enums.MembershipType | int
    """The membership type that will be used to perform the requests with."""

    async def activate_fireteam_lobby(
        self,
        access_token: str,
        /,
        lobby_id: int,
        *,
        force_activation: bool = False,
    ) -> bool:
        """Activates a lobby and initializes it as an active Fireteam."""
        response = await self.rest.static_request(
            "POST",
            f"FireteamFinder/Lobby/Activate/{lobby_id}/{int(self.membership_type)}/{self.membership_id}/{self.character_id}",
            params={"forceActivation": force_activation},
            auth=access_token,
        )
        assert isinstance(response, bool)
        return response

    async def activate_lobby_for_id(
        self,
        access_token: str,
        /,
        lobby_id: int,
        *,
        force_activation: bool = False,
    ) -> bool:
        """Activates a lobby and initializes it as an active Fireteam, returning the updated Listing ID."""
        response = await self.rest.static_request(
            "POST",
            f"FireteamFinder/Lobby/ActivateForNewListingId/{lobby_id}/{int(self.membership_type)}/{self.membership_id}/{self.character_id}",
            params={"forceActivation": force_activation},
            auth=access_token,
        )
        assert isinstance(response, bool)
        return response

    async def apply_to_listing(
        self,
        access_token: str,
        /,
        listing_id: int,
        application_type: enums.OAuthApplicationType | int,
    ) -> typedefs.JSONObject:
        """Applies to have a character join a fireteam."""
        response = await self.rest.static_request(
            "POST",
            f"FireteamFinder/Listing/{listing_id}/Apply/{int(application_type)}/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def bulk_fetch_listing_status(
        self, access_token: str, /
    ) -> typedefs.JSONObject:
        """Retrieves Fireteam listing statuses in bulk."""
        response = await self.rest.static_request(
            "POST",
            f"FireteamFinder/Listing/BulkStatus/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def fetch_application(
        self, access_token: str, /, application_id: int
    ) -> typedefs.JSONObject:
        """Retrieves a Fireteam application."""
        response = await self.rest.static_request(
            "GET",
            f"FireteamFinder/Application/{application_id}/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def fetch_listing_applications(
        self,
        access_token: str,
        /,
        listing_id: int,
        *,
        flags: typing.Literal[0, 1, 2, 3, 4, 5, 6] | None = None,
        page_token: str | None = None,
        page_size: int | None = None,
    ) -> typedefs.JSONObject:
        """Retrieves all applications to a Fireteam Finder listing.

        Parameters
        ----------
        listing_id: `int`
            The ID of the listing whose applications to retrieve.

        Other Parameters
        ----------------
        flags: `int`
            Optional flag representing a filter on the state of the application.
            * `Unknown`: 0
            * `WaitingForApplicants`: 1
            * `WaitingForLobbyOwner`: 2
            * `Accepted`: 3
            * `Rejected`: 4
            * `Deleted`: 5
            * `Expired`: 6
        page_token: `str | None`
            An optional token from a previous response to fetch the next page of results.
        page_size: `int | None`
            The maximum number of results to be returned with this page.
        """
        response = await self.rest.static_request(
            "GET",
            f"FireteamFinder/Listing/{listing_id}/Applications/{int(self.membership_type)}/{self.membership_type}/{self.character_id}",
            params={
                "flags": flags or 0,
                "nextPageToken": page_token or "",
                "pageSize": page_size or 0,
            },
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def fetch_lobby(
        self, access_token: str, /, lobby_id: int
    ) -> typedefs.JSONObject:
        """Retrieves the information for a Fireteam lobby."""
        response = await self.rest.static_request(
            "GET",
            f"FireteamFinder/Lobby/{lobby_id}/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def fetch_player_lobbies(
        self,
        access_token: str,
        /,
        *,
        page_token: str | None = None,
        page_size: int | None = None,
    ) -> typedefs.JSONObject:
        """Retrieves the information for a Fireteam lobby.

        Parameters
        ----------
        page_token: `str | None`
            An optional token from a previous response to fetch the next page of results.
        page_size: `int | None`
            The maximum number of results to be returned with this page.
        """
        response = await self.rest.static_request(
            "GET",
            f"FireteamFinder/PlayerLobbies/{int(self.membership_type)}/{self.membership_id}/{self.character_id}",
            params={"nextPageToken": page_token or "", "pageSize": page_size or 0},
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def fetch_player_applications(
        self,
        access_token: str,
        /,
        *,
        page_token: str | None = None,
        page_size: int | None = None,
    ) -> typedefs.JSONObject:
        """Retrieves Fireteam applications that this player has sent or received.

        Parameters
        ----------
        page_token: `str | None`
            An optional token from a previous response to fetch the next page of results.
        page_size: `int | None`
            The maximum number of results to be returned with this page.
        """
        response = await self.rest.static_request(
            "GET",
            f"FireteamFinder/PlayerApplications/{int(self.membership_type)}/{self.membership_id}/{self.character_id}",
            params={"nextPageToken": page_token or "", "pageSize": page_size or 0},
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def fetch_player_offers(
        self,
        access_token: str,
        /,
        *,
        page_token: str | None = None,
        page_size: int | None = None,
    ) -> typedefs.JSONObject:
        """Retrieves Fireteam offers that this player has received.

        Parameters
        ----------
        page_token: `str | None`
            An optional token from a previous response to fetch the next page of results.
        page_size: `int | None`
            The maximum number of results to be returned with this page.
        """
        response = await self.rest.static_request(
            "GET",
            f"FireteamFinder/PlayerOffers/{int(self.membership_type)}/{self.membership_id}/{self.character_id}",
            params={"nextPageToken": page_token or "", "pageSize": page_size or 0},
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def fetch_character_activity_access(
        self,
        access_token: str,
        /,
    ) -> typedefs.JSONObject:
        """Retrieves the information for a Fireteam lobby."""
        response = await self.rest.static_request(
            "GET",
            f"FireteamFinder/CharacterActivityAccess/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def fetch_offer(
        self,
        access_token: str,
        /,
        offer_id: int,
    ) -> typedefs.JSONObject:
        """Retrieves an offer to a Fireteam lobby."""
        response = await self.rest.static_request(
            "GET",
            f"FireteamFinder/Offer/{offer_id}/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def fetch_lobby_offers(
        self,
        access_token: str,
        /,
        lobby_id: int,
        *,
        page_token: str | None = None,
        page_size: int | None = None,
    ) -> typedefs.JSONObject:
        """Retrieves all offers relevant to a Fireteam lobby.

        Parameters
        ----------
        page_token: `str | None`
            An optional token from a previous response to fetch the next page of results.
        page_size: `int | None`
            The maximum number of results to be returned with this page.
        """
        response = await self.rest.static_request(
            "GET",
            f"FireteamFinder/Lobby/{lobby_id}/Offers/{int(self.membership_type)}/{self.membership_id}/{self.character_id}",
            params={"nextPageToken": page_token or "", "pageSize": page_size or 0},
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def host_lobby(
        self,
        access_token: str,
        /,
        clan_id: int,
        max_players: int,
        online_only: bool,
        privacy_scope: typing.Literal[0, 1, 2, 3, 4],
        scheduled_date: datetime.datetime,
        listing_values: collections.Sequence[_FinderListingValue],
        activity_graph_hash: int,
        activity_hash: int,
    ) -> typedefs.JSONObject:
        """Creates a new Fireteam lobby and Fireteam Finder listing.

        Parameters
        ----------
        max_players: `int`
            The maximum number of players that can join the lobby.
        online_only: `bool`
            If `True`, only online players can join the lobby.
        privacy_scope: `int`
            The privacy scope of this lobby See
            [PrivacyScope](https://bungie-net.github.io/multi/schema_FireteamFinder-DestinyFireteamFinderLobbyPrivacyScope.html#schema_FireteamFinder-DestinyFireteamFinderLobbyPrivacyScope)
            for more details.
        scheduled_date: `datetime.datetime`
            If this lobby is scheduled, this date will be used.
        clan_id: `int`
        listing_values: `Sequence[_FinderListingValue]`
        activity_graph_hash: `int`
        activity_hash: `int`
        """

        response = await self.rest.static_request(
            "POST",
            f"FireteamFinder/Lobby/Host/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            json={
                "maxPlayerCount": max_players,
                "onlinePlayersOnly": online_only,
                "privacyScope": privacy_scope,
                "scheduledDateTime": f"{scheduled_date.year}-{scheduled_date.month}-{scheduled_date.day}",
                "clanId": clan_id,
                "listingValues": listing_values,
                "activityGraphHash": activity_graph_hash,
                "activityHash": activity_hash,
            },
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def join_lobby(
        self, access_token: str, /, lobby_id: int, offer_id: int
    ) -> typedefs.JSONObject:
        """Sends a request to join an available Fireteam lobby.

        Parameters
        ----------
        lobby_id: `int`
            The ID of the lobby to join.
        offer_id: `int`
            The Offer ID.
        """
        response = await self.rest.static_request(
            "POST",
            f"FireteamFinder/Lobby/Join/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            json={"lobbyId": lobby_id, "offerId": offer_id},
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def kick_player(
        self,
        access_token: str,
        /,
        lobby_id: int,
        target_membership_id: int,
        target_character_id: int,
        target_membership_type: enums.MembershipType | int,
    ) -> typedefs.JSONObject:
        """Kicks a player from a Fireteam Finder lobby.

        Parameters
        ----------
        lobby_id: `int`
            The ID of the lobby to kick the targeted player from.
        target_membership_id: `int`
            The membership ID of the target to kick.
        target_character_id: `int`
            The character ID of the target to kick.
        target_membership_type: `aiobungie.MembershipType | int`
            The membership type of the target to kick.
        """
        response = await self.rest.static_request(
            "POST",
            f"FireteamFinder/Lobby/{lobby_id}/KickPlayer/{target_membership_id}/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            json={
                "targetMembershipType": int(target_membership_type),
                "targetCharacterId": target_character_id,
            },
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def leave_application(
        self, access_token: str, /, application_id: int
    ) -> bool:
        """Sends a request to leave a Fireteam listing application.

        Parameters
        ----------
        application_id: `int`
            The ID of the application to leave.

        Returns
        -------
        `bool`
        """
        response = await self.rest.static_request(
            "POST",
            f"FireteamFinder/Application/Leave/{application_id}/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            auth=access_token,
        )
        assert isinstance(response, bool)
        return response

    async def leave_lobby(self, access_token: str, /, lobby_id: int) -> bool:
        """Sends a request to leave a Fireteam lobby.

        Parameters
        ----------
        lobby_id: `int`
            The ID of the application to leave.

        Returns
        -------
        `bool`
        """
        response = await self.rest.static_request(
            "POST",
            f"FireteamFinder/Lobby/Leave/{lobby_id}/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            auth=access_token,
        )
        assert isinstance(response, bool)
        return response

    async def respond_to_application(
        self, access_token: str, /, application_id: int, accepted: bool
    ) -> typedefs.JSONObject:
        """Responds to an application sent to a Fireteam lobby.

        Parameters
        ----------
        application_id: `int`
            The ID of the application to send the request to.
        accepted: `bool`

        Returns
        -------
        A JSON object that contains the application response.
        See [Reference](https://bungie-net.github.io/multi/schema_FireteamFinder-DestinyFireteamFinderRespondToApplicationResponse.html#schema_FireteamFinder-DestinyFireteamFinderRespondToApplicationResponse)
        """
        response = await self.rest.static_request(
            "POST",
            f"FireteamFinder/Application/Respond/{application_id}/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            json={"accepted": accepted},
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def respond_to_authentication(
        self, access_token: str, /, application_id: int, confirmed: bool
    ) -> typedefs.JSONObject:
        """Responds to an authentication request for a Fireteam.

        Parameters
        ----------
        application_id: `int`
            The ID of the application to send the request to.
        confirmed: `bool`

        Returns
        -------
        A JSON object that contains the result of the request.
        See [Reference](https://bungie-net.github.io/multi/schema_FireteamFinder-DestinyFireteamFinderRespondToApplicationResponse.html#schema_FireteamFinder-DestinyFireteamFinderRespondToApplicationResponse)
        """
        response = await self.rest.static_request(
            "POST",
            f"FireteamFinder/Authentication/Respond/{application_id}/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            json={"confirmed": confirmed},
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def respond_to_offer(
        self, access_token: str, /, offer_id: int, accepted: bool
    ) -> typedefs.JSONObject:
        """Responds to a Fireteam lobby offer.

        Parameters
        ----------
        offer_id : `int`
            The offer ID to respond to.
        accepted: `bool`

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object contains the offer response.
            See [Reference](https://bungie-net.github.io/multi/schema_FireteamFinder-DestinyFireteamFinderRespondToOfferResponse.html#schema_FireteamFinder-DestinyFireteamFinderRespondToOfferResponse)
        """
        response = await self.rest.static_request(
            "POST",
            f"FireteamFinder/Offer/Respond/{offer_id}/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            json={"accepted": accepted},
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def search_listings_by_clan(
        self, access_token: str, /, page_size: int, page_token: str, lobby_state: int
    ) -> typedefs.JSONObject:
        """Returns search results for available Fireteams provided a clan.

        Parameters
        ----------
        page_size: `int`
            The maximum number of results to be returned with this page.
        page_token: `str`
            An optional token from a previous response to fetch the next page of results.
        lobby_state: `literal<int>`
            Search lobbies based on their state, The states are listed below.

            * `0`: Unknown
            * `1`: Inactive
            * `2`: Active
            * `3`: Expired
            * `4`: Closed
            * `5`: Canceled
            * `6`: Deleted

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object contains the search results.
            See [Reference](https://bungie-net.github.io/multi/schema_FireteamFinder-DestinyFireteamFinderSearchListingsByClanResponse.html#schema_FireteamFinder-DestinyFireteamFinderSearchListingsByClanResponse)
        """
        response = await self.rest.static_request(
            "POST",
            f"FireteamFinder/Search/Clan/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            json={
                "pageSize": page_size,
                "pageToken": page_token,
                "lobbyState": lobby_state,
            },
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def search_listings_by_filters(
        self,
        access_token: str,
        /,
        filters: collections.Sequence[_ListingFilter],
        page_size: int,
        page_token: str,
        lobby_state: typing.Literal[0, 1, 2, 3, 4, 5, 6],
    ) -> typedefs.JSONObject:
        """Returns search results for available Fireteams provided search filters.

        Parameters
        ----------
        filters: `Sequence[_ListingFilter]`
            A sequence of filters, the type of this sequence is provided as a typed dict
            for better type inference.
        page_size: `int`
            The maximum number of results to be returned with this page.
        page_token: `str`
            An optional token from a previous response to fetch the next page of results.
        lobby_state: `literal<int>`
            Search lobbies based on their state, The states are listed below.

            * `0`: Unknown
            * `1`: Inactive
            * `2`: Active
            * `3`: Expired
            * `4`: Closed
            * `5`: Canceled
            * `6`: Deleted

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the fireteam search results.
            See [Reference](https://bungie-net.github.io/multi/schema_FireteamFinder-DestinyFireteamFinderSearchListingsByFiltersResponse.html#schema_FireteamFinder-DestinyFireteamFinderSearchListingsByFiltersResponse)
        """
        response = await self.rest.static_request(
            "POST",
            f"FireteamFinder/Search/Clan/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            json={
                "filters": filters,
                "pageSize": page_size,
                "pageToken": page_token,
                "lobbyState": lobby_state,
            },
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response

    async def update_lobby_settings(
        self,
        access_token: str,
        /,
        lobby_id: int,
        max_players: int,
        online_only: bool,
        privacy_scope: typing.Literal[0, 1, 2, 3, 4],
        scheduled_date: datetime.datetime,
        clan_id: int,
        listing_values: collections.Sequence[_FinderListingValue],
        activity_graph_hash: int,
        activity_hash: int,
    ) -> typedefs.JSONObject:
        """Updates the settings for a Fireteam lobby.

        Parameters
        ----------
        lobby_id : `int`
            The lobby ID to update.
        max_players: `int`
            The maximum number of players that can join the lobby.
        online_only: `bool`
            If `True`, only online players can join the lobby.
        privacy_scope: `int`
            The privacy scope of this lobby See
            [PrivacyScope](https://bungie-net.github.io/multi/schema_FireteamFinder-DestinyFireteamFinderLobbyPrivacyScope.html#schema_FireteamFinder-DestinyFireteamFinderLobbyPrivacyScope)
            for more details.
        scheduled_date: `datetime.datetime`
            If this lobby is scheduled, this date will be used.
        clan_id: `int`
        listing_values: `Sequence[_FinderListingValue]`
        activity_graph_hash: `int`
        activity_hash: `int`

        Returns
        -------
        `aiobungie.typedefs.JSONObject`
            A JSON object of the updated fireteam lobby response.
            See [Reference](https://bungie-net.github.io/multi/schema_FireteamFinder-DestinyFireteamFinderUpdateLobbySettingsResponse.html#schema_FireteamFinder-DestinyFireteamFinderUpdateLobbySettingsResponse)
        """
        response = await self.rest.static_request(
            "POST",
            f"FireteamFinder/Lobby/UpdateSettings/{lobby_id}/{int(self.membership_type)}/{self.membership_id}/{self.character_id}/",
            json={
                "maxPlayerCount": max_players,
                "onlinePlayersOnly": online_only,
                "privacyScope": privacy_scope,
                "scheduledDateTime": f"{scheduled_date.year}-{scheduled_date.month}-{scheduled_date.day}",
                "clanId": clan_id,
                "listingValues": listing_values,
                "activityGraphHash": activity_graph_hash,
                "activityHash": activity_hash,
            },
            auth=access_token,
        )
        assert isinstance(response, dict)
        return response
