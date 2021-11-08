# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).All notable changes to this project will be documented in this file.

## [Unreleased](https://github.com/nxtlo/aiobungie/compare/0.2.5b11...HEAD)

### Added
- `__repr__` overloaded for `enums.Enum` which just returns `enums.Enum.__str__`.
- `Profile.collect()` method which fetch and collect all characters at once.
- Implemented `aiobungie.crate.fireteams` objects and its methods.
- `RESTClient._request` method now takes and extra `auth` parameter for requests that requires `OAuth` header.
- The base client now takes an extra `rest_client` parameter for a `RESTClient` instance provided by the user.
This is optional and not required.
- Chinese attributes to `fireteams.FireteamLanguage`
- An API interface/abc and docs to the `factory.Factory` deserialazation factory class.
- The base client now takes an extra `rest_client` parameter for a `RESTClient` instance provided by the user.
This is optional and not required.
- A new helper function `helpers.collect()` which collect multiple arguments, join them and separate them.
- Missing `ComponentType` enum fields were added.
- Implemented `profile.ProfileProgression` profile component.
- `fetch_profile` and all alternative methods now takes `**options` kwargs which expects `auth` argument
for components that requires a bearer access token.
- `profile.ProfileItemImpl` class implements profile components that returns items. i.e., `profileinventories`, `profilecurrencies`, etc.
- More enums for Destiny 2 items.

### Breaking changes
- `Friend.user` was returning `User` and not `BungieUser`
- `fetch_profile` and all alternative methods now takes `*components` parameter which accept multiple components to be passed and retuned at once.
- `fetch_profile` and all alrernative methods now return `components.Component` instead of `profile.Profile`.
- `aiobungie.Component` enum name renamed to `ComponentType`.
- `fetch_character` no longer takes an char_type(`aiobungie.Class`) parameter and takes `character_id` which returns the character by its id.
- `fetch_character` now returns `typing.Optional[character.Character]` instead of `character.Character`
- `traits.py` moved to the root directory instead of being in `helpers`
-  All type hints used to be in `helpers.py` moved to new module `typedefs.py` in root directory.
- `undefined` types are now in `undefined.py` new module.
- `helpers.py` now will only include helper functions and classes.
- `helpers.just()` now takes a generic type for the return type.

### Changed
- `RESTClient._request` now takes a string or `rest.RequestMethod` enum for the method.
- `RESTClient._request` now takes `yarl.URL` or a string for the path. Both changes affect `RESTClient.static_request.
- Simplify not found raised errors to only raise `error.NotFound` instead of other not found errors.
- Export `enums.Enum` and `enums.IntEnum` to `enums.__all__`.
- `RESTClient` continues on `RuntimeError` errors instead of raising it.
- `traits.RESTful.static_request` now takes auth parameter for OAuth2 methods as well.
- `fireteams` enums are finalized with `typing.final`
- `Character.stats` now returns a mapping of `aiobungie.Stat` to `int` of the character stats.
- `crate.season.*` objects are now exposed to docs and `crate.__init__.py`

### Removed
- Not found errors removed and now only `error.NotFound` is raised instead.
    - `error.PlayerNotFound`
    - `error.UserNotFound`
    - `error.ActivityNotFound`
    - `error.ClanNotFound` 

### Fixed
- Some methods that required OAuth2 was buggy has been fixed.
- The rest client was showing `unclosed client_session` erros and the end of the request.
- `Friend.unique_name` wan't returning the actual unique name.
- `Factory.deserialize_friends` wasn getting the wrong payload names.
- Closing the rest client connector instead of the session.

## [0.2.5b11](https://github.com/nxtlo/aiobungie/compare/0.2.5b10...0.2.5b11) 2021-10-21

### Fixed
- `fetch_friends` and `fetch_friend_requests` methods were `POST` and fixed to `GET`.

## [0.2.5b10](https://github.com/nxtlo/aiobungie/compare/0.2.5b9...0.2.5b10) 2021-10-20

### Added
- New module `milestones.py` with `Milestone`, `MilestoneItems` objects which implements _(not fully)_ Bungie's Milestones.
- Added Stable Python 3.10 to the CI tests from 3.10-dev.
- A new type hint `IntAnd[EnumSig]` to pass a param as an enum or just an int. Example `aiobungie.Class.WARLOCK` or simply just `2`.
- Let all methods that used to only takes an enum also supports an int.
- Added [_backoff.py](https://github.com/hikari-py/hikari/blob/b6c85c932a1dc2117d2caa669bb7e52f6995273d/hikari/impl/rate_limits.py#L411) for/and Handling ratelimiting and retry after REST errors.
- A new parameter `max_retries` to `RESTClient` and `Client` which lets you choose the max REST requests retries for failuare requests.
- New exception `RateLimitedError` which's raised when being ratelimited.
- Import modules under the `typing.TYPE_CHECKING` for non-runtime modules.
- Implemented methods that requires OAuth2 bearer access tokens
    - `kick_clan_member` can be accessed either via the `Client` which returns the deserialized object or `RESTClient` for the JSON object.
    - `ban_clan_member`, `unban_clan_member` can be accessed from `RESTClient`.
    - `edit_clan`, `edit_clan_options` which edits a clan and can be accessed via `RESTClient`.
    - `equip_item`, `equip_items` in `RESTClient` and `character.Character`
    - `fetch_own_bungie_user` methods which can be accessed via `RESTClient`.
    - `deny_pending_members`, `approve_pending_members`, `add_optional_conversation` methods to `clans.Clan`.
    - `ClanConversation.edit` method to edit the convo settings.
    - Implemeted `friends.Friend` methods flow + `friends.FriendRequestView` object.
    - `transfer_item`, `pull_item` methods.
- `enums.MembershipOption` enum for group member options.
- `errors.InternalServerError` exception.
- `traits.RESTful` REST client protocol for the `RESTClient`.

### Removed
- `player.py` / `.Player` module / object has been removed in-replacement of `user.DestinyUser`.

### Changed
- PRs that used to look like this `patch/...` now should look like this `task/...` instead.
- Bound the rest response signature `ResponseSigT` to `JsonObject` and `JsonArray`
- `Clan.owner` now returns `None` if the owner was not found instead of `UNDEFINED`.
- Separate mock tests from real tests.
- Export `aiobungie/interfaces` and `aiobungie/crates` to `aiobungie/__init__.py`
- Added real client tests to ci workflow.
- Minor changes to nox pipelines.
- Instead of raising `error.AiobungieError` on `5xx` errors. `errors.InternalServerError` is not raised.
- `Profile.warlock`, `Profile.titan` and `Profile.hunter` method names changed to `Profile.fetch_hunter()`
`Profile.fetch_...`.

### Fixed
- Errors now are correctly raised.
- `fetch_membership_from_id` wasn't converting `type` enum parameter to `int`.

## [0.2.5b9](https://github.com/nxtlo/aiobungie/compare/0.2.5b7...0.2.5b8) 2021-10-1

### Added
- Two simple examples for both `RESTClient` and `Client` in `aiobungie/__init__.py` as an introduction examples.
- `__anter__` and `__aexit__` for `RESTClient` for context management and closing the client session correctly.
- `rest._Session()` object which now aquires a new aiohttp.ClientSession() for us with our settings.
- Added a simple rest example under `RESTClient` doc strings.
- Missing docs for `search_users()` method
- Missing assertions from some of the `Client` methods.
- `fetch_linked_profiles()` Method and `profile.LinkedProfile()` implementation for bungie linked profiles.
- `fetch_clan_banners()` Method and `clans.ClanBanner` Implementation for bungie clan banners.
- Added a `__repr__` method to `assets.Image()` which just returns `__str__()`.
- `close()` method for the `RESTClient` which closes the client session correctly
- Added a new class `helpers.AsyncIterator` for `async for ... in ...` support.
- `deserialize_linked_profiles()` method to deserialize linked profiles and returns `profile.LinkedProfile()` object.
- `deserialize_clan_banners()` method to deserialize clan banners and returns `clans.ClanBanner()` object.
- `Ok` class which just raises `StopIteration` exception for `AsyncIterator`.
- Parameters types for `__anter__` and `__aexit__` methods.

### Changed
- Renamed `RESTClient._fetch()` to `RESTClient._request()`.
- Switched to pdoc from pdoc3.
- Stable release for `0.2.5` Extended from `2021-09-30` to `2021-10-05`.
- The rest client now aquires the session using `rest._Session` instead of using `aiohttp.ClientSession` directly.
- Changed what was inside `__all__` in `__init__.py` to let pdoc know whats being included.
- Exporting all objects to `__all__` in `crate/__init__.py/pyi` to let pdoc include all objects.
- Renamed `RESTClient.static_search()` to `static_request()` and also added the request method parameter for the user to select instead of only GET methods.
- New dracula/darkmode style for the docs pages.
- 

### Removed
- `__anter__` and `__aexit__` from the base client.
- `from_path()` method from `Client` which can now be accessed from `Client.rest.static_request(...)`.
- `**kwargs` from `Client` and `RESTClient`.
- `fetch_vendor_sales()` method from `Client`.
- Removed `__all__` from `aiobungie/internal`.
- Removed `__init__.pyi` from `aiobungie/internal`.


### Fixed
- Fixed a bug where `Factory.deserialize_destiny_user()` was returning `displayName` instead of the actual value if the LastSeenDisplayName was not found.
- Fixed a bug where `Factory.deserialize_clan_members()` was raising `KeyError` for members the doesn't have a Bungie membership. It returns `None` intead now.
- Fixed the examples to match the client design.
