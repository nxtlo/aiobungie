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

"""Deserialization for all bungie incoming json payloads."""

from __future__ import annotations

__all__ = ("Deserialize",)

import datetime
import logging
import typing

from aiobungie import error
from aiobungie.crate import activity
from aiobungie.crate import application as app
from aiobungie.crate import character
from aiobungie.crate import clans
from aiobungie.crate import entity
from aiobungie.crate import player
from aiobungie.crate import profile
from aiobungie.crate import user
from aiobungie.internal import Image
from aiobungie.internal import enums
from aiobungie.internal import impl
from aiobungie.internal import time
from aiobungie.internal.helpers import JsonDict
from aiobungie.internal.helpers import JsonList
from aiobungie.internal.helpers import NoneOr
from aiobungie.internal.helpers import Undefined
from aiobungie.internal.helpers import Unknown
from aiobungie.internal.helpers import just

_LOG: typing.Final[logging.Logger] = logging.getLogger(__name__)


class Deserialize:
    """The base Deserialization class for all aiobungie crate."""

    # This is actually inspired by hikari's entity factory.

    __slots__: typing.Sequence[str] = ("_net",)

    def __init__(self, net: impl.Netrunner) -> None:
        self._net = net

    def deserialize_user(self, payload: JsonList, position: int = 0) -> user.User:
        from_id = payload
        try:
            data = payload[position]  # type: ignore
        except (KeyError, UnboundLocalError):
            data = from_id  # type: ignore
        except IndexError:
            if position or position == 0:
                raise error.UserNotFound("Player was not found.") from None

        return user.User(
            id=int(data["membershipId"]),
            created_at=time.clean_date(data["firstAccess"]),
            name=data["displayName"],
            is_deleted=data["isDeleted"],
            about=data["about"],
            updated_at=time.clean_date(data["lastUpdate"]),
            psn_name=data.get("psnDisplayName", None),
            steam_name=data.get("steamDisplayName", None),
            twitch_name=data.get("twitchDisplayName", None),
            blizzard_name=data.get("blizzardDisplayName", None),
            status=data["statusText"],
            locale=data["locale"],
            picture=Image(path=str(data["profilePicturePath"])),
            displayname_code=data.get("cachedBungieGlobalDisplayNameCode", None),
            unique_name=data.get("uniqueName", None),
        )

    @staticmethod
    def set_themese_attrs(payload: JsonList, /) -> typing.ValuesView[user.UserThemes]:
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
                    id=t_id, name=t_name, description=t_desc
                )
        return theme_map.values()

    def deserialize_user_themes(
        self, payload: JsonList
    ) -> typing.Sequence[user.UserThemes]:
        return list(self.set_themese_attrs(payload))

    def deserialize_player(self, payload: JsonDict, /) -> player.Player:
        try:
            data = payload[0]  # type: ignore
        except IndexError:
            raise error.PlayerNotFound("Player was not found.") from None

        types: list[enums.MembershipType] = []
        for type in data["applicableMembershipTypes"]:
            types.append(enums.MembershipType(type))

        return player.Player(
            name=data["displayName"],
            id=int(data["membershipId"]),
            is_public=data["isPublic"],
            icon=Image(str(data["iconPath"])),
            type=enums.MembershipType(data["membershipType"]),
            displayname_code=data.get("bungieGlobalDisplayNameCode", None),
            types=types,
            crossave_override=int(data["crossSaveOverride"]),
        )

    def deseialize_clan_owner(self, data: JsonDict) -> clans.ClanOwner:
        id = data["destinyUserInfo"]["membershipId"]
        name = data["destinyUserInfo"]["displayName"]
        icon = Image(str(data["destinyUserInfo"]["iconPath"]))
        convert = int(data["lastOnlineStatusChange"])
        last_online = time.from_timestamp(convert)
        clan_id = data["groupId"]
        joined_at = data["joinDate"]
        types = data["destinyUserInfo"]["applicableMembershipTypes"]
        is_public = data["destinyUserInfo"]["isPublic"]
        type = enums.MembershipType(data["destinyUserInfo"].get("membershipType", None))

        return clans.ClanOwner(
            id=id,
            name=name,
            icon=icon,
            last_online=last_online,
            clan_id=clan_id,
            joined_at=time.clean_date(joined_at),
            types=types,
            is_public=is_public,
            type=type,
            displayname_code=data.get("bungieGlobalDisplayNameCode", None),
        )

    def deseialize_clan(self, data: JsonDict) -> clans.Clan:
        id = data["detail"]["groupId"]
        name = data["detail"]["name"]
        created_at = data["detail"]["creationDate"]
        member_count = data["detail"]["memberCount"]
        description = data["detail"]["about"]
        about = data["detail"]["motto"]
        is_public = data["detail"]["isPublic"]
        banner = Image(str(data["detail"]["bannerPath"]))
        avatar = Image(str(data["detail"]["avatarPath"]))
        tags = data["detail"]["tags"]
        features = data["detail"]["features"]
        type = data["detail"]["groupType"]

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

        return clans.Clan(
            net=self._net,
            id=id,
            name=name,
            type=enums.GroupType(type),
            created_at=time.clean_date(created_at),
            member_count=member_count,
            description=description,
            about=about,
            is_public=is_public,
            banner=banner,
            avatar=avatar,
            tags=tags,
            features=features_obj,
            owner=self.deseialize_clan_owner(data["founder"]),
        )

    def deserialize_clan_member(self, data: JsonDict, /) -> clans.ClanMember:

        if (payload := data["results"]) is not None:
            attrs = payload[0]
            last_online: datetime.datetime = time.from_timestamp(
                int(attrs["lastOnlineStatusChange"])
            )
            is_online: bool = attrs["isOnline"]
            group_id: int = attrs["groupId"]
            joined_at: datetime.datetime = time.clean_date(str(attrs["joinDate"]))

            try:
                payload = payload[0]["destinyUserInfo"]
            except KeyError:
                raise error.NotFound("Clan member not found.")

            id: int = payload["membershipId"]
            name: str = payload["displayName"]
            type: enums.MembershipType = payload["membershipType"]
            is_public: bool = payload["isPublic"]
            icon: Image = Image(str(payload["iconPath"]))
            type_entires: list[enums.MembershipType] = []

            for member_type in payload["applicableMembershipTypes"]:
                if member_type is None:
                    continue
                type_entires.append(enums.MembershipType(member_type))

        return clans.ClanMember(
            group_id=int(group_id),
            is_online=is_online,
            last_online=last_online,
            id=int(id),
            joined_at=joined_at,
            name=name,
            type=enums.MembershipType(type),
            is_public=is_public,
            icon=icon,
            displayname_code=payload.get("bungieGlobalDisplayNameCode", None),
            types=type_entires,
        )

    @staticmethod
    def set_clan_members_attrs(
        data: JsonDict, /
    ) -> typing.ValuesView[clans.ClanMember]:
        member_view: dict[int, clans.ClanMember] = {}
        if (payload := data["results"]) is not None:

            raw_is_on: list[bool] = just(payload, "isOnline")
            raw_last_sts: list[int] = just(payload, "lastOnlineStatusChange")
            raw_join_date: list[str] = just(payload, "joinDate")
            group_id: list[int] = just(payload, "groupId")

            for is_online, last_online, join_date in zip(
                raw_is_on, raw_last_sts, raw_join_date
            ):
                last_online_fmt: datetime.datetime = time.from_timestamp(
                    int(last_online)
                )
                join_date_fmt: datetime.datetime = time.clean_date(join_date)

            for member in just(payload, "destinyUserInfo"):
                # Some bungie display names apper as ''
                # so we just make sure that the name is not an empty string.
                # otherwise we just grab the last seen name.
                if (name := member["bungieGlobalDisplayName"]) == Unknown:
                    name: str = member["LastSeenDisplayName"]  # type: ignore
                type_entires: list[enums.MembershipType] = []

                for member_type in member["applicableMembershipTypes"]:
                    assert member_type is not None
                    type_entires.append(enums.MembershipType(member_type))

                member_view[int(member["membershipId"])] = clans.ClanMember(
                    id=int(member["membershipId"]),
                    name=name,
                    type=enums.MembershipType(member["membershipType"]),
                    icon=Image(str(member["iconPath"])),
                    is_public=member["isPublic"],
                    group_id=int(group_id[0]),
                    is_online=is_online,
                    last_online=last_online_fmt,
                    joined_at=join_date_fmt,
                    displayname_code=member.get("bungieGlobalDisplayNameCode", None),
                    types=type_entires,
                )

        if member_view is None:
            return dict().values()
        return member_view.values()

    def deserialize_clan_members(
        self, data: JsonDict, /
    ) -> typing.Sequence[clans.ClanMember]:
        return list(self.set_clan_members_attrs(data))

    def deserialize_app_owner(self, payload: JsonDict) -> app.ApplicationOwner:
        return app.ApplicationOwner(
            name=payload["displayName"],
            id=payload["membershipId"],
            type=enums.MembershipType(payload["membershipType"]),
            icon=Image(str(payload["iconPath"])),
            is_public=payload["isPublic"],
            displayname_code=payload.get("bungieGlobalDisplayNameCode", None),
        )

    def deserialize_app(self, payload: JsonDict) -> app.Application:
        return app.Application(
            id=payload["applicationId"],
            name=payload["name"],
            link=payload["link"],
            status=payload["status"],
            redirect_url=payload["redirectUrl"],
            created_at=time.clean_date(str(payload["creationDate"])),
            published_at=time.clean_date(str(payload["firstPublished"])),
            owner=self.deserialize_app_owner(payload["team"][0]["user"]),  # type: ignore
            scope=payload["scope"],
        )

    def deserialize_character(
        self, payload: JsonDict, *, chartype: enums.Class
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
            id=payload["characterId"],
            gender=enums.Gender(payload["genderType"]),
            race=enums.Race(payload["raceType"]),
            class_type=enums.Class(payload["classType"]),
            emblem=Image(str(payload["emblemBackgroundPath"])),
            emblem_icon=Image(str(payload["emblemPath"])),
            emblem_hash=int(payload["emblemHash"]),
            last_played=payload["dateLastPlayed"],
            total_played_time=total_time,
            member_id=payload["membershipId"],
            member_type=enums.MembershipType(payload["membershipType"]),
            level=payload["baseCharacterLevel"],
            title_hash=payload.get("titleRecordHash", None),
            light=payload["light"],
            stats=payload["stats"],
        )

    def deserialize_profile(self, payload: JsonDict, /) -> profile.Profile:

        payload = payload["profile"]["data"]
        id = int(payload["userInfo"]["membershipId"])
        name = payload["userInfo"]["displayName"]
        is_public = payload["userInfo"]["isPublic"]
        type = enums.MembershipType(payload["userInfo"]["membershipType"])
        last_played = time.clean_date(str(payload["dateLastPlayed"]))
        character_ids = payload["characterIds"]
        power_cap = payload["currentSeasonRewardPowerCap"]

        return profile.Profile(
            id=id,
            name=name,
            is_public=is_public,
            type=type,
            last_played=last_played,
            character_ids=character_ids,
            power_cap=power_cap,
            net=self._net,
        )

    def deserialize_inventory_entity(
        self, payload: JsonDict, /
    ) -> entity.InventoryEntity:
        try:
            # All Bungie entities has a display propetie
            # if we don't find it means the entity was not found.
            props: JsonDict = payload["displayProperties"]
        except KeyError:
            raise error.NotFound("The entity inventory item hash is invalid") from None

        # Some entities have an inventory which
        # Includes its hash types.
        # Most entities has this
        # and for some it doesn't exists

        if (raw_inventory := payload.get("inventory", {})) is not None:
            inventory: JsonDict = raw_inventory

        # Entity tier type. Most entities have a tier
        # and some doesn't exists so we have to check.

        if (raw_bucket := inventory.get("bucketTypeHash", None)) is not None:
            bucket_type: int = raw_bucket

        if (raw_tier := inventory.get("tierTypeHash", None)) is not None:
            tier: enums.ItemTier = enums.ItemTier(raw_tier)

        if (raw_tier_name := inventory.get("tierTypeName", None)) is not None:
            tier_name: str = raw_tier_name

        if (name := props.get("name", Unknown)) == Unknown:
            name = Undefined

        if (type_name := payload.get("itemTypeDisplayName")) == Unknown:
            type_name = Undefined

        if (description := props.get("description", Unknown)) == Unknown:
            description = Undefined

        if (about := payload.get("flavorText")) == Unknown:
            about = Undefined

        if (raw_icon := props.get("icon", None)) is not None:
            icon: Image = Image(str(raw_icon))

        if (raw_watermark := payload.get("iconWatermark", None)) is not None:
            water_mark: Image = Image(str(raw_watermark))

        if (screenshot := payload.get("screenshot", None)) is not None:
            banner: Image = Image(str(screenshot))

        if (damage_type := payload.get("defaultDamageTypeHash", None)) is not None:
            damage: enums.DamageType = enums.DamageType(damage_type)

        if (raw_summary_hash := payload.get("summaryItemHash", None)) is not None:
            summary_hash: int = int(raw_summary_hash)

        if (raw_stats := payload.get("stats", {})) is not None:
            stats: JsonDict = raw_stats

        if (ammo := payload.get("equippingBlock", None)) is not None:
            block: enums.AmmoType = enums.AmmoType(ammo["ammoType"])

        if (raw_item_class := payload.get("classType", None)) is not None:
            item_class: enums.Class = enums.Class(raw_item_class)

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
            type=payload.get("itemType", None),
            bucket_type=bucket_type,
            tier=tier,
            tier_name=tier_name,
            type_name=type_name,
            sub_type=payload.get("itemSubType", None),
            item_class=item_class,
            damage=damage,
            summary_hash=summary_hash,
            is_equippable=payload.get("equippable", None),
            stats=stats,
            ammo_type=block,
            lore_hash=payload.get("loreHash", None),
        )

    def deserialize_activity(
        self, payload: JsonDict, /, *, limit: typing.Optional[int] = 1
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
            instance_id=instance_id,
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
