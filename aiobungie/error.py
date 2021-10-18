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
    "PlayerNotFound",
    "ActivityNotFound",
    "ClanNotFound",
    "CharacterError",
    "NotFound",
    "HTTPException",
    "UserNotFound",
    "ComponentError",
    "MembershipTypeError",
    "Forbidden",
    "Unauthorized",
    "ResponseError",
    "RateLimitedError",
    "InternalServerError",
]

import typing

import attr

if typing.TYPE_CHECKING:
    import multidict


class AiobungieError(Exception):
    """The base exception class that all other errors inherit from."""


@attr.define(auto_exc=True, repr=False, weakref_slot=False)
class HTTPException(AiobungieError):
    """Exception for handling `aiobungie.rest.RESTClient` requests errors."""

    message: str = attr.field(default="")
    long_message: str = attr.field(default="")


@attr.define(auto_exc=True, repr=False, weakref_slot=False, kw_only=True)
class RateLimitedError(HTTPException):
    """Raiased when being hit with ratelimits."""

    headers: multidict.CIMultiDictProxy[str] = attr.field(default=None)
    retry_after: float = attr.field(default=0.0)
    url: str = attr.field(default="")


@attr.define(auto_exc=True, repr=False, weakref_slot=False)
class InternalServerError(HTTPException):
    """Raised for other 5xx errors."""

    message: str = attr.field(default="")
    long_message: str = attr.field(default="")


class NotFound(AiobungieError):
    """Raised when an unknown request was not found."""


@typing.final
class ResponseError(AiobungieError):
    """Typical Responses error."""


@typing.final
class PlayerNotFound(NotFound):
    """Raised when a `aiobungie.crate.Player` is not found."""


@typing.final
class Forbidden(HTTPException):
    """Exception that's raised for when status code 403 occurs."""


@typing.final
class Unauthorized(HTTPException):
    """Unauthorized access."""


@typing.final
class ActivityNotFound(NotFound):
    """Raised when a `aiobungie.crate.Activity` not found."""


@typing.final
class CharacterError(HTTPException):
    """Raised when a `aiobungie.crate.Character` not found."""


@typing.final
class ClanNotFound(NotFound):
    """Raised when a `aiobungie.crate.Clan` not found."""


@typing.final
class UserNotFound(NotFound):
    """Raised when a user was not found."""


@typing.final
class ComponentError(HTTPException):
    """Raised when someone uses the wrong `aiobungie.internal.enums.Component.`"""


@typing.final
class MembershipTypeError(HTTPException):
    """Raised when the memberhsip type is invalid.
    or The crate you're trying to fetch doesn't have
    The requested membership type.
    """
