# MIT License
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

"""Marshaller factory for incoming json payloads."""

from __future__ import annotations

__all__ = ("Factory",)

import logging
import typing

from aiobungie import error
from aiobungie.crate import activity
from aiobungie.crate import application as app
from aiobungie.crate import character
from aiobungie.crate import clans
from aiobungie.crate import entity
from aiobungie.crate import friends
from aiobungie.crate import milestones
from aiobungie.crate import profile
from aiobungie.crate import user
from aiobungie.internal import enums
from aiobungie.internal import time
from aiobungie.internal.assets import Image
from aiobungie.internal.helpers import NoneOr
from aiobungie.internal.helpers import Undefined
from aiobungie.internal.helpers import Unknown
from aiobungie.internal.helpers import just

if typing.TYPE_CHECKING:
    import datetime

    from aiobungie.internal import traits
    from aiobungie.internal.helpers import JsonArray
    from aiobungie.internal.helpers import JsonObject
    from aiobungie.internal.helpers import UndefinedOr

_LOG: typing.Final[logging.Logger] = logging.getLogger(__name__)


class Factory:
    """The base Deserialization factory class for all aiobungie objects."""

    # This is kinda inspired by hikari's entity factory :p.

    __slots__: typing.Sequence[str] = ("_net",)

    def __init__(self, net: traits.Netrunner) -> None:
        self._net = net

    def deserialize_bungie_user(self, data: JsonObject) -> user.BungieUser:
        return user.BungieUser(
            id=int(data["membershipId"]),
            created_at=time.clean_date(data["firstAccess"]),
            name=data.get("cachedBungieGlobalDisplayName", Undefined),
            is_deleted=data["isDeleted"],
            about=data["about"],
            updated_at=time.clean_date(data["lastUpdate"]),
            psn_name=data.get("psnDisplayName", None),
            stadia_name=data.get("stadiaDisplayName", None),
            steam_name=data.get("steamDisplayName", None),
            twitch_name=data.get("twitchDisplayName", None),
            blizzard_name=data.get("blizzardDisplayName", None),
            status=data["statusText"],
            locale=data["locale"],
            picture=Image(path=str(data["profilePicturePath"])),
            code=data.get("cachedBungieGlobalDisplayNameCode", None),
            unique_name=data.get("uniqueName", None),
            theme_id=int(data["profileTheme"]),
            show_activity=bool(data["showActivity"]),
            theme_name=data["profileThemeName"],
            display_title=data["userTitleDisplay"],
        )

    # Deserializer for a `bungieNetUserInfo`
    def deserialize_partial_bungie_user(
        self, payload: JsonObject, *, noeq: bool = False
    ) -> user.PartialBungieUser:
        if noeq is True:
            bungie_info = payload
        else:
            bungie_info = payload["bungieNetUserInfo"]
        return user.PartialBungieUser(
            net=self._net,
            name=bungie_info.get("displayName", Undefined),
            id=int(bungie_info["membershipId"]),
            crossave_override=enums.MembershipType(bungie_info["crossSaveOverride"]),
            is_public=bungie_info["isPublic"],
            icon=Image(bungie_info.get("iconPath", Image.partial())),
            type=enums.MembershipType(bungie_info["membershipType"]),
        )

    # Deserializer for a `destinyUserInfo`
    def deserialize_destiny_user(
        self, payload: JsonObject, *, noeq: bool = False
    ) -> user.DestinyUser:
        if noeq is True:
            user_info = payload
        else:
            user_info = payload["destinyUserInfo"]

        memberships = []
        for m_ship in user_info["applicableMembershipTypes"]:
            memberships.append(enums.MembershipType(m_ship))

        if (raw_name := user_info["bungieGlobalDisplayName"]) == Unknown:
            name = Undefined
        else:
            name = raw_name

        return user.DestinyUser(
            net=self._net,
            id=int(user_info["membershipId"]),
            name=name,
            code=user_info.get("bungieGlobalDisplayNameCode", None),
            last_seen_name=user_info.get(
                "LastSeenDisplayName", user_info["displayName"]
            ),
            type=enums.MembershipType(user_info["membershipType"]),
            is_public=user_info["isPublic"],
            crossave_override=enums.MembershipType(user_info["crossSaveOverride"]),
            icon=Image(user_info.get("iconPath", Image.partial())),
            types=memberships,
        )

    # Deserialize a list of `destinyUserInfo`
    def deserialize_destiny_members(
        self, data: typing.Union[JsonObject, JsonArray], *, bound: bool = False
    ) -> typing.Sequence[user.DestinyUser]:
        xbox: int = 0
        psn: int = 1
        steam: int = 2
        stadia: int = 3

        # In order to bind this method between deserializing
        # other objects we have to check if the data was
        # a json object or a json array of objects.

        raw_members: typing.Union[JsonArray, JsonObject, dict[int, typing.Any]] = data

        if bound:
            members_ = raw_members  # type: ignore

        elif (
            isinstance(data, dict)
            and (  # noqa: W503 LINE BREAK
                raw_members := data.get("destinyMemberships", [])
            )
            is not None
        ):
            members_: dict[int, typing.Any] = raw_members  # type: ignore

        stadia_obj: NoneOr[user.DestinyUser] = None  # type: ignore[name-defined]
        try:
            stadia_member = members_[stadia]  # type: ignore[index]
        except (KeyError, IndexError):
            pass
        else:
            stadia_obj = self.deserialize_destiny_user(stadia_member, noeq=True)

        xbox_obj: NoneOr[user.DestinyUser] = None  # type: ignore[name-defined]
        try:
            xbox_member = members_[xbox]  # type: ignore[index]
        except (KeyError, IndexError):
            pass
        else:
            xbox_obj = self.deserialize_destiny_user(xbox_member, noeq=True)

        steam_obj: NoneOr[user.DestinyUser] = None  # type: ignore[name-defined]
        try:
            steam_member = members_[steam]  # type: ignore[index]
        except (KeyError, IndexError):
            pass
        else:
            steam_obj = self.deserialize_destiny_user(steam_member, noeq=True)

        psn_obj: NoneOr[user.DestinyUser] = None  # type: ignore[name-defined]
        try:
            psn_member = members_[psn]  # type: ignore[index]
        except (KeyError, IndexError):
            pass
        else:
            psn_obj = self.deserialize_destiny_user(psn_member, noeq=True)

        vec: list[user.DestinyUser] = []
        objs = [xbox_obj, psn_obj, steam_obj, stadia_obj]
        # No point of returning NoneType objects.
        for obj in objs:
            if obj is None:
                continue
            vec.append(obj)
        return vec

    def deserialize_user(self, data: JsonObject) -> user.User:
        return user.User(
            bungie=self.deserialize_bungie_user(data["bungieNetUser"]),
            destiny=self.deserialize_destiny_members(data),
        )

    def deseialize_found_users(
        self, payload: JsonObject
    ) -> typing.Sequence[user.DestinyUser]:
        result = payload["searchResults"]
        if result is None:
            raise error.NotFound("User not found.")

        vec: list[user.DestinyUser] = []
        for player in result:
            # TODO: Figuire out how to merge this with DestinyUser objects.
            #  name: UndefinedOr[str] = player.get("bungieGlobalDisplayName", Undefined)
            #  code: NoneOr[int] = player.get("bungieGlobalDisplayNameCode", None)
            #  bungie_id: UndefinedOr[int] = player.get('bungieNetMembershipId', Undefined)
            for mship in self.deserialize_destiny_members(player):
                vec.append(mship)
        return vec

    @staticmethod
    def set_themese_attrs(payload: JsonArray, /) -> typing.Collection[user.UserThemes]:
        if isinstance(payload, list):
            if payload is None:
                raise ValueError("No themes found.")

            theme_map: dict[int, user.UserThemes] = {}
            theme_ids: list[int] = just(payload, "userThemeId")
            theme_names: list[NoneOr[str]] = just(payload, "userThemeName")
            theme_descriptions: list[NoneOr[str]] = just(
                payload, "userThemeDescription"
            )

            for t_id, t_name, t_desc in zip(theme_ids, theme_names, theme_descriptions):
                theme_map[t_id] = user.UserThemes(
                    id=int(t_id),
                    name=t_name or Undefined,
                    description=t_desc or Undefined,
                )
        return theme_map.values()

    def deserialize_user_themes(
        self, payload: JsonArray
    ) -> typing.Sequence[user.UserThemes]:
        return list(self.set_themese_attrs(payload))

    def deserialize_player(
        self, payload: JsonArray, /
    ) -> typing.Sequence[user.DestinyUser]:
        if payload is None:
            raise error.PlayerNotFound("Player was not found.") from None

        return self.deserialize_destiny_members(payload, bound=True)

    def deseialize_clan_owner(self, data: JsonObject) -> clans.ClanMember:
        joined_at = data["joinDate"]
        last_online = time.from_timestamp(int(data["lastOnlineStatusChange"]))
        clan_id = data["groupId"]
        destiny_user = self.deserialize_destiny_user(data)
        bungie_user = self.deserialize_partial_bungie_user(data)

        return clans.ClanMember(
            net=self._net,
            last_seen_name=destiny_user.last_seen_name,
            id=destiny_user.id,
            name=destiny_user.name,
            icon=destiny_user.icon,
            last_online=last_online,
            group_id=int(clan_id),
            joined_at=time.clean_date(joined_at),
            types=destiny_user.types,
            is_public=destiny_user.is_public,
            type=destiny_user.type,
            code=destiny_user.code,
            bungie=bungie_user,
        )

    def deserialize_clan(
        self, payload: JsonObject, *, bound: bool = False
    ) -> clans.Clan:
        # To bind this function between this and group for member.
        if bound is True:
            data = payload
        else:
            data = payload["detail"]

        id = data["groupId"]
        name = data["name"]
        created_at = data["creationDate"]
        member_count = data["memberCount"]
        about = data["about"]
        motto = data["motto"]
        is_public = data["isPublic"]
        banner = Image(str(data["bannerPath"]))
        avatar = Image(str(data["avatarPath"]))
        tags = data["tags"]
        features = data["features"]
        type = data["groupType"]

        features_obj = clans.ClanFeatures(
            max_members=features["maximumMembers"],
            max_membership_types=features["maximumMembershipsOfGroupType"],
            capabilities=features["capabilities"],
            membership_types=features["membershipTypes"],
            invite_permissions=features["invitePermissionOverride"],
            update_banner_permissions=features["updateBannerPermissionOverride"],
            update_culture_permissions=features["updateCulturePermissionOverride"],
            join_level=features["joinLevel"],
        )

        founder: NoneOr[clans.ClanMember] = None
        if (raw_founder := payload.get("founder")) is not None:
            if bound is False:
                founder = self.deseialize_clan_owner(raw_founder)

        return clans.Clan(
            net=self._net,
            id=int(id),
            name=name,
            type=enums.GroupType(type),
            created_at=time.clean_date(created_at),
            member_count=member_count,
            motto=motto,
            about=about,
            is_public=is_public,
            banner=banner,
            avatar=avatar,
            tags=tags,
            features=features_obj,
            owner=founder,
        )

    def deserialize_group_member(
        self, payload: JsonObject
    ) -> NoneOr[clans.GroupMember]:
        inactive_memberships = payload.get("areAllMembershipsInactive", None)
        if (raw_results := payload.get("results")) is not None:
            try:
                results = raw_results[0]
            except IndexError:
                return None
            member_results = results["member"]
            last_online: datetime.datetime = time.from_timestamp(
                int(member_results["lastOnlineStatusChange"])
            )
            join_date_fmt: datetime.datetime = time.clean_date(
                member_results["joinDate"]
            )
            member_type: enums.ClanMemberType = enums.ClanMemberType(
                member_results["memberType"]
            )
            is_online: bool = member_results["isOnline"]
            group_id: int = member_results["groupId"]
            destiny_member = self.deserialize_destiny_user(member_results)
            member_obj = clans.GroupMember(
                net=self._net,
                join_date=join_date_fmt,
                group_id=int(group_id),
                member_type=member_type,
                is_online=is_online,
                last_online=last_online,
                inactive_memberships=inactive_memberships,
                member=destiny_member,
                group=self.deserialize_clan(results["group"], bound=True),
            )
            return member_obj
        return None

    def deserialize_clan_admins(
        self, payload: JsonObject
    ) -> typing.Sequence[clans.ClanAdmin]:
        builder = []
        member_types = just(payload["results"], "memberType")
        for member_type in zip(member_types):
            m_type = enums.ClanMemberType(*member_type)

        # Since this requires more attributes
        # We have to do it in two ways.
        obj = self.deserialize_clan_members(payload)
        for member in obj:
            clan_admin = clans.ClanAdmin(
                net=self._net,
                member_type=m_type,
                types=member.types,
                id=member.id,
                name=member.name,
                last_seen_name=member.last_seen_name,
                is_public=member.is_public,
                icon=member.icon,
                code=member.code,
                total_admins=payload["totalResults"],
                type=member.type,
                group_id=member.group_id,
                bungie=member.bungie,
            )
            builder.append(clan_admin)
        return builder

    def deserialize_clan_member(self, data: JsonObject, /) -> clans.ClanMember:

        if (payload := data["results"]) is not None:
            try:
                attrs = payload[0]
                payload = payload[0]["destinyUserInfo"]
            except (KeyError, IndexError):
                raise error.NotFound("Clan member not found.") from None

            destiny_member = self.deserialize_destiny_user(payload, noeq=True)
            last_online: datetime.datetime = time.from_timestamp(
                int(attrs["lastOnlineStatusChange"])
            )
            is_online: bool = attrs["isOnline"]
            group_id: int = attrs["groupId"]
            joined_at: datetime.datetime = time.clean_date(str(attrs["joinDate"]))
            bungie_user = self.deserialize_partial_bungie_user(payload, noeq=True)

        return clans.ClanMember(
            net=self._net,
            group_id=int(group_id),
            is_online=is_online,
            last_online=last_online,
            id=destiny_member.id,
            joined_at=joined_at,
            name=destiny_member.name,
            type=destiny_member.type,
            is_public=destiny_member.is_public,
            icon=destiny_member.icon,
            code=destiny_member.code,
            types=destiny_member.types,
            last_seen_name=destiny_member.last_seen_name,
            bungie=bungie_user,
        )

    def deserialize_clan_convos(
        self, payload: JsonArray
    ) -> typing.Sequence[clans.ClanConversation]:
        map = {}
        vec = []
        if payload is not None:
            for convo in payload:
                for k, v in convo.items():
                    map[k] = v

                if (name := map["chatName"]) == Unknown:
                    name = Undefined

                convo_obj = clans.ClanConversation(
                    net=self._net,
                    group_id=int(map["groupId"]),
                    id=int(map["conversationId"]),
                    chat_enabled=map["chatEnabled"],
                    name=name,
                    security=map["chatSecurity"],
                )
                vec.append(convo_obj)
        return vec

    def deserialize_clan_members(
        self, data: JsonObject, /
    ) -> typing.Sequence[clans.ClanMember]:
        members_vec: list[clans.ClanMember] = []
        if (payload := data["results"]) is not None:

            # raw_is_on: list[bool] = just(payload, "isOnline")
            # raw_last_sts: list[int] = just(payload, "lastOnlineStatusChange")
            # raw_join_date: list[str] = just(payload, "joinDate")
            # metadata = map(
            #     lambda *args: args, raw_is_on, raw_last_sts, raw_join_date
            # )
            # for is_online, last_online, join_date in metadata:
            #     last_online_fmt: datetime.datetime = time.from_timestamp(
            #         int(last_online)
            #     )
            #     join_date_fmt: datetime.datetime = time.clean_date(join_date)

            group_id: list[int] = just(payload, "groupId")

            for memberships in payload:
                wrap_destiny = lambda m: m["destinyUserInfo"]  # noqa: E731 Lambdas
                wrap_bungie = None

                try:
                    wrap_bungie = lambda m: m["bungieNetUserInfo"]  # noqa: E731 Lambdas
                    bungie_user = self.deserialize_partial_bungie_user(
                        wrap_bungie(memberships), noeq=True
                    )
                except KeyError:
                    continue

                member = self.deserialize_destiny_user(
                    wrap_destiny(memberships), noeq=True
                )

                member_obj = clans.ClanMember(
                    net=self._net,
                    id=member.id,
                    name=member.name,
                    type=member.type,
                    icon=member.icon,
                    is_public=member.is_public,
                    code=member.code,
                    types=member.types,
                    last_seen_name=member.last_seen_name,
                    group_id=group_id[0],
                    bungie=bungie_user,
                )
                members_vec.append(member_obj)
        return members_vec

    def deserialize_app_owner(self, payload: JsonObject) -> app.ApplicationOwner:
        return app.ApplicationOwner(
            net=self._net,
            name=payload.get("bungieGlobalDisplayName", Undefined),
            id=int(payload["membershipId"]),
            type=enums.MembershipType(payload["membershipType"]),
            icon=Image(str(payload["iconPath"])),
            is_public=payload["isPublic"],
            code=payload.get("bungieGlobalDisplayNameCode", None),
        )

    def deserialize_app(self, payload: JsonObject) -> app.Application:
        return app.Application(
            id=int(payload["applicationId"]),
            name=payload["name"],
            link=payload["link"],
            status=payload["status"],
            redirect_url=payload.get("redirectUrl", None),
            created_at=time.clean_date(str(payload["creationDate"])),
            published_at=time.clean_date(str(payload["firstPublished"])),
            owner=self.deserialize_app_owner(payload["team"][0]["user"]),  # type: ignore
            scope=payload.get("scope", Undefined),
        )

    def deserialize_character(
        self, payload: JsonObject, *, chartype: enums.Class
    ) -> character.Character:

        try:
            payload = [c for c in payload["characters"]["data"].values()]  # type: ignore
        except TypeError:
            raise error.CharacterError(
                "One of these caused this error, "
                "The membership type is invalid, "
                "the character's id or the member's id are wrong "
                "Please recheck those and retry again."
            ) from None

        try:
            payload = payload[int(chartype)]  # type: ignore
        except IndexError:
            _LOG.warning(
                f" Player doesn't have have a {str(chartype)} character. Will return the first character."
            )
            payload = payload[0]  # type: ignore

        total_time = time.format_played(int(payload["minutesPlayedTotal"]), suffix=True)

        return character.Character(
            net=self._net,
            id=int(payload["characterId"]),
            gender=enums.Gender(payload["genderType"]),
            race=enums.Race(payload["raceType"]),
            class_type=enums.Class(payload["classType"]),
            emblem=Image(str(payload["emblemBackgroundPath"])),
            emblem_icon=Image(str(payload["emblemPath"])),
            emblem_hash=int(payload["emblemHash"]),
            last_played=payload["dateLastPlayed"],
            total_played_time=total_time,
            member_id=int(payload["membershipId"]),
            member_type=enums.MembershipType(payload["membershipType"]),
            level=payload["baseCharacterLevel"],
            title_hash=payload.get("titleRecordHash", None),
            light=payload["light"],
            stats=payload["stats"],
        )

    def deserialize_profile(self, payload: JsonObject, /) -> profile.Profile:

        payload = payload["profile"]["data"]
        id = int(payload["userInfo"]["membershipId"])
        name = payload["userInfo"]["displayName"]
        is_public = payload["userInfo"]["isPublic"]
        type = enums.MembershipType(payload["userInfo"]["membershipType"])
        last_played = time.clean_date(str(payload["dateLastPlayed"]))
        character_ids = payload["characterIds"]
        power_cap = payload["currentSeasonRewardPowerCap"]

        return profile.Profile(
            id=int(id),
            name=name,
            is_public=is_public,
            type=type,
            last_played=last_played,
            character_ids=character_ids,
            power_cap=power_cap,
            net=self._net,
        )

    def deserialize_inventory_entity(
        self, payload: JsonObject, /
    ) -> entity.InventoryEntity:
        try:
            # All Bungie entities has a display propetie
            # if we don't find it means the entity was not found.
            props: JsonObject = payload["displayProperties"]
        except KeyError:
            raise error.NotFound("The entity inventory item hash is invalid") from None

        # Some entities have an inventory which
        # Includes its hash types.
        # Most entities has this
        # and for some it doesn't exists

        if (raw_inventory := payload.get("inventory", {})) is not None:
            inventory: JsonObject = raw_inventory

        # Entity tier type. Most entities have a tier
        # and some doesn't exists so we have to check.

        bucket_type: int = inventory.get("bucketTypeHash", 0)

        tier: enums.ItemTier = enums.ItemTier(
            int(inventory.get("tierTypeHash", enums.ItemTier.NONE))
        )

        tier_name: str = inventory.get("tierTypeName", None)

        if (name := props.get("name", Unknown)) == Unknown:
            name = Undefined

        if (type_name := payload.get("itemTypeDisplayName", Unknown)) == Unknown:
            type_name = Undefined

        if (description := props.get("description", Unknown)) == Unknown:
            description = Undefined

        if (about := payload.get("flavorText", Unknown)) == Unknown:
            about = Undefined

        if (raw_icon := props.get("icon", Image.partial())) is not None:
            icon: Image = Image(str(raw_icon))

        if (raw_watermark := payload.get("iconWatermark", Image.partial())) is not None:
            water_mark: Image = Image(str(raw_watermark))

        if (raw_banner := payload.get("screenshot", Image.partial())) is not None:
            banner = Image(str(raw_banner))

        damage: UndefinedOr[enums.DamageType] = Undefined
        if (raw_damage := payload.get("defaultDamageTypeHash")) is not None:
            damage = enums.DamageType(raw_damage)

        # Ignoring those two so mypy doesn't cry.
        summary_hash: int = 0
        if (raw_summary_hash := payload.get("summaryItemHash")) is not None:
            summary_hash: int = int(raw_summary_hash)  # type: ignore

        if (raw_stats := payload.get("stats", {})) is not None:
            stats: JsonObject = raw_stats

        block = enums.AmmoType.NONE
        if (ammo := payload.get("equippingBlock")) is not None:
            block: enums.AmmoType = enums.AmmoType(ammo["ammoType"])  # type: ignore

        item_class: enums.Class = enums.Class(
            payload.get("classType", enums.Class.UNKNOWN)
        )

        return entity.InventoryEntity(
            net=self._net,
            name=name,
            description=description,
            hash=payload["hash"],
            index=payload["index"],
            icon=icon,
            has_icon=props["hasIcon"],
            water_mark=water_mark,
            banner=banner,
            about=about,
            type=payload.get("itemType", Undefined),
            bucket_type=bucket_type,
            tier=tier,
            tier_name=tier_name,
            type_name=type_name,
            sub_type=payload.get("itemSubType", Undefined),
            item_class=item_class,
            damage=damage,
            summary_hash=summary_hash,
            is_equippable=payload.get("equippable", False),
            stats=stats,
            ammo_type=block,
            lore_hash=payload.get("loreHash", None),
        )

    def deserialize_activity(
        self, payload: JsonObject, /, *, limit: typing.Optional[int] = 1
    ) -> activity.Activity:

        if (activs := payload.get("activities")) is not None:
            activs = dict(*activs)
            period: datetime.datetime = time.clean_date(str(activs["period"]))

            if (details := activs.get("activityDetails")) is not None:
                id: int = details["referenceId"]
                instance_id: int = int(details["instanceId"])

                if game_mode := details.get("mode"):
                    mode: enums.GameMode = enums.GameMode(game_mode)

                if game_modes := details.get("modes"):
                    appended_modes: typing.List[enums.GameMode] = []
                    for _mode in game_modes:
                        appended_modes.append(enums.GameMode(_mode))

                member_type: enums.MembershipType = enums.MembershipType(
                    details["membershipType"]
                )
                if (inner := activs.get("values")) is not None:
                    values = dict(inner.items()).values()
                    data = [
                        basic_data["basic"]["displayValue"] for basic_data in values
                    ]

        return activity.Activity(
            net=self._net,
            period=period,
            hash=id,
            instance_id=int(instance_id),
            mode=mode,
            modes=appended_modes,
            member_type=member_type,
            assists=int(data[0]),
            is_completed=data[1],
            deaths=int(data[2]),
            kills=int(data[3]),
            opponents_defeated=int(data[4]),
            efficiency=float(data[5]),
            kd=float(data[6]),
            score=int(data[8]),
            duration=data[9],
            completion_reason=data[11],
            player_count=int(data[15]),
        )

    def deserialize_linked_profiles(self, payload: JsonObject) -> profile.LinkedProfile:
        bungie_user = self.deserialize_partial_bungie_user(
            payload["bnetMembership"], noeq=True
        )
        error_profiles_vec: typing.MutableSequence[user.DestinyUser] = []
        profiles_vec: typing.MutableSequence[user.DestinyUser] = []

        if (raw_profile := payload.get("profiles")) is not None:
            for pfile in raw_profile:
                profiles_vec.append(self.deserialize_destiny_user(pfile, noeq=True))

        if (raw_profiles_with_errors := payload.get("profilesWithErrors")) is not None:
            for raw_error_pfile in raw_profiles_with_errors:
                if (error_pfile := raw_error_pfile.get("infoCard")) is not None:
                    error_profiles_vec.append(
                        self.deserialize_destiny_user(error_pfile, noeq=True)
                    )

        return profile.LinkedProfile(
            net=self._net,
            bungie=bungie_user,
            profiles=profiles_vec,
            profiles_with_errors=error_profiles_vec,
        )

    def deserialize_clan_banners(
        self, payload: JsonObject
    ) -> typing.Sequence[clans.ClanBanner]:
        banners_seq: typing.MutableSequence[clans.ClanBanner] = []
        if (banners := payload.get("clanBannerDecals")) is not None:
            for k, v in banners.items():
                banner_obj = clans.ClanBanner(
                    id=int(k),
                    foreground=Image(v.get("foregroundPath", Image.partial())),
                    background=Image(v.get("backgroundPath", Image.partial())),
                )
                banners_seq.append(banner_obj)
        return banners_seq

    def deserialize_public_milestone_content(
        self, payload: JsonObject
    ) -> milestones.Milestone:
        items_categoris: NoneOr[milestones.MilestoneItems] = None
        if (raw_categories := payload.get("itemCategories")) is not None:
            for item in raw_categories:
                title = Undefined
                if (raw_title := item.get("title")) is not None:
                    if raw_title != Unknown:
                        title = raw_title
                if (raw_hashes := item.get("itemHashes")) is not None:
                    hashes: typing.Sequence[int] = raw_hashes

                items_categoris = milestones.MilestoneItems(title=title, hashes=hashes)

        about = Undefined
        if (raw_about := payload["about"]) != Unknown:
            about = raw_about

        status = Undefined
        if (raw_status := payload["status"]) != Unknown:
            status = raw_status

        tips: typing.MutableSequence[UndefinedOr[str]] = []
        if (raw_tips := payload.get("tips")) is not None:
            for raw_tip in raw_tips:
                if raw_tip == Unknown:
                    raw_tip = Undefined
                tips.append(raw_tip)

        return milestones.Milestone(
            about=about, status=status, tips=tips, items=items_categoris
        )

    def deserialize_friend(self, payload: JsonObject, /) -> friends.Friend:
        name = Undefined
        if (raw_name := payload["bungieGlobalDisplayName"]) != Unknown:
            name = raw_name

        bungie_user: NoneOr[user.User] = None
        if raw_bungie_user := payload.get("bungieNetUser"):
            bungie_user = self.deserialize_user(raw_bungie_user)

        return friends.Friend(
            net=self._net,
            id=int(payload["lastSeenAsMembershipId"]),
            name=name,
            code=payload.get("bungieGlobalDisplayNameCode"),
            relationship=enums.Relationship(payload["relationship"]),
            user=bungie_user,
            online_status=enums.Presence(payload["onlineStatus"]),
            online_title=payload["onlineTitle"],
            type=enums.MembershipType(payload["lastSeenAsBungieMembershipType"]),
        )

    def deserialize_friends(
        self, payload: JsonObject
    ) -> typing.Sequence[friends.Friend]:
        mut_seq: typing.MutableSequence[friends.Friend] = []
        if raw_friends := payload.get("friends"):
            for friend in raw_friends:
                mut_seq.append(self.deserialize_friend(friend))
        return mut_seq

    def deserialize_friend_requests(
        self, payload: JsonObject
    ) -> friends.FriendRequestView:
        incoming: typing.MutableSequence[friends.Friend] = []
        outgoing: typing.MutableSequence[friends.Friend] = []

        if raw_incoming_requests := payload.get("incmoingRequests"):
            for incoming_request in raw_incoming_requests:
                incoming.append(self.deserialize_friend(incoming_request))

        if raw_outgoing_requests := payload.get("outgoingRequests"):
            for incoming_request in raw_outgoing_requests:
                outgoing.append(self.deserialize_friend(incoming_request))

        return friends.FriendRequestView(incoming=incoming, outgoing=outgoing)
