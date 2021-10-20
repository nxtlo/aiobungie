# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).All notable changes to this project will be documented in this file.

## [Unreleased](https://github.com/nxtlo/aiobungie/compare/0.2.5b10...HEAD)


## [0.2.5b10](https://github.com/nxtlo/aiobungie/compare/0.2.5b9...HEAD) 2021-10-20

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

## [0.2.5b9](https://github.com/nxtlo/aiobungie/compare/0.2.5b8...HEAD) 2021-10-1

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