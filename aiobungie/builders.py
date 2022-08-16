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
"""Objects that helps building entities to be sent/received to/from the API."""

from __future__ import annotations

__all__: tuple[str, ...] = ("OAuth2Response", "PlugSocketBuilder", "OAuthURL")

import typing
import uuid

import attrs

from aiobungie import url

if typing.TYPE_CHECKING:
    from aiobungie import typedefs


@attrs.mutable(kw_only=True, repr=False)
class OAuth2Response:
    """Represents a proxy object for returned information from an OAuth2 successful response."""

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


@attrs.define(kw_only=True)
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

    @property
    def url(self) -> str:
        """An alias for `OAuthURL.compile`."""
        return self.compile()

    def compile(self) -> str:
        """Compiles the URL to finallize the result of the URL."""
        return (
            url.OAUTH_EP
            + f"?client_id={self.client_id}&response_type=code&state={self.state}"  # noqa: W503
        )

    def __str__(self) -> str:
        return self.compile()


class PlugSocketBuilder:
    """A helper for building insert socket plugs.

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

    __slots__ = ("_map",)

    def __init__(self, map: typing.Optional[dict[str, int]] = None, /) -> None:
        self._map = map or {}

    def set_socket_array(
        self, socket_type: typing.Literal[0, 1], /
    ) -> PlugSocketBuilder:
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

    def set_socket_index(self, index: int, /) -> PlugSocketBuilder:
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

    def set_plug_item(self, item_hash: int, /) -> PlugSocketBuilder:
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

    def collect(self) -> dict[str, int]:
        """Collect the set values and return its map to be passed to the request.

        Returns
        -------
        `dict[str, int]`
            The built map.
        """
        return self._map
