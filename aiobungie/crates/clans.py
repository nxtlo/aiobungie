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

"""Implementation of a Bungie a clan and groups."""

from __future__ import annotations

__all__ = (
    "Clan",
    "ClanMember",
    "ClanFeatures",
    "ClanConversation",
    "ClanBanner",
    "GroupMember",
)

import typing

import attrs

from aiobungie import undefined
from aiobungie import url
from aiobungie.crates import fireteams
from aiobungie.crates import user
from aiobungie.internal import enums
from aiobungie.internal import helpers
from aiobungie.internal import iterators

if typing.TYPE_CHECKING:
    import collections.abc as collections
    from datetime import datetime

    from aiobungie import traits
    from aiobungie import typedefs
    from aiobungie.crates import progressions as progressions_
    from aiobungie.internal import assets


@attrs.define(kw_only=True)
class ClanFeatures:
    """Represents Bungie clan features."""

    max_members: int
    """The maximum members the clan can have"""

    max_membership_types: int
    """The maximum membership types the clan can have"""

    capabilities: int
    """An int that represents the clan's capabilities."""

    membership_types: list[enums.MembershipType]
    """The clan's membership types."""

    invite_permissions: bool
    """True if the clan has permissions to invite."""

    update_banner_permissions: bool
    """True if the clan has permissions to updates its banner."""

    update_culture_permissions: bool

    join_level: int
    """The clan's join level."""


@attrs.define(kw_only=True)
class ClanConversation:
    """Represents a clan conversation."""

    net: traits.Netrunner = attrs.field(repr=False, eq=False, hash=False)
    """A network state used for making external requests."""

    group_id: int
    """The clan or group's id."""

    id: int
    """The conversation's id"""

    chat_enabled: bool
    """`True` if the Conversation's chat is enabled."""

    name: undefined.UndefinedOr[str]
    """Conversation chat's name."""

    security: int
    """Conversation's security level."""

    async def edit(
        self,
        access_token: str,
        /,
        *,
        name: undefined.UndefinedOr[str] = undefined.Undefined,
        security: typing.Literal[0, 1] = 0,
        enable_chat: bool = False,
    ) -> None:
        """Edit the settings of this chat/conversation channel.

        ..note::
            This request requires OAuth2: AdminGroups scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Other parameters
        ----------------
        name: `aiobungie.UndefinedOr[str]`
            The new chat name. Default to `UNDEFINED`
        security: `typing.Literal[0, 1]`
            The new security level of the chat.

            If provided and set to 0, It will be to `Group` only.
            If provided and set to 1, It will be `Admins` only.
            Default is `0`
        enable_chat : `bool`
            Whether to enable chatting or not.
            If set to `True` then chatting will be enabled. Otherwise it will be disabled.
        """
        await self.net.request.rest.edit_optional_conversation(
            access_token,
            self.group_id,
            self.id,
            name=name,
            security=security,
            enable_chat=enable_chat,
        )

    def __int__(self) -> int:
        return self.id

    def __str__(self) -> str:
        return str(self.name)


@attrs.define(kw_only=True)
class ClanBanner:
    """Representation of information of the clan banner."""

    id: int
    """The banner's id."""

    foreground: assets.Image
    """The banner's foreground. This field can be `UNDEFINED` if not found."""

    background: assets.Image
    """The banner's background. This field can be `UNDEFINED` if not found."""

    def __int__(self) -> int:
        return self.id


@attrs.define(kw_only=True)
class ClanMember(user.DestinyMembership):
    """Represents a Bungie clan member."""

    net: traits.Netrunner = attrs.field(repr=False, eq=False, hash=False)
    """A network state used for making external requests."""

    last_seen_name: str
    """The clan member's last seen display name"""

    group_id: int
    """The member's group id."""

    member_type: enums.ClanMemberType
    """The runtime type of this clan member."""

    is_online: bool
    """True if the clan member is online or not."""

    last_online: datetime
    """The date of the clan member's last online in UTC time zone."""

    joined_at: datetime
    """The clan member's join date in UTC time zone."""

    bungie: typing.Optional[user.PartialBungieUser]
    """The clan member's bungie partial net user if set. `None` if not found.

    .. note:: This only returns a partial bungie net user.
    You can fetch the fully implemented user using `aiobungie.crates.PartialBungieUser.fetch_self()` method.
    """

    @property
    def is_admin(self) -> bool:
        """Check whether this member is a clan admin or not."""
        return self.member_type is enums.ClanMemberType.ADMIN

    @property
    def is_founder(self) -> bool:
        """Check whether this member is the clan founder or not."""
        return self.member_type is enums.ClanMemberType.FOUNDER

    async def fetch_clan(self) -> Clan:
        """Fetch the clan this member belongs to.

        Returns
        -------
        `Clan`
            The clan admins clan.
        """
        return await self.net.request.fetch_clan_from_id(self.group_id)

    async def ban(
        self,
        access_token: str,
        /,
        *,
        comment: undefined.UndefinedOr[str] = undefined.Undefined,
        length: int = 0,
    ) -> None:
        """Ban this member from the clan.

        .. note::
            This request requires OAuth2: oauth2: `AdminGroups` scope.

        Parameters
        ----------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.

        Other Parameters
        ----------------
        length: `int`
            An optional ban length. Default is 0
        comment: `aiobungie.UndefinedOr[str]`
            An optional comment to this ban. Default is `UNDEFINED`
        """
        await self.net.request.rest.ban_clan_member(
            access_token,
            self.group_id,
            self.id,
            self.type,
            comment=comment,
            length=length,
        )

    async def unban(self, access_token: str, /) -> None:
        """Unban this member from the clan.

        .. note::
            This request requires OAuth2: oauth2: `AdminGroups` scope.

        Parameters
        ----------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.
        """
        await self.net.request.rest.unban_clan_member(
            access_token,
            group_id=self.group_id,
            membership_id=self.id,
            membership_type=self.type,
        )

    async def kick(self, access_token: str, /) -> Clan:
        """Kick this member from the clan.

        .. note::
            This request requires OAuth2: oauth2: `AdminGroups` scope.

        Parameters
        ----------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.

        Returns
        -------
        `aiobungie.crates.clan.Clan`
            The clan that represents the kicked member.
        """
        return await self.net.request.kick_clan_member(
            access_token,
            group_id=self.group_id,
            membership_id=self.id,
            membership_type=self.type,
        )


@attrs.define(kw_only=True)
class GroupMember:
    """Represents information about joined groups/clans for a member."""

    net: traits.Netrunner = attrs.field(repr=False, eq=False, hash=False)
    """A network state used for making external requests."""

    inactive_memberships: typedefs.NoneOr[dict[int, bool]]
    """The member's inactive memberships if provided. This will be `None` if not provided."""

    member_type: enums.ClanMemberType
    """The member's member type."""

    is_online: bool
    """Whether the member is online or not."""

    last_online: datetime
    """Datetime of the member's last online apperation."""

    group_id: int
    """The group id of this member."""

    join_date: datetime
    """Datetime of the member's join date."""

    member: user.DestinyMembership
    """The member's destiny object that represents the group member."""

    group: Clan
    """The member's group/clan object that represents the group member."""

    async def fetch_self_clan(self) -> Clan:
        """Fetch an up-todate clan/group object of the current group.

        Returns
        -------
        `Clan`
            The clan object.
        """
        return await self.net.request.fetch_clan_from_id(self.group_id)

    def __int__(self) -> int:
        return self.group_id


@attrs.define(kw_only=True)
class Clan:
    """Represents a Bungie clan."""

    net: traits.Netrunner = attrs.field(repr=False, eq=False, hash=False)
    """A network state used for making external requests."""

    id: int
    """The clan id"""

    type: enums.GroupType
    """The clan type."""

    name: str
    """The clan's name"""

    created_at: datetime
    """Clan's creation date time in UTC."""

    member_count: int
    """Clan's member count."""

    motto: str
    """Clan's motto."""

    is_public: bool
    """Clan's privacy status."""

    banner: assets.Image
    """Clan's banner"""

    avatar: assets.Image
    """Clan's avatar"""

    about: str
    """Clan's about title."""

    tags: list[str]
    """A list of the clan's tags."""

    theme: str
    """The set clan theme."""

    conversation_id: int

    allow_chat: bool

    chat_security: int

    progressions: collections.Mapping[int, progressions_.Progression]
    """A mapping from progression hash to a progression object."""

    banner_data: collections.Mapping[str, int]

    call_sign: str
    """The clan call sign."""

    owner: typedefs.NoneOr[ClanMember]
    """The clan owner. This field could be `None` if not found."""

    features: ClanFeatures
    """The clan features."""

    current_user_membership: typing.Optional[collections.Mapping[str, ClanMember]]
    """If an authorized user made this request and this user belongs to this clan.
    This field will be available.

    This maps from the membership type represented as a string to the authorized clan member.
    """

    async def edit_options(
        self,
        access_token: str,
        /,
        *,
        invite_permissions_override: typedefs.NoneOr[bool] = None,
        update_culture_permissionOverride: typedefs.NoneOr[bool] = None,
        host_guided_game_permission_override: typedefs.NoneOr[
            typing.Literal[0, 1, 2]
        ] = None,
        update_banner_permission_override: typedefs.NoneOr[bool] = None,
        join_level: typedefs.NoneOr[typedefs.IntAnd[enums.ClanMemberType]] = None,
    ) -> None:
        """Edit this clan's options.

        Notes
        -----
        * This request requires OAuth2: oauth2: `AdminGroups` scope.
        * All arguments will be ignored if set to `None`. This does not include `access_token`

        Parameters
        ----------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.

        Other Parameters
        ----------------
        invite_permissions_override : `aiobungie.typedefs.NoneOr[bool]`
            Minimum Member Level allowed to invite new members to group
            Always Allowed: Founder, Acting Founder
            True means admins have this power, false means they don't
            Default is False for clans, True for groups.
        update_culture_permissionOverride : `aiobungie.typedefs.NoneOr[bool]`
            Minimum Member Level allowed to update group culture
            Always Allowed: Founder, Acting Founder
            True means admins have this power, false means they don't
            Default is False for clans, True for groups.
        host_guided_game_permission_override : `aiobungie.typedefs.NoneOr[typing.Literal[0, 1, 2]]`
            Minimum Member Level allowed to host guided games
            Always Allowed: Founder, Acting Founder, Admin
            Allowed Overrides: `0` -> None, `1` -> Beginner `2` -> Member.
            Default is Member for clans, None for groups, although this means nothing for groups.
        update_banner_permission_override : `aiobungie.typedefs.NoneOr[bool]`
            Minimum Member Level allowed to update banner
            Always Allowed: Founder, Acting Founder
            True means admins have this power, false means they don't
            Default is False for clans, True for groups.
        join_level : `aiobungie.ClanMemberType`
            Level to join a member at when accepting an invite, application, or joining an open clan.
            Default is `aiobungie.ClanMemberType.BEGINNER`
        """
        await self.net.request.rest.edit_clan_options(
            access_token,
            group_id=self.id,
            invite_permissions_override=invite_permissions_override,
            update_culture_permissionOverride=update_culture_permissionOverride,
            host_guided_game_permission_override=host_guided_game_permission_override,
            update_banner_permission_override=update_banner_permission_override,
            join_level=join_level,
        )

    async def edit(
        self,
        access_token: str,
        /,
        *,
        name: typedefs.NoneOr[str] = None,
        about: typedefs.NoneOr[str] = None,
        motto: typedefs.NoneOr[str] = None,
        theme: typedefs.NoneOr[str] = None,
        tags: typedefs.NoneOr[collections.Sequence[str]] = None,
        is_public: typedefs.NoneOr[bool] = None,
        locale: typedefs.NoneOr[str] = None,
        avatar_image_index: typedefs.NoneOr[int] = None,
        membership_option: typedefs.NoneOr[
            typedefs.IntAnd[enums.MembershipOption]
        ] = None,
        allow_chat: typedefs.NoneOr[bool] = None,
        chat_security: typedefs.NoneOr[typing.Literal[0, 1]] = None,
        call_sign: typedefs.NoneOr[str] = None,
        homepage: typedefs.NoneOr[typing.Literal[0, 1, 2]] = None,
        enable_invite_messaging_for_admins: typedefs.NoneOr[bool] = None,
        default_publicity: typedefs.NoneOr[typing.Literal[0, 1, 2]] = None,
        is_public_topic_admin: typedefs.NoneOr[bool] = None,
    ) -> None:
        """Edit this clan.

        Notes
        -----
        * This request requires OAuth2: oauth2: `AdminGroups` scope.
        * All arguments will default to `None` if not provided. This does not include `access_token` and `group_id`

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Other Parameters
        ----------------
        name : `aiobungie.typedefs.NoneOr[str]`
            The name to edit the clan with.
        about : `aiobungie.typedefs.NoneOr[str]`
            The about section to edit the clan with.
        motto : `aiobungie.typedefs.NoneOr[str]`
            The motto section to edit the clan with.
        theme : `aiobungie.typedefs.NoneOr[str]`
            The theme name to edit the clan with.
        tags : `aiobungie.typedefs.NoneOr[collections.Sequence[str]]`
            A sequence of strings to replace the clan tags with.
        is_public : `aiobungie.typedefs.NoneOr[bool]`
            If provided and set to `True`, The clan will set to private.
            If provided and set to `False`, The clan will set to public whether it was or not.
        locale : `aiobungie.typedefs.NoneOr[str]`
            The locale section to edit the clan with.
        avatar_image_index : `aiobungie.typedefs.NoneOr[int]`
            The clan avatar image index to edit the clan with.
        membership_option : `aiobungie.typedefs.NoneOr[aiobungie.typedefs.IntAnd[aiobungie.MembershipOption]]` # noqa: E501 # Line too long
            The clan membership option to edit it with.
        allow_chat : `aiobungie.typedefs.NoneOr[bool]`
            If provided and set to `True`, The clan members will be allowed to chat.
            If provided and set to `False`, The clan members will not be allowed to chat.
        chat_security : `aiobungie.typedefs.NoneOr[typing.Literal[0, 1]]`
            If provided and set to `0`, The clan chat security will be edited to `Group` only.
            If provided and set to `1`, The clan chat security will be edited to `Admin` only.
        call_sign : `aiobungie.typedefs.NoneOr[str]`
            The clan call sign to edit it with.
        homepage : `aiobungie.typedefs.NoneOr[typing.Literal[0, 1, 2]]`
            If provided and set to `0`, The clan chat homepage will be edited to `Wall`.
            If provided and set to `1`, The clan chat homepage will be edited to `Forum`.
            If provided and set to `0`, The clan chat homepage will be edited to `AllianceForum`.
        enable_invite_messaging_for_admins : `aiobungie.typedefs.NoneOr[bool]`
            ???
        default_publicity : `aiobungie.typedefs.NoneOr[typing.Literal[0, 1, 2]]`
            If provided and set to `0`, The clan chat publicity will be edited to `Public`.
            If provided and set to `1`, The clan chat publicity will be edited to `Alliance`.
            If provided and set to `2`, The clan chat publicity will be edited to `Private`.
        is_public_topic_admin : `aiobungie.typedefs.NoneOr[bool]`
            ???
        """
        await self.net.request.rest.edit_clan(
            access_token,
            group_id=self.id,
            name=name,
            about=about,
            motto=motto,
            theme=theme,
            tags=tags,
            is_public=is_public,
            locale=locale,
            avatar_image_index=avatar_image_index,
            membership_option=membership_option,
            allow_chat=allow_chat,
            chat_security=chat_security,
            call_sign=call_sign,
            homepage=homepage,
            enable_invite_messaging_for_admins=enable_invite_messaging_for_admins,
            default_publicity=default_publicity,
            is_public_topic_admin=is_public_topic_admin,
        )

    async def fetch_avaliable_fireteams(
        self,
        access_token: str,
        activity_type: typedefs.IntAnd[fireteams.FireteamActivity],
        *,
        platform: typedefs.IntAnd[fireteams.FireteamPlatform],
        language: typing.Union[fireteams.FireteamLanguage, str],
        date_range: typedefs.IntAnd[
            fireteams.FireteamDate
        ] = fireteams.FireteamDate.ALL,
        page: int = 0,
        public_only: bool = False,
        slots_filter: int = 0,
    ) -> typing.Optional[collections.Sequence[fireteams.Fireteam]]:
        """Fetch a clan's fireteams with open slots.

        .. note::
            This method requires OAuth2: ReadGroups scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.
        activity_type : `aiobungie.typedefs.IntAnd[aiobungie.crates.FireteamActivity]`
            The fireteam activity type.

        Other Parameters
        ----------------
        platform : `aiobungie.typedefs.IntAnd[aiobungie.crates.fireteams.FireteamPlatform]`
            If this is provided. Then the results will be filtered with the given platform.
            Defaults to `aiobungie.crates.FireteamPlatform.ANY` which returns all platforms.
        language : `typing.Union[aiobungie.crates.fireteams.FireteamLanguage, str]`
            A locale language to filter the used language in that fireteam.
            Defaults to `aiobungie.crates.FireteamLanguage.ALL`
        date_range : `aiobungie.typedefs.IntAnd[aiobungie.FireteamDate]`
            An integer to filter the date range of the returned fireteams. Defaults to `aiobungie.FireteamDate.ALL`.
        page : `int`
            The page number. By default its `0` which returns all available activities.
        public_only: `bool`
            If set to True, Then only public fireteams will be returned.
        slots_filter : `int`
            Filter the returned fireteams based on available slots. Default is `0`
        """
        fireteams_ = await self.net.request.fetch_avaliable_clan_fireteams(
            access_token,
            self.id,
            activity_type,
            platform=platform,
            language=language,
            date_range=date_range,
            page=page,
            public_only=public_only,
            slots_filter=slots_filter,
        )
        if fireteams_ is None:
            return None

        return fireteams_

    async def fetch_fireteams(
        self,
        access_token: str,
        *,
        include_closed: bool = True,
        platform: typedefs.IntAnd[fireteams.FireteamPlatform],
        language: typing.Union[fireteams.FireteamLanguage, str],
        filtered: bool = True,
        page: int = 0,
    ) -> collections.Sequence[fireteams.AvailableFireteam]:
        """Fetch this clan's available fireteams.

        .. note::
            This method requires OAuth2: ReadGroups scope.

        Parameters
        ----------
        access_token : str
            The bearer access token associated with the bungie account.

        Other Parameters
        ----------------
        include_closed : bool
            If provided and set to True, It will also return closed fireteams.
            If provided and set to False, It will only return public fireteams. Default is True.
        platform : aiobungie.typedefs.IntAnd[aiobungie.crates.fireteams.FireteamPlatform]
            If this is provided. Then the results will be filtered with the given platform.
            Defaults to aiobungie.crates.FireteamPlatform.ANY which returns all platforms.
        language : typing.Union[aiobungie.crates.fireteams.FireteamLanguage, str]
            A locale language to filter the used language in that fireteam.
            Defaults to aiobungie.crates.FireteamLanguage.ALL
        filtered : bool
            If set to True, it will filter by clan. Otherwise not. Default is True.
        page : int
            The page number. By default its 0 which returns all available activities.

        Returns
        -------
        `typing.Optional[collections.Sequence[aiobungie.crates.AvalaibleFireteam]]`
            A sequence of available fireteams objects if exists. else `None` will be returned.
        """
        return await self.net.request.fetch_my_clan_fireteams(
            access_token,
            self.id,
            include_closed=include_closed,
            platform=platform,
            language=language,
            filtered=filtered,
            page=page,
        )

    async def fetch_conversations(self) -> collections.Sequence[ClanConversation]:
        """Fetch the conversations/chat channels of this clan.

        Returns
        `collections.Sequence[aiobungie.crates.ClanConversation]`
            A sequence of the clan chat channels.
        """
        return await self.net.request.fetch_clan_conversations(self.id)

    async def add_optional_conversation(
        self,
        access_token: str,
        /,
        *,
        name: undefined.UndefinedOr[str] = undefined.Undefined,
        security: typing.Literal[0, 1] = 0,
    ) -> None:
        """Add a new chat channel to a group.

        .. note::
            This request requires OAuth2: AdminGroups scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Other parameters
        ----------------
        name: `aiobungie.UndefinedOr[str]`
            The chat name. Default to `UNDEFINED`
        security: `typing.Literal[0, 1]`
            The security level of the chat.

            If provided and set to 0, It will be to `Group` only.
            If provided and set to 1, It will be `Admins` only.
            Default is `0`
        """
        await self.net.request.rest.add_optional_conversation(
            access_token, self.id, name=name, security=security
        )

    async def fetch_members(
        self,
        *,
        name: typing.Optional[str] = None,
        type: enums.MembershipType = enums.MembershipType.NONE,
    ) -> iterators.Iterator[ClanMember]:
        """Fetch the members of the clan.

        Parameters
        ----------
        name : `typing.Optional[str]`
            If provided, Only players matching this name will be returned.
        type: `aiobungie.MembershipType`
            Filters the membership types of the players to return.
            Default is `aiobungie.MembershipType.NONE` which returns all membership types.

        Returns
        --------
        `aiobungie.Iterator[ClanMember]`
            An iterator over the clan members found in this clan.

        Raises
        ------
        `aiobungie.NotFound`
            The clan was not found.
        """
        return await self.net.request.fetch_clan_members(self.id, type=type, name=name)

    async def approve_pending_members(
        self,
        access_token: str,
        /,
        *,
        message: undefined.UndefinedOr[str] = undefined.Undefined,
    ) -> None:
        """Approve all pending users for this clan.

        .. note::
            This request requires OAuth2: AdminGroups scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Other Parameters
        ----------------
        message: `aiobungie.UndefinedOr[str]`
            A message to send with the request. Defaults to `UNDEFINED`
        """
        await self.net.request.rest.approve_all_pending_group_users(
            access_token, self.id, message=message
        )

    async def deny_pending_members(
        self,
        access_token: str,
        /,
        *,
        message: undefined.UndefinedOr[str] = undefined.Undefined,
    ) -> None:
        """Deny all pending users for this clan.

        .. note::
            This request requires OAuth2: AdminGroups scope.

        Parameters
        ----------
        access_token : `str`
            The bearer access token associated with the bungie account.

        Other Parameters
        ----------------
        message: `aiobungie.UndefinedOr[str]`
            A message to send with the request. Defaults to `UNDEFINED`
        """
        await self.net.request.rest.deny_all_pending_group_users(
            access_token, self.id, message=message
        )

    @helpers.unimplemented()
    async def fetch_banned_members(self) -> collections.Sequence[ClanMember]:
        """Fetch members who has been banned from the clan.

        .. warning::
            This method is still not implemented.

        Returns
        --------
        `collections.Sequence[aiobungie.crates.clans.ClanMember]`
            A sequence of clan members or are banned.
        """
        ...

    @helpers.unimplemented()
    async def fetch_pending_members(self) -> collections.Sequence[ClanMember]:
        """Fetch members who are waiting to get accepted.

        .. warning::
            This method is still not implemented.

        Returns
        --------
        `collections.Sequence[aiobungie.crates.clans.ClanMember]`
            A sequence of clan members who are awaiting
            to get accepted to the clan.
        """
        ...

    @helpers.unimplemented()
    async def fetch_invited_members(self) -> collections.Sequence[ClanMember]:
        """Fetch members who has been invited.

        .. warning::
            This method is still not implemented.

        Returns
        --------
        `collections.Sequence[aiobungie.crates.clans.ClanMember]`
            A sequence of members who have been invited.
        """
        ...

    @property
    def url(self) -> str:
        return f"{url.BASE}/en/ClanV2/Index?groupId={self.id}"

    def __int__(self) -> int:
        return self.id

    def __str__(self) -> str:
        return self.name
