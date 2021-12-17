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

__all__: list[str] = [
    "AiobungieError",
    "CharacterError",
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
]

import http
import typing

import attr

if typing.TYPE_CHECKING:
    import aiohttp
    import multidict
    from aiohttp import typedefs


@attr.define(auto_exc=True, repr=False, weakref_slot=False)
class AiobungieError(RuntimeError):
    """Base exception class that all other errors inherit from."""


@attr.define(auto_exc=True, repr=False, weakref_slot=False)
class HTTPError(AiobungieError):
    """Exception base used for HTTP request errors."""

    message: str = attr.field()
    """The error message."""

    http_status: http.HTTPStatus = attr.field()
    """The response status."""


@attr.define(auto_exc=True, repr=False, weakref_slot=False)
class CharacterError(HTTPError):
    """Raised when a encountring making a character-based request."""


@attr.define(auto_exc=True, repr=False, weakref_slot=False, kw_only=True)
class HTTPException(HTTPError):
    """Exception base internally used for an HTTP request response errors."""

    error_code: int = attr.field()
    """The returned Bungie error status code."""

    http_status: http.HTTPStatus = attr.field()
    """The request response http status."""

    throttle_seconds: int = attr.field()
    """The Bungie response throttle seconds."""

    url: typing.Optional[typedefs.StrOrURL] = attr.field()
    """The URL/endpoint caused this error."""

    body: typing.Any = attr.field()
    """The response body."""

    headers: multidict.CIMultiDictProxy[str] = attr.field()
    """The response headers."""

    message: str = attr.field()
    """A Bungie human readable message describes the cause of the error."""

    error_status: str = attr.field()
    """A Bungie short error status describes the cause of the error."""

    message_data: dict[str, str] = attr.field()
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


@attr.define(auto_exc=True, repr=False, weakref_slot=False)
class Forbidden(HTTPException):
    """Exception that's raised for when status code 403 occurs."""

    http_status: http.HTTPStatus = attr.field(
        default=http.HTTPStatus.FORBIDDEN, init=False
    )


@attr.define(auto_exc=True, repr=False, weakref_slot=False)
class NotFound(HTTPException):
    """Raised when an unknown request was not found."""

    http_status: http.HTTPStatus = attr.field(
        default=http.HTTPStatus.NOT_FOUND, init=False
    )


@attr.define(auto_exc=True, repr=False, weakref_slot=False)
class Unauthorized(HTTPException):
    """Unauthorized access."""

    http_status: http.HTTPStatus = attr.field(
        default=http.HTTPStatus.UNAUTHORIZED, init=False
    )


@attr.define(auto_exc=True, repr=False, weakref_slot=False)
class BadRequest(HTTPError):
    """Bad requests exceptions."""

    url: typing.Optional[typedefs.StrOrURL] = attr.field()
    """The URL/endpoint caused this error."""

    body: typing.Any = attr.field()
    """The response body."""

    headers: multidict.CIMultiDictProxy[str] = attr.field()
    """The response headers."""

    http_status: http.HTTPStatus = attr.field(default=http.HTTPStatus.BAD_REQUEST)


@attr.define(auto_exc=True, repr=False, weakref_slot=False)
class MembershipTypeError(BadRequest):
    """A bad request error raised when passing wrong membership to the request.

    Those fields are useful since it returns the correct membership and id which can be used
    to make the request again with those fields.
    """

    membership_type: str = attr.field(default="")
    """The errored membership type passed to the request."""

    membership_id: int = attr.field(default=0)
    """The errored user's membership id."""

    required_membership: str = attr.field(default="")
    """The required correct membership for errored user."""

    def __str__(self) -> str:
        return (
            f"Expected membership: {self.required_membership}, "
            f"But got {self.membership_type} for id {self.membership_id}"
        )

    def __int__(self) -> int:
        return int(self.membership_id)


@attr.define(auto_exc=True, repr=False, weakref_slot=False)
class InternalServerError(HTTPException):
    """Raised for other 5xx errors."""


@attr.define(auto_exc=True, repr=False, weakref_slot=False)
class ResponseError(HTTPException):
    """Standard Responses error."""


@attr.define(auto_exc=True, repr=False, weakref_slot=False)
class RateLimitedError(HTTPError):
    """Raiased when being hit with ratelimits."""

    http_status: http.HTTPStatus = attr.field(
        default=http.HTTPStatus.TOO_MANY_REQUESTS, init=False
    )
    """The request response http status."""

    url: typedefs.StrOrURL = attr.field()
    """The URL/endpoint caused this error."""

    body: typing.Any = attr.field()
    """The response body."""

    retry_after: float = attr.field(default=0.0)
    """The amount of seconds you need to wait before retrying to requests."""

    message: str = attr.field(init=False)
    """A Bungie human readable message describes the cause of the error."""

    @message.default  # type: ignore
    def _(self) -> str:
        return f"You're being ratelimited for {self.retry_after} endpoint: {self.url}"

    def __str__(self) -> str:
        return self.message


async def raise_error(response: aiohttp.ClientResponse, msg: str) -> AiobungieError:
    """Generates and raise exceptions on error responses."""

    if response.content_type != "application/json":
        return HTTPError(
            f"Expected JSON content but got {response.content_type}, {str(response.real_url)}",
            http.HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        )

    body = await response.json()
    message: str = body.get("Message", "")
    error_status: str = body.get("ErrorStatus", "")
    message_data: dict[str, str] = body.get("MessageData", {})
    throttle_seconds: int = body.get("ThrottleSeconds", 0)
    error_code: int = body.get("ErrorCode", 0)

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
        if msg == "InvalidParameters":
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

    # Need to handle errors our selves :>
    elif 500 <= status < 600:
        # No API key or method requires OAuth2 most likely.
        if msg in {
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

        # API is down...
        elif msg == "SystemDisabled":
            raise OSError(
                message,
                error_code,
                throttle_seconds,
                str(response.real_url),
                body,
                response.headers,
                error_status,
                message_data,
            )

        # Anything contains not found.
        elif msg and "NotFound" in msg or "UserCannotFindRequestedUser" == msg:
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

        # Any other errors.
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
