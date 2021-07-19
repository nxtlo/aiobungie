# -*- coding: utf-8 -*-

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

"""A very basic OAuth2 implementation for aiobungie."""

from __future__ import annotations

__all__: Sequence[str] = ["OAuth2", "refresh"]

import asyncio
import inspect
import logging
import uuid
from ..utils import RedisCache
from typing import Any, Sequence, Optional, Dict, TYPE_CHECKING
from requests_oauthlib import OAuth2Session
from functools import wraps
from ..http import HTTPClient

if TYPE_CHECKING:
    import builtins

log: logging.Logger = logging.getLogger(__name__)


class OAuth2:
    """
    OAuth2 implemention for the Bungie API.

    Attributes
    -----------
    token: `builtins.str`
            Your application's token or API Key
    secret: `builtins.str`
            Your application's client secret.
    """

    CLIENT_ID: int = 33953

    def __init__(
        self,
        token: str,
        secret: str,
        *,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        **options: Any,
    ) -> None:
        self._token: str = token
        self._secret: str = secret
        self.loop: asyncio.AbstractEventLoop = (
            asyncio.get_event_loop() if not loop else loop
        )
        self.cache: RedisCache = RedisCache()

        if self._token is None:
            raise ValueError("Token have to be passed.")

        if self._secret is None:
            raise ValueError("Client Secret has to be passed.")

        self._http: HTTPClient = HTTPClient(key=token)

    async def do_auth(self) -> None:
        req = OAuth2Session(
            client_id=self.CLIENT_ID,
            redirect_uri="https://www.bungie.net/",
            auto_refresh_url="https://www.bungie.net/Platform/App/OAuth/token/",
        )
        url, _ = req.authorization_url(
            "https://www.bungie.net/en/OAuth/Authorize/", state=uuid.uuid4()
        )
        print(url)
        wait = input("Please click the url and Enter the code: ")
        data = req.fetch_token(
            "https://www.bungie.net/Platform/App/Oauth/token/",
            code=wait,
            client_secret=self._secret,
        )
        refresh: str = data.get("refresh_token")
        access: str = data.get("access_token")
        await self.cache.hash.set("tokens", "access", access)
        await self.cache.hash.set("tokens", "refresh", refresh)
        log.info("Tokens INSERTED")

    async def get_current_user(self) -> Any:
        """
        GET method to retrieve the user data.
        """
        key = await self.cache.hash.get("tokens", "access")
        headers: Dict[str, str] = {
            "X-API-KEY": self._token,
            "Authorization": f"Bearer {key}",
        }
        return await self._http.fetch(
            method="GET", route="User/GetBungieNetUser/", headers=headers
        )


# This works but will not refresh in time
# Still working on a better method.
def refresh(
    *, seconds: float = 0, minutes: float = 0, hours: float = 0, cls: OAuth2 = None
):
    """
    a decorator to refresh the token every ??? seconds.

    Parameters
    ----------
    every: `builtins.int`
            The amount of seconds to refresh after. Default is 59 minutes
    cls: `object`
            This should your OAuth2 class.

    Raises
    ------
    `builtins.TypeError`
            The function was not a coroutine.
    """

    if cls is None:
        cls = OAuth2  # type: ignore

    def inner(inject: Any):
        if not inspect.iscoroutinefunction(inject):
            raise TypeError(
                f"Expected coroutine function, not {type(inject).__name__!r}"
            )

        @wraps(inject)
        async def decorator(*args, **kwargs):
            coro = await inject(*args, **kwargs)
            data: Dict[str, Any] = {
                "grant_type": "refresh_token",
                "refresh_token": await cls.cache.hash.get("tokens", "refresh"),
                "client_id": cls.CLIENT_ID,
                "client_secret": cls._secret,
                "Content-Type": "application/x-www-form-urlencoded",
            }

            post = await cls._http.fetch("POST", "App/OAuth/token/", data=data)
            new_token = post.get("access_token")
            new_ref = post.get("refresh_token")

            if (new_ref, new_token) is not None:
                await cls.cache.hash.set("tokens", "refresh", new_ref)
                await cls.cache.hash.set("tokens", "access", new_token)
            return coro

        return decorator

    return inner
