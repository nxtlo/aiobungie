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

"""A basic REST only client to interact with Bungie's REST API."""

from __future__ import annotations

__all__: tuple[str, ...] = ("RESTClient",)

import asyncio
import http
import logging
import sys
import typing
from urllib import parse

import aiohttp
import attr

from aiobungie import _info as info
from aiobungie import error
from aiobungie import interfaces
from aiobungie import url
from aiobungie.internal import _backoff as backoff
from aiobungie.internal import enums
from aiobungie.internal import helpers

if typing.TYPE_CHECKING:
    import types

    ResponseSigT = typing.TypeVar(
        "ResponseSigT",
        covariant=True,
        bound=typing.Union[helpers.JsonArray, helpers.JsonObject, None],
    )
    """The signature of the response."""

    ResponseSig = typing.Coroutine[typing.Any, typing.Any, ResponseSigT]
    """A type hint for a general coro method that returns a type
    that's mostly going to be on of `aiobungie.internal.helpers.JsonObject`
    or `aiobungie.internal.helpers.JsonArray`
    """

_APP_JSON: typing.Final[str] = "application/json"
_LOG: typing.Final[logging.Logger] = logging.getLogger("aiobungie.rest")


async def handle_errors(
    response: aiohttp.ClientResponse, msg: typing.Optional[str] = None
) -> error.AiobungieError:

    if response.content_type != _APP_JSON:
        return error.HTTPException(
            f"Expected json content but got {response.content_type}, {str(response.real_url)}"
        )

    from_json = await response.json()
    data = [str(response.real_url), from_json, msg]

    if response.status == http.HTTPStatus.NOT_FOUND:
        return error.NotFound(*data)
    elif response.status == http.HTTPStatus.FORBIDDEN:
        return error.Forbidden(*data)
    elif response.status == http.HTTPStatus.UNAUTHORIZED:
        return error.Unauthorized(*data)

    status = http.HTTPStatus(response.status)

    if 400 <= status < 500:
        return error.ResponseError(*data, status)

    # For some WEIRD reason bungie doesn't follow the http
    # error codes protocol and almost return 5xx on any failed request
    # except very few. The only way currently to handle this is by their
    # custom error codes.
    elif 500 <= status < 600:
        if msg in ("ApiKeyMissingFromRequest", "WebAuthRequired"):
            # No API key or method requires OAuth2 most likely.
            return error.Unauthorized(*data)
        if msg == "ClanNotFound":
            return error.ClanNotFound(*data)
        elif msg == "NotFound":
            return error.NotFound(*data)
        elif msg == "DestinyInvalidMembershipType":
            return error.MembershipTypeError(*data)
        elif msg == "Group Not Found":
            return error.ClanNotFound(*data)
        elif msg == "UserCannotFindRequestedUser":
            return error.UserNotFound(*data)
        else:
            return error.InternalServerError(
                message=str(msg), long_message=from_json.get("Message", "")
            )
    else:
        return error.HTTPException(*data)


class PreLock:
    __slots__ = ("_lock",)

    def __init__(self) -> None:
        self._lock = asyncio.Lock()

    async def __aenter__(self) -> None:
        await self.acquire()

    async def __aexit__(
        self,
        exception_type: typing.Optional[type[BaseException]],
        exception: typing.Optional[BaseException],
        exception_traceback: typing.Optional[types.TracebackType],
    ) -> None:
        self._lock.release()

    async def acquire(self) -> None:
        if not self._lock.locked():
            await self._lock.acquire()


@attr.define()
class _Session:
    client_session: aiohttp.ClientSession = attr.field()

    @classmethod
    def acquire_session(
        cls,
        *,
        owner: bool = False,
        raise_status: bool = False,
        total_timeout: typing.Optional[float] = 30,
        connect: typing.Optional[float] = None,
        socket_read: typing.Optional[float] = None,
        socket_connect: typing.Optional[float] = None,
        **kwargs: typing.Any,
    ) -> _Session:
        session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False, **kwargs),
            headers={
                "User-Agent": f"AiobungieClient/{info.__version__}"
                f" ({info.__url__}) Python/{sys.version_info}"
                f"Aiohttp/{aiohttp.HttpVersion11}"
            },
            connector_owner=owner,
            raise_for_status=raise_status,
            timeout=aiohttp.ClientTimeout(
                total=total_timeout,
                sock_read=socket_read,
                sock_connect=socket_connect,
                connect=connect,
            ),
        )
        return cls(client_session=session)

    async def __aenter__(self) -> _Session:
        return self

    async def __aexit__(
        self,
        exception_type: typing.Optional[type[BaseException]],
        exception: typing.Optional[BaseException],
        exception_traceback: typing.Optional[types.TracebackType],
    ) -> None:
        await self.close()

    async def close(self) -> None:
        await self.client_session.connector.close()  # type: ignore
        await asyncio.sleep(0.025)


class RESTClient(interfaces.RESTInterface):
    """A REST only client implementation for interacting with Bungie's REST API.

    Example
    -------
    ```py
    async def main():
        async with aiobungie.RESTClient("TOKEN") as rest_client:
            req = await rest_client.fetch_clan_members(4389205)
            clan_members = req['results']
            for member in clan_members:
                for k, v in member['destinyUserInfo'].items():
                    print(k, v)
    ```

    Attributes
    ----------
    token : `builtins.str`
        A valid application token from Bungie's developer portal.
    max_retries : `builtins.int`
        The max retries number to retry if the request hit a `5xx` status code.
    """

    __slots__: typing.Sequence[str] = ("_token", "_session", "_max_retries")

    def __init__(self, token: str, /, *, max_retries: int = 4) -> None:
        self._session: typing.Optional[_Session] = None
        self._token: str = token
        self._max_retries = max_retries

    def _acquire_session(self) -> _Session:
        asyncio.get_running_loop()
        if self._session is None:
            self._session = _Session.acquire_session(
                owner=False,
                raise_status=False,
                connect=None,
                socket_read=None,
                socket_connect=None,
            )
        return self._session

    @typing.final
    async def close(self) -> None:
        _LOG.info("Closing REST client.")
        await self._acquire_session().close()

    @typing.final
    async def _request(
        self,
        method: str,
        route: str,
        base: bool = False,
        type: typing.Literal["json", "read"] = "json",
        **kwargs: typing.Any,
    ) -> typing.Any:

        retries: int = 0
        if isinstance(self._token, str) and self._token is not None:
            kwargs["headers"] = headers = {}
            headers["X-API-KEY"] = self._token
        else:
            raise ValueError("No API KEY was passed.")

        while True:
            try:
                async with PreLock():
                    async with self._acquire_session().client_session.request(
                        method=method,
                        url=f"{url.REST_EP if base is False else url.BASE}/{route}",
                        **kwargs,
                    ) as response:

                        await self._handle_ratelimit(response)

                        if response.status == http.HTTPStatus.NO_CONTENT:
                            return None

                        data = await response.json(encoding="utf-8")
                        if 300 > response.status >= 200:
                            if type == "read":
                                # We want to read the bytes for the manifest response.
                                data = await response.read()
                                return data

                            _LOG.debug(
                                "{} Request success from {} with status {}".format(
                                    method,
                                    f"{url.REST_EP}/{route}",
                                    response.status,
                                )
                            )

                            if response.content_type == _APP_JSON:
                                try:
                                    return data["Response"]

                                # In case we didn't find the Response key
                                # its safer to just return the data.
                                except KeyError:
                                    _LOG.warning(
                                        "Couldn't return the response key, Data: %s",
                                        data,
                                    )
                                    return data

                        if (
                            response.status in {500, 502, 503, 504}
                            and retries < self._max_retries  # noqa: W503
                        ):
                            backoff_ = backoff.ExponentialBackOff(maximum=6)
                            sleep_time = next(backoff_)
                            _LOG.warning(
                                f"Received: {response.status}, Message: {data['Message']}, sleeping for {sleep_time}, "
                                f"Remaining retries: {self._max_retries - retries}"
                            )

                            retries += 1
                            await asyncio.sleep(sleep_time)
                            continue

                        await self._handle_err(response, data["ErrorStatus"])

            except RuntimeError:
                continue

    async def __aenter__(self) -> RESTClient:
        return self

    async def __aexit__(
        self,
        exception_type: typing.Optional[type[BaseException]],
        exception: typing.Optional[BaseException],
        exception_traceback: typing.Optional[types.TracebackType],
    ) -> None:
        if self._session:
            await self._session.close()
        return None

    # We don't want this to be super complicated.
    @typing.final
    @staticmethod
    async def _handle_ratelimit(response: aiohttp.ClientResponse) -> None:
        if response.status == http.HTTPStatus.TOO_MANY_REQUESTS:
            if response.content_type != _APP_JSON:
                _LOG.error(
                    f"we're being ratelmited on non JSON request, {response.content_type}. Returning."
                )
                return None

            json = await response.json()
            retry_after = float(json["retry-after"])
            _LOG.critical("We're being ratelimited. Sleeping for %f:,", retry_after)
            await asyncio.sleep(retry_after)

            raise error.RateLimitedError(
                retry_after=retry_after,
                headers=response.headers,
                url=str(response.real_url),
            )
        return None

    @staticmethod
    @typing.final
    async def _handle_err(
        response: aiohttp.ClientResponse, msg: typing.Optional[str] = None
    ) -> typing.NoReturn:
        raise await handle_errors(response, msg)

    def fetch_user(self, id: int) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request("GET", f"User/GetBungieNetUserById/{id}/")

    def fetch_user_themes(self) -> ResponseSig[helpers.JsonArray]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request("GET", "User/GetAvailableThemes/")

    def fetch_membership_from_id(
        self,
        id: int,
        type: helpers.IntAnd[enums.MembershipType] = enums.MembershipType.NONE,
        /,
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request("GET", f"User/GetMembershipsById/{id}/{int(type)}")

    def static_request(
        self, method: str, path: str, **kwargs: typing.Any
    ) -> ResponseSig[typing.Any]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(method, path, **kwargs)

    def fetch_player(
        self,
        name: str,
        type: helpers.IntAnd[enums.MembershipType] = enums.MembershipType.ALL,
        /,
    ) -> ResponseSig[helpers.JsonArray]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "GET", f"Destiny2/SearchDestinyPlayer/{int(type)}/{parse.quote(name)}/"
        )

    def search_users(self, name: str, /) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request("GET", f"User/Search/Prefix/{name}/0")

    def fetch_clan_from_id(self, id: int) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request("GET", f"GroupV2/{id}")

    def fetch_clan(
        self, name: str, type: helpers.IntAnd[enums.GroupType] = enums.GroupType.CLAN
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request("GET", f"GroupV2/Name/{name}/{int(type)}")

    def fetch_clan_admins(self, clan_id: int, /) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request("GET", f"GroupV2/{clan_id}/AdminsAndFounder/")

    def fetch_clan_conversations(
        self, clan_id: int, /
    ) -> ResponseSig[helpers.JsonArray]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request("GET", f"GroupV2/{clan_id}/OptionalConversations/")

    def fetch_app(self, appid: int, /) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request("GET", f"App/Application/{appid}")

    def fetch_character(
        self, memberid: int, type: helpers.IntAnd[enums.MembershipType], /
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "GET",
            f"Destiny2/{int(type)}/Profile/{memberid}/?components={int(enums.Component.CHARACTERS)}",
        )

    def fetch_activity(
        self,
        member_id: int,
        character_id: int,
        mode: helpers.IntAnd[enums.GameMode],
        membership_type: helpers.IntAnd[
            enums.MembershipType
        ] = enums.MembershipType.ALL,
        *,
        page: int = 0,
        limit: int = 1,
    ) -> ResponseSig[typing.Any]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "GET",
            f"Destiny2/{int(membership_type)}/Account/"
            f"{member_id}/Character/{character_id}/Stats/Activities"
            f"/?mode={int(mode)}&count={limit}&page={page}",
        )

    def fetch_vendor_sales(self) -> ResponseSig[typing.Any]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "GET", f"Destiny2/Vendors/?components={int(enums.Component.VENDOR_SALES)}"
        )

    def fetch_profile(
        self, memberid: int, type: helpers.IntAnd[enums.MembershipType], /
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "GET",
            f"Destiny2/{int(type)}/Profile/{int(memberid)}/?components={int(enums.Component.PROFILE)}",
        )

    def fetch_entity(self, type: str, hash: int) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request("GET", route=f"Destiny2/Manifest/{type}/{hash}")

    def fetch_inventory_item(self, hash: int) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self.fetch_entity("DestinyInventoryItemDefinition", hash)

    def fetch_groups_for_member(
        self,
        member_id: int,
        member_type: helpers.IntAnd[enums.MembershipType],
        /,
        *,
        filter: int = 0,
        group_type: helpers.IntAnd[enums.GroupType] = enums.GroupType.CLAN,
    ) -> ResponseSig[helpers.JsonObject]:
        return self._request(
            "GET",
            f"GroupV2/User/{int(member_type)}/{member_id}/{filter}/{int(group_type)}/",
        )

    def fetch_potential_groups_for_member(
        self,
        member_id: int,
        member_type: helpers.IntAnd[enums.MembershipType],
        /,
        *,
        filter: int = 0,
        group_type: helpers.IntAnd[enums.GroupType] = enums.GroupType.CLAN,
    ) -> ResponseSig[helpers.JsonObject]:
        return self._request(
            "GET",
            f"GroupV2/User/Potential/{int(member_type)}/{member_id}/{filter}/{int(group_type)}/",
        )

    def fetch_clan_members(
        self,
        id: int,
        type: helpers.IntAnd[enums.MembershipType] = enums.MembershipType.NONE,
        name: typing.Optional[str] = None,
        /,
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "GET",
            f"/GroupV2/{id}/Members/?memberType={int(type)}&nameSearch={name if name else ''}&currentpage=1",
        )

    def fetch_hard_linked(
        self,
        credential: int,
        type: helpers.IntAnd[enums.CredentialType] = enums.CredentialType.STADIAID,
        /,
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "GET",
            f"User/GetMembershipFromHardLinkedCredential/{int(type)}/{credential}/",
        )

    async def fetch_manifest_path(self) -> str:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        request = await self._request("GET", "Destiny2/Manifest")
        return request["mobileWorldContentPaths"]["en"]

    async def fetch_manifest(self) -> bytes:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        content = await self.fetch_manifest_path()
        resp = await self._request("GET", content, type="read", base=True)
        return resp

    def fetch_linked_profiles(
        self,
        member_id: int,
        member_type: helpers.IntAnd[enums.MembershipType],
        /,
        *,
        all: bool = False,
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "GET",
            f"Destiny2/{int(member_type)}/Profile/{member_id}/LinkedProfiles/?getAllMemberships={all}",
        )

    def fetch_clan_banners(self) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request("GET", "Destiny2/Clan/ClanBannerDictionary/")

    def fetch_public_milestones(self) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request("GET", "Destiny2/Milestones/")

    def fetch_public_milestone_content(
        self, milestone_hash: int, /
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request("GET", f"Destiny2/Milestones/{milestone_hash}/Content/")

    # * OAuth2 methods.

    def fetch_own_bungie_user(
        self, access_token: str, /
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "GET",
            "User/GetMembershipsForCurrentUser/",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def equip_item(
        self,
        access_token: str,
        /,
        item_id: int,
        character_id: int,
        membership_type: helpers.IntAnd[enums.MembershipType],
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        payload = {
            "itemId": item_id,
            "characterId": character_id,
            "membershipType": int(membership_type),
        }

        return self._request(
            "POST",
            "Destiny2/Actions/Items/EquipItem/",
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def equip_items(
        self,
        access_token: str,
        /,
        item_ids: list[int],
        character_id: int,
        membership_type: helpers.IntAnd[enums.MembershipType],
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        payload = {
            "itemIds": item_ids,
            "characterId": character_id,
            "membershipType": int(membership_type),
        }
        return self._request(
            "POST",
            "Destiny2/Actions/Items/EquipItems/",
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def ban_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: helpers.IntAnd[enums.MembershipType],
        *,
        length: int = 0,
        comment: helpers.UndefinedOr[str] = helpers.Undefined,
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        payload = {"comment": str(comment), "length": length}
        return self._request(
            "POST",
            f"GroupV2/{group_id}/Members/{int(membership_type)}/{membership_id}/Ban/",
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def unban_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: helpers.IntAnd[enums.MembershipType],
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "POST",
            f"GroupV2/{group_id}/Members/{int(membership_type)}/{membership_id}/Unban/",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def kick_clan_member(
        self,
        access_token: str,
        /,
        group_id: int,
        membership_id: int,
        membership_type: helpers.IntAnd[enums.MembershipType],
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "POST",
            f"GroupV2/{group_id}/Members/{int(membership_type)}/{membership_id}/Kick/",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def edit_clan(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        name: helpers.NoneOr[str] = None,
        about: helpers.NoneOr[str] = None,
        motto: helpers.NoneOr[str] = None,
        theme: helpers.NoneOr[str] = None,
        tags: helpers.NoneOr[typing.Sequence[str]] = None,
        is_public: helpers.NoneOr[bool] = None,
        locale: helpers.NoneOr[str] = None,
        avatar_image_index: helpers.NoneOr[int] = None,
        membership_option: helpers.NoneOr[
            helpers.IntAnd[enums.MembershipOption]
        ] = None,
        allow_chat: helpers.NoneOr[bool] = None,
        chat_security: helpers.NoneOr[typing.Literal[0, 1]] = None,
        call_sign: helpers.NoneOr[str] = None,
        homepage: helpers.NoneOr[typing.Literal[0, 1, 2]] = None,
        enable_invite_messaging_for_admins: helpers.NoneOr[bool] = None,
        default_publicity: helpers.NoneOr[typing.Literal[0, 1, 2]] = None,
        is_public_topic_admin: helpers.NoneOr[bool] = None,
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        payload = {
            "name": name,
            "about": about,
            "motto": motto,
            "theme": theme,
            "tags": tags,
            "isPublic": is_public,
            "avatarImageIndex": avatar_image_index,
            "isPublicTopicAdminOnly": is_public_topic_admin,
            "allowChat": allow_chat,
            "chatSecurity": chat_security,
            "callsign": call_sign,
            "homepage": homepage,
            "enableInvitationMessagingForAdmins": enable_invite_messaging_for_admins,
            "defaultPublicity": default_publicity,
            "locale": locale,
        }
        if membership_option is not None:
            payload["membershipOption"] = int(membership_option)

        return self._request(
            "POST",
            f"GroupV2/{group_id}/Edit",
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def edit_clan_options(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        invite_permissions_override: helpers.NoneOr[bool] = None,
        update_culture_permissionOverride: helpers.NoneOr[bool] = None,
        host_guided_game_permission_override: helpers.NoneOr[
            typing.Literal[0, 1, 2]
        ] = None,
        update_banner_permission_override: helpers.NoneOr[bool] = None,
        join_level: helpers.NoneOr[helpers.IntAnd[enums.ClanMemberType]] = None,
    ) -> ResponseSig[None]:

        payload = {
            "InvitePermissionOverride": invite_permissions_override,
            "UpdateCulturePermissionOverride": update_culture_permissionOverride,
            "HostGuidedGamePermissionOverride": host_guided_game_permission_override,
            "UpdateBannerPermissionOverride": update_banner_permission_override,
            "JoinLevel": int(join_level) if join_level else None,
        }

        return self._request(
            "POST",
            f"GroupV2/{group_id}/EditFounderOptions",
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def fetch_friends(self, access_token: str, /) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "POST",
            "Social/Friends",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def fetch_friend_requests(
        self, access_token: str, /
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "POST",
            "Social/Friends/Requests",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def accept_friend_request(
        self, access_token: str, /, member_id: int
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "POST",
            f"Social/Friends/Requests/Accept/{member_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def send_friend_request(
        self, access_token: str, /, member_id: int
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "POST",
            f"Social/Friends/Add/{member_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def decline_friend_request(
        self, access_token: str, /, member_id: int
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "POST",
            f"Social/Friends/Requests/Decline/{member_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def remove_friend(self, access_token: str, /, member_id: int) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        return self._request(
            "POST",
            f"Social/Friends/Remove/{member_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def remove_friend_request(
        self, access_token: str, /, member_id: int
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        return self._request(
            "POST",
            f"Social/Friends/Requests/Remove/{member_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def approve_all_pending_group_users(
        self,
        access_token: str,
        /,
        group_id: int,
        message: helpers.UndefinedOr[str] = helpers.Undefined,
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        return self._request(
            "POST",
            f"GroupV2/{group_id}/Members/ApproveAll",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"message": str(message)},
        )

    def deny_all_pending_group_users(
        self,
        access_token: str,
        /,
        group_id: int,
        message: helpers.UndefinedOr[str] = helpers.Undefined,
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        return self._request(
            "POST",
            f"GroupV2/{group_id}/Members/DenyAll",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"message": str(message)},
        )

    def add_optional_conversation(
        self,
        access_token: str,
        /,
        group_id: int,
        *,
        name: helpers.UndefinedOr[str] = helpers.Undefined,
        security: typing.Literal[0, 1] = 0,
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        payload = {"chatName": str(name), "chatSecurity": security}
        return self._request(
            "POST",
            f"GroupV2/{group_id}/OptionalConversations/Add",
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def edit_optional_conversation(
        self,
        access_token: str,
        /,
        group_id: int,
        conversation_id: int,
        *,
        name: helpers.UndefinedOr[str] = helpers.Undefined,
        security: typing.Literal[0, 1] = 0,
        enable_chat: bool = False,
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        payload = {
            "chatEnabled": enable_chat,
            "chatName": str(name),
            "chatSecurity": security,
        }
        return self._request(
            "POST",
            f"GroupV2/{group_id}/OptionalConversations/Edit/{conversation_id}",
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def transfer_item(
        self,
        access_token: str,
        /,
        item_id: int,
        item_hash: int,
        character_id: int,
        member_type: helpers.IntAnd[enums.MembershipType],
        *,
        stack_size: int = 1,
        vault: bool = False,
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        payload = {
            "characterId": character_id,
            "membershipType": int(member_type),
            "itemId": item_id,
            "itemReferenceHash": item_hash,
            "stackSize": stack_size,
            "transferToVault": vault,
        }
        return self._request(
            "POST",
            "Destiny2/Actions/Items/PullFromPostmaster",
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def pull_item(
        self,
        access_token: str,
        /,
        item_id: int,
        item_hash: int,
        character_id: int,
        member_type: helpers.IntAnd[enums.MembershipType],
        *,
        stack_size: int = 1,
        vault: bool = False,
    ) -> ResponseSig[None]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>
        payload = {
            "characterId": character_id,
            "membershipType": int(member_type),
            "itemId": item_id,
            "itemReferenceHash": item_hash,
            "stackSize": stack_size,
            "transferToVault": vault,
        }
        return self._request(
            "POST",
            "Destiny2/Actions/Items/TransferItem",
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    # * Not implemented yet.

    def fetch_item(
        self, member_id: int, item_id: int, /
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        raise NotImplementedError

    def fetch_clan_weekly_rewards(
        self, clan_id: int, /
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        raise NotImplementedError

    def fetch_weapon_history(
        self,
        character_id: int,
        member_id: int,
        member_type: helpers.IntAnd[enums.MembershipType],
    ) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        raise NotImplementedError

    def fetch_post_activity(self, instance: int, /) -> ResponseSig[helpers.JsonObject]:
        # <<inherited docstring from aiobungie.interfaces.rest.RESTInterface>>.
        # return self._request("GET", f"Destiny2/Stats/PostGameCarnageReport/{instance}")
        raise NotImplementedError
