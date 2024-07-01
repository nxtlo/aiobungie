# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).All notable changes to this project will be documented in this file.

## [Unreleased](https://github.com/nxtlo/aiobungie/compare/0.2.11...HEAD)

### Added

#### methods

* `fetch_sanitized_membership`, available on both client APIs
* `search_groups`, available on both client APIs
* `RESTClient.report_player`
* `RESTClient.force_drops_repair`
* `RESTClient.claim_partner_offer`
* `RESTClient.fetch_bungie_rewards_for_user`
* `RESTClient.fetch_bungie_rewards_for_platform`
* `RESTClient.fetch_bungie_rewards`
* `Image.stream`
* `Image.chunks`

#### components

* Fully implemented the `CHARACTER LOADOUTS` component along with its framework methods, You can access it via `Components.character_loadouts`
after fetching a profile.

#### object fields

* `type`, `profile_ban_expire` and `egs_name` fields to `BungieUser`
* `code` field to `PartialBungieUser`
* `origin` field to `Application`

#### misc

* [`sain`](https://github.com/nxtlo/sain) as a required dependency. this is used mainly to replace `iterators`
* An option to use a specific executor for downloading the manifest and `Image.save` method.

```py
import concurrent.futures
# Use process pool executor to write the manifest data.
await rest.download_json_manifest(
  ...,
  executor=concurrent.futures.ProcessPoolExecutor()
)
```

### Changed

* `interfaces` dir is renamed to `api`.
* `factory` renamed to `framework` and exported to top level, no longer an `internal` package
* `factory.Factory` is now `framework.Framework`.
* `interfaces.RESTInterface` renamed to `api.RESTClient` which matches `rest.RESTClient`.
* `interfaces.FactoryInterface` renamed to `api.Framework` which matches `framework.Framework`.
* trait `Netrunner` renamed to `Send` and is no longer used, currently kept for future plans.
* trait `Serializable` renamed to `Deserialize` and its method `factory` renamed to `framework`.
* trait `ClientApp` renamed to `Compact`.
* `Client.factory` is now `Client.framework`.
* `factory.EmptyFactory` is now `framework.Empty` and is now deprecated, use `Framework()` instead.
* `Framework` doesn't require a `net` parameter anymore.
* `.net` field removed from all objects.
* `UserLike` abstract class renamed to `Unique`.
* `Framework.deserialize_fireteam_destiny_users` renamed to `deserialize_fireteam_destiny_membership`
* `FireteamMember.destiny_user` renamed to `FireteamMember.membership`
* `deserialize_app` renamed to `deserialize_application`.
* `deserialize_app_owner` renamed to `deserialize_application_member`
* `ApplicationOwner` is now `ApplicationMember` and the user fields are accessible through `.user`
* `Application.owner` field is now `Application.team` which returns the entire application roaster instead of just the owner.
* `Client.run` is deprecated and will be removed in the next major release.
* `RESTClient.with_debug` has been moved to `traits.RESTful` with a default final impl.
* `internal.assets` which contained `Image` has been moved to `aiobungie.builders`
* `Image.default_or_else` is now just `Image.default`
* `Image` now accepts `None` as a default path.
* [`sain`](https://github.com/nxtlo/sain) package is now used as the default iterator builder.
it is a dependency free that's developed by me so it won't really have any side-effects.
* If you're a `RESTPool` user, it is possible to call `build_oauth2_url` without acquiring a client instance
this is a good change for performance improvements since acquiring a client instance also means opening a TCP connection,
which is useless when you're still not making any requests.

```py
pool = aiobungie.RESTPool("token", client_id=0000, client_secret="secret")
url = pool.build_oauth2_url()

# same as
async with pool.acquire() as client:
  url = client.build_oauth2_url()
```

## Removed

The following methods were scheduled to be removed in this version.

* `PartialBungieUser.fetch_self()`
* `ProfileItemImpl.is_transferable`
* `ProfileItemImpl.collect_characters`
* `ProfileItemImpl.fetch_self`
* `DestinyMembership.fetch_self_profile`
* `QuesStatus.fetch_quest`
* `QuestStatus.fetch_step`
* `Objective.fetch_self`
* `ItemsComponent.any`
* `ItemsComponent.all`
* `Challenges.fetch_objective`
* `Rewards.fetch_self`
* `Activity.is_solo`
* `Activity.is_flawless`
* `Activity.is_solo_flawless`
* `Activity.fetch_post`
* `Character.transfer_item`
* `Character.equip_item`
* `Character.equip_items`
* `Character.pull_item`
* `Character.fetch_activities`
* `RenderedData.fetch_my_items`
* `MinimalEquipments.fetch_my_item`
* `AvailableActivity.fetch_self`
* `ClanMember.ban`
* `ClanMember.unban`
* `ClanMember.kick`
* `ClanMember.fetch_clan`
* `GroupMember.fetch_self_clan`
* `Clan.deny_pending_members`
* `Clan.approve_pending_members`
* `Clan.add_optional_conversations`
* `Clan.fetch_banned_members`
* `Clan.fetch_pending_members`
* `Clan.fetch_invited_members`
* `Clan.fetch_conversations`
* `Clan.fetch_available_fireteams`
* `Clan.fetch_fireteams`
* `Clan.fetch_members`
* `Clan.edit`
* `Clan.edit_options`
* `ClanConversation.edit`
* `CraftablesComponent.fetch_craftables`
* `SearchableEntity.fetch_self_item`

these methods above are still accessible via the both clients, either the `RESTClient` or `Client`,
their abstraction on the object just got removed not that actual implementation of the method.

> ok but how do i reproduce those?

```py
client = aiobungie.Client("...")

async def character_transfer_item() -> None:
    # Instead of: await character.transfer_item(...)
    # call it from the client directly.
    await client.rest.transfer_item(token, char_id, item_id)

async def character_fetch_activities() -> None:
    # Instead of: await character.fetch_activities(...)
    # call it from the client directly.
    await client.fetch_activities(cid, mid, mode, ...)
```

ok but why? there're multiple reasons why those got removed.

good practices; at the beginning, those methods were meant to provide a higher-level abstraction over the object itself,
so you can call them directly from the object, while it is a nice QoL thing, it can, *if misused*, end up with worse overall code.
this change should forward users with developing good code and practices and them more aware of `client` and `client.rest`.

conflict and unsafety; since those methods can also be accessed via an empty deserializer results, this introduces bugs for the user of this lib,

Example:

```py
framework = aiobungie.framework.Empty()

response = requests.get(...)
user_object = framework.deserialize_user(response.json())

# this is undefined behavior, since an empty deserializer doesn't have a client associated with it.
await user_object.fetch_self()
```

aiobungie crates are meant to be a stand-alone representation of the fetched API results. which payloads deserializes into. so those methods won't really fit in.

* `UserLike.icon`
* `UserLike.last_seen_name`
* `UserLike.is_public`
* `ComponentFields` enum
* `Image.url`, use `Image.create_url` instead.
* `iterators` package in favor of [`sain`](https://github.com/nxtlo/sain)

### Fixed

* deserializing `Friend` object was raising `KeyError` due to `name` field.
* `vault` option in method `pull_item` now works as intended, thanks to [#418](https://github.com/nxtlo/aiobungie/issues/418) for opening the issue.
* `ComponentType.CHARACTER_PROGRESSIONS` enum field name typo fixed.

## [0.2.11](https://github.com/nxtlo/aiobungie/compare/0.2.10...0.2.11) - 2024-02-05

### Added

* `Iterator.by_ref` method.
* Installing option `full` by calling `pip install aiobungie[full]`.

### Removed

* `traits.Debug` trait.
* The alias `crate` for `crates` is removed. Use `aiobungie.crates` instead.
* `rest.RequestMethod` enum.

### Changed

* Object immutability, all objects are now *frozen*.
* All sequences are now built as tuples instead of list, This helps reducing the size of the allocated bytes
and increases the speed by a little bit since tuples are sized and lists are dynamic, This obviously depends on how
large the data that has been fetched. But in general tuples are *faster*.
* Logging an `Iterator` object now doesn't consume the data.
* `set_item_lock_state` is currently unstable due to Bungie returning HTML.
* `ClanMember.current_user_memberships` is now nullable.
* Optimized factory deserialization methods.
* The `enable_debugging` parameter renamed to `debug`.
* You won't need to pass `True` when calling `RESTClient.enable_debug`.
* You'll be getting deprecation warning on `crates` level helper methods.
* `RESTClient.enable_debug` renamed to `RESTClient.with_debug` method.

## [0.2.10](https://github.com/nxtlo/aiobungie/compare/0.2.9...0.2.19) - 2023-12-12

### Fixed

* Fixed `fetch_oauth2_tokens` and `refresh_access_token` raising `BadRequest`.
* `client_secret` was being logged in the headers when enabling `TRACE` log level.

## [0.2.9](https://github.com/nxtlo/aiobungie/compare/0.2.8...0.2.9) - 2023-12-1

### Performance Improvements

* Optimized converting ISO8661 date strings to datetime, date-util package has been dropped and the converting process has been implemented directly using stdlib datetime.
* `orjson` and `ujson` are a faster replacement for the JSON lib, If were found installed, They will be used as the default JSON encode/decoder.
* `ruff` is now used as the default formatter. This is rather an internal change and shouldn't affect users.

### Added

* Added more examples.
* Lightfall loadouts methods to the `RESTClient`.
  * `equip_loadout`
  * `clear_loadout`
  * `snapshot_loadout`
  * `update_loadout`
* `CHARACTER_LOADOUTS` components type enum field.
* If your Python version is `3.10`, A backport of `datetime.fromisoformat` module will be installed.
This is required due to this specific Python version not able to parse some ISO date formats.
* `aiobungie.EmptyFactory` object. See the object docs for more info.
* `Iterator.last()` method which return the last item in the iterator.

### Changed

* Python 3.10 and above is now supported, 3.9.0 is no longer supported.
* `download_manifest` method has been renamed to `download_sqlite_manifest`
* Method `fetch_player` renamed to `fetch_membership`.
* `User.destiny` renamed to `User.memberships`, `ClanMember.bungie` to `ClanMember.bungie_user`,
`LinkedProfile.bungie` to `LinkedProfile.bungie_user` for naming consistency.
* Both download manifest methods now return `pathlib.Path` object.
* All arguments in the client constructors now required to be passed as a kwarg besides the token.
* Refactor examples code.
* `Factory` methods that used to return `Optional[T]` now returns just `T`.
* `Enum.__int__` and `Flag.__int__` doesn't check the instance of the type anymore.
* `iterators.into_iter` function renamed to `iterators.iter`.
* Use new `str | None` union instead of `Optional[str, None]`
* Improved documentations on objects.
* Some object field names has been typo fixed.
* Method `fetch_available_fireteams` typo name fixed.
* `Character.total_played_time` now returns the total time in seconds instead of string.
* Fields `emblem`, `emblem_icon` and `emblem_hash` are now Optional.

### Removed

* The `net` field has been removed from some objects.
* The `UNDEFINED` object, Fields now return `T or None` instead.

### Fixed

* Fixed multiple bugged `Factory` methods.
* `Factory.deserialize_character` was raising `KeyError` when accessing the emblem keys, Thanks to @spacez320 (#303)

## [0.2.8](https://github.com/nxtlo/aiobungie/compare/0.2.7...0.2.8) 1-24-2023

## Changed

* You can no longer pass `rest_client` instance to `Client` object.
* `Friend` object methods has been removed since they can be performed using the `RESTClient`, Including
  * `accept` -> `rest.accept_friend_request`
  * `decline` -> `rest.decline_friend_request`
  * `remove` -> `rest.remove_friend`
  * `remove_request` -> `rest.remove_friend_request`

* The `_info.py` package is renamed to `metadata.py`.

* Updated requirements versions.

## Added

* New method added to `MembershipTypeError` exception `into_membership` which converts the membership from str to `MembershipType` enum.

## Removed

* Parameter `max_ratelimit_retries` removed from client impls.

## [0.2.7](https://github.com/nxtlo/aiobungie/compare/0.2.6...0.2.7) 10-08-2022

## Breaking Changes

* Base `Client` users now will need to open the REST client before making any requests.

The old way.

```py
import aiobungie

# Here the client will initialize the TCP connector even though
# we're still not planning on making  any request which's not performant.
client = aiobungie.Client('...')
results = await client.fetch('...')
```

The new way

```py
client = aiobungie.Client('...')

# Open the REST connection and use the client normally.
async with client.rest:
    users = await client.search_users('...')
    return users[0]

# Another way of doing that manually
# This must be called within an event loop
client.rest.open()

# Do stuff with the client...

# Close.
await client.rest.close()
```

* `build_oauth2_url` now returns `builders.OAuthURL` object instead of a string URL, This is intentionally changed to seperate
the state field from the URL. A fully generated URL can still be acquired via `.compile()` method or `.url` property.

## Added

* Special method `__or__` to `FlatIterator` which allows to union two iterators togather as `x = iterator1 | iterator2`

* New method FlatIterator. `async_for_each`, whichs equavilant to `for_each` but takes an async function instead.
* Allow to customize where to download the manifest file.

Example:

```py
await client.download_manifest(name='Destiny', path='G:/Files' or pathlib.Path("Path/**/**")) # -> G:/Files/Destiny.sqlite3
```

## Added

* Enum fields `EPIC_GAMES_STORE` and `DEMON`. [#214](https://github.com/nxtlo/aiobungie/pull/214)

## Changed

* `FlatIterator` no longer support async iteration.

* Removed method `FlatIterator.discard` in favor of `FlatIterator.filter` mathod.
* `FlatIterator` class renamed to `Iterator`.
* Enum flags now uses bitwise `<<` for its fields instead of `=` numbers assign.

## Removed

* `CharacterError` exception. This was supposed to be removed with `0.2.6`.

## Fixed

* Docs colors.

## [0.2.6](https://github.com/nxtlo/aiobungie/compare/0.2.5...0.2.6)

## Added

* `Debug` trait.

* Seson 17 new activities.
* Internal methods names has changed.
* Rift, Lostsector, Zonecontrol and Iron Banner Rift enum gamemode fields.

## Changed

* Optimized object deserialization proccess.

* `helpers.awaits` now returns `Sequence` instead of `Collection`.
* `RESPool` No longer sets the metadata after acquiring new instance everytime. The pool's `metadata` must be used now.
* Some of `PostActivityPlayer` fields changed to optional due to Bungie not including them in payloads.
* `_deserialize_post_activity` is now exposed in the interface for self use.

## Removed

* `helpers.just` function.

* Useless ABCs.
* Guardian Games fireteam activity.

## Fixed

* Thanks to @xhl6666, A bug has been Fixed (#193) where using `fetch_post_activity` raised `KeyError` in some cases.

## [0.2.6a3](https://github.com/nxtlo/aiobungie/compare/0.2.6a2...0.2.6a3) 2022-05-8

## Added

* New `builders.py` contains results of received/sent objects to the API.

* `RESTPool` impl.

## Changed

* `REST_DEBUG` level name to `TRACE`

* `enable_logging` parameter now accepts `str | int | bool`.
* Setting the level to `True` now will only log minimal information.
* `PlugSocketBuilder` and `OAuth2Response` has been moved to `builders.py`
and both objects are not exposed to the project namespace anymore. However `aiobungie.builders.*` is exposed.
* `aiobungie.crate` is renamed to `crates` + Added an alias for `crate` for backward versions.
* `RESTnterface` and `RESTClient` is now completly `async def` + typesafe.

## Removed

## Fixed

* Objective in metrics components was always returning `None`

## [0.2.6a2](https://github.com/nxtlo/aiobungie/compare/0.2.6a1...0.2.6a2) 2022-03-17

## Added

* Ability to read and save any resource that returns an `Image`.

* Image mime types enum in assets.
* fetch_aggregated_activity_stats method.
* fetch_json_manifest method.
* fetch_manifest_version method.

## Changed

* Objects no longer type hinted with `MaybeImage` and now return `Image` instead.

* Manifest methods that open files are non-blocking now.
* connect_manifest is now deprecated and scheduled for removal in 0.2.6.
* fetch_manifest_path now return all JSON object paths instead of the SQLite one.
* download_manifest now takes a `force` parameter to force downloading the manifest.
* ABC class `Entity` is renamed to `EntityBase` and `BaseEntity` is now `Entity`.
* property `index` has been removed from `EntityBase` to allow `SearchableEntity` inherit from it.

## Removed

* MaybeImage type hint.

## Fixed

* FlatIterator.sort wasn't sorting right.

## [0.2.6a1](https://github.com/nxtlo/aiobungie/compare/0.2.6a0...0.2.6a1) 2022-03-05

## Major API changes

* All methods that used to take `*components` now take a list of component types instead.
* All components should be passed as is without unpacking nor using the `.value` attribute.

* The `auth` parameter is now exposed as an actual parameter and not a kwarg.

Example

```py
await client.fetch_profile(
    ...,
    components=[aiobungie.ComponentType.ALL_PROFILES, aiobungie.ComponentType.CHARACTERS, ...],
    auth="..."
)
```

## Added

* Included all activities in `FireteamActivity`.

* Standard `FlatIterator` and `into_iter` in `internal.iterators` and exported to the project's namespace.

Example usage

```py
import aiobungie

client = aiobungie.Client()

friends = await client.fetch_friends(...)

# This can either be used with `async for` or `for`

async for friend in (
    aiobungie.into_iter(friends) # Transform the sequence into a flat iterator.
    .filter(lambda friend: friend.type is MembershipType.STEAM)  # Filter to only steam friends.
    .take(5)  # Limit the results to 5 friends
    .discard(lambda friend: friend.online_status is Presence.ONLINE)  # Drop friends that are not online.
    .reversed()  # Reverse them.
):
    print(friend.unique_name)
```

## Changed

* Parameter `memberid` in `fetch_profile` is now `membership_id`.

* Methods that now return a `FlatIterator` instead of a standard sequence.
  * fetch_activities
  * search_users
  * fetch_clan_admins
  * fetch_clan_members
  * search_entities

## Fixed

* `KeyError` was being thrown when deserializing `fireteam_activities`.

## Removed

* Method `helpers.collect`.

## [0.2.6a0](https://github.com/nxtlo/aiobungie/compare/0.2.5...0.2.6a0) 2022-02-26

## Added

* `RESTClient` now takes an extra parameter `enable_debugging`, If set to `True` then
it will debug responses and log them.

* `RESTClient.enable_debugging` method which does the same thing as above.
* A better looking headers logging.
* A unique trace logging level `rest.REST_DEBUG` which will be used as the main logging level
for REST debugging.
* `destination_hash` and `activity_hash` fields to `Objective`.
* `Flag` enumeration.

## Changed

* Implemented The Witch Queen API update changes
  * `OFFSNSIVE` Game field to enum `GameMode`.
  * `CRAFTABLES` enum field to `ComponentType`.
  * New `CraftablesComponent` which's returned when fetching a profile with the craftables component,
    This is accessed by `Component.character_craftables`.
  * Added `entity.ObjectiveUIStyle` enum.
  * `ui_label` and `ui_style` fields to `ObjectiveEntity`.
  * `LEVEL_AND_REWARD` field to `ValueUIStyle` enum.
  * `CraftableItem` and `CraftableSocket` and `CraftableSocketPlug` objects.

* `InventoryEntity.tier_type` now returns `TierType` instead of `int`.
* `TierType` enum.
* `helpers.unimplemented` methods which marks methods and classes as unimplemented.
* Improve documentation for `traits.py`.
* `traits.ClientBase` name changed to `ClientApp`.
* Methods that used to raise `NotImplementedError` no only warns.
* Improve `helpers.deprecated` method.
* `CraftablesComponent.craftables` now return an optional `CraftableItem` if it returns null.
* `MetricsComponent.metrics`'s objective now return `None` it returns null.
* `Objective.progress` is not optional.

## Removed

* `IntEnum` since now its independently used with builtin `int`.

## Fixed

* enum field `GreenPips` wasn't incluede in `ValueUIStyle` which was raising `ValueError` [#123](https://github.com/nxtlo/aiobungie/pull/132)

* Fix a bug where `ApplicationOwner__str__()` was raising `RecursionError`.

* Fixes an error where `error.raise_error` wasn't being called when getting a non JSON response AKA `text/**`.
See [#143](https://github.com/nxtlo/aiobungie/issues/143)

## [0.2.5](https://github.com/nxtlo/aiobungie/compare/0.2.5b14...0.2.5) 2022-02-02

This is `0.2.5` stable release and all alpha/beta releases falls under this.

These changes are considered part of `0.2.5`.

### Added

* `user.SearchableDestinyUser`.

* More profile and characters components.
* `factory.Factory` and `assets.Image` are now exported to top level.
* Almost 95% of the API endpoints has been added.
* `__int__` method to `UndefinedType` which returns a literal `0`
* `KeyError`s was being raised during deserialization payloads.

### Changed

* `DestinyUser` has been renamed to `DestinyMembership`.

* `InternalServerError` is now raised when the API is down instead of `OSError`.
* Factory methods name changes for consistency.
  * `deserialize_destiny_user` -> `*_destiny_membership`.
  * `deserialize_destiny_members` -> `*_destiny_memberships`
  * `deserialize_found_users` -> `*_searched_user` and no longer returns a sequence.
* `Client.search_users` now returns `Sequence[SearchableDestinyUser]`

### Fixed

* `Client.search_users` was raising errors due to deserializing.

## [0.2.5b14](https://github.com/nxtlo/aiobungie/compare/0.2.5b13...0.2.5b14) 2022-1-13

### Added

* `fetch_unique_weapon_history` method.

* Assists fields to `activity.ExtendedWeaponValues`
* `joine_date` field to `clans.ClanAdmin`
* Logging time takes between each request.
* Implmented `transitory` profile component along with its objects in `fireteams.py`.
* You can now store data using `client.metadata` property from either rest or base client which can be used globally.
* Added a profile_link property to `BungieUser` which returns their profile link.
* Implemented `components.ItemComponent`.
* new `items.py` module includes all item related objects.
* `enums.ItemSubType` for subtype inventory items.
* `ClanMember.member_type` field.
* `ClanMember.is_admin` and `is_founder` fields.
* `Clan.progression` and some extra other fields to `clans.Clan`.
* `fetch_clan_weekly_rewards` method.
* `fetch_clan` and `fetch_clan_from_id` now can take `access_token` parameter for authorized user requests.

### Removed

* `Friend.is_pending` method since this can be checked using `Friend.relationship`.

* `Friend.pending` method since this can be checked using `Client.fetch_friend_requests`.
* `Friend.add` method since this can be used via `RESTClient.send_friend_request`
* `helpers.AsyncIterator` has been removed.
* `clans.ClanOwner` in-favor of `clans.ClanMember`.
* `fetch_member`, use `fetch_members(name="...")` instead.

### Changed

* Significantly optimized factory's checkings and deserializing.

* `Client.fetch_groups_for_member` now returns a sequence instead of a signle object.
This also references `fetch_potentional_groups_forr_member`.
* Only non-abcs and non-enums classes are exported to `__all__` in `crate.__init__.py`
* `access_token` parameter is now always positional on all methods.
* enum `Item` name changed to `ItemType`.
* enum `DamageType` now holds the actual enum values instead of the hashes.
* All crate fields are now relaxed. Which have the field name and type only.
* All objects that inherits from `user.UserLike`. `object.__str__()` and `str(object)` will now return the full unique name for that object.
* `LinkedProfile` no longer supports `async for`.
* `InventoryEntity.sub_type` now returns `enums.ItemSubType` instead of `enums.ItemType`.
* Some parameters are now positional.
* `Client.fetch_clan_members` now accepts `name` parameter.
* `Client.fetch_clan_admins` now returns a sequence of `ClanMember` instead of `ClanAdmin`.
* `ClanMember.bungie` is now an optional field.
* `Clan.fetch_my_fireteams` method renamed to `fetch_fireteams`.
* `ClanMember` now inherits from `user.DesinyUser` for no field duplications.
* Name Changes for consistensy
  * `fetch_user` method renamed to `fetch_bungie_user`.
  * `fetch_hard_linked` method renamed to `fetch_hardlinked_credentials`.
  * `fetch_app` method renamed to `fetch_application`.
  * `fetch_own_bungie_user` renamed to `fetch_current_user_memberships`.
* More methods has been added to `RESTClient`.

### Fixed

* `Character.last_played` wasn't returning a datetime object.

* `is_online`, `last_online`, `joined_at` and `group_id` fields now correctly returned for `ClanMember`

## [0.2.5b13](https://github.com/nxtlo/aiobungie/compare/0.2.5b12...0.2.5b13) 2021-12-24

### Added

* `BadRequest` exception.

* `Character.transfer_item` and `Character.pull_item` now takes missing `vault` option.
* `Character.fetch_activities` method.
* Finished implementing post activities methods.
* `is_flawless`, `is_solo` and `is_solo_flawless` useful properties to for both `Activity` and `PostActivity`.
* Post activity extended values and player weapons values.
* `rest._handle_error` method moved to `error.py` and renamed to `raise_error`
* `rest.OAuth2Response` class returned for OAuth2 responses.
* `RESTClient.client_id` property.
* `RESTClient.collect_components` is now protected for the class.
* `RESTClient.build_oauth2_url` method to build an OAuth2 URL.
* `RESTClient.fetch_oauth2_tokens` and `RESTClient.refresh_access_token` new methods.
* Missing `entity.InventoryEntity` fields were added.
* `fetch_user_credentials` method.
* `insert_socket_plug` and `insert_socket_plug_free` methods.
* `rest.PlugSocketBuilder` to build socket plugs.
* `set_item_lock_state` and `set_quest_lock_state` methods.
* `search_entities` method.
* OAuth2 example.
* Manifest example.
* `download_manifest`, `connect_manifest` REST methods.

### Changed

* Python 3.8 is now dropped, Python 3.9 and above are supported.

* `collections.abc` is now used for all type hints excluding `typing.Union[]` and `typing.Opional[]`.
* `typedefs.JsonObject` and `JsonArray` uses uppercase `JSON`.
* Exceptions now has fields and improved.
* `fetch_activity` function name changed to `fetch_activities`
* `fetch_activities` now returns a sequence(`collections.Sequence[Activity]`) of activities instead of a singular activity object.
* `ActivityVaules.team` returns `typing.Optional[int]` now instead of `int`.
* Exported `aiobungie.url` to `aiobungie.__init__.py`
* `Client` and `RESTClient` now take 2 extra optional parameters, `client_secret` and `client_id` for OAuth2 usage.
* `traits.Serializeable.serialize` property name changed to `factory`.
* `static_request` now only takes a str for the route.
* All manifest methods are accessed through the RESTClient.
* `fetch_manifest` method renamed to `read_manifest_bytes`.

### Removed

* Fields from `enums.Item` since they don't belong to there.

* web_app example.
* `Client.fetch_manifest` method.
* Manifest object

## [0.2.5b12](https://github.com/nxtlo/aiobungie/compare/0.2.5b11...0.2.5b12) 2021-12-10

### Added

* Implemented Bungie profile components. *`not all of them`*.

* `crate.records` which implements Bungie record component.
* `__repr__` overloaded for `enums.Enum` which just returns `enums.Enum.__str__`.
* `Profile.collect_characters()` method which fetch and collect all profile characters at once.
* Implemented `aiobungie.crate.fireteams` objects and its methods.
* `RESTClient._request` method now takes and extra `auth` parameter for requests that requires `OAuth` header.
* The base client now takes an extra `rest_client` parameter for a `RESTClient` instance provided by the user.
This is optional and not required.
* Chinese attributes to `fireteams.FireteamLanguage`
* An API interface/abc and docs to the `factory.Factory` deserialazation factory class.
This is optional and not required.
* A new helper function `helpers.collect()` which collect multiple arguments, join them and separate them.
* Missing `ComponentType` enum fields were added.
* Implemented `profile.ProfileProgression` profile component.
* `profile.ProfileItemImpl` class implements profile components that returns items. i.e., `profileinventories`, `profilecurrencies`, etc.
* More enums for Destiny 2 items.
* `entity.BaseEntity` class which all entities now inherit from.
* `fetch_objective_entity()` method which returns `entity.ObjetiveEntity` entity.
* `enums.ComponentType` now has fields `ALL_X` which includes all component fields for a specific component.
* Implemented new Activities classes and entities in `crate.activity`.

### Breaking changes

* `Profile.collect` method renamed to `collect_characters` for consistency.

* `fetch_profile` and all alternative methods now takes `**options` kwargs which expects `auth` argument- `fetch_profile` and all alternative methods now takes `*components` parameter which accept multiple components to be passed and retuned at once.
* `fetch_profile` now returns `components.Component` instead of `profile.Profile`.
* `fetch_character` now returns `components.CharacterComponent` instead of `character.Character`.
* `fetch_character` no longer takes a char_type(`aiobungie.Class`) parameter and takes `character_id` which returns the character by its id instead of type.
* `fetch_character` and all alternative methods now takes `*components` parameter which accept multiple components to be passed and retuned at once and
`**options` kwargs which expects `auth="BEARER_TOKEN"` argument for components that requires a bearer access token.
* `aiobungie.Component` enum name renamed to `ComponentType`.
* `traits.py` moved to the root directory instead of being in `helpers`
* All type hints used to be in `helpers.py` moved to new module `typedefs.py` in root directory.
* `undefined` types are now in `undefined.py` new module.
* `profile.ProfileComponent` ABC has been removed in favor of `profile.Profile`.
* `Client.serialize` property name changed to `Client.factory`.
* `Client.fetch_public_milestone_content` method now returns `MilesonteContent` instead of `Milesonte`.

### Changed

* `RESTClient._request` now takes a string or `rest.RequestMethod` enum for the method.

* `RESTClient._request` now takes `yarl.URL` or a string for the path. Both changes affect `RESTClient.static_request.
* `helpers.just()` now takes a generic type for the return type hint.
* `helpers.py` now only include helper functions and classes.
* Simplify not found raised errors to only raise `error.NotFound` instead of other not found errors.
* Export `enums.Enum` and `enums.IntEnum` to `enums.__all__`.
* `RESTClient` continues on `RuntimeError` errors instead of raising it.
* `traits.RESTful.static_request` now takes auth parameter for OAuth2 methods as well.
* `fireteams` enums are finalized with `typing.final`
* `Character.stats` now returns a mapping of `aiobungie.Stat` to `int` of the character stats.
* `crate.season.*` objects are now exposed to docs and `crate.__init__.py`
* `fetch_membership()` Now requires an extra parameter `code` seperatly instead of `NAME#123`

### Removed

* `profile.Profile` methods `fetch_warlock`, `fetch_titan`, and `fetch_hunter` has been removed since the expected character to be returned wasn't always guranteed, This method has been replaced with `collect_characters` which fetch all found characters
and returns a collection of them.

You can always check for the character class type i.e.,

```py
characters_components = await profile.collect_characters(aiobungie.ComponentType.CHARACTERS)
for component in characters_components:
    # Check if the character component avilable.
    # This should always be available since we passed it to the request.
    if character := component.character:
        if isinstance(character.class_type, aiobungie.Class.WARLOCK):
            ...
    else:
        ...
```

* Not found errors removed and now only `error.NotFound` is raised instead.
  * `error.PlayerNotFound`
  * `error.UserNotFound`
  * `error.ActivityNotFound`
  * `error.ClanNotFound`

### Fixed

* Fixed `Friend.user` was returning `User` and not `BungieUser`

* Some methods that required OAuth2 was buggy has been fixed.
* The rest client was showing `unclosed client_session` erros and the end of the request.
* `Friend.unique_name` wasn't returning the actual unique name.
* `Factory.deserialize_friends` wasn getting the wrong payload names.
* Closing the rest client connector instead of the session.

## [0.2.5b11](https://github.com/nxtlo/aiobungie/compare/0.2.5b10...0.2.5b11) 2021-10-21

### Fixed

* `fetch_friends` and `fetch_friend_requests` methods were `POST` and fixed to `GET`.

## [0.2.5b10](https://github.com/nxtlo/aiobungie/compare/0.2.5b9...0.2.5b10) 2021-10-20

### Added

* New module `milestones.py` with `Milestone`, `MilestoneItems` objects which implements *(not fully)* Bungie's Milestones.

* Added Stable Python 3.10 to the CI tests from 3.10-dev.
* A new type hint `IntAnd[EnumSig]` to pass a param as an enum or just an int. Example `aiobungie.Class.WARLOCK` or simply just `2`.
* Let all methods that used to only takes an enum also supports an int.
* Added [_backoff.py](https://github.com/hikari-py/hikari/blob/b6c85c932a1dc2117d2caa669bb7e52f6995273d/hikari/impl/rate_limits.py#L411) for/and Handling ratelimiting and retry after REST errors.
* A new parameter `max_retries` to `RESTClient` and `Client` which lets you choose the max REST requests retries for failuare requests.
* New exception `RateLimitedError` which's raised when being ratelimited.
* Import modules under the `typing.TYPE_CHECKING` for non-runtime modules.
* Implemented methods that requires OAuth2 bearer access tokens
  * `kick_clan_member` can be accessed either via the `Client` which returns the deserialized object or `RESTClient` for the JSON object.
  * `ban_clan_member`, `unban_clan_member` can be accessed from `RESTClient`.
  * `edit_clan`, `edit_clan_options` which edits a clan and can be accessed via `RESTClient`.
  * `equip_item`, `equip_items` in `RESTClient` and `character.Character`
  * `fetch_own_bungie_user` methods which can be accessed via `RESTClient`.
  * `deny_pending_members`, `approve_pending_members`, `add_optional_conversation` methods to `clans.Clan`.
  * `ClanConversation.edit` method to edit the convo settings.
  * Implemeted `friends.Friend` methods flow + `friends.FriendRequestView` object.
  * `transfer_item`, `pull_item` methods.
* `enums.MembershipOption` enum for group member options.
* `errors.InternalServerError` exception.
* `traits.RESTful` REST client protocol for the `RESTClient`.

### Removed

* `player.py` / `.Player` module / object has been removed in-replacement of `user.DestinyUser`.

### Changed

* PRs that used to look like this `patch/...` now should look like this `task/...` instead.

* Bound the rest response signature `ResponseSigT` to `JsonObject` and `JsonArray`
* `Clan.owner` now returns `None` if the owner was not found instead of `UNDEFINED`.
* Separate mock tests from real tests.
* Export `aiobungie/interfaces` and `aiobungie/crates` to `aiobungie/__init__.py`
* Added real client tests to ci workflow.
* Minor changes to nox pipelines.
* Instead of raising `error.AiobungieError` on `5xx` errors. `errors.InternalServerError` is not raised.
* `Profile.warlock`, `Profile.titan` and `Profile.hunter` method names changed to `Profile.fetch_hunter()`
`Profile.fetch_...`.

### Fixed

* Errors now are correctly raised.

* `fetch_membership_from_id` wasn't converting `type` enum parameter to `int`.

## [0.2.5b9](https://github.com/nxtlo/aiobungie/compare/0.2.5b7...0.2.5b8) 2021-10-1

### Added

* Two simple examples for both `RESTClient` and `Client` in `aiobungie/__init__.py` as an introduction examples.

* `__anter__` and `__aexit__` for `RESTClient` for context management and closing the client session correctly.
* `rest._Session()` object which now aquires a new aiohttp.ClientSession() for us with our settings.
* Added a simple rest example under `RESTClient` doc strings.
* Missing docs for `search_users()` method
* Missing assertions from some of the `Client` methods.
* `fetch_linked_profiles()` Method and `profile.LinkedProfile()` implementation for bungie linked profiles.
* `fetch_clan_banners()` Method and `clans.ClanBanner` Implementation for bungie clan banners.
* Added a `__repr__` method to `assets.Image()` which just returns `__str__()`.
* `close()` method for the `RESTClient` which closes the client session correctly
* Added a new class `helpers.AsyncIterator` for `async for ... in ...` support.
* `deserialize_linked_profiles()` method to deserialize linked profiles and returns `profile.LinkedProfile()` object.
* `deserialize_clan_banners()` method to deserialize clan banners and returns `clans.ClanBanner()` object.
* `Ok` class which just raises `StopIteration` exception for `AsyncIterator`.
* Parameters types for `__anter__` and `__aexit__` methods.

### Changed

* Renamed `RESTClient._fetch()` to `RESTClient._request()`.

* Switched to pdoc from pdoc3.
* Stable release for `0.2.5` Extended from `2021-09-30` to `2021-10-05`.
* The rest client now aquires the session using `rest._Session` instead of using `aiohttp.ClientSession` directly.
* Changed what was inside `__all__` in `__init__.py` to let pdoc know whats being included.
* Exporting all objects to `__all__` in `crate/__init__.py/pyi` to let pdoc include all objects.
* Renamed `RESTClient.static_search()` to `static_request()` and also added the request method parameter for the user to select instead of only GET methods.
* New dracula/darkmode style for the docs pages.
*

### Removed

* `__anter__` and `__aexit__` from the base client.

* `from_path()` method from `Client` which can now be accessed from `Client.rest.static_request(...)`.
* `**kwargs` from `Client` and `RESTClient`.
* `fetch_vendor_sales()` method from `Client`.
* Removed `__all__` from `aiobungie/internal`.
* Removed `__init__.pyi` from `aiobungie/internal`.

### Fixed

* Fixed a bug where `Factory.deserialize_destiny_user()` was returning `displayName` instead of the actual value if the LastSeenDisplayName was not found.

* Fixed a bug where `Factory.deserialize_clan_members()` was raising `KeyError` for members the doesn't have a Bungie membership. It returns `None` intead now.
* Fixed the examples to match the client design.
