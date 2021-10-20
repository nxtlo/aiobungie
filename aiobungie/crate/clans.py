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

"""Basic implementation for a Bungie a clan."""


from __future__ import annotations

__all__ = (
    "Clan",
    "ClanMember",
    "ClanAdmin",
    "ClanFeatures",
    "ClanConversation",
    "ClanBanner",
    "GroupMember",
)

import typing

import attr

from aiobungie import url
from aiobungie.crate import user
from aiobungie.internal import enums
from aiobungie.internal import helpers

if typing.TYPE_CHECKING:
    from datetime import datetime

    from aiobungie.internal import assets
    from aiobungie.internal import traits


@attr.define(kw_only=True, hash=False, weakref_slot=False)
class ClanFeatures:
    """Represents Bungie clan features."""

    max_members: int = attr.field(repr=True)
    """The maximum members the clan can have"""

    max_membership_types: int = attr.field(repr=False)
    """The maximum membership types the clan can have"""

    capabilities: int = attr.field(repr=False)
    """An int that represents the clan's capabilities."""

    membership_types: typing.List[enums.MembershipType] = attr.field(repr=True)
    """The clan's membership types."""

    invite_permissions: bool = attr.field(repr=False)
    """True if the clan has permissions to invite."""

    update_banner_permissions: bool = attr.field(repr=False)
    """True if the clan has permissions to updates its banner."""

    update_culture_permissions: bool = attr.field(repr=False)

    join_level: int = attr.field(repr=True)
    """The clan's join level."""


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class ClanConversation:
    """Represents a clan conversation."""

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    group_id: int = attr.field(repr=True)
    """The clan or group's id."""

    id: int = attr.field(repr=True, hash=True)
    """The conversation's id"""

    chat_enabled: bool = attr.field(repr=True)
    """`True` if the Conversation's chat is enabled."""

    name: helpers.UndefinedOr[str] = attr.field(repr=True)
    """Conversation chat's name."""

    security: int = attr.field(repr=False)
    """Conversation's security level."""

    async def edit(
        self,
        access_token: str,
        /,
        *,
        name: helpers.UndefinedOr[str] = helpers.Undefined,
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
        name: `aiobungie.internal.helpers.UndefinedOr[str]`
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


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class ClanBanner:
    """Representation of information of the clan banner."""

    id: int = attr.field(repr=True)
    """The banner's id."""

    foreground: assets.MaybeImage = attr.field(repr=True)
    """The banner's foreground. This field can be `UNDEFINED` if not found."""

    background: assets.MaybeImage = attr.field(repr=True)
    """The banner's background. This field can be `UNDEFINED` if not found."""

    def __int__(self) -> int:
        return self.id


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class ClanMember(user.UserLike):
    """Represents a Bungie clan member."""

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    id: int = attr.field(repr=True, hash=True)
    """Clan member's id"""

    name: helpers.UndefinedOr[str] = attr.field(repr=True)
    """Clan member's name. This can be `UNDEFINED` if not found."""

    last_seen_name: str = attr.field(repr=True)
    """The clan member's last seen display name"""

    type: enums.MembershipType = attr.field(repr=True)
    """Clan member's membership type."""

    types: typing.Sequence[enums.MembershipType] = attr.field(repr=False)
    """A sequence of the available clan member membership types."""

    icon: assets.MaybeImage = attr.field(repr=False)
    """Clan member's icon"""

    is_public: bool = attr.field(repr=False)
    """`builtins.True` if the clan member is public."""

    group_id: int = attr.field(repr=True)
    """The member's group id."""

    is_online: bool = attr.field(repr=False, default=None)
    """True if the clan member is online or not."""

    last_online: datetime = attr.field(repr=False, default=None)
    """The date of the clan member's last online in UTC time zone."""

    joined_at: datetime = attr.field(repr=False, default=None)
    """The clan member's join date in UTC time zone."""

    code: helpers.NoneOr[int] = attr.field(repr=True)
    """The clan member's bungie display name code
    This is new and was added in Season of the lost update
    """

    bungie: user.PartialBungieUser = attr.field(repr=True)
    """The clan member's bungie partial net user.

    .. note:: This only returns a partial bungie net user.
    You can fetch the fully implemented user using `aiobungie.crate.PartialBungieUser.fetch_self()` method.
    """

    @property
    def unique_name(self) -> str:
        """The clan member's unique name which includes their unique code."""
        return f"{self.name}#{self.code}"

    @property
    def link(self) -> str:
        """Clan member's profile link."""
        return f"{url.BASE}/en/Profile/index/{int(self.type)}/{self.id}"

    # These are not implemented yet
    # Since they requires OAuth2.

    async def ban(
        self,
        access_token: str,
        /,
        *,
        comment: helpers.UndefinedOr[str] = helpers.Undefined,
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
        comment: `aiobungie.internal.helpers.UndefinedOr[str]`
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
        """Unbans this member from the clan.

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
        `aiobungie.crate.clan.Clan`
            The clan that represents the kicked member.
        """
        return await self.net.request.kick_clan_member(
            access_token,
            group_id=self.group_id,
            membership_id=self.id,
            membership_type=self.type,
        )


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class GroupMember:
    """Represents information about joined groups/clans for a member."""

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    inactive_memberships: helpers.NoneOr[dict[int, bool]] = attr.field(repr=False)
    """The member's inactive memberships if provided. This will be `None` if not provided."""

    member_type: enums.ClanMemberType = attr.field(repr=True)
    """The member's member type."""

    is_online: bool = attr.field(repr=False)
    """Whether the member is online or not."""

    last_online: datetime = attr.field(repr=False)
    """An awre UTC datetime of the member's last online status."""

    group_id: int = attr.field(repr=True)
    """The group id of this member."""

    join_date: datetime = attr.field(repr=False)
    """An awre UTC datetime of the member's join date."""

    member: user.DestinyUser = attr.field(repr=True)
    """The member's destiny object that represents the group member."""

    group: Clan = attr.field(repr=True)
    """The member's group/clan object that represents the group member."""

    async def fetch_self_clan(self) -> Clan:
        """Fetch an up-todate clan/group object of the current group.

        Returns
        -------
        `Clan`
            The clan object.
        """
        clan = await self.net.request.fetch_clan_from_id(self.group_id)
        assert isinstance(clan, Clan)
        return clan

    def __int__(self) -> int:
        return self.group_id


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class ClanAdmin(user.UserLike):
    """Represents a clan admin."""

    member_type: enums.ClanMemberType = attr.field(repr=True)
    """The clan admin's member type.
    This can be Admin or owner or any other type.
    """

    net: traits.Netrunner = attr.field(repr=False)
    """A network state used for making external requests."""

    total_admins: int = attr.field(repr=True)
    """The total count of the clan admins."""

    id: int = attr.field(repr=True, hash=True)
    """Clan admin's id"""

    name: helpers.UndefinedOr[str] = attr.field(repr=True)
    """Clan admin's name. This can be `UNDEFINED` if not found."""

    last_seen_name: str = attr.field(repr=False)
    """The clan admin's last seen display name"""

    type: enums.MembershipType = attr.field(repr=True)
    """Clan admin's membership type."""

    types: typing.Sequence[enums.MembershipType] = attr.field(repr=False)
    """A sequence of the available clan admin membership types."""

    icon: assets.MaybeImage = attr.field(repr=False)
    """Clan admin's icon"""

    is_public: bool = attr.field(repr=False)
    """`builtins.True` if the clan admin is public."""

    group_id: int = attr.field(repr=True)
    """The admin's group or clan id."""

    is_online: bool = attr.field(repr=False, default=None)
    """True if the clan admin is online or not."""

    last_online: datetime = attr.field(repr=False, default=None)
    """The date of the clan admin's last online in UTC time zone."""

    joined_at: datetime = attr.field(repr=False, default=None)
    """The clan admin's join date in UTC time zone."""

    code: helpers.NoneOr[int] = attr.field(repr=True)
    """The clan admin's bungie display name code
    This is new and was added in Season of the lost update
    """

    bungie: user.PartialBungieUser = attr.field(repr=True)
    """The clan admin's bungie partial net user.

    .. note:: This only returns a partial bungie net user.
    You can fetch the fully implemented user using
    `aiobungie.crate.PartialBungieUser.fetch_self()` method.
    """

    async def fetch_clan(self) -> Clan:
        """Fetch the clan that represents the clan admins.

        Returns
        -------
        `Clan`
            The clan admins clan.
        """
        clan = await self.net.request.fetch_clan_from_id(self.group_id)
        assert isinstance(clan, Clan)
        return clan

    @property
    def unique_name(self) -> str:
        """The admin's unique name which includes their unique code."""
        return f"{self.name}#{self.code}"

    @property
    def link(self) -> str:
        """Clan member's profile link."""
        return f"{url.BASE}/en/Profile/index/{int(self.type)}/{self.id}"


@attr.define(hash=False, kw_only=True, weakref_slot=False)
class Clan:
    """Represents a Bungie clan."""

    net: traits.Netrunner = attr.field(repr=False, eq=False, hash=False)
    """A network state used for making external requests."""

    id: int = attr.field(hash=True, repr=True, eq=True)
    """The clan id"""

    type: enums.GroupType = attr.field(repr=True)
    """The clan type."""

    name: str = attr.field(repr=True)
    """The clan's name"""

    created_at: datetime = attr.field(repr=True)
    """Clan's creation date time in UTC."""

    member_count: int = attr.field(repr=True)
    """Clan's member count."""

    motto: str = attr.field(repr=False, eq=False)
    """Clan's motto."""

    is_public: bool = attr.field(repr=False, eq=False)
    """Clan's privacy status."""

    banner: assets.MaybeImage = attr.field(repr=False)
    """Clan's banner"""

    avatar: assets.MaybeImage = attr.field(repr=False)
    """Clan's avatar"""

    about: str = attr.field(repr=False, eq=False)
    """Clan's about title."""

    tags: typing.List[str] = attr.field(repr=False)
    """A list of the clan's tags."""

    owner: helpers.NoneOr[ClanMember] = attr.field(repr=True)
    """The clan owner. This field could be `None` if not found."""

    features: ClanFeatures = attr.field(repr=False, hash=False, eq=False)
    """The clan features."""

    async def edit_options(
        self,
        access_token: str,
        /,
        *,
        invite_permissions_override: helpers.NoneOr[bool] = None,
        update_culture_permissionOverride: helpers.NoneOr[bool] = None,
        host_guided_game_permission_override: helpers.NoneOr[
            typing.Literal[0, 1, 2]
        ] = None,
        update_banner_permission_override: helpers.NoneOr[bool] = None,
        join_level: helpers.NoneOr[helpers.IntAnd[enums.ClanMemberType]] = None,
    ) -> None:
        """Edit the clan options.

        Notes
        -----
        * This request requires OAuth2: oauth2: `AdminGroups` scope.
        * All arguments will default to `None` if not provided. This does not include `access_token` and `group_id`

        Parameters
        ----------
        access_token : `builtins.str`
            The bearer access token associated with the bungie account.

        Other Parameters
        ----------------
        invite_permissions_override : `aiobungie.internal.helpers.NoneOr[bool]`
            Minimum Member Level allowed to invite new members to group
            Always Allowed: Founder, Acting Founder
            True means admins have this power, false means they don't
            Default is False for clans, True for groups.
        update_culture_permissionOverride : `aiobungie.internal.helpers.NoneOr[bool]`
            Minimum Member Level allowed to update group culture
            Always Allowed: Founder, Acting Founder
            True means admins have this power, false means they don't
            Default is False for clans, True for groups.
        host_guided_game_permission_override : `aiobungie.internal.helpers.NoneOr[typing.Literal[0, 1, 2]]`
            Minimum Member Level allowed to host guided games
            Always Allowed: Founder, Acting Founder, Admin
            Allowed Overrides: `0` -> None, `1` -> Beginner `2` -> Member.
            Default is Member for clans, None for groups, although this means nothing for groups.
        update_banner_permission_override : `aiobungie.internal.helpers.NoneOr[bool]`
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
        name : `aiobungie.internal.helpers.NoneOr[str]`
            The name to edit the clan with.
        about : `aiobungie.internal.helpers.NoneOr[str]`
            The about section to edit the clan with.
        motto : `aiobungie.internal.helpers.NoneOr[str]`
            The motto section to edit the clan with.
        theme : `aiobungie.internal.helpers.NoneOr[str]`
            The theme name to edit the clan with.
        tags : `aiobungie.internal.helpers.NoneOr[typing.Sequence[str]]`
            A sequence of strings to replace the clan tags with.
        is_public : `aiobungie.internal.helpers.NoneOr[bool]`
            If provided and set to `True`, The clan will set to private.
            If provided and set to `False`, The clan will set to public whether it was or not.
        locale : `aiobungie.internal.helpers.NoneOr[str]`
            The locale section to edit the clan with.
        avatar_image_index : `aiobungie.internal.helpers.NoneOr[int]`
            The clan avatar image index to edit the clan with.
        membership_option : `aiobungie.internal.helpers.NoneOr[aiobungie.internal.helpers.IntAnd[aiobungie.MembershipOption]]` # noqa: E501 # Line too long
            The clan membership option to edit it with.
        allow_chat : `aiobungie.internal.helpers.NoneOr[bool]`
            If provided and set to `True`, The clan members will be allowed to chat.
            If provided and set to `False`, The clan members will not be allowed to chat.
        chat_security : `aiobungie.internal.helpers.NoneOr[typing.Literal[0, 1]]`
            If provided and set to `0`, The clan chat security will be edited to `Group` only.
            If provided and set to `1`, The clan chat security will be edited to `Admin` only.
        call_sign : `aiobungie.internal.helpers.NoneOr[str]`
            The clan call sign to edit it with.
        homepage : `aiobungie.internal.helpers.NoneOr[typing.Literal[0, 1, 2]]`
            If provided and set to `0`, The clan chat homepage will be edited to `Wall`.
            If provided and set to `1`, The clan chat homepage will be edited to `Forum`.
            If provided and set to `0`, The clan chat homepage will be edited to `AllianceForum`.
        enable_invite_messaging_for_admins : `aiobungie.internal.helpers.NoneOr[bool]`
            ???
        default_publicity : `aiobungie.internal.helpers.NoneOr[typing.Literal[0, 1, 2]]`
            If provided and set to `0`, The clan chat publicity will be edited to `Public`.
            If provided and set to `1`, The clan chat publicity will be edited to `Alliance`.
            If provided and set to `2`, The clan chat publicity will be edited to `Private`.
        is_public_topic_admin : `aiobungie.internal.helpers.NoneOr[bool]`
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

    async def fetch_conversations(self) -> typing.Sequence[ClanConversation]:
        """Fetch the conversations/chat channels of this clan.

        Returns
        `typing.Sequence[aiobungie.crate.ClanConversation]`
            A sequence of the clan chat channels.
        """
        return await self.net.request.fetch_clan_conversations(self.id)

    async def add_optional_conversation(
        self,
        access_token: str,
        /,
        *,
        name: helpers.UndefinedOr[str] = helpers.Undefined,
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
        name: `aiobungie.internal.helpers.UndefinedOr[str]`
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

    async def fetch_member(
        self, name: str, type: enums.MembershipType = enums.MembershipType.NONE, /
    ) -> ClanMember:
        """Fetch a specific clan member by their name and membership type.

        if the memberhship type is None we will
        try to return the first member matches the name.
        its also better to leave this parameter on None
        since usually only one player has this name.

        Parameters
        ----------
        name: `builtins.str`
            The clan member name.
        type: `aiobungie.MembershipType`
            The member's membership type. Default is 0
            which returns any member matches the name.

        Returns
        --------
        `ClanMember`

        Raises
        ------
        `aiobungie.ClanNotFound`
            The clan was not found.

        `aiobungie.NotFound`
            The member was not found
        """
        member = await self.net.request.fetch_clan_member(self.id, name, type)
        assert isinstance(member, ClanMember)
        return member

    async def fetch_members(
        self, type: enums.MembershipType = enums.MembershipType.NONE, /
    ) -> typing.Sequence[ClanMember]:
        """Fetch the members of the clan.

        if the memberhship type is None it will
        All membership types.

        Parameters
        ----------
        type: `aiobungie.MembershipType`
            Filters the membership types to return.
            Default is `aiobungie.MembershipType.NONE` which returns all membership types.

        Returns
        --------
        `typing.Sequence[ClanMember]`
            A sequence of the clan members found in this clan.

        Raises
        ------
        `aiobungie.ClanNotFound`
            The clan was not found.
        """
        return await self.net.request.fetch_clan_members(self.id, type)

    async def approve_pending_members(
        self,
        access_token: str,
        /,
        *,
        message: helpers.UndefinedOr[str] = helpers.Undefined,
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
        message: `aiobungie.internal.helpers.Undefinedor[str]`
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
        message: helpers.UndefinedOr[str] = helpers.Undefined,
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
        message: `aiobungie.internal.helpers.Undefinedor[str]`
            A message to send with the request. Defaults to `UNDEFINED`
        """
        await self.net.request.rest.deny_all_pending_group_users(
            access_token, self.id, message=message
        )

    # These ones is not implemented since it
    # requires OAUth2

    async def fetch_banned_members(self) -> typing.Sequence[ClanMember]:
        """Fetch members who has been banned from the clan.

        .. warning::
            This method is still not implemented.

        Returns
        --------
        `typing.Sequence[aiobungie.crate.clans.ClanMember]`
            A sequence of clan members or are banned.
        """
        raise NotImplementedError

    async def fetch_pending_members(self) -> typing.Sequence[ClanMember]:
        """Fetch members who are waiting to get accepted.

        .. warning::
            This method is still not implemented.

        Returns
        --------
        `typing.Sequence[aiobungie.crate.clans.ClanMember]`
            A sequence of clan members who are awaiting
            to get accepted to the clan.
        """
        raise NotImplementedError

    async def fetch_invited_members(self) -> typing.Sequence[ClanMember]:
        """Fetch members who has been invited.

        .. warning::
            This method is still not implemented.

        Returns
        --------
        `typing.Sequence[aiobungie.crate.clans.ClanMember]`
            A sequence of members who have been invited.
        """
        raise NotImplementedError

    @property
    def url(self) -> str:
        return f"{url.BASE}/en/ClanV2/Index?groupId={self.id}"

    def __int__(self) -> int:
        return self.id

    def __str__(self) -> str:
        return self.name
