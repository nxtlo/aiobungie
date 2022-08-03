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

import collections

__all__: list[str] = [
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
]

import http
import typing

import attrs

if typing.TYPE_CHECKING:
    import aiohttp
    import multidict
    from aiohttp import typedefs


@attrs.define(auto_exc=True)
class AiobungieError(RuntimeError):
    """Base exception class that all other errors inherit from."""


@attrs.define(auto_exc=True)
class HTTPError(AiobungieError):
    """Exception base used for HTTP request errors."""

    message: str
    """The error message."""

    http_status: http.HTTPStatus
    """The response status."""


@attrs.define(auto_exc=True, kw_only=True)
class HTTPException(HTTPError):
    """Exception base internally used for an HTTP request response errors."""

    error_code: int
    """The returned Bungie error status code."""

    http_status: http.HTTPStatus
    """The request response http status."""

    throttle_seconds: int
    """The Bungie response throttle seconds."""

    url: typing.Optional[typedefs.StrOrURL]
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
    """Raised when an unknown request was not found."""

    http_status: http.HTTPStatus = attrs.field(
        default=http.HTTPStatus.NOT_FOUND, init=False
    )


@attrs.define(auto_exc=True)
class Unauthorized(HTTPException):
    """Unauthorized access."""

    http_status: http.HTTPStatus = attrs.field(
        default=http.HTTPStatus.UNAUTHORIZED, init=False
    )


@attrs.define(auto_exc=True)
class BadRequest(HTTPError):
    """Bad requests exceptions."""

    url: typing.Optional[typedefs.StrOrURL]
    """The URL/endpoint caused this error."""

    body: typing.Any
    """The response body."""

    headers: multidict.CIMultiDictProxy[str]
    """The response headers."""

    http_status: http.HTTPStatus = attrs.field(default=http.HTTPStatus.BAD_REQUEST)


@attrs.define(auto_exc=True)
class MembershipTypeError(BadRequest):
    """A bad request error raised when passing wrong membership to the request.

    Those fields are useful since it returns the correct membership and id which can be used
    to make the request again with those fields.
    """

    membership_type: str = attrs.field(default="")
    """The errored membership type passed to the request."""

    membership_id: int = attrs.field(default=0)
    """The errored user's membership id."""

    required_membership: str = attrs.field(default="")
    """The required correct membership for errored user."""

    def __str__(self) -> str:
        return (
            f"Expected membership: {self.required_membership}, "
            f"But got {self.membership_type} for id {self.membership_id}"
        )

    def __int__(self) -> int:
        return int(self.membership_id)


@attrs.define(auto_exc=True)
class InternalServerError(HTTPException):
    """Raised for 5xx internal server errors."""


@attrs.define(auto_exc=True)
class ResponseError(HTTPException):
    """Standard HTTP responses exception."""


@attrs.define(auto_exc=True)
class RateLimitedError(HTTPError):
    """Raised when being hit with ratelimits."""

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

    body = await response.json()
    message: str = body.get("Message", "UNDEFINED_MESSAGE")
    error_status: str = body.get("ErrorStatus", "UNDEFINED_ERROR_STATUS")
    message_data: dict[str, str] = body.get("MessageData", {})
    throttle_seconds: int = body.get("ThrottleSeconds", 0)
    error_code: int = body.get("ErrorCode", 0)

    # Standard HTTP status.
    if response.status == http.HTTPStatus.NOT_FOUND:
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

    elif response.status == http.HTTPStatus.FORBIDDEN:
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

    elif response.status == http.HTTPStatus.UNAUTHORIZED:
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

    elif response.status == http.HTTPStatus.BAD_REQUEST:
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
            "NotFound" in error_status or error_status == "UserCannotFindRequestedUser"
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
            if key not in ("Authorization", "X-API-KEY")
            else f"   {key}: HIDDEN_TOKEN"
            for key, value in headers.items()
        )
        + "\n}"  # noqa: W503
    )
