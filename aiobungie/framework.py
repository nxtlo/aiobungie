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

"""Implementation of the library's deserialization framework.

* `Framework` Is the default deserialization framework that's used within client impl's.
* `Global` Is a pre-initialized instance of `Framework` that can be used at any scope.
"""

from __future__ import annotations

__all__ = ("Framework", "Global")

import typing

import sain

from aiobungie import api, builders, typedefs
from aiobungie.crates import (
    activity,
    application,
    character,
    clans,
    components,
    entity,
    fireteams,
    friends,
    items,
    milestones,
    profile,
    progressions,
    records,
    season,
    user,
)
from aiobungie.internal import enums, time

if typing.TYPE_CHECKING:
    import collections.abc as collections
    import datetime

    # from aiobungie import traits


class Framework(api.Framework):
    """The base deserialization framework implementation.

    This framework is used to deserialize JSON responses from the REST client and turning them into a `aiobungie.crates` Python classes.

    Example
    --------
    ```py
    import aiobungie

    from aiobungie import traits
    from aiobungie import framework

    class MyClient(traits.Deserialize):
        def __init__(self) -> None:
            self.rest = aiobungie.RESTClient("token")
            self.my_name = "Fate怒"
            self.my_code = 4275

        @property # required method.
        def framework(self) -> framework.Empty:
            return framework.Global

        async def my_memberships(self):
            response = await self.rest.fetch_membership(self.my_name, self.my_code)
            return self.factory.deserialize_destiny_memberships(response)

    async def main() -> None:
        client = MyClient()
        async with client.rest:
            print(await client.my_memberships())

    asyncio.run(main())
    ```
    """

    __slots__ = ()

    def __init__(self) -> None:
        super().__init__()

    def deserialize_bungie_user(self, data: typedefs.JSONObject) -> user.BungieUser:
        return user.BungieUser(
            id=int(data["membershipId"]),
            created_at=time.clean_date(data["firstAccess"]),
            name=data.get("cachedBungieGlobalDisplayName"),
            is_deleted=data["isDeleted"],
            about=data["about"],
            updated_at=time.clean_date(data["lastUpdate"]),
            psn_name=data.get("psnDisplayName", None),
            stadia_name=data.get("stadiaDisplayName", None),
            steam_name=data.get("steamDisplayName", None),
            twitch_name=data.get("twitchDisplayName", None),
            blizzard_name=data.get("blizzardDisplayName", None),
            egs_name=data.get("egsDisplayName", None),
            status=data["statusText"],
            locale=data["locale"],
            picture=builders.Image(path=data["profilePicturePath"]),
            code=data.get("cachedBungieGlobalDisplayNameCode", None),
            unique_name=data.get("uniqueName", None),
            theme_id=int(data["profileTheme"]),
            show_activity=bool(data["showActivity"]),
            theme_name=data["profileThemeName"],
            display_title=data["userTitleDisplay"],
            profile_ban_expire=time.clean_date(data["profileBanExpire"])
            if "profileBanExpire" in data
            else None,
        )

    def deserialize_partial_bungie_user(
        self, payload: typedefs.JSONObject
    ) -> user.PartialBungieUser:
        return user.PartialBungieUser(
            types=tuple(
                enums.MembershipType(type_)
                for type_ in payload.get("applicableMembershipTypes", ())
            ),
            name=payload["bungieGlobalDisplayName"]
            if "bungieGlobalDisplayName" in payload
            else payload.get("displayName"),
            id=int(payload["membershipId"]),
            crossave_override=enums.MembershipType(payload["crossSaveOverride"]),
            is_public=payload["isPublic"],
            icon=builders.Image(path=payload.get("iconPath", "")),
            type=enums.MembershipType(payload["membershipType"]),
            code=payload.get("bungieGlobalDisplayNameCode"),
        )

    def deserialize_destiny_membership(
        self, payload: typedefs.JSONObject
    ) -> user.DestinyMembership:
        name: str | None = None
        if (raw_name := payload.get("bungieGlobalDisplayName")) is not None:
            name = typedefs.unknown(raw_name)

        return user.DestinyMembership(
            id=int(payload["membershipId"]),
            name=name,
            code=payload.get("bungieGlobalDisplayNameCode", None),
            last_seen_name=payload.get("LastSeenDisplayName")
            or payload.get("displayName")  # noqa: W503
            or "",  # noqa: W503
            type=enums.MembershipType(payload["membershipType"]),
            is_public=payload["isPublic"],
            crossave_override=enums.MembershipType(payload["crossSaveOverride"]),
            icon=builders.Image(path=payload.get("iconPath", "")),
            types=tuple(
                enums.MembershipType(type_)
                for type_ in payload.get("applicableMembershipTypes", ())
            ),
        )

    def deserialize_destiny_memberships(
        self, data: typedefs.JSONArray
    ) -> collections.Sequence[user.DestinyMembership]:
        return tuple(
            self.deserialize_destiny_membership(membership) for membership in data
        )

    def deserialize_user(self, data: typedefs.JSONObject) -> user.User:
        primary_membership_id: int | None = None
        if raw_primary_id := data.get("primaryMembershipId"):
            primary_membership_id = int(raw_primary_id)

        return user.User(
            bungie_user=self.deserialize_bungie_user(data["bungieNetUser"]),
            memberships=self.deserialize_destiny_memberships(
                data["destinyMemberships"]
            ),
            primary_membership_id=primary_membership_id,
        )

    def deserialize_sanitized_membership(
        self, payload: typedefs.JSONObject
    ) -> user.SanitizedMembership:
        return user.SanitizedMembership(
            epic_games=payload.get("EgsId"),
            psn=payload.get("PsnId"),
            steam=payload.get("SteamId"),
            xbox=payload.get("XboxId"),
            twitch=payload.get("TwitchId"),
        )

    def deserialize_searched_user(
        self, payload: typedefs.JSONObject
    ) -> user.SearchableDestinyUser:
        code: int | None = None
        if raw_code := payload.get("bungieGlobalDisplayNameCode"):
            code = int(raw_code)

        bungie_id: int | None = None
        if raw_bungie_id := payload.get("bungieNetMembershipId"):
            bungie_id = int(raw_bungie_id)

        return user.SearchableDestinyUser(
            name=typedefs.unknown(payload["bungieGlobalDisplayName"]),
            code=code,
            bungie_id=bungie_id,
            memberships=self.deserialize_destiny_memberships(
                payload["destinyMemberships"]
            ),
        )

    def deserialize_user_credentials(
        self, payload: typedefs.JSONArray
    ) -> collections.Sequence[user.UserCredentials]:
        return tuple(
            user.UserCredentials(
                type=enums.CredentialType(int(credit["credentialType"])),
                display_name=credit["credentialDisplayName"],
                is_public=credit["isPublic"],
                self_as_string=credit.get("credentialAsString"),
            )
            for credit in payload
        )

    def deserialize_user_themes(
        self, payload: typedefs.JSONArray
    ) -> collections.Sequence[user.UserThemes]:
        return tuple(
            user.UserThemes(
                id=int(entry["userThemeId"]),
                name=entry["userThemeName"] if "userThemeName" in entry else None,
                description=entry["userThemeDescription"]
                if "userThemeDescription" in entry
                else None,
            )
            for entry in payload
        )

    def deserialize_group(self, payload: typedefs.JSONObject) -> clans.Group:
        clan_info_obj: typedefs.JSONObject | None = None
        if raw_clan_info := payload.get("clanInfo"):
            clan_info_obj = clans.ClanInfo(
                call_sign=raw_clan_info["clanCallsign"],
                banner_data=raw_clan_info["clanBannerData"],
            )
        return clans.Group(
            group_id=int(payload["groupId"]),
            name=payload["name"],
            creation_date=time.clean_date(payload["creationDate"]),
            about=payload["about"],
            clan_info=clan_info_obj,
            motto=payload.get("motto"),
            member_count=int(payload["memberCount"]),
            locale=payload["locale"],
            membership_option=int(payload["membershipOption"]),
            capabilities=int(payload["capabilities"]),
            remote_group_id=int(payload["remoteGroupId"])
            if "remoteGroupId" in payload
            else None,
            group_type=enums.GroupType(int(payload["groupType"])),
            avatar_path=builders.Image(payload["avatarPath"]),
            theme=payload["theme"],
        )

    def _deserialize_group_details(
        self,
        data: typedefs.JSONObject,
        current_user_memberships: collections.Mapping[str, clans.ClanMember]
        | None = None,
        clan_founder: clans.ClanMember | None = None,
    ) -> clans.Clan:
        features = data["features"]
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
        information: typedefs.JSONObject = data["clanInfo"]
        progression: collections.Mapping[int, progressions.Progression] = {
            int(prog_hash): self.deserialize_progressions(prog)
            for prog_hash, prog in information["d2ClanProgressions"].items()
        }

        return clans.Clan(
            id=int(data["groupId"]),
            name=data["name"],
            type=enums.GroupType(data["groupType"]),
            created_at=time.clean_date(data["creationDate"]),
            member_count=data["memberCount"],
            motto=data["motto"],
            about=data["about"],
            is_public=data["isPublic"],
            banner=builders.Image(path=data["bannerPath"]),
            avatar=builders.Image(path=data["avatarPath"]),
            tags=tuple(data["tags"]),
            features=features_obj,
            owner=clan_founder,
            progressions=progression,
            call_sign=information["clanCallsign"],
            banner_data=information["clanBannerData"],
            chat_security=data["chatSecurity"],
            conversation_id=int(data["conversationId"]),
            allow_chat=data["allowChat"],
            theme=data["theme"],
            current_user_membership=current_user_memberships,
        )

    def deserialize_clan(self, payload: typedefs.JSONObject) -> clans.Clan:
        current_user_map: collections.Mapping[str, clans.ClanMember] | None = None
        if raw_current_user := payload.get("currentUserMemberMap"):
            # This will get populated if only it was a GroupsV2.GroupResponse.
            # GroupsV2.GetGroupsForMemberResponse doesn't have this field.
            current_user_map = {
                membership_type: self.deserialize_clan_member(membership)
                for membership_type, membership in raw_current_user.items()
            }

        return self._deserialize_group_details(
            data=payload["detail"],
            clan_founder=self.deserialize_clan_member(payload["founder"]),
            current_user_memberships=current_user_map,
        )

    def deserialize_clan_member(self, data: typedefs.JSONObject, /) -> clans.ClanMember:
        destiny_user = self.deserialize_destiny_membership(data["destinyUserInfo"])
        return clans.ClanMember(
            last_seen_name=destiny_user.last_seen_name,
            id=destiny_user.id,
            name=destiny_user.name,
            icon=destiny_user.icon,
            last_online=time.from_timestamp(int(data["lastOnlineStatusChange"])),
            group_id=int(data["groupId"]),
            joined_at=time.clean_date(data["joinDate"]),
            types=destiny_user.types,
            is_public=destiny_user.is_public,
            type=destiny_user.type,
            code=destiny_user.code,
            is_online=data["isOnline"],
            crossave_override=destiny_user.crossave_override,
            bungie_user=self.deserialize_partial_bungie_user(data["bungieNetUserInfo"])
            if "bungieNetUserInfo" in data
            else None,
            member_type=enums.ClanMemberType(int(data["memberType"])),
        )

    def deserialize_clan_members(
        self, data: typedefs.JSONObject, /
    ) -> sain.Iterator[clans.ClanMember]:
        return sain.Iter(
            self.deserialize_clan_member(member) for member in data["results"]
        )

    def deserialize_group_member(
        self, payload: typedefs.JSONObject
    ) -> clans.GroupMember:
        member = payload["member"]
        return clans.GroupMember(
            join_date=time.clean_date(member["joinDate"]),
            group_id=int(member["groupId"]),
            member_type=enums.ClanMemberType(member["memberType"]),
            is_online=member["isOnline"],
            last_online=time.from_timestamp(int(member["lastOnlineStatusChange"])),
            inactive_memberships=payload.get("areAllMembershipsInactive", None),
            member=self.deserialize_destiny_membership(member["destinyUserInfo"]),
            group=self._deserialize_group_details(payload["group"]),
        )

    def _deserialize_clan_conversation(
        self, payload: typedefs.JSONObject
    ) -> clans.ClanConversation:
        return clans.ClanConversation(
            id=int(payload["conversationId"]),
            group_id=int(payload["groupId"]),
            name=typedefs.unknown(payload["chatName"]),
            chat_enabled=payload["chatEnabled"],
            security=payload["chatSecurity"],
        )

    def deserialize_clan_conversations(
        self, payload: typedefs.JSONArray
    ) -> collections.Sequence[clans.ClanConversation]:
        return tuple(self._deserialize_clan_conversation(conv) for conv in payload)

    def deserialize_application_member(
        self, payload: typedefs.JSONObject
    ) -> application.ApplicationMember:
        return application.ApplicationMember(
            api_eula_version=payload["apiEulaVersion"],
            role=payload["role"],
            user=self.deserialize_partial_bungie_user(payload["user"]),
        )

    def deserialize_application(
        self, payload: typedefs.JSONObject
    ) -> application.Application:
        return application.Application(
            id=int(payload["applicationId"]),
            name=payload["name"],
            origin=payload["origin"],
            link=payload["link"],
            status=payload["status"],
            redirect_url=payload.get("redirectUrl", None),
            created_at=time.clean_date(payload["creationDate"]),
            status_changed=time.clean_date(payload["statusChanged"]),
            published_at=time.clean_date(payload["firstPublished"]),
            team=tuple(
                self.deserialize_application_member(member)
                for member in payload["team"]
            ),
            scope=payload.get("scope"),
        )

    def _set_character_attrs(self, payload: typedefs.JSONObject) -> character.Character:
        if raw_emblem_color := payload.get("emblemColor"):
            emblem_color: tuple[int, int, int, int] = (
                int(raw_emblem_color["red"]),
                int(raw_emblem_color["green"]),
                int(raw_emblem_color["blue"]),
                int(raw_emblem_color["alpha"]),
            )
        else:
            emblem_color = (0, 0, 0, 0)

        return character.Character(
            id=int(payload["characterId"]),
            gender=enums.Gender(payload["genderType"]),
            race=enums.Race(payload["raceType"]),
            class_type=enums.Class(payload["classType"]),
            emblem=builders.Image(path=payload["emblemBackgroundPath"])
            if "emblemBackgroundPath" in payload
            else None,
            emblem_icon=builders.Image(path=payload["emblemPath"])
            if "emblemPath" in payload
            else None,
            emblem_hash=int(payload["emblemHash"]) if "emblemHash" in payload else None,
            last_played=time.clean_date(payload["dateLastPlayed"]),
            total_played_time=int(payload["minutesPlayedTotal"]),
            member_id=int(payload["membershipId"]),
            member_type=enums.MembershipType(payload["membershipType"]),
            level=payload["baseCharacterLevel"],
            title_hash=payload.get("titleRecordHash", None),
            light=payload["light"],
            stats={enums.Stat(int(k)): v for k, v in payload["stats"].items()},
            emblem_color=emblem_color,
            minutes_played_this_session=int(payload["minutesPlayedThisSession"])
            if "minutesPlayedThisSession" in payload
            else 0,
            percent_to_next_level=float(payload["percentToNextLevel"]),
        )

    def deserialize_profile(self, payload: typedefs.JSONObject, /) -> profile.Profile:
        return profile.Profile(
            user=self.deserialize_destiny_membership(payload["userInfo"]),
            last_played=time.clean_date(payload["dateLastPlayed"]),
            versions_owned=enums.GameVersions(int(payload["versionsOwned"])),
            character_ids=tuple(
                int(character_id) for character_id in payload["characterIds"]
            ),
            season_hashes=tuple(payload["seasonHashes"]),
            event_card_hashes=tuple(payload["eventCardHashesOwned"]),
            season_hash=payload["currentSeasonHash"],
            power_cap=payload["currentSeasonRewardPowerCap"],
            guardian_rank=payload["currentGuardianRank"],
            highest_guardian_rank=payload["lifetimeHighestGuardianRank"],
            renewed_guardian_rank=payload["renewedGuardianRank"],
        )

    def deserialize_profile_item(
        self, payload: typedefs.JSONObject
    ) -> profile.ProfileItemImpl:
        instance_id: int | None = None
        if raw_instance_id := payload.get("itemInstanceId"):
            instance_id = int(raw_instance_id)

        version_number: int | None = None
        if raw_version := payload.get("versionNumber"):
            version_number = int(raw_version)

        transfer_status = enums.TransferStatus(payload["transferStatus"])

        return profile.ProfileItemImpl(
            hash=payload["itemHash"],
            quantity=payload["quantity"],
            bind_status=enums.ItemBindStatus(payload["bindStatus"]),
            location=enums.ItemLocation(payload["location"]),
            bucket=payload["bucketHash"],
            transfer_status=transfer_status,
            lockable=payload["lockable"],
            state=enums.ItemState(payload["state"]),
            dismantle_permissions=payload["dismantlePermission"],
            is_wrapper=payload["isWrapper"],
            instance_id=instance_id,
            version_number=version_number,
            ornament_id=payload.get("overrideStyleItemHash"),
        )

    def deserialize_objectives(self, payload: typedefs.JSONObject) -> records.Objective:
        return records.Objective(
            hash=payload["objectiveHash"],
            visible=payload["visible"],
            complete=payload["complete"],
            completion_value=payload["completionValue"],
            progress=payload.get("progress"),
            destination_hash=payload.get("destinationHash"),
            activity_hash=payload.get("activityHash"),
        )

    # TODO: Remove **nodes and get it directly from the payload.
    def deserialize_records(
        self,
        payload: typedefs.JSONObject,
        scores: records.RecordScores | None = None,
        **nodes: int,
    ) -> records.Record:
        objectives: collections.Sequence[records.Objective] | None = None
        interval_objectives: collections.Sequence[records.Objective] | None = None
        record_state: records.RecordState | int

        record_state = records.RecordState(payload["state"])

        if raw_objs := payload.get("objectives"):
            objectives = tuple(self.deserialize_objectives(obj) for obj in raw_objs)

        if raw_interval_objs := payload.get("intervalObjectives"):
            interval_objectives = tuple(
                self.deserialize_objectives(obj) for obj in raw_interval_objs
            )

        return records.Record(
            scores=scores,
            categories_node_hash=nodes.get("categories_hash"),
            seals_node_hash=nodes.get("seals_hash"),
            state=record_state,
            objectives=objectives,
            interval_objectives=interval_objectives,
            redeemed_count=payload.get("intervalsRedeemedCount", 0),
            completion_times=payload.get("completedCount", None),
            reward_visibility=payload.get("rewardVisibility"),
        )

    def deserialize_character_records(
        self,
        payload: typedefs.JSONObject,
        scores: records.RecordScores | None = None,
        record_hashes: collections.Sequence[int] = (),
    ) -> records.CharacterRecord:
        record = self.deserialize_records(payload, scores)
        return records.CharacterRecord(
            scores=scores,
            categories_node_hash=record.categories_node_hash,
            seals_node_hash=record.seals_node_hash,
            state=record.state,
            objectives=record.objectives,
            interval_objectives=record.interval_objectives,
            redeemed_count=payload.get("intervalsRedeemedCount", 0),
            completion_times=payload.get("completedCount"),
            reward_visibility=payload.get("rewardVisibility"),
            record_hashes=record_hashes,
        )

    def deserialize_character_dye(self, payload: typedefs.JSONObject) -> character.Dye:
        return character.Dye(
            channel_hash=payload["channelHash"], dye_hash=payload["dyeHash"]
        )

    def deserialize_character_customization(
        self, payload: typedefs.JSONObject
    ) -> character.CustomizationOptions:
        return character.CustomizationOptions(
            personality=payload["personality"],
            face=payload["face"],
            skin_color=payload["skinColor"],
            lip_color=payload["lipColor"],
            eye_color=payload["eyeColor"],
            hair_colors=payload.get("hairColors", ()),
            feature_colors=payload.get("featureColors", ()),
            decal_color=payload["decalColor"],
            wear_helmet=payload["wearHelmet"],
            hair_index=payload["hairIndex"],
            feature_index=payload["featureIndex"],
            decal_index=payload["decalIndex"],
        )

    def deserialize_character_minimal_equipments(
        self, payload: typedefs.JSONObject
    ) -> character.MinimalEquipments:
        if raw_dyes := payload.get("dyes"):
            dyes = tuple(self.deserialize_character_dye(dye) for dye in raw_dyes)
        else:
            dyes = ()

        return character.MinimalEquipments(item_hash=payload["itemHash"], dyes=dyes)

    def deserialize_character_render_data(
        self, payload: typedefs.JSONObject, /
    ) -> character.RenderedData:
        return character.RenderedData(
            customization=self.deserialize_character_customization(
                payload["customization"]
            ),
            custom_dyes=tuple(
                self.deserialize_character_dye(dye)
                for dye in payload["customDyes"]
                if dye
            ),
            equipment=tuple(
                self.deserialize_character_minimal_equipments(equipment)
                for equipment in payload["peerView"]["equipment"]
            ),
        )

    def deserialize_available_activity(
        self, payload: typedefs.JSONObject
    ) -> activity.AvailableActivity:
        return activity.AvailableActivity(
            hash=payload["activityHash"],
            is_new=payload["isNew"],
            is_completed=payload["isCompleted"],
            is_visible=payload["isVisible"],
            display_level=payload.get("displayLevel"),
            recommended_light=payload.get("recommendedLight"),
            difficulty=activity.Difficulty(payload["difficultyTier"]),
            can_join=payload["canJoin"],
            can_lead=payload["canLead"],
        )

    def deserialize_character_activity(
        self, payload: typedefs.JSONObject
    ) -> activity.CharacterActivity:
        current_mode = enums.GameMode.NONE
        if raw_current_mode := payload.get("currentActivityModeType"):
            current_mode = enums.GameMode(raw_current_mode)

        if raw_current_modes := payload.get("currentActivityModeTypes"):
            current_mode_types = tuple(
                enums.GameMode(type_) for type_ in raw_current_modes
            )
        else:
            current_mode_types = ()

        return activity.CharacterActivity(
            date_started=time.clean_date(payload["dateActivityStarted"]),
            current_hash=payload["currentActivityHash"],
            current_mode_hash=payload["currentActivityModeHash"],
            current_mode=current_mode,
            current_mode_hashes=payload.get("currentActivityModeHashes", ()),
            current_mode_types=current_mode_types,
            current_playlist_hash=payload.get("currentPlaylistActivityHash"),
            last_story_hash=payload["lastCompletedStoryHash"],
            available_activities=tuple(
                self.deserialize_available_activity(activity_)
                for activity_ in payload["availableActivities"]
            ),
            available_activity_interactables=tuple(
                activity.InteractablesRef(
                    hash=interact["activityInteractableHash"],
                    element_index=interact["activityInteractableElementIndex"],
                )
                for interact in payload["availableActivityInteractables"]
            ),
        )

    def deserialize_profile_items(
        self, payload: typedefs.JSONObject, /
    ) -> collections.Sequence[profile.ProfileItemImpl]:
        return tuple(self.deserialize_profile_item(item) for item in payload["items"])

    def _deserialize_node(self, payload: typedefs.JSONObject) -> records.Node:
        return records.Node(
            state=int(payload["state"]),
            objective=self.deserialize_objectives(payload["objective"])
            if "objective" in payload
            else None,
            progress_value=int(payload["progressValue"]),
            completion_value=int(payload["completionValue"]),
            record_category_score=int(payload["recordCategoryScore"])
            if "recordCategoryScore" in payload
            else None,
        )

    @staticmethod
    def _deserialize_collectible(payload: typedefs.JSONObject) -> items.Collectible:
        recent_collectibles: collections.Collection[int] | None = None
        if raw_recent_collectibles := payload.get("recentCollectibleHashes"):
            recent_collectibles = tuple(
                int(item_hash) for item_hash in raw_recent_collectibles
            )

        collectibles: dict[int, int] = {}
        for item_hash, mapping in payload["collectibles"].items():
            collectibles[int(item_hash)] = int(mapping["state"])

        return items.Collectible(
            recent_collectibles=recent_collectibles,
            collectibles=collectibles,
            collection_category_hash=int(payload["collectionCategoriesRootNodeHash"]),
            collection_badges_hash=int(payload["collectionBadgesRootNodeHash"]),
        )

    @staticmethod
    def _deserialize_currencies(
        payload: typedefs.JSONObject,
    ) -> collections.Sequence[items.Currency]:
        return tuple(
            items.Currency(hash=int(item_hash), amount=int(amount))
            for item_hash, amount in payload["itemQuantities"].items()
        )

    def deserialize_progressions(
        self, payload: typedefs.JSONObject
    ) -> progressions.Progression:
        return progressions.Progression(
            hash=int(payload["progressionHash"]),
            level=int(payload["level"]),
            cap=int(payload["levelCap"]),
            daily_limit=int(payload["dailyLimit"]),
            weekly_limit=int(payload["weeklyLimit"]),
            current_progress=int(payload["currentProgress"]),
            daily_progress=int(payload["dailyProgress"]),
            needed=int(payload["progressToNextLevel"]),
            next_level=int(payload["nextLevelAt"]),
        )

    def _deserialize_factions(
        self, payload: typedefs.JSONObject
    ) -> progressions.Factions:
        progs = self.deserialize_progressions(payload)
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
        self, payload: typedefs.JSONObject
    ) -> milestones.MilestoneQuest:
        return milestones.MilestoneQuest(
            item_hash=payload["questItemHash"],
            status=self._deserialize_milestone_quest_status(payload["status"]),
        )

    def _deserialize_milestone_activity(
        self, payload: typedefs.JSONObject
    ) -> milestones.MilestoneActivity:
        phases: collections.Sequence[milestones.MilestoneActivityPhase] | None = None
        if raw_phases := payload.get("phases"):
            phases = tuple(
                milestones.MilestoneActivityPhase(
                    is_completed=obj["complete"], hash=obj["phaseHash"]
                )
                for obj in raw_phases
            )

        return milestones.MilestoneActivity(
            hash=payload["activityHash"],
            challenges=tuple(
                self.deserialize_objectives(obj["objective"])
                for obj in payload["challenges"]
            ),
            modifier_hashes=payload.get("modifierHashes"),
            boolean_options=payload.get("booleanActivityOptions"),
            phases=phases,
        )

    def _deserialize_milestone_quest_status(
        self, payload: typedefs.JSONObject
    ) -> milestones.QuestStatus:
        return milestones.QuestStatus(
            quest_hash=payload["questHash"],
            step_hash=payload["stepHash"],
            step_objectives=tuple(
                self.deserialize_objectives(objective)
                for objective in payload["stepObjectives"]
            ),
            is_tracked=payload["tracked"],
            is_completed=payload["completed"],
            started=payload["started"],
            item_instance_id=payload["itemInstanceId"],
            vendor_hash=payload.get("vendorHash"),
            is_redeemed=payload["redeemed"],
        )

    def _deserialize_milestone_rewards(
        self, payload: typedefs.JSONObject
    ) -> milestones.MilestoneReward:
        return milestones.MilestoneReward(
            category_hash=payload["rewardCategoryHash"],
            entries=tuple(
                milestones.MilestoneRewardEntry(
                    entry_hash=entry["rewardEntryHash"],
                    is_earned=entry["earned"],
                    is_redeemed=entry["redeemed"],
                )
                for entry in payload["entries"]
            ),
        )

    def deserialize_milestone(
        self, payload: typedefs.JSONObject
    ) -> milestones.Milestone:
        start_date: datetime.datetime | None = None
        if raw_start_date := payload.get("startDate"):
            start_date = time.clean_date(raw_start_date)

        end_date: datetime.datetime | None = None
        if raw_end_date := payload.get("endDate"):
            end_date = time.clean_date(raw_end_date)

        rewards: collections.Collection[milestones.MilestoneReward] | None = None
        if raw_rewards := payload.get("rewards"):
            rewards = tuple(
                self._deserialize_milestone_rewards(reward) for reward in raw_rewards
            )

        activities: collections.Sequence[milestones.MilestoneActivity] | None = None
        if raw_activities := payload.get("activities"):
            activities = tuple(
                self._deserialize_milestone_activity(active)
                for active in raw_activities
            )

        quests: collections.Sequence[milestones.MilestoneQuest] | None = None
        if raw_quests := payload.get("availableQuests"):
            quests = tuple(
                self._deserialize_milestone_available_quest(quest)
                for quest in raw_quests
            )

        vendors: collections.Sequence[milestones.MilestoneVendor] | None = None
        if raw_vendors := payload.get("vendors"):
            vendors = tuple(
                milestones.MilestoneVendor(
                    vendor_hash=vendor["vendorHash"],
                    preview_itemhash=vendor.get("previewItemHash"),
                )
                for vendor in raw_vendors
            )

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
        self, payload: typedefs.JSONObject
    ) -> season.ArtifactTier:
        return season.ArtifactTier(
            hash=payload["tierHash"],
            is_unlocked=payload["isUnlocked"],
            points_to_unlock=payload["pointsToUnlock"],
            items=tuple(
                season.ArtifactTierItem(
                    hash=item["itemHash"], is_active=item["isActive"]
                )
                for item in payload["items"]
            ),
        )

    def deserialize_characters(
        self, payload: typedefs.JSONObject
    ) -> collections.Mapping[int, character.Character]:
        return {
            int(char_id): self._set_character_attrs(char)
            for char_id, char in payload["data"].items()
        }

    def deserialize_character(
        self, payload: typedefs.JSONObject
    ) -> character.Character:
        return self._set_character_attrs(payload)

    def deserialize_character_equipments(
        self, payload: typedefs.JSONObject
    ) -> collections.Mapping[int, collections.Sequence[profile.ProfileItemImpl]]:
        return {
            int(char_id): self.deserialize_profile_items(item)
            for char_id, item in payload["data"].items()
        }

    def deserialize_character_activities(
        self, payload: typedefs.JSONObject
    ) -> collections.Mapping[int, activity.CharacterActivity]:
        return {
            int(char_id): self.deserialize_character_activity(data)
            for char_id, data in payload["data"].items()
        }

    def deserialize_characters_render_data(
        self, payload: typedefs.JSONObject
    ) -> collections.Mapping[int, character.RenderedData]:
        return {
            int(char_id): self.deserialize_character_render_data(data)
            for char_id, data in payload["data"].items()
        }

    def deserialize_character_progressions(
        self, payload: typedefs.JSONObject
    ) -> character.CharacterProgression:
        progressions_ = {
            int(prog_id): self.deserialize_progressions(prog)
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
            tiers=tuple(
                self._deserialize_artifact_tiers(tier) for tier in artifact["tiers"]
            ),
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

    def deserialize_character_progressions_mapping(
        self, payload: typedefs.JSONObject
    ) -> collections.Mapping[int, character.CharacterProgression]:
        character_progressions: collections.MutableMapping[
            int, character.CharacterProgression
        ] = {}
        for char_id, data in payload["data"].items():
            character_progressions[int(char_id)] = (
                self.deserialize_character_progressions(data)
            )
        return character_progressions

    def _deserialize_character_loadout_item(
        self, payload: typedefs.JSONObject
    ) -> character.LoadoutItem:
        return character.LoadoutItem(
            instance_id=payload["itemInstanceId"],
            plug_hashes=tuple(payload["plugItemHashes"]),
        )

    def deserialize_character_loadout(
        self, payload: typedefs.JSONObject
    ) -> character.Loadout:
        return character.Loadout(
            color_hash=payload["colorHash"],
            icon_hash=payload["iconHash"],
            name_hash=payload["nameHash"],
            items=tuple(
                self._deserialize_character_loadout_item(item)
                for item in payload["items"]
            ),
        )

    def deserialize_characters_records(
        self,
        payload: typedefs.JSONObject,
    ) -> collections.Mapping[int, records.CharacterRecord]:
        return {
            int(rec_id): self.deserialize_character_records(
                rec, record_hashes=payload.get("featuredRecordHashes", ())
            )
            for rec_id, rec in payload["records"].items()
        }

    def deserialize_profile_records(
        self, payload: typedefs.JSONObject
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

    def _deserialize_craftable_socket_plug(
        self, payload: typedefs.JSONObject
    ) -> items.CraftableSocketPlug:
        return items.CraftableSocketPlug(
            item_hash=int(payload["plugItemHash"]),
            failed_requirement_indexes=payload.get("failedRequirementIndexes", ()),
        )

    def _deserialize_craftable_socket(
        self, payload: typedefs.JSONObject
    ) -> items.CraftableSocket:
        if raw_plug := payload.get("plug"):
            plugs = tuple(
                self._deserialize_craftable_socket_plug(plug) for plug in raw_plug
            )
        else:
            plugs = ()

        return items.CraftableSocket(
            plug_set_hash=int(payload["plugSetHash"]), plugs=plugs
        )

    def _deserialize_craftable_item(
        self, payload: typedefs.JSONObject
    ) -> items.CraftableItem:
        return items.CraftableItem(
            is_visible=payload["visible"],
            failed_requirement_indexes=payload.get("failedRequirementIndexes", ()),
            sockets=tuple(
                self._deserialize_craftable_socket(socket)
                for socket in payload["sockets"]
            ),
        )

    def deserialize_craftables_component(
        self, payload: typedefs.JSONObject
    ) -> components.CraftablesComponent:
        return components.CraftablesComponent(
            craftables={
                int(item_id): self._deserialize_craftable_item(item)
                for item_id, item in payload["craftables"].items()
                if item is not None
            },
            crafting_root_node_hash=payload["craftingRootNodeHash"],
        )

    def _deserialize_commendations_component(
        self, payload: typedefs.JSONObject
    ) -> components.Commendation:
        return components.Commendation(
            total_score=payload["totalScore"],
            node_percentages={
                int(node_hash): node_percent
                for node_hash, node_percent in payload[
                    "commendationNodePercentagesByHash"
                ].items()
            },
            score_detail_values=tuple(payload["scoreDetailValues"]),
            node_scores={
                int(node_score_hash): node_score_value
                for node_score_hash, node_score_value in payload[
                    "commendationNodeScoresByHash"
                ].items()
            },
            commendation_scores={
                int(score_hash): score_value
                for score_hash, score_value in payload[
                    "commendationScoresByHash"
                ].items()
            },
        )

    def deserialize_components(  # noqa: C901 Too complex.
        self, payload: typedefs.JSONObject
    ) -> components.Component:
        # Due to how complex this method is, We'll stick to
        # typing.Optional here.

        profile_: profile.Profile | None = None
        if raw_profile := payload.get("profile"):
            profile_ = self.deserialize_profile(raw_profile["data"])

        profile_progression: profile.ProfileProgression | None = None
        if raw_profile_progression := payload.get("profileProgression"):
            profile_progression = self.deserialize_profile_progression(
                raw_profile_progression
            )

        profile_currencies: typing.Optional[
            collections.Sequence[profile.ProfileItemImpl]
        ] = None
        if raw_profile_currencies := payload.get("profileCurrencies"):
            if "data" in raw_profile_currencies:
                profile_currencies = self.deserialize_profile_items(
                    raw_profile_currencies["data"]
                )

        profile_inventories: typing.Optional[
            collections.Sequence[profile.ProfileItemImpl]
        ] = None
        if raw_profile_inventories := payload.get("profileInventory"):
            if "data" in raw_profile_inventories:
                profile_inventories = self.deserialize_profile_items(
                    raw_profile_inventories["data"]
                )

        profile_records: typing.Optional[collections.Mapping[int, records.Record]] = (
            None
        )

        if raw_profile_records_ := payload.get("profileRecords"):
            profile_records = self.deserialize_profile_records(raw_profile_records_)

        characters: typing.Optional[collections.Mapping[int, character.Character]] = (
            None
        )
        if raw_characters := payload.get("characters"):
            characters = self.deserialize_characters(raw_characters)

        character_records: typing.Optional[
            collections.Mapping[int, records.CharacterRecord]
        ] = None

        if raw_character_records := payload.get("characterRecords"):
            # Had to do it in two steps..
            to_update = {}
            for _, data in raw_character_records["data"].items():
                for record_id, record in data.items():
                    to_update[record_id] = record

            character_records = {
                int(rec_id): self.deserialize_character_records(
                    rec, record_hashes=to_update.get("featuredRecordHashes", ())
                )
                for rec_id, rec in to_update["records"].items()
            }

        character_equipments: typing.Optional[
            collections.Mapping[int, collections.Sequence[profile.ProfileItemImpl]]
        ] = None
        if raw_character_equips := payload.get("characterEquipment"):
            character_equipments = self.deserialize_character_equipments(
                raw_character_equips
            )

        character_inventories: typing.Optional[
            collections.Mapping[int, collections.Sequence[profile.ProfileItemImpl]]
        ] = None
        if raw_character_inventories := payload.get("characterInventories"):
            if "data" in raw_character_inventories:
                character_inventories = self.deserialize_character_equipments(
                    raw_character_inventories
                )

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
            character_progressions = self.deserialize_character_progressions_mapping(
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
                collections.Mapping[int, tuple[bool, records.Objective | None]]
            ]
        ] = None
        root_node_hash: int | None = None

        if raw_metrics := payload.get("metrics"):
            root_node_hash = raw_metrics["data"]["metricsRootNodeHash"]
            metrics = tuple(
                {
                    int(metrics_hash): (
                        data["invisible"],
                        self.deserialize_objectives(data["objectiveProgress"])
                        if "objectiveProgress" in data
                        else None,
                    )
                }
                for metrics_hash, data in raw_metrics["data"]["metrics"].items()
            )
        transitory: fireteams.FireteamParty | None = None
        if raw_transitory := payload.get("profileTransitoryData"):
            if "data" in raw_transitory:
                transitory = self.deserialize_fireteam_party(raw_transitory["data"])

        item_components: components.ItemsComponent | None = None
        if raw_item_components := payload.get("itemComponents"):
            item_components = self.deserialize_items_component(raw_item_components)

        profile_plugsets: typing.Optional[
            collections.Mapping[int, collections.Sequence[items.PlugItemState]]
        ] = None

        if raw_profile_plugs := payload.get("profilePlugSets"):
            profile_plugsets = {
                int(index): [self.deserialize_plug_item_state(state) for state in data]
                for index, data in raw_profile_plugs["data"]["plugs"].items()
            }

        character_plugsets: typing.Optional[
            collections.Mapping[
                int, collections.Mapping[int, collections.Sequence[items.PlugItemState]]
            ]
        ] = None
        if raw_char_plugsets := payload.get("characterPlugSets"):
            character_plugsets = {
                int(char_id): {
                    int(index): [
                        self.deserialize_plug_item_state(state) for state in data
                    ]
                    for index, data in inner["plugs"].items()
                }
                for char_id, inner in raw_char_plugsets["data"].items()
            }

        character_collectibles: typing.Optional[
            collections.Mapping[int, items.Collectible]
        ] = None
        if raw_character_collectibles := payload.get("characterCollectibles"):
            character_collectibles = {
                int(char_id): self._deserialize_collectible(data)
                for char_id, data in raw_character_collectibles["data"].items()
            }

        profile_collectibles: items.Collectible | None = None
        if raw_profile_collectibles := payload.get("profileCollectibles"):
            profile_collectibles = self._deserialize_collectible(
                raw_profile_collectibles["data"]
            )

        profile_nodes: typing.Optional[collections.Mapping[int, records.Node]] = None
        if raw_profile_nodes := payload.get("profilePresentationNodes"):
            profile_nodes = {
                int(node_hash): self._deserialize_node(node)
                for node_hash, node in raw_profile_nodes["data"]["nodes"].items()
            }

        character_nodes: typing.Optional[
            collections.Mapping[int, collections.Mapping[int, records.Node]]
        ] = None
        if raw_character_nodes := payload.get("characterPresentationNodes"):
            character_nodes = {
                int(char_id): {
                    int(node_hash): self._deserialize_node(node)
                    for node_hash, node in each_character["nodes"].items()
                }
                for char_id, each_character in raw_character_nodes["data"].items()
            }

        platform_silver: typing.Optional[
            collections.Mapping[str, profile.ProfileItemImpl]
        ] = None
        if raw_platform_silver := payload.get("platformSilver"):
            if "data" in raw_platform_silver:
                platform_silver = {
                    platform_name: self.deserialize_profile_item(item)
                    for platform_name, item in raw_platform_silver["data"][
                        "platformSilver"
                    ].items()
                }

        character_currency_lookups: typing.Optional[
            collections.Mapping[int, collections.Sequence[items.Currency]]
        ] = None
        if raw_char_lookups := payload.get("characterCurrencyLookups"):
            if "data" in raw_char_lookups:
                character_currency_lookups = {
                    int(char_id): self._deserialize_currencies(currency)
                    for char_id, currency in raw_char_lookups["data"].items()
                }

        character_craftables: typing.Optional[
            collections.Mapping[int, components.CraftablesComponent]
        ] = None
        if raw_character_craftables := payload.get("characterCraftables"):
            if "data" in raw_character_craftables:
                character_craftables = {
                    int(char_id): self.deserialize_craftables_component(craftable)
                    for char_id, craftable in raw_character_craftables["data"].items()
                }

        character_loadouts: (
            collections.Mapping[int, collections.Sequence[character.Loadout]] | None
        ) = None
        if raw_character_loadouts := payload.get("characterLoadouts"):
            if "data" in raw_character_loadouts:
                character_loadouts = {
                    int(char_id): tuple(
                        self.deserialize_character_loadout(loadout)
                        for loadout in raw_loadouts["loadouts"]
                    )
                    for char_id, raw_loadouts in raw_character_loadouts["data"].items()
                }

        commendations: components.Commendation | None = None
        if (
            raw_commendations := payload.get("profileCommendations")
        ) and "data" in raw_commendations:
            commendations = self._deserialize_commendations_component(
                raw_commendations["data"]
            )

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
            transitory=transitory,
            item_components=item_components,
            profile_plugsets=profile_plugsets,
            character_plugsets=character_plugsets,
            character_collectibles=character_collectibles,
            profile_collectibles=profile_collectibles,
            profile_nodes=profile_nodes,
            character_nodes=character_nodes,
            platform_silver=platform_silver,
            character_currency_lookups=character_currency_lookups,
            character_craftables=character_craftables,
            character_loadouts=character_loadouts,
            commendation=commendations,
        )

    def deserialize_items_component(
        self, payload: typedefs.JSONObject
    ) -> components.ItemsComponent:
        # Due to how complex this method is, We'll stick to typing.Optional.
        instances: typing.Optional[
            collections.Sequence[collections.Mapping[int, items.ItemInstance]]
        ] = None
        if raw_instances := payload.get("instances"):
            instances = tuple(
                {int(ins_id): self.deserialize_instanced_item(item)}
                for ins_id, item in raw_instances["data"].items()
            )

        render_data: typing.Optional[
            collections.Mapping[int, tuple[bool, dict[int, int]]]
        ] = None
        if raw_render_data := payload.get("renderData"):
            render_data = {
                int(ins_id): (data["useCustomDyes"], data["artRegions"])
                for ins_id, data in raw_render_data["data"].items()
            }

        stats: typing.Optional[collections.Mapping[int, items.ItemStatsView]] = None
        if raw_stats := payload.get("stats"):
            stats = {}
            for ins_id, stat in raw_stats["data"].items():
                for _, items_ in stat.items():
                    stats[int(ins_id)] = self.deserialize_item_stats_view(items_)

        sockets: typing.Optional[
            collections.Mapping[int, collections.Sequence[items.ItemSocket]]
        ] = None
        if raw_sockets := payload.get("sockets"):
            sockets = {
                int(ins_id): tuple(
                    self.deserialize_item_socket(socket) for socket in item["sockets"]
                )
                for ins_id, item in raw_sockets["data"].items()
            }

        objectives: typing.Optional[
            collections.Mapping[int, collections.Sequence[records.Objective]]
        ] = None
        if raw_objectives := payload.get("objectives"):
            objectives = {
                int(ins_id): tuple(
                    self.deserialize_objectives(objective)
                    for objective in data["objectives"]
                )
                for ins_id, data in raw_objectives["data"].items()
            }

        perks: typing.Optional[
            collections.Mapping[int, collections.Collection[items.ItemPerk]]
        ] = None
        if raw_perks := payload.get("perks"):
            perks = {
                int(ins_id): tuple(
                    self.deserialize_item_perk(perk) for perk in item["perks"]
                )
                for ins_id, item in raw_perks["data"].items()
            }

        plug_states: typing.Optional[collections.Sequence[items.PlugItemState]] = None
        if raw_plug_states := payload.get("plugStates"):
            plug_states = tuple(
                self.deserialize_plug_item_state(plug)
                for _, plug in raw_plug_states["data"].items()
            )

        reusable_plugs: typing.Optional[
            collections.Mapping[int, collections.Sequence[items.PlugItemState]]
        ] = None
        if raw_re_plugs := payload.get("reusablePlugs"):
            reusable_plugs = {
                int(ins_id): tuple(
                    self.deserialize_plug_item_state(state) for state in inner
                )
                for ins_id, plug in raw_re_plugs["data"].items()
                for inner in tuple(plug["plugs"].values())
            }

        plug_objectives: typing.Optional[
            collections.Mapping[
                int, collections.Mapping[int, collections.Collection[records.Objective]]
            ]
        ] = None
        if raw_plug_objectives := payload.get("plugObjectives"):
            plug_objectives = {
                int(ins_id): {
                    int(obj_hash): tuple(
                        self.deserialize_objectives(obj) for obj in objs
                    )
                    for obj_hash, objs in inner["objectivesPerPlug"].items()
                }
                for ins_id, inner in raw_plug_objectives["data"].items()
            }

        return components.ItemsComponent(
            sockets=sockets,
            stats=stats,
            render_data=render_data,
            instances=instances,
            objectives=objectives,
            perks=perks,
            plug_states=plug_states,
            reusable_plugs=reusable_plugs,
            plug_objectives=plug_objectives,
        )

    def deserialize_character_component(
        self, payload: typedefs.JSONObject
    ) -> components.CharacterComponent:
        character_: character.Character | None = None
        if raw_singular_character := payload.get("character"):
            character_ = self.deserialize_character(raw_singular_character["data"])

        inventory: typing.Optional[collections.Sequence[profile.ProfileItemImpl]] = None
        loadouts: collections.Sequence[character.Loadout] | None = None
        if raw_inventory := payload.get("inventory"):
            if "data" in raw_inventory:
                inventory = self.deserialize_profile_items(raw_inventory["data"])

            # The inventory component also returns the loadouts component
            if raw_loadouts := payload.get("loadouts"):
                if "data" in raw_loadouts:
                    loadouts = tuple(
                        self.deserialize_character_loadout(loadout)
                        # very interesting nesting bungie...
                        for loadout in raw_loadouts["data"]["loadouts"]
                    )

        activities: activity.CharacterActivity | None = None
        if raw_activities := payload.get("activities"):
            activities = self.deserialize_character_activity(raw_activities["data"])

        equipment: typing.Optional[collections.Sequence[profile.ProfileItemImpl]] = None
        if raw_equipments := payload.get("equipment"):
            equipment = self.deserialize_profile_items(raw_equipments["data"])

        progressions_: character.CharacterProgression | None = None
        if raw_progressions := payload.get("progressions"):
            progressions_ = self.deserialize_character_progressions(
                raw_progressions["data"]
            )

        render_data: character.RenderedData | None = None
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

        item_components: components.ItemsComponent | None = None
        if raw_item_components := payload.get("itemComponents"):
            item_components = self.deserialize_items_component(raw_item_components)

        nodes: typing.Optional[collections.Mapping[int, records.Node]] = None
        if raw_nodes := payload.get("presentationNodes"):
            nodes = {
                int(node_hash): self._deserialize_node(node)
                for node_hash, node in raw_nodes["data"]["nodes"].items()
            }

        collectibles: items.Collectible | None = None
        if raw_collectibles := payload.get("collectibles"):
            collectibles = self._deserialize_collectible(raw_collectibles["data"])

        currency_lookups: typing.Optional[collections.Sequence[items.Currency]] = None
        if raw_currencies := payload.get("currencyLookups"):
            if "data" in raw_currencies:
                currency_lookups = self._deserialize_currencies(raw_currencies)

        return components.CharacterComponent(
            activities=activities,
            equipment=equipment,
            inventory=inventory,
            progressions=progressions_,
            render_data=render_data,
            character=character_,
            character_records=character_records,
            profile_records=None,
            item_components=item_components,
            currency_lookups=currency_lookups,
            collectibles=collectibles,
            nodes=nodes,
            loadouts=loadouts,
        )

    def _set_entity_attrs(
        self, payload: typedefs.JSONObject, *, key: str = "displayProperties"
    ) -> entity.Entity:
        properties = payload[key]
        name = typedefs.unknown(properties["name"])
        description = typedefs.unknown(properties["description"])

        return entity.Entity(
            hash=payload["hash"],
            index=payload["index"],
            name=name,
            description=description,
            has_icon=properties["hasIcon"],
            icon=builders.Image(properties.get("icon")),
        )

    def deserialize_inventory_results(
        self, payload: typedefs.JSONObject
    ) -> sain.Iterator[entity.SearchableEntity]:
        return sain.Iter(
            entity.SearchableEntity(
                hash=data["hash"],
                entity_type=data["entityType"],
                weight=data["weight"],
                suggested_words=payload["suggestedWords"],
                name=data["displayProperties"]["name"],
                has_icon=data["displayProperties"]["hasIcon"],
                description=typedefs.unknown(data["displayProperties"]["description"]),
                icon=builders.Image(path=data["displayProperties"]["icon"]),
            )
            for data in payload["results"]["results"]
        )

    def _deserialize_inventory_item_objects(
        self, payload: typedefs.JSONObject
    ) -> entity.InventoryEntityObjects:
        return entity.InventoryEntityObjects(
            action=payload.get("action"),
            set_data=payload.get("setData"),
            stats=payload.get("stats"),
            equipping_block=payload.get("equippingBlock"),
            translation_block=payload.get("translationBlock"),
            preview=payload.get("preview"),
            quality=payload.get("quality"),
            value=payload.get("value"),
            source_data=payload.get("sourceData"),
            objectives=payload.get("objectives"),
            plug=payload.get("plug"),
            metrics=payload.get("metrics"),
            gearset=payload.get("gearset"),
            sack=payload.get("sack"),
            sockets=payload.get("sockets"),
            summary=payload.get("summary"),
            talent_gird=payload.get("talentGrid"),
            investments_stats=payload.get("investmentStats"),
            perks=payload.get("perks"),
            animations=payload.get("animations", ()),
            links=payload.get("links", ()),
        )

    def deserialize_inventory_entity(  # noqa: C901 Too complex.
        self, payload: typedefs.JSONObject, /
    ) -> entity.InventoryEntity:
        props = self._set_entity_attrs(payload)
        objects = self._deserialize_inventory_item_objects(payload)

        collectible_hash: int | None = None
        if raw_collectible_hash := payload.get("collectibleHash"):
            collectible_hash = int(raw_collectible_hash)

        secondary_icon: builders.Image | None = None
        if raw_second_icon := payload.get("secondaryIcon"):
            secondary_icon = builders.Image(path=raw_second_icon)

        secondary_overlay: builders.Image | None = None
        if raw_second_overlay := payload.get("secondaryOverlay"):
            secondary_overlay = builders.Image(path=raw_second_overlay)

        secondary_special: builders.Image | None = None
        if raw_second_special := payload.get("secondarySpecial"):
            secondary_special = builders.Image(path=raw_second_special)

        screenshot: builders.Image | None = None
        if raw_screenshot := payload.get("screenshot"):
            screenshot = builders.Image(path=raw_screenshot)

        watermark_icon: builders.Image | None = None
        if raw_watermark_icon := payload.get("iconWatermark"):
            watermark_icon = builders.Image(path=raw_watermark_icon)

        watermark_shelved: builders.Image | None = None
        if raw_watermark_shelved := payload.get("iconWatermarkShelved"):
            watermark_shelved = builders.Image(path=raw_watermark_shelved)

        about: str | None = None
        if raw_about := payload.get("flavorText"):
            about = raw_about

        ui_item_style: str | None = None
        if raw_ui_style := payload.get("uiItemDisplayStyle"):
            ui_item_style = raw_ui_style

        tier_and_name: str | None = None
        if raw_tier_and_name := payload.get("itemTypeAndTierDisplayName"):
            tier_and_name = raw_tier_and_name

        type_name: str | None = None
        if raw_type_name := payload.get("itemTypeDisplayName"):
            type_name = raw_type_name

        display_source: str | None = None
        if raw_display_source := payload.get("displaySource"):
            display_source = raw_display_source

        lorehash: int | None = None
        if raw_lore_hash := payload.get("loreHash"):
            lorehash = int(raw_lore_hash)

        summary_hash: int | None = None
        if raw_summary_hash := payload.get("summaryItemHash"):
            summary_hash = raw_summary_hash

        breaker_type_hash: int | None = None
        if raw_breaker_type_hash := payload.get("breakerTypeHash"):
            breaker_type_hash = int(raw_breaker_type_hash)

        damage_types: typing.Optional[collections.Sequence[int]] = None
        if raw_damage_types := payload.get("damageTypes"):
            damage_types = tuple(int(type_) for type_ in raw_damage_types)

        damagetype_hashes: typing.Optional[collections.Sequence[int]] = None
        if raw_damagetype_hashes := payload.get("damageTypeHashes"):
            damagetype_hashes = tuple(int(type_) for type_ in raw_damagetype_hashes)

        default_damagetype_hash: int | None = None
        if raw_defaultdmg_hash := payload.get("defaultDamageTypeHash"):
            default_damagetype_hash = int(raw_defaultdmg_hash)

        emblem_objective_hash: int | None = None
        if raw_emblem_obj_hash := payload.get("emblemObjectiveHash"):
            emblem_objective_hash = int(raw_emblem_obj_hash)

        tier_type: enums.TierType | None = None
        tier: enums.ItemTier | None = None
        bucket_hash: int | None = None
        recovery_hash: int | None = None
        tier_name: str | None = None
        isinstance_item: bool = False
        expire_tool_tip: str | None = None
        expire_in_orbit_message: str | None = None
        suppress_expiration: bool = False
        max_stack_size: int | None = None
        stack_label: str | None = None

        if inventory := payload.get("inventory"):
            tier_type = enums.TierType(int(inventory["tierType"]))
            tier = enums.ItemTier(int(inventory["tierTypeHash"]))
            bucket_hash = int(inventory["bucketTypeHash"])
            recovery_hash = int(inventory["recoveryBucketTypeHash"])
            tier_name = inventory["tierTypeName"]
            isinstance_item = inventory["isInstanceItem"]
            suppress_expiration = inventory["suppressExpirationWhenObjectivesComplete"]
            max_stack_size = int(inventory["maxStackSize"])

            try:
                stack_label = inventory["stackUniqueLabel"]
            except KeyError:
                pass

        if "traitHashes" in payload:
            trait_hashes = tuple(
                int(trait_hash) for trait_hash in payload["traitHashes"]
            )
        else:
            trait_hashes = ()

        if "traitIds" in payload:
            trait_ids = tuple(trait_id for trait_id in payload["traitIds"])
        else:
            trait_ids = ()

        return entity.InventoryEntity(
            collectible_hash=collectible_hash,
            name=props.name,
            about=about,
            emblem_objective_hash=emblem_objective_hash,
            suppress_expiration=suppress_expiration,
            max_stack_size=max_stack_size,
            stack_label=stack_label,
            tier=tier,
            tier_type=tier_type,
            tier_name=tier_name,
            bucket_hash=bucket_hash,
            recovery_bucket_hash=recovery_hash,
            isinstance_item=isinstance_item,
            expire_in_orbit_message=expire_in_orbit_message,
            expiration_tooltip=expire_tool_tip,
            lore_hash=lorehash,
            type_and_tier_name=tier_and_name,
            summary_hash=summary_hash,
            ui_display_style=ui_item_style,
            type_name=type_name,
            breaker_type_hash=breaker_type_hash,
            description=props.description,
            display_source=display_source,
            hash=props.hash,
            damage_types=damage_types,
            index=props.index,
            icon=props.icon,
            has_icon=props.has_icon,
            screenshot=screenshot,
            watermark_icon=watermark_icon,
            watermark_shelved=watermark_shelved,
            secondary_icon=secondary_icon,
            secondary_overlay=secondary_overlay,
            secondary_special=secondary_special,
            type=enums.ItemType(int(payload["itemType"])),
            category_hashes=tuple(
                int(hash_) for hash_ in payload["itemCategoryHashes"]
            ),
            item_class=enums.Class(int(payload["classType"])),
            sub_type=enums.ItemSubType(int(payload["itemSubType"])),
            breaker_type=int(payload["breakerType"]),
            default_damagetype=int(payload["defaultDamageType"]),
            default_damagetype_hash=default_damagetype_hash,
            damagetype_hashes=damagetype_hashes,
            tooltip_notifications=payload["tooltipNotifications"],
            not_transferable=payload["nonTransferrable"],
            allow_actions=payload["allowActions"],
            is_equippable=payload["equippable"],
            objects=objects,
            background_colors=payload.get("backgroundColor", {}),
            season_hash=payload.get("seasonHash"),
            has_postmaster_effect=payload["doesPostmasterPullHaveSideEffects"],
            trait_hashes=trait_hashes,
            trait_ids=trait_ids,
        )

    def deserialize_objective_entity(
        self, payload: typedefs.JSONObject, /
    ) -> entity.ObjectiveEntity:
        props = self._set_entity_attrs(payload)
        return entity.ObjectiveEntity(
            hash=props.hash,
            index=props.index,
            description=props.description,
            name=props.name,
            has_icon=props.has_icon,
            icon=props.icon,
            unlock_value_hash=payload["unlockValueHash"],
            completion_value=payload["completionValue"],
            scope=entity.GatingScope(int(payload["scope"])),
            location_hash=payload["locationHash"],
            allowed_negative_value=payload["allowNegativeValue"],
            allowed_value_change=payload["allowValueChangeWhenCompleted"],
            counting_downward=payload["isCountingDownward"],
            value_style=entity.ValueUIStyle(int(payload["valueStyle"])),
            progress_description=payload["progressDescription"],
            perks=payload["perks"],
            stats=payload["stats"],
            minimum_visibility=payload["minimumVisibilityThreshold"],
            allow_over_completion=payload["allowOvercompletion"],
            show_value_style=payload["showValueOnComplete"],
            display_only_objective=payload["isDisplayOnlyObjective"],
            complete_value_style=entity.ValueUIStyle(
                int(payload["completedValueStyle"])
            ),
            progress_value_style=entity.ValueUIStyle(
                int(payload["inProgressValueStyle"])
            ),
            ui_label=payload["uiLabel"],
            ui_style=entity.ObjectiveUIStyle(int(payload["uiStyle"])),
        )

    def _deserialize_activity_values(
        self, payload: typedefs.JSONObject, /
    ) -> activity.ActivityValues:
        team: int | None = None
        if raw_team := payload.get("team"):
            team = raw_team["basic"]["value"]
        return activity.ActivityValues(
            assists=payload["assists"]["basic"]["value"],
            deaths=payload["deaths"]["basic"]["value"],
            kills=payload["kills"]["basic"]["value"],
            is_completed=bool(payload["completed"]["basic"]["value"]),
            opponents_defeated=payload["opponentsDefeated"]["basic"]["value"],
            efficiency=payload["efficiency"]["basic"]["value"],
            kd_ratio=payload["killsDeathsRatio"]["basic"]["value"],
            kd_assists=payload["killsDeathsAssists"]["basic"]["value"],
            score=payload["score"]["basic"]["value"],
            duration=payload["activityDurationSeconds"]["basic"]["displayValue"],
            team=team,
            completion_reason=payload["completionReason"]["basic"]["displayValue"],
            fireteam_id=payload["fireteamId"]["basic"]["value"],
            start_seconds=payload["startSeconds"]["basic"]["value"],
            played_time=payload["timePlayedSeconds"]["basic"]["displayValue"],
            player_count=payload["playerCount"]["basic"]["value"],
            team_score=payload["teamScore"]["basic"]["value"],
        )

    def deserialize_activity(
        self,
        payload: typedefs.JSONObject,
        /,
    ) -> activity.Activity:
        period = time.clean_date(payload["period"])
        details = payload["activityDetails"]
        ref_id = int(details["referenceId"])
        instance_id = int(details["instanceId"])
        mode = enums.GameMode(details["mode"])
        modes = tuple(enums.GameMode(int(mode_)) for mode_ in details["modes"])
        is_private = details["isPrivate"]
        membership_type = enums.MembershipType(int(details["membershipType"]))

        # Since we're using the same fields for post activity method
        # this check is required since post activity doesn't values values
        values = self._deserialize_activity_values(payload["values"])

        return activity.Activity(
            hash=ref_id,
            instance_id=instance_id,
            mode=mode,
            modes=modes,
            is_private=is_private,
            membership_type=membership_type,
            occurred_at=period,
            values=values,
        )

    def deserialize_activities(
        self, payload: typedefs.JSONObject
    ) -> sain.Iterator[activity.Activity]:
        return sain.Iter(
            self.deserialize_activity(activity_) for activity_ in payload["activities"]
        )

    def deserialize_extended_weapon_values(
        self, payload: typedefs.JSONObject
    ) -> activity.ExtendedWeaponValues:
        assists: int | None = None
        if raw_assists := payload["values"].get("uniqueWeaponAssists"):
            assists = raw_assists["basic"]["value"]
        assists_damage: int | None = None

        if raw_assists_damage := payload["values"].get("uniqueWeaponAssistDamage"):
            assists_damage = raw_assists_damage["basic"]["value"]

        return activity.ExtendedWeaponValues(
            reference_id=int(payload["referenceId"]),
            kills=payload["values"]["uniqueWeaponKills"]["basic"]["value"],
            precision_kills=payload["values"]["uniqueWeaponPrecisionKills"]["basic"][
                "value"
            ],
            assists=assists,
            assists_damage=assists_damage,
            precision_kills_percentage=(
                payload["values"]["uniqueWeaponKillsPrecisionKills"]["basic"]["value"],
                payload["values"]["uniqueWeaponKillsPrecisionKills"]["basic"][
                    "displayValue"
                ],
            ),
        )

    def _deserialize_extended_values(
        self, payload: typedefs.JSONObject
    ) -> activity.ExtendedValues:
        if raw_weapons := payload.get("weapons"):
            weapons = tuple(
                self.deserialize_extended_weapon_values(value) for value in raw_weapons
            )
        else:
            weapons = ()

        return activity.ExtendedValues(
            precision_kills=payload["values"]["precisionKills"]["basic"]["value"],
            grenade_kills=payload["values"]["weaponKillsGrenade"]["basic"]["value"],
            melee_kills=payload["values"]["weaponKillsMelee"]["basic"]["value"],
            super_kills=payload["values"]["weaponKillsSuper"]["basic"]["value"],
            ability_kills=payload["values"]["weaponKillsAbility"]["basic"]["value"],
            weapons=weapons,
        )

    def deserialize_post_activity_player(
        self, payload: typedefs.JSONObject, /
    ) -> activity.PostActivityPlayer:
        player = payload["player"]

        class_hash: int | None = None
        if (class_hash := player.get("classHash")) is not None:
            class_hash = class_hash

        race_hash: int | None = None
        if (race_hash := player.get("raceHash")) is not None:
            race_hash = race_hash

        gender_hash: int | None = None
        if (gender_hash := player.get("genderHash")) is not None:
            gender_hash = gender_hash

        character_class: str | None = None
        if character_class := player.get("characterClass"):
            character_class = character_class

        character_level: int | None = None
        if (character_level := player.get("characterLevel")) is not None:
            character_level = character_level

        return activity.PostActivityPlayer(
            standing=int(payload["standing"]),
            score=int(payload["score"]["basic"]["value"]),
            character_id=payload["characterId"],
            destiny_user=self.deserialize_destiny_membership(player["destinyUserInfo"]),
            character_class=character_class,
            character_level=character_level,
            race_hash=race_hash,
            gender_hash=gender_hash,
            class_hash=class_hash,
            light_level=int(player["lightLevel"]),
            emblem_hash=int(player["emblemHash"]),
            values=self._deserialize_activity_values(payload["values"]),
            extended_values=self._deserialize_extended_values(payload["extended"]),
        )

    def _deserialize_post_activity_team(
        self, payload: typedefs.JSONObject
    ) -> activity.PostActivityTeam:
        return activity.PostActivityTeam(
            id=payload["teamId"],
            is_defeated=bool(payload["standing"]["basic"]["value"]),
            score=int(payload["score"]["basic"]["value"]),
            name=payload["teamName"],
        )

    def deserialize_post_activity(
        self, payload: typedefs.JSONObject
    ) -> activity.PostActivity:
        period = time.clean_date(payload["period"])
        details = payload["activityDetails"]
        ref_id = int(details["referenceId"])
        instance_id = int(details["instanceId"])
        mode = enums.GameMode(details["mode"])
        modes = tuple(enums.GameMode(int(mode_)) for mode_ in details["modes"])
        is_private = details["isPrivate"]
        membership_type = enums.MembershipType(int(details["membershipType"]))
        return activity.PostActivity(
            hash=ref_id,
            membership_type=membership_type,
            instance_id=instance_id,
            mode=mode,
            modes=modes,
            is_private=is_private,
            occurred_at=period,
            starting_phase=int(payload["startingPhaseIndex"]),
            players=tuple(
                self.deserialize_post_activity_player(player)
                for player in payload["entries"]
            ),
            teams=tuple(
                self._deserialize_post_activity_team(team) for team in payload["teams"]
            ),
        )

    def _deserialize_aggregated_activity_values(
        self, payload: typedefs.JSONObject
    ) -> activity.AggregatedActivityValues:
        # This ID is always the same for all aggregated values.
        activity_id = int(payload["fastestCompletionMsForActivity"]["activityId"])

        return activity.AggregatedActivityValues(
            id=activity_id,
            fastest_completion_time=(
                int(payload["fastestCompletionMsForActivity"]["basic"]["value"]),
                payload["fastestCompletionMsForActivity"]["basic"]["displayValue"],
            ),
            completions=int(payload["activityCompletions"]["basic"]["value"]),
            kills=int(payload["activityKills"]["basic"]["value"]),
            deaths=int(payload["activityDeaths"]["basic"]["value"]),
            assists=int(payload["activityAssists"]["basic"]["value"]),
            seconds_played=(
                int(payload["activitySecondsPlayed"]["basic"]["value"]),
                payload["activitySecondsPlayed"]["basic"]["displayValue"],
            ),
            wins=int(payload["activityWins"]["basic"]["value"]),
            goals_missed=int(payload["activityGoalsMissed"]["basic"]["value"]),
            special_actions=int(payload["activitySpecialActions"]["basic"]["value"]),
            best_goals_hit=int(payload["activityBestGoalsHit"]["basic"]["value"]),
            best_single_score=int(
                payload["activityBestSingleGameScore"]["basic"]["value"]
            ),
            goals_hit=int(payload["activityGoalsHit"]["basic"]["value"]),
            special_score=int(payload["activitySpecialScore"]["basic"]["value"]),
            kd_assists=int(payload["activityKillsDeathsAssists"]["basic"]["value"]),
            kd_ratio=float(
                payload["activityKillsDeathsAssists"]["basic"]["displayValue"]
            ),
            precision_kills=int(payload["activityPrecisionKills"]["basic"]["value"]),
        )

    def deserialize_aggregated_activity(
        self, payload: typedefs.JSONObject
    ) -> activity.AggregatedActivity:
        return activity.AggregatedActivity(
            hash=int(payload["activityHash"]),
            values=self._deserialize_aggregated_activity_values(payload["values"]),
        )

    def deserialize_aggregated_activities(
        self, payload: typedefs.JSONObject
    ) -> sain.Iterator[activity.AggregatedActivity]:
        return sain.Iter(
            self.deserialize_aggregated_activity(activity)
            for activity in payload["activities"]
        )

    def deserialize_linked_profiles(
        self, payload: typedefs.JSONObject
    ) -> profile.LinkedProfile:
        bungie_user = self.deserialize_partial_bungie_user(payload["bnetMembership"])

        if raw_profile := payload.get("profiles"):
            profiles = tuple(
                self.deserialize_destiny_membership(p) for p in raw_profile
            )
        else:
            profiles = ()

        error_profiles = ()
        if raw_profiles_with_errors := payload.get("profilesWithErrors"):
            for raw_error_p in raw_profiles_with_errors:
                if "infoCard" in raw_error_p:
                    error_profiles = tuple(
                        self.deserialize_destiny_membership(error_p)
                        for error_p in raw_error_p
                    )

        return profile.LinkedProfile(
            bungie_user=bungie_user,
            profiles=profiles,
            profiles_with_errors=error_profiles,
        )

    def deserialize_clan_banners(
        self, payload: typedefs.JSONObject
    ) -> collections.Sequence[clans.ClanBanner]:
        if banners := payload.get("clanBannerDecals"):
            banner_obj = tuple(
                clans.ClanBanner(
                    id=int(k),
                    foreground=builders.Image(path=v["foregroundPath"]),
                    background=builders.Image(path=v["backgroundPath"]),
                )
                for k, v in banners.items()
            )
        else:
            banner_obj = ()
        return banner_obj

    def deserialize_public_milestone_content(
        self, payload: typedefs.JSONObject
    ) -> milestones.MilestoneContent:
        if raw_categories := payload.get("itemCategories"):
            items_categories = tuple(
                milestones.MilestoneItems(
                    title=item["title"], hashes=item["itemHashes"]
                )
                for item in raw_categories
            )
        else:
            items_categories = ()

        return milestones.MilestoneContent(
            about=typedefs.unknown(payload["about"]),
            status=typedefs.unknown(payload["status"]),
            tips=payload.get("tips", ()),
            items=items_categories,
        )

    def deserialize_friend(self, payload: typedefs.JSONObject, /) -> friends.Friend:
        bungie_user: user.BungieUser | None = None

        if raw_bungie_user := payload.get("bungieNetUser"):
            bungie_user = self.deserialize_bungie_user(raw_bungie_user)

        return friends.Friend(
            id=int(payload["lastSeenAsMembershipId"]),
            name=typedefs.unknown(payload.get("bungieGlobalDisplayName", "")),
            code=payload.get("bungieGlobalDisplayNameCode"),
            relationship=enums.Relationship(payload["relationship"]),
            user=bungie_user,
            online_status=enums.Presence(payload["onlineStatus"]),
            online_title=payload["onlineTitle"],
            type=enums.MembershipType(payload["lastSeenAsBungieMembershipType"]),
        )

    def deserialize_friends(
        self, payload: typedefs.JSONObject
    ) -> collections.Sequence[friends.Friend]:
        return tuple(self.deserialize_friend(friend) for friend in payload["friends"])

    def deserialize_friend_requests(
        self, payload: typedefs.JSONObject
    ) -> friends.FriendRequestView:
        if raw_incoming_requests := payload.get("incomingRequests"):
            incoming = tuple(
                self.deserialize_friend(incoming_request)
                for incoming_request in raw_incoming_requests
            )
        else:
            incoming = ()

        if raw_outgoing_requests := payload.get("outgoingRequests"):
            outgoing = tuple(
                self.deserialize_friend(outgoing_request)
                for outgoing_request in raw_outgoing_requests
            )
        else:
            outgoing = ()

        return friends.FriendRequestView(incoming=incoming, outgoing=outgoing)

    def _set_fireteam_fields(
        self, payload: typedefs.JSONObject, total_results: int | None = None
    ) -> fireteams.Fireteam:
        activity_type = fireteams.FireteamActivity(payload["activityType"])
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
            date_modified=time.clean_date(payload["dateModified"])
            if "dateModified" in payload
            else None,
            scheduled_time=time.clean_date(payload["scheduledTime"])
            if "scheduledTime" in payload
            else None,
            total_results=total_results or 0,
        )

    def deserialize_fireteams(
        self, payload: typedefs.JSONObject
    ) -> collections.Sequence[fireteams.Fireteam]:
        if "results" in payload:
            fireteams_ = tuple(
                self._set_fireteam_fields(
                    elem, total_results=int(payload["totalResults"])
                )
                for elem in payload["results"]
            )
        else:
            fireteams_ = ()
        return fireteams_

    def deserialize_fireteam_destiny_membership(
        self, payload: typedefs.JSONObject
    ) -> fireteams.FireteamUser:
        destiny_obj = self.deserialize_destiny_membership(payload)
        return fireteams.FireteamUser(
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
        self, payload: typedefs.JSONObject, *, alternatives: bool = False
    ) -> collections.Sequence[fireteams.FireteamMember]:
        members_: list[fireteams.FireteamMember] = []
        if members := payload.get("Members" if not alternatives else "Alternates"):
            for member in members:
                bungie_fields = self.deserialize_partial_bungie_user(member)
                members_fields = fireteams.FireteamMember(
                    membership=self.deserialize_fireteam_destiny_membership(member),
                    has_microphone=member["hasMicrophone"],
                    character_id=int(member["characterId"]),
                    date_joined=time.clean_date(member["dateJoined"]),
                    last_platform_invite_date=time.clean_date(
                        member["lastPlatformInviteAttemptDate"]
                    ),
                    last_platform_invite_result=int(
                        member["lastPlatformInviteAttemptResult"]
                    ),
                    name=bungie_fields.name,
                    id=bungie_fields.id,
                    icon=bungie_fields.icon,
                    is_public=bungie_fields.is_public,
                    crossave_override=bungie_fields.crossave_override,
                    types=bungie_fields.types,
                    type=bungie_fields.type,
                    code=bungie_fields.code,
                )
                members_.append(members_fields)
        return tuple(members_)

    def deserialize_available_fireteam(
        self, payload: typedefs.JSONObject
    ) -> fireteams.AvailableFireteam:
        fields = self._set_fireteam_fields(payload["Summary"])
        return fireteams.AvailableFireteam(
            id=fields.id,
            group_id=fields.group_id,
            platform=fields.platform,
            activity_type=fields.activity_type,
            is_immediate=fields.is_immediate,
            is_public=fields.is_public,
            is_valid=fields.is_valid,
            owner_id=fields.owner_id,
            player_slot_count=fields.player_slot_count,
            available_player_slots=fields.available_player_slots,
            available_alternate_slots=fields.available_alternate_slots,
            title=fields.title,
            date_created=fields.date_created,
            locale=fields.locale,
            last_modified=fields.last_modified,
            total_results=fields.total_results,
            scheduled_time=fields.scheduled_time,
            date_modified=fields.date_modified,
            members=self.deserialize_fireteam_members(payload),
            alternatives=self.deserialize_fireteam_members(payload, alternatives=True),
        )

    def deserialize_available_fireteams(
        self, data: typedefs.JSONObject
    ) -> collections.Sequence[fireteams.AvailableFireteam]:
        if raw_results := data.get("results"):
            fireteam_results = tuple(
                self.deserialize_available_fireteam(f) for f in raw_results
            )
        else:
            fireteam_results = ()
        return fireteam_results

    def deserialize_fireteam_party(
        self, payload: typedefs.JSONObject
    ) -> fireteams.FireteamParty:
        last_destination_hash: int | None = None
        if raw_dest_hash := payload.get("lastOrbitedDestinationHash"):
            last_destination_hash = int(raw_dest_hash)

        return fireteams.FireteamParty(
            members=tuple(
                self._deserialize_fireteam_party_member(member)
                for member in payload["partyMembers"]
            ),
            activity=self._deserialize_fireteam_party_current_activity(
                payload["currentActivity"]
            ),
            settings=self._deserialize_fireteam_party_settings(payload["joinability"]),
            last_destination_hash=last_destination_hash,
            tracking=payload["tracking"],
        )

    def _deserialize_fireteam_party_member(
        self, payload: typedefs.JSONObject
    ) -> fireteams.FireteamPartyMember:
        status = fireteams.FireteamPartyMemberState(payload["status"])

        return fireteams.FireteamPartyMember(
            membership_id=int(payload["membershipId"]),
            emblem_hash=int(payload["emblemHash"]),
            status=status,
            display_name=payload["displayName"] if payload["displayName"] else None,
        )

    def _deserialize_fireteam_party_current_activity(
        self, payload: typedefs.JSONObject
    ) -> fireteams.FireteamPartyCurrentActivity:
        start_date: datetime.datetime | None = None
        if raw_start_date := payload.get("startTime"):
            start_date = time.clean_date(raw_start_date)

        end_date: datetime.datetime | None = None
        if raw_end_date := payload.get("endTime"):
            end_date = time.clean_date(raw_end_date)
        return fireteams.FireteamPartyCurrentActivity(
            start_time=start_date,
            end_time=end_date,
            score=float(payload["score"]),
            highest_opposing_score=float(payload["highestOpposingFactionScore"]),
            opponents_count=int(payload["numberOfOpponents"]),
            player_count=int(payload["numberOfPlayers"]),
        )

    def _deserialize_fireteam_party_settings(
        self, payload: typedefs.JSONObject
    ) -> fireteams.FireteamPartySettings:
        closed_reasons = enums.ClosedReasons(payload["closedReasons"])
        return fireteams.FireteamPartySettings(
            open_slots=int(payload["openSlots"]),
            privacy_setting=enums.PrivacySetting(int(payload["privacySetting"])),
            closed_reasons=closed_reasons,
        )

    def deserialize_seasonal_artifact(
        self, payload: typedefs.JSONObject
    ) -> season.Artifact:
        raw_artifact = payload["seasonalArtifact"]

        points = raw_artifact["pointProgression"]
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

        bonus = raw_artifact["powerBonusProgression"]
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
        return season.Artifact(
            hash=raw_artifact["artifactHash"],
            power_bonus=raw_artifact["powerBonus"],
            acquired_points=raw_artifact["pointsAcquired"],
            bonus=power_bonus_prog,
            points=points_prog,
        )

    def deserialize_profile_progression(
        self, payload: typedefs.JSONObject
    ) -> profile.ProfileProgression:
        return profile.ProfileProgression(
            artifact=self.deserialize_seasonal_artifact(payload["data"]),
            checklist={
                int(check_id): checklists
                for check_id, checklists in payload["data"]["checklists"].items()
            },
        )

    def deserialize_instanced_item(
        self, payload: typedefs.JSONObject
    ) -> items.ItemInstance:
        damage_type_hash: int | None = None
        if raw_damagetype_hash := payload.get("damageTypeHash"):
            damage_type_hash = int(raw_damagetype_hash)

        required_hashes: typing.Optional[collections.Collection[int]] = None
        if raw_required_hashes := payload.get("unlockHashesRequiredToEquip"):
            required_hashes = tuple(int(raw_hash) for raw_hash in raw_required_hashes)

        breaker_type: items.ItemBreakerType | None = None
        if raw_break_type := payload.get("breakerType"):
            breaker_type = items.ItemBreakerType(int(raw_break_type))

        breaker_type_hash: int | None = None
        if raw_break_type_hash := payload.get("breakerTypeHash"):
            breaker_type_hash = int(raw_break_type_hash)

        energy: items.ItemEnergy | None = None
        if raw_energy := payload.get("energy"):
            energy = self.deserialize_item_energy(raw_energy)

        primary_stats = None
        if raw_primary_stats := payload.get("primaryStat"):
            primary_stats = self.deserialize_item_stats_view(raw_primary_stats)

        return items.ItemInstance(
            damage_type=enums.DamageType(int(payload["damageType"])),
            damage_type_hash=damage_type_hash,
            primary_stat=primary_stats,
            item_level=int(payload["itemLevel"]),
            quality=int(payload["quality"]),
            is_equipped=payload["isEquipped"],
            can_equip=payload["canEquip"],
            equip_required_level=int(payload["equipRequiredLevel"]),
            required_equip_unlock_hashes=required_hashes,
            cant_equip_reason=int(payload["cannotEquipReason"]),
            breaker_type=breaker_type,
            breaker_type_hash=breaker_type_hash,
            energy=energy,
        )

    def deserialize_item_energy(self, payload: typedefs.JSONObject) -> items.ItemEnergy:
        energy_hash: int | None = None
        if raw_energy_hash := payload.get("energyTypeHash"):
            energy_hash = int(raw_energy_hash)

        return items.ItemEnergy(
            hash=energy_hash,
            type=items.ItemEnergyType(int(payload["energyType"])),
            capacity=int(payload["energyCapacity"]),
            used_energy=int(payload["energyUsed"]),
            unused_energy=int(payload["energyUnused"]),
        )

    def deserialize_item_perk(self, payload: typedefs.JSONObject) -> items.ItemPerk:
        perk_hash: int | None = None
        if raw_perk_hash := payload.get("perkHash"):
            perk_hash = int(raw_perk_hash)

        return items.ItemPerk(
            hash=perk_hash,
            icon=builders.Image(path=payload["iconPath"]),
            is_active=payload["isActive"],
            is_visible=payload["visible"],
        )

    def deserialize_item_socket(self, payload: typedefs.JSONObject) -> items.ItemSocket:
        plug_hash: int | None = None
        if raw_plug_hash := payload.get("plugHash"):
            plug_hash = int(raw_plug_hash)

        enable_fail_indexes: collections.Sequence[int] | None = None
        if raw_indexes := payload.get("enableFailIndexes"):
            enable_fail_indexes = tuple(int(index) for index in raw_indexes)

        return items.ItemSocket(
            plug_hash=plug_hash,
            is_enabled=payload["isEnabled"],
            enable_fail_indexes=enable_fail_indexes,
            is_visible=payload.get("visible"),
        )

    def deserialize_item_stats_view(
        self, payload: typedefs.JSONObject
    ) -> items.ItemStatsView:
        return items.ItemStatsView(
            stat_hash=payload.get("statHash"), value=payload.get("value")
        )

    def deserialize_plug_item_state(
        self, payload: typedefs.JSONObject
    ) -> items.PlugItemState:
        item_hash: int | None = None
        if raw_item_hash := payload.get("plugItemHash"):
            item_hash = int(raw_item_hash)

        insert_fail_indexes: collections.Sequence[int] | None = None
        if raw_fail_indexes := payload.get("insertFailIndexes"):
            insert_fail_indexes = tuple(int(k) for k in raw_fail_indexes)

        enable_fail_indexes: collections.Sequence[int] | None = None
        if raw_enabled_indexes := payload.get("enableFailIndexes"):
            enable_fail_indexes = tuple(int(k) for k in raw_enabled_indexes)

        return items.PlugItemState(
            item_hash=item_hash,
            insert_fail_indexes=insert_fail_indexes,
            enable_fail_indexes=enable_fail_indexes,
            is_enabled=payload["enabled"],
            can_insert=payload["canInsert"],
        )


Global = Framework()
"""The global framework instance.

This type is global constant that can be used to deserialize payloads
without the need to initialize a new instance of the framework.
"""
