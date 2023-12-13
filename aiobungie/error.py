# MIT License
#
# Copyright (c) 2020 - Present nxtlo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""aiobungie Exceptions."""

from __future__ import annotations

__all__ = (
    "AiobungieError",
    "NotFound",
    "HTTPException",
    "MembershipTypeError",
    "Forbidden",
    "Unauthorized",
    "ResponseError",
    "RateLimitedError",
    "InternalServerError",
    "HTTPError",
    "BadRequest",
    "raise_error",
    "stringify_http_message",
)

import collections.abc as collections
import http
import typing

import attrs

from aiobungie.internal import enums
from aiobungie.internal import helpers

if typing.TYPE_CHECKING:
    import aiohttp
    import multidict
    from aiohttp import typedefs

_MEMBERSHIP_LOOKUP: dict[str, enums.MembershipType] = {
    "TigerSteam": enums.MembershipType.STEAM,
    "TigerXbox": enums.MembershipType.XBOX,
    "TigerPsn": enums.MembershipType.PSN,
    "TigerBlizzard": enums.MembershipType.BLIZZARD,
    "TigerEgs": enums.MembershipType.EPIC_GAMES_STORE,
    "BungieNext": enums.MembershipType.BUNGIE,
    "TigerStadia": enums.MembershipType.STADIA,
    "TigerDemon": enums.MembershipType.DEMON,
}


def _determine_membership(membership: str) -> enums.MembershipType:
    return _MEMBERSHIP_LOOKUP[membership]


@attrs.define(auto_exc=True)
class AiobungieError(RuntimeError):
    """Base class that all other exceptions inherit from."""


@attrs.define(auto_exc=True)
class HTTPError(AiobungieError):
    """Base HTTP request errors exception."""

    message: str
    """The error message."""

    http_status: http.HTTPStatus
    """The response status."""


@attrs.define(auto_exc=True, kw_only=True)
class HTTPException(HTTPError):
    """An in-depth HTTP exception that's raised with more information."""

    error_code: int
    """The returned Bungie error status code."""

    http_status: http.HTTPStatus
    """The request response http status."""

    throttle_seconds: int
    """The Bungie response throttle seconds."""

    url: typedefs.StrOrURL | None
    """The URL/endpoint caused this error."""

    body: typing.Any
    """The response body."""

    headers: multidict.CIMultiDictProxy[str]
    """The response headers."""

    message: str
    """A Bungie human readable message describes the cause of the error."""

    error_status: str
    """A Bungie short error status describes the cause of the error."""

    message_data: dict[str, str]
    """A dict of string key, value that includes each cause of the error
    to a message describes information about that error.
    """

    def __str__(self) -> str:
        if self.message:
            message_body = self.message

        if self.error_status:
            error_status_body = self.error_status

        return (
            f"{self.http_status.name.replace('_', '').title()} {self.http_status.value}: "
            f"Error status: {error_status_body}, Error message: {message_body} from {self.url} "
            f"{str(self.body)}"
        )


@attrs.define(auto_exc=True)
class Forbidden(HTTPException):
    """Exception that's raised for when status code 403 occurs."""

    http_status: http.HTTPStatus = attrs.field(
        default=http.HTTPStatus.FORBIDDEN, init=False
    )


@attrs.define(auto_exc=True)
class NotFound(HTTPException):
    """Raised when an unknown resource was not found."""

    http_status: http.HTTPStatus = attrs.field(
        default=http.HTTPStatus.NOT_FOUND, init=False
    )


@attrs.define(auto_exc=True)
class Unauthorized(HTTPException):
    """An exception that's raised when trying to make unauthorized call to a resource and it returns 404."""

    http_status: http.HTTPStatus = attrs.field(
        default=http.HTTPStatus.UNAUTHORIZED, init=False
    )


@attrs.define(auto_exc=True)
class BadRequest(HTTPError):
    """An exception raised when requesting a resource with the provided data is wrong."""

    url: typedefs.StrOrURL | None
    """The URL/endpoint caused this error."""

    body: typing.Any
    """The response body."""

    headers: multidict.CIMultiDictProxy[str]
    """The response headers."""

    http_status: http.HTTPStatus = attrs.field(
        default=http.HTTPStatus.BAD_REQUEST, init=False
    )


@attrs.define(auto_exc=True)
class MembershipTypeError(BadRequest):
    """A bad request error raised when passing wrong membership to the request.

    Those fields are useful since it returns the correct membership and id which can be used
    to make the request again with those fields.

    Example
    -------
    ```py
    try:
        profile = await client.fetch_profile(
            member_id=1,
            type=aiobungie.MembershipType.STADIA,
            components=()
        )

    # Membership type is wrong!
    except aiobungie.MembershipTypeError as err:
        correct_membersip = err.into_membership()
        profile_id = err.membership_id

        # Recall the method.
        profile = await client.fetch_profile(
            member_id=profile_id,
            type=correct_membership,
            components=()
        )
    ```
    """

    membership_type: str
    """The errored membership type passed to the request."""

    membership_id: int
    """The errored user's membership id."""

    required_membership: str
    """The required correct membership for errored user."""

    def into_membership(self, value: str | None = None) -> enums.MembershipType:
        """Turn the required membership from `str` into `aiobungie.Membership` type.

        If value parameter is not provided it will fall back to the required membership.
        """
        if value is None:
            return _determine_membership(self.required_membership)
        return _determine_membership(value)

    def __str__(self) -> str:
        return (
            f"Expected membership: {self.into_membership().name.replace('_', '').title()}, "
            f"But got {self.into_membership(self.membership_type)} for id {self.membership_id}"
        )

    def __int__(self) -> int:
        return int(self.membership_id)


@attrs.define(auto_exc=True)
class InternalServerError(HTTPException):
    """Raised for 5xx internal server errors."""


@attrs.define(auto_exc=True)
class ResponseError(HTTPException):
    """Exception for other HTTP response errors."""


@attrs.define(auto_exc=True)
class RateLimitedError(HTTPError):
    """Raised when too many request status code is returned."""

    http_status: http.HTTPStatus = attrs.field(
        default=http.HTTPStatus.TOO_MANY_REQUESTS, init=False
    )
    """The request response http status."""

    url: typedefs.StrOrURL
    """The URL/endpoint caused this error."""

    body: typing.Any
    """The response body."""

    retry_after: float = attrs.field(default=0.0)
    """The amount of seconds you need to wait before retrying to requests."""

    message: str = attrs.field(init=False)
    """A Bungie human readable message describes the cause of the error."""

    @message.default  # type: ignore
    def _(self) -> str:
        return f"You're ratelimited for {self.retry_after}, Endpoint: {self.url}. Slow down!"

    def __str__(self) -> str:
        return self.message


async def raise_error(response: aiohttp.ClientResponse) -> AiobungieError:
    """Generates and raise exceptions on error responses."""

    # Not a JSON response, raise immediately.

    # Also Bungie sometimes get funky and return HTML instead of JSON when making an authorized
    # request with a dummy access token. I can't really do anything about this..
    if response.content_type != "application/json":
        return HTTPError(
            f"Expected JSON content but got {response.content_type!s}, {response.real_url!s}",
            http.HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        )

    body: collections.Mapping[str, typing.Any] = helpers.loads(await response.read())  # type: ignore
    message: str = body.get("Message", "UNDEFINED_MESSAGE")
    error_status: str = body.get("ErrorStatus", "UNDEFINED_ERROR_STATUS")
    message_data: dict[str, str] = body.get("MessageData", {})
    throttle_seconds: int = body.get("ThrottleSeconds", 0)
    error_code: int = body.get("ErrorCode", 0)

    # Standard HTTP status.
    match response.status:
        case http.HTTPStatus.NOT_FOUND:
            return NotFound(
                message=message,
                error_code=error_code,
                throttle_seconds=throttle_seconds,
                url=str(response.real_url),
                body=body,
                headers=response.headers,
                error_status=error_status,
                message_data=message_data,
            )

        case http.HTTPStatus.FORBIDDEN:
            return Forbidden(
                message=message,
                error_code=error_code,
                throttle_seconds=throttle_seconds,
                url=str(response.real_url),
                body=body,
                headers=response.headers,
                error_status=error_status,
                message_data=message_data,
            )

        case http.HTTPStatus.UNAUTHORIZED:
            return Unauthorized(
                message=message,
                error_code=error_code,
                throttle_seconds=throttle_seconds,
                url=str(response.real_url),
                body=body,
                headers=response.headers,
                error_status=error_status,
                message_data=message_data,
            )

        case http.HTTPStatus.BAD_REQUEST:
            # Membership needs to be alone.
            if error_status == "InvalidParameters":
                return MembershipTypeError(
                    message=message,
                    body=body,
                    headers=response.headers,
                    url=str(response.url),
                    membership_type=message_data["membershipType"],
                    required_membership=message_data["membershipInfo.membershipType"],
                    membership_id=int(message_data["membershipId"]),
                )
            return BadRequest(
                message=message,
                body=body,
                headers=response.headers,
                url=str(response.url),
            )
        case _:
            status = http.HTTPStatus(response.status)

            if 400 <= status < 500:
                return ResponseError(
                    message=message,
                    error_code=error_code,
                    throttle_seconds=throttle_seconds,
                    url=str(response.real_url),
                    body=body,
                    headers=response.headers,
                    error_status=error_status,
                    message_data=message_data,
                    http_status=status,
                )

            # Need to self handle ~5xx errors
            elif 500 <= status < 600:
                # No API key or method requires OAuth2 most likely.
                if error_status in {
                    "ApiKeyMissingFromRequest",
                    "WebAuthRequired",
                    "ApiInvalidOrExpiredKey",
                    "AuthenticationInvalid",
                    "AuthorizationCodeInvalid",
                }:
                    return Unauthorized(
                        message=message,
                        error_code=error_code,
                        throttle_seconds=throttle_seconds,
                        url=str(response.real_url),
                        body=body,
                        headers=response.headers,
                        error_status=error_status,
                        message_data=message_data,
                    )

                # Anything contains not found.
                elif (
                    "NotFound" in error_status
                    or error_status == "UserCannotFindRequestedUser"
                ):
                    return NotFound(
                        message=message,
                        error_code=error_code,
                        throttle_seconds=throttle_seconds,
                        url=str(response.real_url),
                        body=body,
                        headers=response.headers,
                        error_status=error_status,
                        message_data=message_data,
                    )

                # Other 5xx errors.
                else:
                    return InternalServerError(
                        message=message,
                        error_code=error_code,
                        throttle_seconds=throttle_seconds,
                        url=str(response.real_url),
                        body=body,
                        headers=response.headers,
                        error_status=error_status,
                        message_data=message_data,
                        http_status=status,
                    )
            # Something else.
            else:
                return HTTPException(
                    message=message,
                    error_code=error_code,
                    throttle_seconds=throttle_seconds,
                    url=str(response.real_url),
                    body=body,
                    headers=response.headers,
                    error_status=error_status,
                    message_data=message_data,
                    http_status=status,
                )


def stringify_http_message(headers: collections.Mapping[str, str]) -> str:
    return (
        "{ \n"
        + "\n".join(  # noqa: W503
            f"{f'   {key}'}: {value}"
            if key not in ("Authorization", "X-API-KEY", "client_secret", "client_id")
            else f"   {key}: REDACTED_TOKEN"
            for key, value in headers.items()
        )
        + "\n}"  # noqa: W503
    )
