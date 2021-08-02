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

"""Deserialization for all bungie incoming json payloads."""

from __future__ import annotations

__all__: typing.Sequence[str] = ["Deserialize"]

import logging
import typing

# Utils
from aiobungie import error
from aiobungie.internal import Image, Time, enums, impl
# Objects
from aiobungie.objects import application as app
from aiobungie.objects import character, clans, entity, player, profile, user

from .helpers import JsonDict, JsonList

_LOG: typing.Final[logging.Logger] = logging.getLogger(__name__)


class Deserialize:
    """The base Deserialization class for all aiobungie objects."""

    # This is actually inspired by hikari's entity factory.

    __slots__: typing.Sequence[str] = "_rest"

    def __init__(self, rest: impl.RESTful) -> None:
        self._rest = rest

    def deserialize_user(self, payload: JsonList, position: int = 0) -> user.User:
        from_id = payload
        try:
            data = payload[position]  # type: ignore
        except (KeyError, UnboundLocalError):
            data = from_id  # type: ignore
        except IndexError:
            if position or position == 0:
                raise error.UserNotFound("Player was not found.")

        return user.User(
            id=int(data["membershipId"]),
            created_at=Time.clean_date(data["firstAccess"]),
            name=data["displayName"],
            is_deleted=data["isDeleted"],
            about=data["about"],
            updated_at=Time.clean_date(data["lastUpdate"]),
            psn_name=data.get("psnDisplayName", None),
            steam_name=data.get("steamDisplayName", None),
            twitch_name=data.get("twitchDisplayName", None),
            blizzard_name=data.get("blizzardDisplayName", None),
            status=data["statusText"],
            locale=data["locale"],
            picture=Image(path=str(data["profilePicturePath"])),
        )

    def deserialize_player(self, payload: JsonDict, position: int = 0) -> player.Player:
        old_data = payload
        try:
            data = payload[position]  # type: ignore
        except IndexError:
            try:
                # This is kinda cluster fuck
                # if we're out of index the first time
                # we try to return the first player
                # otherwise the list is empty meaning
                # the player was not found.
                data = old_data[0]  # type: ignore
            except IndexError:
                raise error.PlayerNotFound("Player was not found.")

        return player.Player(
            name=data["displayName"],
            id=int(data["membershipId"]),
            is_public=data["isPublic"],
            icon=Image(str(data["iconPath"])),
            type=enums.MembershipType(data["membershipType"]),
        )

    def deseialize_clan_owner(self, data: JsonDict) -> clans.ClanOwner:
        id = data["destinyUserInfo"]["membershipId"]
        name = data["destinyUserInfo"]["displayName"]
        icon = Image(str(data["destinyUserInfo"]["iconPath"]))
        convert = int(data["lastOnlineStatusChange"])
        last_online = Time.from_timestamp(convert)
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
            joined_at=Time.clean_date(joined_at),
            types=types,
            is_public=is_public,
            type=type,
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

        return clans.Clan(
            id=id,
            name=name,
            created_at=Time.clean_date(created_at),
            member_count=member_count,
            description=description,
            about=about,
            is_public=is_public,
            banner=banner,
            avatar=avatar,
            tags=tags,
            owner=self.deseialize_clan_owner(data["founder"]),
        )

    def deserialize_app_owner(self, payload: JsonDict) -> app.ApplicationOwner:
        return app.ApplicationOwner(
            name=payload["displayName"],
            id=payload["membershipId"],
            type=enums.MembershipType(payload["membershipType"]),
            icon=Image(str(payload["iconPath"])),
            is_public=payload["isPublic"],
        )

    def deserialize_app(self, payload: JsonDict) -> app.Application:
        return app.Application(
            id=payload["applicationId"],
            name=payload["name"],
            link=payload["link"],
            status=payload["status"],
            redirect_url=payload["redirectUrl"],
            created_at=Time.clean_date(str(payload["creationDate"])),
            published_at=Time.clean_date(str(payload["firstPublished"])),
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

        total_time = Time.format_played(int(payload["minutesPlayedTotal"]), suffix=True)

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
        last_played = Time.clean_date(str(payload["dateLastPlayed"]))
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
            app=self._rest,
        )

    def deserialize_entity(self, payload: JsonDict, /) -> entity.Entity:
        props: JsonDict = payload["displayProperties"]
        inventory: JsonDict = payload["inventory"]
        return entity.Entity(
            app=self._rest,
            name=props["name"],
            description=props["description"],
            hash=payload["hash"],
            index=payload["index"],
            icon=Image(str(props["icon"])),
            has_icon=props["hasIcon"],
            water_mark=Image(str(payload["iconWatermark"])),
            banner=payload["screenshot"],
            about=payload["flavorText"],
            type=enums.Item(payload["itemType"]),
            bucket_type=enums.Item(inventory["bucketTypeHash"]),
            type_name=payload["itemTypeDisplayName"],
            tier=enums.ItemTier(inventory["tierTypeHash"]),
            tier_name=inventory["tierTypeName"],
            sub_type=enums.Item(payload["itemSubType"]),
            item_class=enums.Class(payload["classType"]),
            damage=enums.DamageType(payload["defaultDamageTypeHash"]),
            summary_hash=payload["summaryItemHash"],
            is_equippable=payload["equippable"],
            stats=payload["stats"],
            ammo_type=enums.AmmoType(payload["equippingBlock"]["ammoType"]),
            lore_hash=payload.get("loreHash", None),
        )
