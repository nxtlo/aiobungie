# MIT License
# mypy: ignore-errors
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
from aiobungie.internal.helpers import JsonDict, JsonList, Undefined, Unknown

# Objects
from aiobungie.objects import application as app
from aiobungie.objects import character, clans, entity, player, profile, user

_LOG: typing.Final[logging.Logger] = logging.getLogger(__name__)


class Deserialize:
    """The base Deserialization class for all aiobungie objects."""

    # This is actually inspired by hikari's entity factory.

    __slots__: typing.Sequence[str] = ("_rest",)

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
                raise error.UserNotFound("Player was not found.") from None

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
                raise error.PlayerNotFound("Player was not found.") from None

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
        try:
            # All Bungie entities has a display propetie
            # if we don't find it means the entitiy was not found.
            props: JsonDict = payload["displayProperties"]
        except KeyError:
            raise error.NotFound(
                "The entity hash or the definition type is invalid"
            ) from None

        # Some entities have an inventory which
        # Includes its hash types.
        # Most entites has this
        # and for some it doesn't exists
        inventory: JsonDict = {}

        if (raw_inventory := payload.get("inventory")) is not None:
            inventory: JsonDict = raw_inventory

        # Entity tier type. Most entities have tier
        # and some doesn't exists so we have to check.

        bucket_type: typing.Optional[int] = None
        tier: typing.Optional[enums.ItemTier] = None
        tier_name: typing.Optional[str] = None

        if (raw_bucket := inventory.get("bucketTypeHash")) is not None:
            bucket_type: int = raw_bucket

        if (raw_tier := inventory.get("tierTypeHash")) is not None:
            tier: enums.ItemTier = enums.ItemTier(raw_tier)

        if (raw_tier_name := inventory.get("tierTypeName")) is not None:
            tier_name: str = raw_tier_name

        if (name := props.get("name")) == Unknown:
            name = Undefined

        if (type_name := payload.get("itemTypeDisplayName")) == Unknown:
            type_name = Undefined

        if (description := props.get("description")) == Unknown:
            description = Undefined

        if (about := payload.get("flavorText")) == Unknown:
            about = Undefined

        icon: typing.Optional[Image] = None
        if (raw_icon := props.get("icon")) is not None:
            icon: Image = Image(str(raw_icon))

        water_mark: typing.Optional[Image] = None
        if (raw_watermark := payload.get("iconWatermark")) is not None:
            water_mark: Image = Image(str(raw_watermark))

        banner: typing.Optional[Image] = None
        if (screenshot := payload.get("screenshot")) is not None:
            banner: Image = Image(str(screenshot))

        damage: typing.Optional[enums.DamageType] = None
        if (damage_type := payload.get("defaultDamageTypeHash")) is not None:
            damage: enums.DamageType = enums.DamageType(damage_type)

        summary_hash: typing.Optional[int] = None
        if (raw_summary_hash := payload.get("summaryItemHash")) is not None:
            summary_hash: int = int(raw_summary_hash)

        stats: typing.Optional[JsonDict] = {}
        if (raw_stats := payload.get("stats")) is not None:
            stats: JsonDict = raw_stats

        block: typing.Optional[enums.AmmoType] = None
        if (ammo := payload.get("equippingBlock")) is not None:
            block: enums.AmmoType = enums.AmmoType(ammo["ammoType"])

        item_class: typing.Optional[enums.Class] = None
        if (raw_item_class := payload.get("classType")) is not None:
            item_class: enums.Class = enums.Class(raw_item_class)

        return entity.Entity(
            app=self._rest,
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
