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

"""Marshaller factory for deserializing Bungie's JSON payloads."""

from __future__ import annotations

__all__ = ("Factory",)

import collections.abc as collections
import typing

from aiobungie import error
from aiobungie import interfaces
from aiobungie import typedefs
from aiobungie import undefined
from aiobungie.crate import activity
from aiobungie.crate import application as app
from aiobungie.crate import character
from aiobungie.crate import clans
from aiobungie.crate import components
from aiobungie.crate import entity
from aiobungie.crate import fireteams
from aiobungie.crate import friends
from aiobungie.crate import milestones
from aiobungie.crate import profile
from aiobungie.crate import progressions
from aiobungie.crate import records
from aiobungie.crate import season
from aiobungie.crate import user
from aiobungie.internal import assets
from aiobungie.internal import enums
from aiobungie.internal import helpers
from aiobungie.internal import time

if typing.TYPE_CHECKING:
    import datetime

    from aiobungie import traits


class Factory(interfaces.FactoryInterface):
    """The base deserialization factory class for all aiobungie data classes.

    This factory is used to deserialize JSON responses from the REST client and turning them
    into a Python data classes object.

    This is only provided by `aiobungie.Client` base client.
    """

    # This is kinda inspired by hikari's entity factory :p.

    __slots__: collections.Sequence[str] = ("_net",)

    def __init__(self, net: traits.Netrunner) -> None:
        self._net = net

    def deserialize_bungie_user(self, data: typedefs.JsonObject) -> user.BungieUser:
        return user.BungieUser(
            id=int(data["membershipId"]),
            created_at=time.clean_date(data["firstAccess"]),
            name=data.get("cachedBungieGlobalDisplayName", undefined.Undefined),
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
            picture=assets.Image(path=str(data["profilePicturePath"])),
            code=data.get("cachedBungieGlobalDisplayNameCode", None),
            unique_name=data.get("uniqueName", None),
            theme_id=int(data["profileTheme"]),
            show_activity=bool(data["showActivity"]),
            theme_name=data["profileThemeName"],
            display_title=data["userTitleDisplay"],
        )

    # Deserializer for a `bungieNetUserInfo`
    def deserialize_partial_bungie_user(
        self, payload: typedefs.JsonObject, *, noeq: bool = False
    ) -> user.PartialBungieUser:
        if noeq is True:
            bungie_info = payload
        else:
            bungie_info = payload["bungieNetUserInfo"]

        memberships = []

        try:
            for m_ship in bungie_info["applicableMembershipTypes"]:
                memberships.append(enums.MembershipType(m_ship))
        except KeyError:
            pass

        return user.PartialBungieUser(
            net=self._net,
            types=memberships,
            name=bungie_info.get("displayName", undefined.Undefined),
            id=int(bungie_info["membershipId"]),
            crossave_override=enums.MembershipType(bungie_info["crossSaveOverride"]),
            is_public=bungie_info["isPublic"],
            icon=assets.Image(bungie_info.get("iconPath", assets.Image.partial())),
            type=enums.MembershipType(bungie_info["membershipType"]),
        )

    # Deserializer for a `destinyUserInfo`
    def deserialize_destiny_user(
        self, payload: typedefs.JsonObject, *, noeq: bool = False
    ) -> user.DestinyUser:
        if noeq is True:
            user_info = payload
        else:
            user_info = payload["destinyUserInfo"]

        memberships = []
        for m_ship in user_info["applicableMembershipTypes"]:
            memberships.append(enums.MembershipType(m_ship))

        if (raw_name := user_info["bungieGlobalDisplayName"]) == typedefs.Unknown:
            name = undefined.Undefined
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
            icon=assets.Image(user_info.get("iconPath", assets.Image.partial())),
            types=memberships,
        )

    # Deserialize a list of `destinyUserInfo`
    def deserialize_destiny_members(
        self,
        data: typing.Union[typedefs.JsonObject, typedefs.JsonArray],
        *,
        bound: bool = False,
    ) -> collections.Sequence[user.DestinyUser]:
        xbox: int = 0
        psn: int = 1
        steam: int = 2
        stadia: int = 3

        # In order to bind this method between deserializing
        # other objects we have to check if the data was
        # a json object or a json array of objects.

        raw_members: typing.Union[
            typedefs.JsonArray, typedefs.JsonObject, dict[int, typing.Any]
        ] = data

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

        stadia_obj: typedefs.NoneOr[user.DestinyUser] = None  # type: ignore[name-defined]
        try:
            stadia_member = members_[stadia]  # type: ignore[index]
        except (KeyError, IndexError):
            pass
        else:
            stadia_obj = self.deserialize_destiny_user(stadia_member, noeq=True)

        xbox_obj: typedefs.NoneOr[user.DestinyUser] = None  # type: ignore[name-defined]
        try:
            xbox_member = members_[xbox]  # type: ignore[index]
        except (KeyError, IndexError):
            pass
        else:
            xbox_obj = self.deserialize_destiny_user(xbox_member, noeq=True)

        steam_obj: typedefs.NoneOr[user.DestinyUser] = None  # type: ignore[name-defined]
        try:
            steam_member = members_[steam]  # type: ignore[index]
        except (KeyError, IndexError):
            pass
        else:
            steam_obj = self.deserialize_destiny_user(steam_member, noeq=True)

        psn_obj: typedefs.NoneOr[user.DestinyUser] = None  # type: ignore[name-defined]
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

    def deserialize_user(self, data: typedefs.JsonObject) -> user.User:
        return user.User(
            bungie=self.deserialize_bungie_user(data["bungieNetUser"]),
            destiny=self.deserialize_destiny_members(data),
        )

    def deseialize_found_users(
        self, payload: typedefs.JsonObject
    ) -> collections.Sequence[user.DestinyUser]:
        result = payload["searchResults"]
        if result is None:
            raise error.NotFound("User not found.")

        vec: list[user.DestinyUser] = []
        for player in result:
            # TODO: Figuire out how to merge this with DestinyUser objects.
            #  name: undefined.UndefinedOr[str] = player.get("bungieGlobalDisplayName", undefined.Undefined)
            #  code: typedefs.NoneOr[int] = player.get("bungieGlobalDisplayNameCode", None)
            #  bungie_id: undefined.UndefinedOr[int] = player.get('bungieNetMembershipId', undefined.Undefined)
            for mship in self.deserialize_destiny_members(player):
                vec.append(mship)
        return vec

    @staticmethod
    def set_themese_attrs(
        payload: typedefs.JsonArray, /
    ) -> typing.Collection[user.UserThemes]:
        if payload is None:
            raise ValueError("No themes found.")

        theme_map: dict[int, user.UserThemes] = {}
        theme_ids: list[int] = helpers.just(payload, "userThemeId")
        theme_names: list[typedefs.NoneOr[str]] = helpers.just(payload, "userThemeName")
        theme_descriptions: list[typedefs.NoneOr[str]] = helpers.just(
            payload, "userThemeDescription"
        )

        for t_id, t_name, t_desc in zip(theme_ids, theme_names, theme_descriptions):
            theme_map[t_id] = user.UserThemes(
                id=int(t_id),
                name=t_name or undefined.Undefined,
                description=t_desc or undefined.Undefined,
            )
        return theme_map.values()

    def deserialize_user_themes(
        self, payload: typedefs.JsonArray
    ) -> collections.Sequence[user.UserThemes]:
        return list(self.set_themese_attrs(payload))

    def deserialize_player(
        self, payload: typedefs.JsonArray, /
    ) -> collections.Sequence[user.DestinyUser]:
        if payload is None:
            raise error.NotFound("Player was not found.") from None

        return self.deserialize_destiny_members(payload, bound=True)

    def deseialize_clan_owner(self, data: typedefs.JsonObject) -> clans.ClanMember:
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
        self, payload: typedefs.JsonObject, *, bound: bool = False
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
        banner = assets.Image(str(data["bannerPath"]))
        avatar = assets.Image(str(data["avatarPath"]))
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

        founder: typedefs.NoneOr[clans.ClanMember] = None
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
        self, payload: typedefs.JsonObject
    ) -> typedefs.NoneOr[clans.GroupMember]:
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
        self, payload: typedefs.JsonObject
    ) -> collections.Sequence[clans.ClanAdmin]:
        builder = []
        member_types = helpers.just(payload["results"], "memberType")
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

    def deserialize_clan_member(self, data: typedefs.JsonObject, /) -> clans.ClanMember:

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
        self, payload: typedefs.JsonArray
    ) -> collections.Sequence[clans.ClanConversation]:
        map = {}
        vec = []
        if payload is not None:
            for convo in payload:
                for k, v in convo.items():
                    map[k] = v

                if (name := map["chatName"]) == typedefs.Unknown:
                    name = undefined.Undefined

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
        self, data: typedefs.JsonObject, /
    ) -> collections.Sequence[clans.ClanMember]:

        members_vec: list[clans.ClanMember] = []
        _fn_type_optional = typing.Optional[typing.Callable[..., typing.Dict[str, str]]]
        _fn_type = typing.Callable[..., typing.Dict[str, str]]
        payload: typing.List[typing.Dict[str, typing.Any]]

        if (payload := data["results"]) is not None:

            # raw_is_on: list[bool] = helpers.just(payload, "isOnline")
            # raw_last_sts: list[int] = helpers.just(payload, "lastOnlineStatusChange")
            # raw_join_date: list[str] = helpers.just(payload, "joinDate")
            # metadata = map(
            #     lambda *args: args, raw_is_on, raw_last_sts, raw_join_date
            # )
            # for is_online, last_online, join_date in metadata:
            #     last_online_fmt: datetime.datetime = time.from_timestamp(
            #         int(last_online)
            #     )
            #     join_date_fmt: datetime.datetime = time.clean_date(join_date)

            group_id = helpers.just(payload, "groupId")

            for memberships in payload:
                wrap_destiny: _fn_type = lambda m: m["destinyUserInfo"]  # type: ignore[no-any-return]
                wrap_bungie: _fn_type_optional = None

                try:
                    wrap_bungie: _fn_type_optional = lambda m: m["bungieNetUserInfo"]  # type: ignore[no-redef]
                    if wrap_bungie:
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

    def deserialize_app_owner(
        self, payload: typedefs.JsonObject
    ) -> app.ApplicationOwner:
        return app.ApplicationOwner(
            net=self._net,
            name=payload.get("bungieGlobalDisplayName", undefined.Undefined),
            id=int(payload["membershipId"]),
            type=enums.MembershipType(payload["membershipType"]),
            icon=assets.Image(str(payload["iconPath"])),
            is_public=payload["isPublic"],
            code=payload.get("bungieGlobalDisplayNameCode", None),
        )

    def deserialize_app(self, payload: typedefs.JsonObject) -> app.Application:
        return app.Application(
            id=int(payload["applicationId"]),
            name=payload["name"],
            link=payload["link"],
            status=payload["status"],
            redirect_url=payload.get("redirectUrl", None),
            created_at=time.clean_date(str(payload["creationDate"])),
            published_at=time.clean_date(str(payload["firstPublished"])),
            owner=self.deserialize_app_owner(payload["team"][0]["user"]),  # type: ignore
            scope=payload.get("scope", undefined.Undefined),
        )

    def _set_character_attrs(self, payload: typedefs.JsonObject) -> character.Character:
        total_time = time.format_played(int(payload["minutesPlayedTotal"]), suffix=True)
        return character.Character(
            net=self._net,
            id=int(payload["characterId"]),
            gender=enums.Gender(payload["genderType"]),
            race=enums.Race(payload["raceType"]),
            class_type=enums.Class(payload["classType"]),
            emblem=assets.Image(str(payload["emblemBackgroundPath"])),
            emblem_icon=assets.Image(str(payload["emblemPath"])),
            emblem_hash=int(payload["emblemHash"]),
            last_played=payload["dateLastPlayed"],
            total_played_time=total_time,
            member_id=int(payload["membershipId"]),
            member_type=enums.MembershipType(payload["membershipType"]),
            level=payload["baseCharacterLevel"],
            title_hash=payload.get("titleRecordHash", None),
            light=payload["light"],
            stats={enums.Stat(int(k)): v for k, v in payload["stats"].items()},
        )

    def deserialize_profile(
        self, payload: typedefs.JsonObject, /
    ) -> typing.Optional[profile.Profile]:
        if (raw_profile := payload.get("data")) is None:
            return None

        payload = raw_profile
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

    def deserialize_profile_item(
        self, payload: typedefs.JsonObject
    ) -> profile.ProfileItemImpl:

        instance_id: typing.Optional[int] = None
        if raw_instance_id := payload.get("itemInstanceId"):
            instance_id = int(raw_instance_id)

        version_number: typing.Optional[int] = None
        if raw_version := payload.get("versionNumber"):
            version_number = int(raw_version)

        transfer_status: int = payload["transferStatus"]
        try:
            transfer_status = enums.TransferStatus(payload["transferStatus"])
        except ValueError:
            pass

        return profile.ProfileItemImpl(
            net=self._net,
            hash=payload["itemHash"],
            quantity=payload["quantity"],
            bind_status=enums.ItemBindStatus(payload["bindStatus"]),
            location=enums.ItemLocation(payload["location"]),
            bucket=payload["bucketHash"],
            transfer_status=transfer_status,
            lockable=payload["lockable"],
            state=enums.ItemState(payload["state"]),
            dismantel_permissions=payload["dismantlePermission"],
            is_wrapper=payload["isWrapper"],
            instance_id=instance_id,
            version_number=version_number,
            ornament_id=payload.get("overrideStyleItemHash"),
        )

    def deserialize_objectives(self, payload: typedefs.JsonObject) -> records.Objective:
        return records.Objective(
            net=self._net,
            hash=payload["objectiveHash"],
            visible=payload["visible"],
            complete=payload["complete"],
            completion_value=payload["completionValue"],
            progress=payload["progress"],
        )

    def deserialize_records(
        self,
        payload: typedefs.JsonObject,
        scores: typing.Optional[records.RecordScores] = None,
        **nodes: int,
    ) -> records.Record:
        objectives: typing.Optional[list[records.Objective]] = None
        interval_objectives: typing.Optional[list[records.Objective]] = None
        record_state: typedefs.IntAnd[records.RecordState]

        try:
            record_state = records.RecordState(payload.get("state", 999))
        except ValueError:
            record_state = payload.get("state", 0)

        if raw_objs := payload.get("objectives"):
            objectives = [self.deserialize_objectives(obj) for obj in raw_objs]

        if raw_interval_objs := payload.get("intervalObjectives"):
            interval_objectives = [
                self.deserialize_objectives(obj) for obj in raw_interval_objs
            ]

        if scores:
            assert scores is not None

        return records.Record(
            scores=scores,
            categories_node_hash=nodes.get("categories_hash", undefined.Undefined),
            seals_node_hash=nodes.get("seals_hash", undefined.Undefined),
            state=record_state,
            objectives=objectives,
            interval_objectives=interval_objectives,
            redeemed_count=payload.get("intervalsRedeemedCount", 0),
            completion_times=payload.get("completedCount", None),
            reward_visibility=payload.get("rewardVisibilty", None),
        )

    def deserialize_character_records(
        self,
        payload: typedefs.JsonObject,
        scores: typing.Optional[records.RecordScores] = None,
        record_hashes: typing.Optional[list[int]] = None,
    ) -> records.CharacterRecord:

        record = self.deserialize_records(payload, scores)
        # This is always None but available to keep the Record
        # Signature.
        assert scores is None
        return records.CharacterRecord(
            scores=scores,
            categories_node_hash=record.categories_node_hash,
            seals_node_hash=record.seals_node_hash,
            state=record.state,
            objectives=record.objectives,
            interval_objectives=record.interval_objectives,
            redeemed_count=payload.get("intervalsRedeemedCount", 0),
            completion_times=payload.get("completedCount"),
            reward_visibility=payload.get("rewardVisibilty"),
            record_hashes=record_hashes or [],
        )

    def deserialize_character_dye(self, payload: typedefs.JsonObject) -> character.Dye:
        return character.Dye(
            channel_hash=payload["channelHash"], dye_hash=payload["dyeHash"]
        )

    def deserialize_character_customazition(
        self, payload: typedefs.JsonObject
    ) -> character.CustomizationOptions:
        return character.CustomizationOptions(
            personality=payload["personality"],
            face=payload["face"],
            skin_color=payload["skinColor"],
            lip_color=payload["lipColor"],
            eye_color=payload["eyeColor"],
            hair_colors=payload.get("hairColors", []),
            feature_colors=payload.get("featureColors", []),
            decal_color=payload["decalColor"],
            wear_helmet=payload["wearHelmet"],
            hair_index=payload["hairIndex"],
            feature_index=payload["featureIndex"],
            decal_index=payload["decalIndex"],
        )

    def deserialize_character_minimal_equipments(
        self, payload: typedefs.JsonObject
    ) -> character.MinimalEquipments:
        dyes = None
        if raw_dyes := payload.get("dyes"):
            if raw_dyes:
                dyes = [self.deserialize_character_dye(dye) for dye in raw_dyes]
        return character.MinimalEquipments(
            net=self._net, item_hash=payload["itemHash"], dyes=dyes
        )

    def deserialize_character_render_data(
        self, payload: typedefs.JsonObject, /
    ) -> character.RenderedData:
        return character.RenderedData(
            net=self._net,
            customization=self.deserialize_character_customazition(
                payload["customization"]
            ),
            custom_dyes=[
                self.deserialize_character_dye(dye)
                for dye in payload["customDyes"]
                if dye
            ],
            equipment=[
                self.deserialize_character_minimal_equipments(equipment)
                for equipment in payload["peerView"]["equipment"]
            ],
        )

    def deserialize_available_activity(
        self, payload: typedefs.JsonObject
    ) -> activity.AvailableActivity:
        return activity.AvailableActivity(
            hash=payload["activityHash"],
            is_new=payload["isNew"],
            is_completed=payload["isCompleted"],
            is_visible=payload["isVisible"],
            display_level=payload.get("displayLevel"),
            recommended_light=payload.get("recommendedLight"),
            diffculity=activity.Diffculity(payload["difficultyTier"]),
            can_join=payload["canJoin"],
            can_lead=payload["canLead"],
        )

    def deserialize_character_activity(
        self, payload: typedefs.JsonObject
    ) -> activity.CharacterActivity:
        current_mode: typing.Optional[enums.GameMode] = None
        if raw_current_mode := payload.get("currentActivityModeType"):
            current_mode = enums.GameMode(raw_current_mode)

        current_mode_types: typing.Optional[collections.Sequence[enums.GameMode]] = None
        if raw_current_modes := payload.get("currentActivityModeTypes"):
            current_mode_types = [enums.GameMode(type_) for type_ in raw_current_modes]

        return activity.CharacterActivity(
            date_started=time.clean_date(payload["dateActivityStarted"]),
            current_hash=payload["currentActivityHash"],
            current_mode_hash=payload["currentActivityModeHash"],
            current_mode=current_mode,
            current_mode_hashes=payload.get("currentActivityModeHashes"),
            current_mode_types=current_mode_types,
            current_playlist_hash=payload.get("currentPlaylistActivityHash"),
            last_story_hash=payload["lastCompletedStoryHash"],
            available_activities=[
                self.deserialize_available_activity(activity_)
                for activity_ in payload["availableActivities"]
            ],
        )

    def deserialize_profile_items(
        self, payload: typedefs.JsonObject, /
    ) -> list[profile.ProfileItemImpl]:
        return [self.deserialize_profile_item(item) for item in payload["items"]]

    def _deserialize_progressions(
        self, payload: typedefs.JsonObject
    ) -> progressions.Progression:
        return progressions.Progression(
            hash=payload["progressionHash"],
            level=payload["level"],
            cap=payload["levelCap"],
            daily_limit=payload["dailyLimit"],
            weekly_limit=payload["weeklyLimit"],
            current_progress=payload["currentProgress"],
            daily_progress=payload["dailyProgress"],
            needed=payload["progressToNextLevel"],
            next_level=payload["nextLevelAt"],
        )

    def _deserialize_factions(
        self, payload: typedefs.JsonObject
    ) -> progressions.Factions:
        progs = self._deserialize_progressions(payload)
        return progressions.Factions(
            hash=progs.hash,
            level=progs.level,
            cap=progs.cap,
            daily_limit=progs.daily_limit,
            weekly_limit=progs.weekly_limit,
            current_progress=progs.current_progress,
            daily_progress=progs.daily_progress,
            needed=progs.needed,
            next_level=progs.next_level,
            faction_hash=payload["factionHash"],
            faction_vendor_hash=payload["factionVendorIndex"],
        )

    def _deserialize_milestone_available_quest(
        self, payload: typedefs.JsonObject
    ) -> milestones.MilestoneQuest:
        return milestones.MilestoneQuest(
            item_hash=payload["questItemHash"],
            status=self._deserialize_milestone_quest_status(payload["status"]),
        )

    def _deserialize_milestone_activity(
        self, payload: typedefs.JsonObject
    ) -> milestones.MilestoneActivity:

        phases: typing.Optional[
            collections.Sequence[milestones.MilestoneActivityPhase]
        ] = None
        if raw_phases := payload.get("phases"):
            phases = [
                milestones.MilestoneActivityPhase(
                    is_completed=obj["complete"], hash=obj["phaseHash"]
                )
                for obj in raw_phases
            ]

        return milestones.MilestoneActivity(
            hash=payload["activityHash"],
            challenges=[
                self.deserialize_objectives(obj["objective"])
                for obj in payload["challenges"]
            ],
            modifier_hashes=payload.get("modifierHashes"),
            boolean_options=payload.get("booleanActivityOptions"),
            phases=phases,
        )

    def _deserialize_milestone_quest_status(
        self, payload: typedefs.JsonObject
    ) -> milestones.QuestStatus:
        return milestones.QuestStatus(
            net=self._net,
            quest_hash=payload["questHash"],
            step_hash=payload["stepHash"],
            step_objectives=[
                self.deserialize_objectives(objective)
                for objective in payload["stepObjectives"]
            ],
            is_tracked=payload["tracked"],
            is_completed=payload["completed"],
            started=payload["started"],
            item_instance_id=payload["itemInstanceId"],
            vendor_hash=payload.get("vendorHash"),
            is_redeemed=payload["redeemed"],
        )

    def _deserialize_milestone_rewards(
        self, payload: typedefs.JsonObject
    ) -> milestones.MilestoneReward:
        return milestones.MilestoneReward(
            category_hash=payload["rewardCategoryHash"],
            entries=[
                milestones.MilestoneRewardEntry(
                    entry_hash=entry["rewardEntryHash"],
                    is_earned=entry["earned"],
                    is_redeemed=entry["redeemed"],
                )
                for entry in payload["entries"]
            ],
        )

    def deserialize_milestone(
        self, payload: typedefs.JsonObject
    ) -> milestones.Milestone:
        start_date: typing.Optional[datetime.datetime] = None
        if raw_start_date := payload.get("startDate"):
            start_date = time.clean_date(raw_start_date)

        end_date: typing.Optional[datetime.datetime] = None
        if raw_end_date := payload.get("endDate"):
            end_date = time.clean_date(raw_end_date)

        rewards: typing.Optional[
            collections.Collection[milestones.MilestoneReward]
        ] = None
        if raw_rewards := payload.get("rewards"):
            rewards = [
                self._deserialize_milestone_rewards(reward) for reward in raw_rewards
            ]

        activities: typing.Optional[
            collections.Sequence[milestones.MilestoneActivity]
        ] = None
        if raw_activities := payload.get("activities"):
            activities = [
                self._deserialize_milestone_activity(active)
                for active in raw_activities
            ]

        quests: typing.Optional[collections.Sequence[milestones.MilestoneQuest]] = None
        if raw_quests := payload.get("availableQuests"):
            quests = [
                self._deserialize_milestone_available_quest(quest)
                for quest in raw_quests
            ]

        vendors: typing.Optional[
            collections.Sequence[milestones.MilestoneVendor]
        ] = None
        if raw_vendors := payload.get("vendors"):
            vendors = [
                milestones.MilestoneVendor(
                    vendor_hash=vendor["vendorHash"],
                    preview_itemhash=vendor.get("previewItemHash"),
                )
                for vendor in raw_vendors
            ]

        return milestones.Milestone(
            hash=payload["milestoneHash"],
            start_date=start_date,
            end_date=end_date,
            order=payload["order"],
            rewards=rewards,
            available_quests=quests,
            activities=activities,
            vendors=vendors,
        )

    def _deserialize_artifact_tiers(
        self, payload: typedefs.JsonObject
    ) -> season.ArtifactTier:
        return season.ArtifactTier(
            hash=payload["tierHash"],
            is_unlocked=payload["isUnlocked"],
            points_to_unlock=payload["pointsToUnlock"],
            items=[
                season.ArtifactTierItem(
                    hash=item["itemHash"], is_active=item["isActive"]
                )
                for item in payload["items"]
            ],
        )

    def deserialize_characters(
        self, payload: typedefs.JsonObject
    ) -> collections.Mapping[int, character.Character]:
        return {
            int(char_id): self._set_character_attrs(char)
            for char_id, char in payload["data"].items()
        }

    def deserialize_character(
        self, payload: typedefs.JsonObject
    ) -> character.Character:
        return self._set_character_attrs(payload)

    def deserialize_character_equipmnets(
        self, payload: typedefs.JsonObject
    ) -> collections.Mapping[int, collections.Sequence[profile.ProfileItemImpl]]:
        return {
            int(char_id): self.deserialize_profile_items(item)
            for char_id, item in payload["data"].items()
        }

    def deserialize_character_activities(
        self, payload: typedefs.JsonObject
    ) -> collections.Mapping[int, activity.CharacterActivity]:
        return {
            int(char_id): self.deserialize_character_activity(data)
            for char_id, data in payload["data"].items()
        }

    def deserialize_characters_render_data(
        self, payload: typedefs.JsonObject
    ) -> collections.Mapping[int, character.RenderedData]:
        return {
            int(char_id): self.deserialize_character_render_data(data)
            for char_id, data in payload["data"].items()
        }

    def deserialize_progressions(
        self, payload: typedefs.JsonObject
    ) -> character.CharacterProgression:
        progressions_ = {
            int(prog_id): self._deserialize_progressions(prog)
            for prog_id, prog in payload["progressions"].items()
        }

        factions = {
            int(faction_id): self._deserialize_factions(faction)
            for faction_id, faction in payload["factions"].items()
        }

        milestones_ = {
            int(milestone_hash): self.deserialize_milestone(milestone)
            for milestone_hash, milestone in payload["milestones"].items()
        }

        uninstanced_item_objectives = {
            int(item_hash): [self.deserialize_objectives(ins) for ins in obj]
            for item_hash, obj in payload["uninstancedItemObjectives"].items()
        }

        artifact = payload["seasonalArtifact"]
        seasonal_artifact = season.CharacterScopedArtifact(
            hash=artifact["artifactHash"],
            points_used=artifact["pointsUsed"],
            reset_count=artifact["resetCount"],
            tiers=[
                self._deserialize_artifact_tiers(tier) for tier in artifact["tiers"]
            ],
        )
        checklists = payload["checklists"]

        return character.CharacterProgression(
            progressions=progressions_,
            factions=factions,
            checklists=checklists,
            milestones=milestones_,
            seasonal_artifact=seasonal_artifact,
            uninstanced_item_objectives=uninstanced_item_objectives,
        )

    def deserialize_character_progressions(
        self, payload: typedefs.JsonObject
    ) -> collections.Mapping[int, character.CharacterProgression]:
        character_progressions: collections.Mapping[
            int, character.CharacterProgression
        ] = {}
        for char_id, data in payload["data"].items():
            # A little hack to stop mypy complaining about Mapping <-> dict
            character_progressions[int(char_id)] = self.deserialize_progressions(data)  # type: ignore[index]
        return character_progressions

    def deserialize_characters_records(
        self,
        payload: typedefs.JsonObject,
        scores: typing.Optional[records.RecordScores] = None,
        record_hashes: typing.Optional[list[int]] = None,
    ) -> collections.Mapping[int, records.CharacterRecord]:

        return {
            int(rec_id): self.deserialize_character_records(
                rec, record_hashes=payload.get("featuredRecordHashes")
            )
            for rec_id, rec in payload["records"].items()
        }

    def deserialize_profile_records(
        self, payload: typedefs.JsonObject
    ) -> collections.Mapping[int, records.Record]:
        raw_profile_records = payload["data"]
        scores = records.RecordScores(
            current_score=raw_profile_records["score"],
            legacy_score=raw_profile_records["legacyScore"],
            lifetime_score=raw_profile_records["lifetimeScore"],
        )
        return {
            int(record_id): self.deserialize_records(
                record,
                scores,
                categories_hash=raw_profile_records["recordCategoriesRootNodeHash"],
                seals_hash=raw_profile_records["recordSealsRootNodeHash"],
            )
            for record_id, record in raw_profile_records["records"].items()
        }

    def deserialize_components(  # noqa: C901 Too complex.
        self, payload: typedefs.JsonObject
    ) -> components.Component:

        profile_: typing.Optional[profile.Profile] = None
        if raw_profile := payload.get("profile"):
            profile_ = self.deserialize_profile(raw_profile)

        profile_progression: typing.Optional[profile.ProfileProgression] = None
        if raw_profile_progression := payload.get("profileProgression"):
            profile_progression = self.deserialize_profile_progression(
                raw_profile_progression
            )

        profile_currencies: typing.Optional[
            collections.Sequence[profile.ProfileItemImpl]
        ] = None
        if raw_profile_currencies := payload.get("profileCurrencies"):

            try:
                profile_currencies = self.deserialize_profile_items(
                    raw_profile_currencies["data"]
                )
            except KeyError:
                pass

        profile_inventories: typing.Optional[
            collections.Sequence[profile.ProfileItemImpl]
        ] = None
        if raw_profile_inventories := payload.get("profileInventory"):
            try:
                profile_inventories = self.deserialize_profile_items(
                    raw_profile_inventories["data"]
                )
            except KeyError:
                pass

        profile_records: typing.Optional[
            collections.Mapping[int, records.Record]
        ] = None

        if raw_profile_records_ := payload.get("profileRecords"):
            profile_records = self.deserialize_profile_records(raw_profile_records_)

        characters: typing.Optional[typing.Mapping[int, character.Character]] = None
        if raw_characters := payload.get("characters"):
            characters = self.deserialize_characters(raw_characters)

        character_records: typing.Optional[
            collections.Mapping[int, records.CharacterRecord]
        ] = None

        if raw_character_records := payload.get("characterRecords"):
            # Had to do it in two steps..
            to_update: typedefs.JsonObject = {}
            for _, data in raw_character_records["data"].items():
                for record_id, record in data.items():
                    to_update[record_id] = record

            character_records = {
                int(rec_id): self.deserialize_character_records(
                    rec, record_hashes=to_update.get("featuredRecordHashes")
                )
                for rec_id, rec in to_update["records"].items()
            }

        character_equipments: typing.Optional[
            collections.Mapping[int, collections.Sequence[profile.ProfileItemImpl]]
        ] = None
        if raw_character_equips := payload.get("characterEquipment"):
            character_equipments = self.deserialize_character_equipmnets(
                raw_character_equips
            )

        character_inventories: typing.Optional[
            collections.Mapping[int, collections.Sequence[profile.ProfileItemImpl]]
        ] = None
        if raw_character_inventories := payload.get("characterInventories"):
            try:
                character_inventories = self.deserialize_character_equipmnets(
                    raw_character_inventories
                )
            except KeyError:
                pass

        character_activities: typing.Optional[
            collections.Mapping[int, activity.CharacterActivity]
        ] = None
        if raw_char_acts := payload.get("characterActivities"):
            character_activities = self.deserialize_character_activities(raw_char_acts)

        character_render_data: typing.Optional[
            collections.Mapping[int, character.RenderedData]
        ] = None
        if raw_character_render_data := payload.get("characterRenderData"):
            character_render_data = self.deserialize_characters_render_data(
                raw_character_render_data
            )

        character_progressions: typing.Optional[
            collections.Mapping[int, character.CharacterProgression]
        ] = None

        if raw_character_progressions := payload.get("characterProgressions"):
            character_progressions = self.deserialize_character_progressions(
                raw_character_progressions
            )

        profile_string_vars: typing.Optional[collections.Mapping[int, int]] = None
        if raw_profile_string_vars := payload.get("profileStringVariables"):
            profile_string_vars = raw_profile_string_vars["data"]["integerValuesByHash"]

        character_string_vars: typing.Optional[
            collections.Mapping[int, collections.Mapping[int, int]]
        ] = None
        if raw_character_string_vars := payload.get("characterStringVariables"):
            character_string_vars = {
                int(char_id): data["integerValuesByHash"]
                for char_id, data in raw_character_string_vars["data"].items()
            }

        metrics: typing.Optional[
            collections.Sequence[
                collections.Mapping[int, tuple[bool, records.Objective]]
            ]
        ] = None
        root_node_hash: typing.Optional[int] = None
        if raw_metrics := payload.get("metrics"):
            root_node_hash = raw_metrics["data"]["metricsRootNodeHash"]
            metrics = [
                {
                    int(metrics_hash): (
                        data["invisible"],
                        self.deserialize_objectives(data["objectiveProgress"]),
                    )
                    for metrics_hash, data in raw_metrics["data"]["metrics"].items()
                }
            ]

        return components.Component(
            profiles=profile_,
            profile_progression=profile_progression,
            profile_currencies=profile_currencies,
            profile_inventories=profile_inventories,
            profile_records=profile_records,
            characters=characters,
            character_records=character_records,
            character_equipments=character_equipments,
            character_inventories=character_inventories,
            character_activities=character_activities,
            character_render_data=character_render_data,
            character_progressions=character_progressions,
            profile_string_variables=profile_string_vars,
            character_string_variables=character_string_vars,
            metrics=metrics,
            root_node_hash=root_node_hash,
        )

    def deserialize_character_component(  # type: ignore[call-arg]
        self, payload: typedefs.JsonObject
    ) -> components.CharacterComponent:

        character_: typing.Optional[character.Character] = None
        if raw_singuler_character := payload.get("character"):
            character_ = self.deserialize_character(raw_singuler_character["data"])

        inventory: typing.Optional[collections.Sequence[profile.ProfileItemImpl]] = None
        if raw_inventory := payload.get("inventory"):
            try:
                inventory = self.deserialize_profile_items(raw_inventory["data"])
            except KeyError:
                pass

        activities: typing.Optional[activity.CharacterActivity] = None
        if raw_activities := payload.get("activities"):
            activities = self.deserialize_character_activity(raw_activities["data"])

        equipment: typing.Optional[collections.Sequence[profile.ProfileItemImpl]] = None
        if raw_equipments := payload.get("equipment"):
            equipment = self.deserialize_profile_items(raw_equipments["data"])

        progressions_: typing.Optional[character.CharacterProgression] = None
        if raw_progressions := payload.get("progressions"):
            progressions_ = self.deserialize_progressions(raw_progressions["data"])

        render_data: typing.Optional[character.RenderedData] = None
        if raw_render_data := payload.get("renderData"):
            render_data = self.deserialize_character_render_data(
                raw_render_data["data"]
            )

        character_records: typing.Optional[
            collections.Mapping[int, records.CharacterRecord]
        ] = None
        if raw_char_records := payload.get("records"):
            character_records = self.deserialize_characters_records(
                raw_char_records["data"]
            )

        return components.CharacterComponent(
            activities=activities,
            equipment=equipment,
            inventory=inventory,
            progressions=progressions_,
            render_data=render_data,
            character=character_,
            character_records=character_records,
            profile_records=None,
        )

    def _set_entity_attrs(
        self, payload: typedefs.JsonObject, *, key: str = "displayProperties"
    ) -> entity.BaseEntity:
        name: undefined.UndefinedOr[str] = undefined.Undefined
        description: undefined.UndefinedOr[str] = undefined.Undefined
        icon: assets.MaybeImage = assets.Image.partial()

        if properties := payload[key]:
            if (raw_name := properties["name"]) is not typedefs.Unknown:
                name = raw_name
            if (raw_description := properties["description"]) is not typedefs.Unknown:
                description = raw_description
            if raw_icon := properties.get("icon"):
                icon = assets.Image(raw_icon)
            has_icon = properties["hasIcon"]

        return entity.BaseEntity(
            net=self._net,
            hash=payload["hash"],
            index=payload["index"],
            name=name,
            description=description,
            has_icon=has_icon,
            icon=icon,
        )

    def deserialize_inventory_entity(
        self, payload: typedefs.JsonObject, /
    ) -> entity.InventoryEntity:

        props = self._set_entity_attrs(payload)

        # Some entities have an inventory which
        # Includes its hash types.
        # Most entities has this
        # and for some it doesn't exists

        if (raw_inventory := payload.get("inventory", {})) is not None:
            inventory: typedefs.JsonObject = raw_inventory

        # Entity tier type. Most entities have a tier
        # and some doesn't exists so we have to check.

        bucket_type: int = inventory.get("bucketTypeHash", 0)

        tier: enums.ItemTier = enums.ItemTier(
            int(inventory.get("tierTypeHash", enums.ItemTier.NONE))
        )

        tier_name: str = inventory.get("tierTypeName", None)

        if (
            type_name := payload.get("itemTypeDisplayName", typedefs.Unknown)
        ) == typedefs.Unknown:
            type_name = undefined.Undefined

        if (about := payload.get("flavorText", typedefs.Unknown)) == typedefs.Unknown:
            about = undefined.Undefined

        if (
            raw_watermark := payload.get("iconWatermark", assets.Image.partial())
        ) is not None:
            water_mark: assets.Image = assets.Image(str(raw_watermark))

        if (
            raw_banner := payload.get("screenshot", assets.Image.partial())
        ) is not None:
            banner = assets.Image(str(raw_banner))

        damage: undefined.UndefinedOr[enums.DamageType] = undefined.Undefined
        if (raw_damage := payload.get("defaultDamageTypeHash")) is not None:
            damage = enums.DamageType(raw_damage)

        # Ignoring those two so mypy doesn't cry.
        summary_hash: int = 0
        if (raw_summary_hash := payload.get("summaryItemHash")) is not None:
            summary_hash: int = int(raw_summary_hash)  # type: ignore

        if (raw_stats := payload.get("stats", {})) is not None:
            stats: typedefs.JsonObject = raw_stats

        block = enums.AmmoType.NONE
        if (ammo := payload.get("equippingBlock")) is not None:
            block: enums.AmmoType = enums.AmmoType(ammo["ammoType"])  # type: ignore

        item_class: enums.Class = enums.Class(
            payload.get("classType", enums.Class.UNKNOWN)
        )

        return entity.InventoryEntity(
            net=self._net,
            name=props.name,
            description=props.description,
            hash=props.hash,
            index=props.index,
            icon=props.icon,
            has_icon=props.has_icon,
            water_mark=water_mark,
            banner=banner,
            about=about,
            type=payload.get("itemType", undefined.Undefined),
            bucket_type=bucket_type,
            tier=tier,
            tier_name=tier_name,
            type_name=type_name,
            sub_type=payload.get("itemSubType", undefined.Undefined),
            item_class=item_class,
            damage=damage,
            summary_hash=summary_hash,
            is_equippable=payload.get("equippable", False),
            stats=stats,
            ammo_type=block,
            lore_hash=payload.get("loreHash", None),
        )

    def deserialize_objective_entity(
        self, payload: typedefs.JsonObject, /
    ) -> entity.ObjectiveEntity:
        props = self._set_entity_attrs(payload)
        return entity.ObjectiveEntity(
            net=self._net,
            hash=props.hash,
            index=props.index,
            description=props.description,
            name=props.name,
            has_icon=props.has_icon,
            icon=props.icon,
            unlock_value_hash=payload["unlockValueHash"],
            completion_value=payload["completionValue"],
            scope=entity.GatingScope(payload["scope"]),
            location_hash=payload["locationHash"],
            allowed_negative_value=payload["allowNegativeValue"],
            allowed_value_change=payload["allowValueChangeWhenCompleted"],
            counting_downward=payload["isCountingDownward"],
            value_style=entity.ValueUIStyle(payload["valueStyle"]),
            progress_description=payload["progressDescription"],
            perks=payload["perks"],
            stats=payload["stats"],
            minimum_visibility=payload["minimumVisibilityThreshold"],
            allow_over_completion=payload["allowOvercompletion"],
            show_value_style=payload["showValueOnComplete"],
            display_only_objective=payload["isDisplayOnlyObjective"],
            complete_value_style=entity.ValueUIStyle(payload["completedValueStyle"]),
            progress_value_style=entity.ValueUIStyle(payload["inProgressValueStyle"]),
        )

    # TODO: Re-implement this.
    def deserialize_activity(
        self, payload: typedefs.JsonObject, /, *, limit: typing.Optional[int] = 1
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

    def deserialize_linked_profiles(
        self, payload: typedefs.JsonObject
    ) -> profile.LinkedProfile:
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
        self, payload: typedefs.JsonObject
    ) -> collections.Sequence[clans.ClanBanner]:
        banners_seq: typing.MutableSequence[clans.ClanBanner] = []
        if (banners := payload.get("clanBannerDecals")) is not None:
            for k, v in banners.items():
                banner_obj = clans.ClanBanner(
                    id=int(k),
                    foreground=assets.Image(
                        v.get("foregroundPath", assets.Image.partial())
                    ),
                    background=assets.Image(
                        v.get("backgroundPath", assets.Image.partial())
                    ),
                )
                banners_seq.append(banner_obj)
        return banners_seq

    def deserialize_public_milestone_content(
        self, payload: typedefs.JsonObject
    ) -> milestones.MilestoneContent:
        items_categoris: typedefs.NoneOr[milestones.MilestoneItems] = None
        if (raw_categories := payload.get("itemCategories")) is not None:
            for item in raw_categories:
                title = undefined.Undefined
                if (raw_title := item.get("title")) is not None:
                    if raw_title != typedefs.Unknown:
                        title = raw_title
                if (raw_hashes := item.get("itemHashes")) is not None:
                    hashes: collections.Sequence[int] = raw_hashes

                items_categoris = milestones.MilestoneItems(title=title, hashes=hashes)

        about = undefined.Undefined
        if (raw_about := payload["about"]) != typedefs.Unknown:
            about = raw_about

        status = undefined.Undefined
        if (raw_status := payload["status"]) != typedefs.Unknown:
            status = raw_status

        tips: typing.MutableSequence[undefined.UndefinedOr[str]] = []
        if (raw_tips := payload.get("tips")) is not None:
            for raw_tip in raw_tips:
                if raw_tip == typedefs.Unknown:
                    raw_tip = undefined.Undefined
                tips.append(raw_tip)

        return milestones.MilestoneContent(
            about=about, status=status, tips=tips, items=items_categoris
        )

    def deserialize_friend(self, payload: typedefs.JsonObject, /) -> friends.Friend:
        name = undefined.Undefined
        if (raw_name := payload["bungieGlobalDisplayName"]) != typedefs.Unknown:
            name = raw_name

        bungie_user: typedefs.NoneOr[user.BungieUser] = None

        if raw_bungie_user := payload.get("bungieNetUser"):
            bungie_user = self.deserialize_bungie_user(raw_bungie_user)

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
        self, payload: typedefs.JsonObject
    ) -> collections.Sequence[friends.Friend]:
        mut_seq: typing.MutableSequence[friends.Friend] = []
        if raw_friends := payload.get("friends"):
            for friend in raw_friends:
                mut_seq.append(self.deserialize_friend(friend))
        return mut_seq

    def deserialize_friend_requests(
        self, payload: typedefs.JsonObject
    ) -> friends.FriendRequestView:
        incoming: typing.MutableSequence[friends.Friend] = []
        outgoing: typing.MutableSequence[friends.Friend] = []

        if raw_incoming_requests := payload.get("incomingRequests"):
            for incoming_request in raw_incoming_requests:
                incoming.append(self.deserialize_friend(incoming_request))

        if raw_outgoing_requests := payload.get("outgoingRequests"):
            for outgoing_request in raw_outgoing_requests:
                outgoing.append(self.deserialize_friend(outgoing_request))

        return friends.FriendRequestView(incoming=incoming, outgoing=outgoing)

    def _set_fireteam_fields(self, payload: typedefs.JsonObject) -> fireteams.Fireteam:
        activity_type = payload["activityType"]
        try:
            activity_type = fireteams.FireteamActivity(payload["activityType"])
        except ValueError:
            pass
        return fireteams.Fireteam(
            id=int(payload["fireteamId"]),
            group_id=int(payload["groupId"]),
            platform=fireteams.FireteamPlatform(payload["platform"]),
            is_immediate=payload["isImmediate"],
            activity_type=activity_type,
            owner_id=int(payload["ownerMembershipId"]),
            player_slot_count=payload["playerSlotCount"],
            available_player_slots=payload["availablePlayerSlotCount"],
            available_alternate_slots=payload["availableAlternateSlotCount"],
            title=payload["title"],
            date_created=time.clean_date(payload["dateCreated"]),
            is_public=payload["isPublic"],
            locale=fireteams.FireteamLanguage(payload["locale"]),
            is_valid=payload["isValid"],
            last_modified=time.clean_date(payload["datePlayerModified"]),
            total_results=payload.get("totlaResults", 0),
        )

    def deserialize_fireteams(
        self, payload: typedefs.JsonObject
    ) -> typedefs.NoneOr[collections.Sequence[fireteams.Fireteam]]:
        fireteams_: typing.MutableSequence[fireteams.Fireteam] = []

        result: list[typedefs.JsonObject]
        if (result := payload["results"]) is not None:
            for elem in result:
                fireteams_.append(self._set_fireteam_fields(elem))
        else:
            return None
        return fireteams_

    def deserialize_fireteam_destiny_users(
        self, payload: typedefs.JsonObject
    ) -> fireteams.FireteamUser:
        destiny_obj = self.deserialize_destiny_user(payload)
        # We could helpers.just return a DestinyUser object but this is
        # missing the fireteam display name and id fields.
        return fireteams.FireteamUser(
            net=self._net,
            id=destiny_obj.id,
            code=destiny_obj.code,
            icon=destiny_obj.icon,
            types=destiny_obj.types,
            type=destiny_obj.type,
            is_public=destiny_obj.is_public,
            crossave_override=destiny_obj.crossave_override,
            name=destiny_obj.name,
            last_seen_name=destiny_obj.last_seen_name,
            fireteam_display_name=payload["FireteamDisplayName"],
            fireteam_membership_id=enums.MembershipType(
                payload["FireteamMembershipType"]
            ),
        )

    def deserialize_fireteam_members(
        self, payload: typedefs.JsonObject, *, alternatives: bool = False
    ) -> typing.Optional[collections.Sequence[fireteams.FireteamMember]]:
        members_: list[fireteams.FireteamMember] = []
        if members := payload.get("Members" if not alternatives else "Alternates"):
            for member in members:
                bungie_fields = self.deserialize_partial_bungie_user(member)
                members_fields = fireteams.FireteamMember(
                    destiny_user=self.deserialize_fireteam_destiny_users(member),
                    has_microphone=member["hasMicrophone"],
                    character_id=int(member["characterId"]),
                    date_joined=time.clean_date(member["dateJoined"]),
                    last_platform_invite_date=time.clean_date(
                        member["lastPlatformInviteAttemptDate"]
                    ),
                    last_platform_invite_result=int(
                        member["lastPlatformInviteAttemptResult"]
                    ),
                    net=self._net,
                    name=bungie_fields.name,
                    id=bungie_fields.id,
                    icon=bungie_fields.icon,
                    is_public=bungie_fields.is_public,
                    crossave_override=bungie_fields.crossave_override,
                    types=bungie_fields.types,
                    type=bungie_fields.type,
                )
                members_.append(members_fields)
        else:
            return None
        return members_

    def deserialize_available_fireteams(
        self,
        data: typedefs.JsonObject,
        *,
        no_results: bool = False,
    ) -> typing.Union[
        fireteams.AvalaibleFireteam, collections.Sequence[fireteams.AvalaibleFireteam]
    ]:
        fireteams_: list[fireteams.AvalaibleFireteam] = []

        # This needs to be used outside the results
        # JSON key.
        if no_results is True:
            payload = data

        if result := payload.get("results"):

            for fireteam in result:
                found_fireteams = self._set_fireteam_fields(fireteam["Summary"])
                fireteams_fields = fireteams.AvalaibleFireteam(
                    id=found_fireteams.id,
                    group_id=found_fireteams.group_id,
                    platform=found_fireteams.platform,
                    activity_type=found_fireteams.activity_type,
                    is_immediate=found_fireteams.is_immediate,
                    is_public=found_fireteams.is_public,
                    is_valid=found_fireteams.is_valid,
                    owner_id=found_fireteams.owner_id,
                    player_slot_count=found_fireteams.player_slot_count,
                    available_player_slots=found_fireteams.available_player_slots,
                    available_alternate_slots=found_fireteams.available_alternate_slots,
                    title=found_fireteams.title,
                    date_created=found_fireteams.date_created,
                    locale=found_fireteams.locale,
                    last_modified=found_fireteams.last_modified,
                    total_results=found_fireteams.total_results,
                    members=self.deserialize_fireteam_members(payload),
                    alternatives=self.deserialize_fireteam_members(
                        payload, alternatives=True
                    ),
                )
            fireteams_.append(fireteams_fields)
            if no_results:
                return fireteams_fields
        return fireteams_

    def deserialize_seasonal_artifact(
        self, payload: typedefs.JsonObject
    ) -> season.Artifact:
        if raw_artifact := payload.get("seasonalArtifact"):
            if points := raw_artifact.get("pointProgression"):
                points_prog = progressions.Progression(
                    hash=points["progressionHash"],
                    level=points["level"],
                    cap=points["levelCap"],
                    daily_limit=points["dailyLimit"],
                    weekly_limit=points["weeklyLimit"],
                    current_progress=points["currentProgress"],
                    daily_progress=points["dailyProgress"],
                    needed=points["progressToNextLevel"],
                    next_level=points["nextLevelAt"],
                )

            if bonus := raw_artifact.get("powerBonusProgression"):
                power_bonus_prog = progressions.Progression(
                    hash=bonus["progressionHash"],
                    level=bonus["level"],
                    cap=bonus["levelCap"],
                    daily_limit=bonus["dailyLimit"],
                    weekly_limit=bonus["weeklyLimit"],
                    current_progress=bonus["currentProgress"],
                    daily_progress=bonus["dailyProgress"],
                    needed=bonus["progressToNextLevel"],
                    next_level=bonus["nextLevelAt"],
                )
            artifact = season.Artifact(
                net=self._net,
                hash=raw_artifact["artifactHash"],
                power_bonus=raw_artifact["powerBonus"],
                acquired_points=raw_artifact["pointsAcquired"],
                bonus=power_bonus_prog,
                points=points_prog,
            )
        return artifact

    def deserialize_profile_progression(
        self, payload: typedefs.JsonObject
    ) -> profile.ProfileProgression:
        return profile.ProfileProgression(
            artifact=self.deserialize_seasonal_artifact(payload["data"]),
            checklist={
                int(check_id): checklists
                for check_id, checklists in payload["data"]["checklists"].items()
            },
        )
