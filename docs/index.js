URLS=[
"aiobungie/index.html",
"aiobungie/client.html",
"aiobungie/crate/index.html",
"aiobungie/crate/user.html",
"aiobungie/crate/character.html",
"aiobungie/crate/profile.html",
"aiobungie/crate/activity.html",
"aiobungie/crate/application.html",
"aiobungie/crate/clans.html",
"aiobungie/crate/entity.html",
"aiobungie/crate/friends.html",
"aiobungie/crate/members.html",
"aiobungie/crate/player.html",
"aiobungie/crate/season.html",
"aiobungie/error.html",
"aiobungie/ext/index.html",
"aiobungie/ext/meta.html",
"aiobungie/interfaces/index.html",
"aiobungie/interfaces/rest.html",
"aiobungie/internal/index.html",
"aiobungie/internal/assets.html",
"aiobungie/internal/enums.html",
"aiobungie/internal/helpers.html",
"aiobungie/internal/serialize.html",
"aiobungie/internal/time.html",
"aiobungie/internal/traits.html",
"aiobungie/rest.html",
"aiobungie/url.html"
];
INDEX=[
{
"ref":"aiobungie",
"url":0,
"doc":"A Pythonic  async / await framework / wrapper for interacting with the Bungie API."
},
{
"ref":"aiobungie.Client",
"url":0,
"doc":"Basic implementation for a client that interacts with Bungie's API. Attributes      - token:  builtins.str Your Bungie's API key or Token from the developer's portal."
},
{
"ref":"aiobungie.Client.serialize",
"url":0,
"doc":"A property that returns a deserializer object for the client."
},
{
"ref":"aiobungie.Client.rest",
"url":0,
"doc":"The rest client we make the http request to the API with."
},
{
"ref":"aiobungie.Client.request",
"url":0,
"doc":"Returns a client network state for making external requests."
},
{
"ref":"aiobungie.Client.run",
"url":0,
"doc":"Runs a Coro function until its complete. This is equivalent to asyncio.get_event_loop().run_until_complete( .) Parameters      future:  typing.Coroutine[typing.Any, typing.Any, typing.Any] Your coro function. Example    -   async def main() -> None: player = await client.fetch_player(\"Fate\") print(player.name) client.run(main(  ",
"func":1
},
{
"ref":"aiobungie.Client.from_path",
"url":0,
"doc":"Raw http search given a valid bungie endpoint. Parameters      path:  builtins.str The bungie endpoint or path. A path must look something like this \"Destiny2/3/Profile/46111239123/ .\" kwargs:  typing.Any Any other key words you'd like to pass through. Returns    -  typing.Any Any object.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_manifest",
"url":0,
"doc":"Access The bungie Manifest. Returns    -  aiobungie.ext.Manifest A Manifest crate.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_user",
"url":0,
"doc":"Fetch a Bungie user by their id.  note This returns a Bungie user membership only. Take a look at  Client.fetch_membership_from_id for other memberships. Parameters      id:  builtins.int The user id. Returns    -  aiobungie.crate.user.BungieUser A Bungie user. Raises     aiobungie.error.UserNotFound The user was not found.",
"func":1
},
{
"ref":"aiobungie.Client.search_users",
"url":0,
"doc":"",
"func":1
},
{
"ref":"aiobungie.Client.fetch_user_themes",
"url":0,
"doc":"Fetch all available user themes. Returns    -  typing.Sequence[aiobungie.crate.user.UserThemes] A sequence of user themes.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_hard_types",
"url":0,
"doc":"Gets any hard linked membership given a credential. Only works for credentials that are public just  aiobungie.CredentialType.STEAMID right now. Cross Save aware. Parameters      credential:  builtins.int A valid SteamID64 type:  aiobungie.CredentialType The crededntial type. This must not be changed Since its only credential that works \"currently\" Returns    -  aiobungie.crate.user.HardLinkedMembership Information about the hard linked data.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_membership_from_id",
"url":0,
"doc":"Fetch Bungie user's memberships from their id. Notes   -  This returns both BungieNet membership and a sequence of the player's DestinyMemberships Which includes Stadia, Xbox, Steam and PSN memberships if the player has them, see  aiobungie.crate.user.DestinyUser for indetailed.  If you only want the bungie user. Consider using  Client.fetch_user method. Parameters      id :  builtins.int The user's id. type :  aiobungie.MembershipType The user's membership type. Returns    -  aiobungie.crate.User A Bungie user with their membership types. Raises    aiobungie.UserNotFound The requested user was not found.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_profile",
"url":0,
"doc":"Fetche a bungie profile. See  aiobungie.crate.Profile to access other components. Parameters      memberid:  builtins.int The member's id. type:  aiobungie.MembershipType A valid membership type. Returns      aiobungie.crate.Profile A Destiny 2 player profile. Raises     aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_player",
"url":0,
"doc":"Fetch a Destiny 2 Player. Parameters      - name:  builtins.str The Player's Name.  note You must also pass the player's unique code. A full name parameter should look like this  Fate\u6012 4275 type:  aiobungie.internal.enums.MembershipType The player's membership type, e,g. XBOX, STEAM, PSN Returns      typing.Sequence[aiobungie.crate.Player] A sequence of the found Destiny 2 Player memberships. Raises     aiobungie.PlayerNotFound The player was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_character",
"url":0,
"doc":"Fetch a Destiny 2 character. Parameters      memberid:  builtins.int A valid bungie member id. character:  aiobungie.internal.enums.Class The Destiny character to retrieve. type:  aiobungie.internal.enums.MembershipType The member's membership type. Returns    -  aiobungie.crate.Character A Bungie character crate. Raises     aiobungie.error.CharacterError raised if the Character was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_vendor_sales",
"url":0,
"doc":"",
"func":1
},
{
"ref":"aiobungie.Client.fetch_activity",
"url":0,
"doc":"Fetch a Destiny 2 activity for the specified user id and character. Parameters      member_id:  builtins.int The user id that starts with  4611 . character_id:  builtins.int The id of the character to retrieve. mode:  aiobungie.internal.enums.GameMode This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc. membership_type:  aiobungie.internal.enums.MembershipType The Member ship type, if nothing was passed than it will return all. page: typing.Optional[builtins.int] The page number limit: typing.Optional[builtins.int] Limit the returned result. Returns    -  aiobungie.crate.Activity A Bungie activity. Raises     aiobungie.error.ActivityNotFound The activity was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_post_activity",
"url":0,
"doc":"Fetch a post activity details.  warning This http request is not implemented yet and it will raise  NotImplementedError Parameters      instance:  builtins.int The activity instance id. Returns    -  aiobungie.crate.activity.PostActivity Information about the requested post activity.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_clan_from_id",
"url":0,
"doc":"Fetch a Bungie Clan by its id. Parameters      - id:  builtins.int The clan id. Returns      aiobungie.crate.Clan An Bungie clan. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_clan",
"url":0,
"doc":"Fetch a Clan by its name. This method will return the first clan found with given name name. Parameters      name:  builtins.str The clan name type  aiobungie.GroupType The group type, Default is one. Returns    -  aiobungie.crate.Clan A Bungie clan. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_clan_member",
"url":0,
"doc":"Fetch a Bungie Clan member.  note This method also can be also accessed via  aiobungie.crate.Clan.fetch_member() to fetch a member for the fetched clan. Parameters      clan_id :  builsins.int The clans id name :  builtins.str The clan member's name type :  aiobungie.MembershipType An optional clan member's membership type. Default is set to  aiobungie.MembershipType.NONE Which returns the first matched clan member by their name. Returns    -  aiobungie.crate.ClanMember A Bungie Clan member. Raises     aiobungie.ClanNotFound The clan was not found.  aiobungie.NotFound The member was not found.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_clan_members",
"url":0,
"doc":"Fetch a Bungie Clan member. if no members found in the clan you will get an empty sequence.  note This method also can be also accessed via  aiobungie.crate.Clan.fetch_members() to fetch a member for the fetched clan. Parameters      clan_id :  builsins.int The clans id type :  aiobungie.MembershipType An optional clan member's membership type. Default is set to  aiobungie.MembershipType.NONE Which returns the first matched clan member by their name. Returns    -  typing.Sequence[aiobungie.crate.ClanMember] A sequence of bungie clan members. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_inventory_item",
"url":0,
"doc":"Fetch a static inventory item entity given a its hash. Parameters      type:  builtins.str Entity's type definition. hash:  builtins.int Entity's hash. Returns    -  aiobungie.crate.InventoryEntity A bungie inventory item.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_app",
"url":0,
"doc":"Fetch a Bungie Application. Parameters      - appid:  builtins.int The application id. Returns      aiobungie.crate.Application A Bungie application.",
"func":1
},
{
"ref":"aiobungie.RESTClient",
"url":0,
"doc":"A REST only client implementation for interacting with Bungie's REST API. Attributes      token :  builtins.str A valid application token from Bungie's developer portal."
},
{
"ref":"aiobungie.RESTClient.fetch_user",
"url":0,
"doc":"Fetch a Bungie user by their id. Parameters      id:  builtins.int The user id. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of users objects. Raises     aiobungie.error.UserNotFound The user was not found.",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_user_themes",
"url":0,
"doc":"Fetch all available user themes. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonArray] A JSON array of user themes.",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_membership_from_id",
"url":0,
"doc":"Fetch Bungie user's memberships from their id. Parameters      id :  builtins.int The user's id. type :  aiobungie.MembershipType The user's membership type. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the found user. Raises    aiobungie.UserNotFound The requested user was not found.",
"func":1
},
{
"ref":"aiobungie.RESTClient.static_search",
"url":0,
"doc":"Raw http search given a valid bungie endpoint. Parameters      path:  builtins.str The bungie endpoint or path. A path must look something like this \"Destiny2/3/Profile/46111239123/ .\" kwargs:  typing.Any Any other key words you'd like to pass through. Returns    -  typing.Any Any object.",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_player",
"url":0,
"doc":"Fetch a Destiny 2 Player. Parameters      - name:  builtins.str The Player's Name.  note You must also pass the player's unique code. A full name parameter should look like this  Fate\u6012 4275 type:  aiobungie.internal.enums.MembershipType The player's membership type, e,g. XBOX, STEAM, PSN Returns      ResponseSig[aiobungie.internal.helpers.JsonArray] A JSON array of the found players. Raises     aiobungie.PlayerNotFound The player was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.RESTClient.search_users",
"url":0,
"doc":"Search for users by their global name and return all users who share this name. Parameters      name :  str The user name. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonArray] A JSON array of the found users. Raises     aiobungie.NotFound The user(s) was not found.",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_clan_from_id",
"url":0,
"doc":"Fetch a Bungie Clan by its id. Parameters      - id:  builtins.int The clan id. Returns      ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the clan. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_clan",
"url":0,
"doc":"Fetch a Clan by its name. This method will return the first clan found with given name name. Parameters      name:  builtins.str The clan name type  aiobungie.GroupType The group type, Default is one. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the clan. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_app",
"url":0,
"doc":"Fetch a Bungie Application. Parameters      - appid:  builtins.int The application id. Returns      ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the application.",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_character",
"url":0,
"doc":"Fetch a Destiny 2 player's characters. Parameters      memberid:  builtins.int A valid bungie member id. type:  aiobungie.internal.enums.MembershipType The member's membership type. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the requested character. Raises     aiobungie.error.CharacterError raised if the Character was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_activity",
"url":0,
"doc":"Fetch a Destiny 2 activity for the specified user id and character. Parameters      member_id:  builtins.int The user id that starts with  4611 . character_id:  builtins.int The id of the character to retrieve. mode:  aiobungie.internal.enums.GameMode This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc. membership_type:  aiobungie.internal.enums.MembershipType The Member ship type, if nothing was passed than it will return all. page: typing.Optional[builtins.int] The page number limit: typing.Optional[builtins.int] Limit the returned result. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the player's activities. Raises     aiobungie.error.ActivityNotFound The activity was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_post_activity",
"url":0,
"doc":"Fetch a post activity details.  warning This http request is not implemented yet and it will raise  NotImplementedError Parameters      instance:  builtins.int The activity instance id. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the post activity.",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_vendor_sales",
"url":0,
"doc":"",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_profile",
"url":0,
"doc":"Fetche a bungie profile. Parameters      memberid:  builtins.int The member's id. type:  aiobungie.MembershipType A valid membership type. Returns      ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the found profile. Raises     aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_entity",
"url":0,
"doc":"",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_inventory_item",
"url":0,
"doc":"Fetch a static inventory item entity given a its hash. Parameters      type:  builtins.str Entity's type definition. hash:  builtins.int Entity's hash. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON array object of the inventory item.",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_clan_members",
"url":0,
"doc":"Fetch all Bungie Clan members. Parameters      clan_id :  builsins.int The clans id type :  aiobungie.MembershipType An optional clan member's membership type. Default is set to  aiobungie.MembershipType.NONE Which returns the first matched clan member by their name. name :  builtins.str This parameter is only provided here to keep the signature with the main client implementation, Which only works with the non-rest clients. It returns a specific clan member by their name. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonArray] A JSON array of clan members. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_hard_linked",
"url":0,
"doc":"Gets any hard linked membership given a credential. Only works for credentials that are public just  aiobungie.CredentialType.STEAMID right now. Cross Save aware. Parameters      credential:  builtins.int A valid SteamID64 type:  aiobungie.CredentialType The crededntial type. This must not be changed Since its only credential that works \"currently\" Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the found user hard linked types.",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_manifest_path",
"url":0,
"doc":"Return a string of the bungie manifest database url. Returns    -  builtins.str A downloadable url for the bungie manifest database.",
"func":1
},
{
"ref":"aiobungie.RESTClient.fetch_manifest",
"url":0,
"doc":"Access The bungie Manifest. Returns    -  builtins.bytes The bytes to read and write the manifest database.",
"func":1
},
{
"ref":"aiobungie.PlayerNotFound",
"url":0,
"doc":"Raised when a  aiobungie.crate.Player is not found."
},
{
"ref":"aiobungie.ActivityNotFound",
"url":0,
"doc":"Raised when a  aiobungie.crate.Activity not found."
},
{
"ref":"aiobungie.ClanNotFound",
"url":0,
"doc":"Raised when a  aiobungie.crate.Clan not found."
},
{
"ref":"aiobungie.NotFound",
"url":0,
"doc":"Raised when an unknown request was not found."
},
{
"ref":"aiobungie.HTTPException",
"url":0,
"doc":"Exception for handling  aiobungie.rest.RESTClient requests errors. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.HTTPException.long_message",
"url":0,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.HTTPException.message",
"url":0,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.UserNotFound",
"url":0,
"doc":"Raised when a  aiobungie.crate.User not found."
},
{
"ref":"aiobungie.ResponseError",
"url":0,
"doc":"Typical Responses error."
},
{
"ref":"aiobungie.Unauthorized",
"url":0,
"doc":"Unauthorized access. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.Unauthorized.message",
"url":0,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.Unauthorized.long_message",
"url":0,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.Forbidden",
"url":0,
"doc":"Exception that's raised for when status code 403 occurs. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.Forbidden.message",
"url":0,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.Forbidden.long_message",
"url":0,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.MembershipTypeError",
"url":0,
"doc":"Raised when the memberhsip type is invalid. or The crate you're trying to fetch doesn't have The requested membership type. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.MembershipTypeError.message",
"url":0,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.MembershipTypeError.long_message",
"url":0,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.GameMode",
"url":0,
"doc":"An Enum for all available gamemodes in Destiny 2."
},
{
"ref":"aiobungie.GameMode.NONE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.STORY",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.STRIKE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.RAID",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.ALLPVP",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.PATROL",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.ALLPVE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.TOF",
"url":0,
"doc":"Trials Of Osiris"
},
{
"ref":"aiobungie.GameMode.CONTROL",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.NIGHTFALL",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.IRONBANER",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.ALLSTRIKES",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.DUNGEON",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.GAMBIT",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.EMIPIRE_HUNT",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.RUMBLE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.CLASSIC_MIX",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.COUNTDOWN",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.DOUBLES",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.CLASH",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.MAYHEM",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GameMode.SURVIVAL",
"url":0,
"doc":""
},
{
"ref":"aiobungie.MembershipType",
"url":0,
"doc":"An Enum for Bungie membership types."
},
{
"ref":"aiobungie.MembershipType.NONE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.MembershipType.XBOX",
"url":0,
"doc":""
},
{
"ref":"aiobungie.MembershipType.PSN",
"url":0,
"doc":""
},
{
"ref":"aiobungie.MembershipType.STEAM",
"url":0,
"doc":""
},
{
"ref":"aiobungie.MembershipType.BLIZZARD",
"url":0,
"doc":""
},
{
"ref":"aiobungie.MembershipType.STADIA",
"url":0,
"doc":""
},
{
"ref":"aiobungie.MembershipType.BUNGIE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.MembershipType.ALL",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Class",
"url":0,
"doc":"An Enum for Destiny character classes."
},
{
"ref":"aiobungie.Class.TITAN",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Class.HUNTER",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Class.WARLOCK",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Class.UNKNOWN",
"url":0,
"doc":""
},
{
"ref":"aiobungie.MilestoneType",
"url":0,
"doc":"An Enum for Destiny 2 milestone types."
},
{
"ref":"aiobungie.MilestoneType.UNKNOWN",
"url":0,
"doc":""
},
{
"ref":"aiobungie.MilestoneType.TUTORIAL",
"url":0,
"doc":""
},
{
"ref":"aiobungie.MilestoneType.ONETIME",
"url":0,
"doc":""
},
{
"ref":"aiobungie.MilestoneType.WEEKLY",
"url":0,
"doc":""
},
{
"ref":"aiobungie.MilestoneType.DAILY",
"url":0,
"doc":""
},
{
"ref":"aiobungie.MilestoneType.SPECIAL",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Race",
"url":0,
"doc":"An Enum for Destiny races."
},
{
"ref":"aiobungie.Race.HUMAN",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Race.AWOKEN",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Race.EXO",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Race.UNKNOWN",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Vendor",
"url":0,
"doc":"An Enum for all available vendors in Destiny 2."
},
{
"ref":"aiobungie.Vendor.ZAVALA",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Vendor.XUR",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Vendor.BANSHE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Vendor.SPIDER",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Vendor.SHAXX",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Vendor.KADI",
"url":0,
"doc":"Postmaster exo."
},
{
"ref":"aiobungie.Vendor.YUNA",
"url":0,
"doc":"Asia servers only."
},
{
"ref":"aiobungie.Vendor.EVERVERSE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Vendor.AMANDA",
"url":0,
"doc":"Amanda holiday"
},
{
"ref":"aiobungie.Vendor.CROW",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Vendor.HAWTHORNE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Vendor.ADA1",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Vendor.DRIFTER",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Vendor.IKORA",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Vendor.SAINT",
"url":0,
"doc":"Saint-14"
},
{
"ref":"aiobungie.Vendor.ERIS_MORN",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Vendor.SHAW_HAWN",
"url":0,
"doc":"COSMODROME Guy"
},
{
"ref":"aiobungie.Vendor.VARIKS",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Raid",
"url":0,
"doc":"An Enum for all available raids in Destiny 2."
},
{
"ref":"aiobungie.Raid.DSC",
"url":0,
"doc":"Deep Stone Crypt"
},
{
"ref":"aiobungie.Raid.LW",
"url":0,
"doc":"Last Wish"
},
{
"ref":"aiobungie.Raid.VOG",
"url":0,
"doc":"Normal Valut of Glass"
},
{
"ref":"aiobungie.Raid.GOS",
"url":0,
"doc":"Garden Of Salvation"
},
{
"ref":"aiobungie.Dungeon",
"url":0,
"doc":"An Enum for all available Dungeon/Like missions in Destiny 2."
},
{
"ref":"aiobungie.Dungeon.NORMAL_PRESAGE",
"url":0,
"doc":"Normal Presage"
},
{
"ref":"aiobungie.Dungeon.MASTER_PRESAGE",
"url":0,
"doc":"Master Presage"
},
{
"ref":"aiobungie.Dungeon.HARBINGER",
"url":0,
"doc":"Harbinger"
},
{
"ref":"aiobungie.Dungeon.PROPHECY",
"url":0,
"doc":"Prophecy"
},
{
"ref":"aiobungie.Dungeon.MASTER_POH",
"url":0,
"doc":"Master Pit of Heresy?"
},
{
"ref":"aiobungie.Dungeon.LEGEND_POH",
"url":0,
"doc":"Legend Pit of Heresy?"
},
{
"ref":"aiobungie.Dungeon.POH",
"url":0,
"doc":"Normal Pit of Heresy."
},
{
"ref":"aiobungie.Dungeon.SHATTERED",
"url":0,
"doc":"Shattered Throne"
},
{
"ref":"aiobungie.Gender",
"url":0,
"doc":"An Enum for Destiny Genders."
},
{
"ref":"aiobungie.Gender.MALE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Gender.FEMALE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Gender.UNKNOWN",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Component",
"url":0,
"doc":"An Enum for Destiny 2 Components."
},
{
"ref":"aiobungie.Component.NONE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Component.PROFILE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Component.SILVER",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Component.PROGRESSION",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Component.INVENTORIES",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Component.CHARACTERS",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Component.CHAR_INVENTORY",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Component.CHARECTER_PROGRESSION",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Component.EQUIPED_ITEMS",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Component.VENDORS",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Component.RECORDS",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Component.VENDOR_SALES",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Planet",
"url":0,
"doc":"An Enum for all available planets in Destiny 2."
},
{
"ref":"aiobungie.Planet.UNKNOWN",
"url":0,
"doc":"Unknown space"
},
{
"ref":"aiobungie.Planet.EARTH",
"url":0,
"doc":"Earth"
},
{
"ref":"aiobungie.Planet.DREAMING_CITY",
"url":0,
"doc":"The Dreaming city."
},
{
"ref":"aiobungie.Planet.NESSUS",
"url":0,
"doc":"Nessus"
},
{
"ref":"aiobungie.Planet.MOON",
"url":0,
"doc":"The Moon"
},
{
"ref":"aiobungie.Planet.COSMODROME",
"url":0,
"doc":"The Cosmodrome"
},
{
"ref":"aiobungie.Planet.TANGLED_SHORE",
"url":0,
"doc":"The Tangled Shore"
},
{
"ref":"aiobungie.Planet.VENUS",
"url":0,
"doc":"Venus"
},
{
"ref":"aiobungie.Planet.EAZ",
"url":0,
"doc":"European Aerial Zone"
},
{
"ref":"aiobungie.Planet.EUROPA",
"url":0,
"doc":"Europa"
},
{
"ref":"aiobungie.Stat",
"url":0,
"doc":"An Enum for Destiny 2 character stats."
},
{
"ref":"aiobungie.Stat.NONE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Stat.MOBILITY",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Stat.RESILIENCE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Stat.RECOVERY",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Stat.DISCIPLINE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Stat.INTELLECT",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Stat.STRENGTH",
"url":0,
"doc":""
},
{
"ref":"aiobungie.WeaponType",
"url":0,
"doc":"Enums for The three Destiny Weapon Types"
},
{
"ref":"aiobungie.WeaponType.NONE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.WeaponType.KINETIC",
"url":0,
"doc":""
},
{
"ref":"aiobungie.WeaponType.ENERGY",
"url":0,
"doc":""
},
{
"ref":"aiobungie.WeaponType.POWER",
"url":0,
"doc":""
},
{
"ref":"aiobungie.DamageType",
"url":0,
"doc":"Enums for Destiny Damage types"
},
{
"ref":"aiobungie.DamageType.NONE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.DamageType.KINETIC",
"url":0,
"doc":""
},
{
"ref":"aiobungie.DamageType.SOLAR",
"url":0,
"doc":""
},
{
"ref":"aiobungie.DamageType.VOID",
"url":0,
"doc":""
},
{
"ref":"aiobungie.DamageType.ARC",
"url":0,
"doc":""
},
{
"ref":"aiobungie.DamageType.STASIS",
"url":0,
"doc":""
},
{
"ref":"aiobungie.DamageType.RAID",
"url":0,
"doc":"This is a special damage type reserved for some raid activity encounters."
},
{
"ref":"aiobungie.Item",
"url":0,
"doc":"Enums for Destiny2's inventory bucket items"
},
{
"ref":"aiobungie.Item.NONE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.ARMOR",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.WEAPON",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.AUTO_RIFLE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.SHOTGUN",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.MACHINE_GUN",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.HANDCANNON",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.ROCKET_LAUNCHER",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.FUSION_RIFLE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.SNIPER_RIFLE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.PULSE_RIFLE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.SCOUT_RIFLE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.SIDEARM",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.SWORD",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.MASK",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.SHADER",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.ORNAMENT",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.FUSION_RIFLELINE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.GRENADE_LAUNCHER",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.SUBMACHINE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.TRACE_RIFLE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.HELMET_ARMOR",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.GAUNTLET_ARMOR",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.CHEST_ARMOR",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.LEG_ARMOR",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.CLASS_ARMOR",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.HELMET",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.GAUNTLET",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.CHEST",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.LEG",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.CLASS",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.BOW",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.EMBLEMS",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.LEGENDRY_SHARDS",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.GHOST",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.SUBCLASS",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.SEASONAL_ARTIFACT",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.EMOTES",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.SYNTHWAEV_TEMPLATE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.KINETIC",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.ENERGY",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Item.POWER",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Place",
"url":0,
"doc":"An Enum for Destiny 2 Places and NOT Planets"
},
{
"ref":"aiobungie.Place.ORBIT",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Place.SOCIAL",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Place.LIGHT_HOUSE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Place.EXPLORE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.CredentialType",
"url":0,
"doc":"The types of the accounts system supports at bungie."
},
{
"ref":"aiobungie.CredentialType.NONE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.CredentialType.XUID",
"url":0,
"doc":""
},
{
"ref":"aiobungie.CredentialType.PSNID",
"url":0,
"doc":""
},
{
"ref":"aiobungie.CredentialType.WILD",
"url":0,
"doc":""
},
{
"ref":"aiobungie.CredentialType.FAKE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.CredentialType.FACEBOOK",
"url":0,
"doc":""
},
{
"ref":"aiobungie.CredentialType.GOOGLE",
"url":0,
"doc":""
},
{
"ref":"aiobungie.CredentialType.WINDOWS",
"url":0,
"doc":""
},
{
"ref":"aiobungie.CredentialType.DEMONID",
"url":0,
"doc":""
},
{
"ref":"aiobungie.CredentialType.STEAMID",
"url":0,
"doc":""
},
{
"ref":"aiobungie.CredentialType.BATTLENETID",
"url":0,
"doc":""
},
{
"ref":"aiobungie.CredentialType.STADIAID",
"url":0,
"doc":""
},
{
"ref":"aiobungie.CredentialType.TWITCHID",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GroupType",
"url":0,
"doc":"An enums for the known bungie group types."
},
{
"ref":"aiobungie.GroupType.GENERAL",
"url":0,
"doc":""
},
{
"ref":"aiobungie.GroupType.CLAN",
"url":0,
"doc":""
},
{
"ref":"aiobungie.client",
"url":1,
"doc":"The base aiobungie Client that your should inherit from / use."
},
{
"ref":"aiobungie.client.Client",
"url":1,
"doc":"Basic implementation for a client that interacts with Bungie's API. Attributes      - token:  builtins.str Your Bungie's API key or Token from the developer's portal."
},
{
"ref":"aiobungie.client.Client.serialize",
"url":1,
"doc":"A property that returns a deserializer object for the client."
},
{
"ref":"aiobungie.client.Client.rest",
"url":1,
"doc":"The rest client we make the http request to the API with."
},
{
"ref":"aiobungie.client.Client.request",
"url":1,
"doc":"Returns a client network state for making external requests."
},
{
"ref":"aiobungie.client.Client.run",
"url":1,
"doc":"Runs a Coro function until its complete. This is equivalent to asyncio.get_event_loop().run_until_complete( .) Parameters      future:  typing.Coroutine[typing.Any, typing.Any, typing.Any] Your coro function. Example    -   async def main() -> None: player = await client.fetch_player(\"Fate\") print(player.name) client.run(main(  ",
"func":1
},
{
"ref":"aiobungie.client.Client.from_path",
"url":1,
"doc":"Raw http search given a valid bungie endpoint. Parameters      path:  builtins.str The bungie endpoint or path. A path must look something like this \"Destiny2/3/Profile/46111239123/ .\" kwargs:  typing.Any Any other key words you'd like to pass through. Returns    -  typing.Any Any object.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_manifest",
"url":1,
"doc":"Access The bungie Manifest. Returns    -  aiobungie.ext.Manifest A Manifest crate.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_user",
"url":1,
"doc":"Fetch a Bungie user by their id.  note This returns a Bungie user membership only. Take a look at  Client.fetch_membership_from_id for other memberships. Parameters      id:  builtins.int The user id. Returns    -  aiobungie.crate.user.BungieUser A Bungie user. Raises     aiobungie.error.UserNotFound The user was not found.",
"func":1
},
{
"ref":"aiobungie.client.Client.search_users",
"url":1,
"doc":"",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_user_themes",
"url":1,
"doc":"Fetch all available user themes. Returns    -  typing.Sequence[aiobungie.crate.user.UserThemes] A sequence of user themes.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_hard_types",
"url":1,
"doc":"Gets any hard linked membership given a credential. Only works for credentials that are public just  aiobungie.CredentialType.STEAMID right now. Cross Save aware. Parameters      credential:  builtins.int A valid SteamID64 type:  aiobungie.CredentialType The crededntial type. This must not be changed Since its only credential that works \"currently\" Returns    -  aiobungie.crate.user.HardLinkedMembership Information about the hard linked data.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_membership_from_id",
"url":1,
"doc":"Fetch Bungie user's memberships from their id. Notes   -  This returns both BungieNet membership and a sequence of the player's DestinyMemberships Which includes Stadia, Xbox, Steam and PSN memberships if the player has them, see  aiobungie.crate.user.DestinyUser for indetailed.  If you only want the bungie user. Consider using  Client.fetch_user method. Parameters      id :  builtins.int The user's id. type :  aiobungie.MembershipType The user's membership type. Returns    -  aiobungie.crate.User A Bungie user with their membership types. Raises    aiobungie.UserNotFound The requested user was not found.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_profile",
"url":1,
"doc":"Fetche a bungie profile. See  aiobungie.crate.Profile to access other components. Parameters      memberid:  builtins.int The member's id. type:  aiobungie.MembershipType A valid membership type. Returns      aiobungie.crate.Profile A Destiny 2 player profile. Raises     aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_player",
"url":1,
"doc":"Fetch a Destiny 2 Player. Parameters      - name:  builtins.str The Player's Name.  note You must also pass the player's unique code. A full name parameter should look like this  Fate\u6012 4275 type:  aiobungie.internal.enums.MembershipType The player's membership type, e,g. XBOX, STEAM, PSN Returns      typing.Sequence[aiobungie.crate.Player] A sequence of the found Destiny 2 Player memberships. Raises     aiobungie.PlayerNotFound The player was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_character",
"url":1,
"doc":"Fetch a Destiny 2 character. Parameters      memberid:  builtins.int A valid bungie member id. character:  aiobungie.internal.enums.Class The Destiny character to retrieve. type:  aiobungie.internal.enums.MembershipType The member's membership type. Returns    -  aiobungie.crate.Character A Bungie character crate. Raises     aiobungie.error.CharacterError raised if the Character was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_vendor_sales",
"url":1,
"doc":"",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_activity",
"url":1,
"doc":"Fetch a Destiny 2 activity for the specified user id and character. Parameters      member_id:  builtins.int The user id that starts with  4611 . character_id:  builtins.int The id of the character to retrieve. mode:  aiobungie.internal.enums.GameMode This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc. membership_type:  aiobungie.internal.enums.MembershipType The Member ship type, if nothing was passed than it will return all. page: typing.Optional[builtins.int] The page number limit: typing.Optional[builtins.int] Limit the returned result. Returns    -  aiobungie.crate.Activity A Bungie activity. Raises     aiobungie.error.ActivityNotFound The activity was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_post_activity",
"url":1,
"doc":"Fetch a post activity details.  warning This http request is not implemented yet and it will raise  NotImplementedError Parameters      instance:  builtins.int The activity instance id. Returns    -  aiobungie.crate.activity.PostActivity Information about the requested post activity.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_clan_from_id",
"url":1,
"doc":"Fetch a Bungie Clan by its id. Parameters      - id:  builtins.int The clan id. Returns      aiobungie.crate.Clan An Bungie clan. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_clan",
"url":1,
"doc":"Fetch a Clan by its name. This method will return the first clan found with given name name. Parameters      name:  builtins.str The clan name type  aiobungie.GroupType The group type, Default is one. Returns    -  aiobungie.crate.Clan A Bungie clan. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_clan_member",
"url":1,
"doc":"Fetch a Bungie Clan member.  note This method also can be also accessed via  aiobungie.crate.Clan.fetch_member() to fetch a member for the fetched clan. Parameters      clan_id :  builsins.int The clans id name :  builtins.str The clan member's name type :  aiobungie.MembershipType An optional clan member's membership type. Default is set to  aiobungie.MembershipType.NONE Which returns the first matched clan member by their name. Returns    -  aiobungie.crate.ClanMember A Bungie Clan member. Raises     aiobungie.ClanNotFound The clan was not found.  aiobungie.NotFound The member was not found.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_clan_members",
"url":1,
"doc":"Fetch a Bungie Clan member. if no members found in the clan you will get an empty sequence.  note This method also can be also accessed via  aiobungie.crate.Clan.fetch_members() to fetch a member for the fetched clan. Parameters      clan_id :  builsins.int The clans id type :  aiobungie.MembershipType An optional clan member's membership type. Default is set to  aiobungie.MembershipType.NONE Which returns the first matched clan member by their name. Returns    -  typing.Sequence[aiobungie.crate.ClanMember] A sequence of bungie clan members. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_inventory_item",
"url":1,
"doc":"Fetch a static inventory item entity given a its hash. Parameters      type:  builtins.str Entity's type definition. hash:  builtins.int Entity's hash. Returns    -  aiobungie.crate.InventoryEntity A bungie inventory item.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_app",
"url":1,
"doc":"Fetch a Bungie Application. Parameters      - appid:  builtins.int The application id. Returns      aiobungie.crate.Application A Bungie application.",
"func":1
},
{
"ref":"aiobungie.crate",
"url":2,
"doc":"Basic implementations of aiobungie client crates. These crates are used to organize the flow and how things stracture for functional usage for the Bungie API objects."
},
{
"ref":"aiobungie.crate.Application",
"url":2,
"doc":"Represents a Bungie developer application. Method generated by attrs for class Application."
},
{
"ref":"aiobungie.crate.Application.created_at",
"url":2,
"doc":"App creation date in UTC timezone"
},
{
"ref":"aiobungie.crate.Application.id",
"url":2,
"doc":"App id"
},
{
"ref":"aiobungie.crate.Application.link",
"url":2,
"doc":"App's link"
},
{
"ref":"aiobungie.crate.Application.name",
"url":2,
"doc":"App name"
},
{
"ref":"aiobungie.crate.Application.owner",
"url":2,
"doc":"App's owner"
},
{
"ref":"aiobungie.crate.Application.published_at",
"url":2,
"doc":"App's publish date in UTC timezone"
},
{
"ref":"aiobungie.crate.Application.redirect_url",
"url":2,
"doc":"App redirect url"
},
{
"ref":"aiobungie.crate.Application.scope",
"url":2,
"doc":"App's scope"
},
{
"ref":"aiobungie.crate.Application.status",
"url":2,
"doc":"App's status"
},
{
"ref":"aiobungie.crate.PostActivity",
"url":2,
"doc":"Represents a Destiny 2 post activity details. Method generated by attrs for class PostActivity."
},
{
"ref":"aiobungie.crate.PostActivity.get_players",
"url":2,
"doc":"Returns a sequence of the players that were in this activity. Returns    -  typing.Sequence[aiobungie.crate.Player] the players that were in this activity.",
"func":1
},
{
"ref":"aiobungie.crate.PostActivity.is_fresh",
"url":2,
"doc":"Determines if the activity was fresh or no."
},
{
"ref":"aiobungie.crate.PostActivity.membership_type",
"url":2,
"doc":"The post activity's membership type."
},
{
"ref":"aiobungie.crate.PostActivity.mode",
"url":2,
"doc":"The post activity's game mode, Can be  Undefined if unknown."
},
{
"ref":"aiobungie.crate.PostActivity.modes",
"url":2,
"doc":"A list of the post activity's game mode."
},
{
"ref":"aiobungie.crate.PostActivity.period",
"url":2,
"doc":"The post activity's period utc date."
},
{
"ref":"aiobungie.crate.PostActivity.players",
"url":2,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.crate.PostActivity.reference_id",
"url":2,
"doc":"The post activity reference id. AKA the activity hash."
},
{
"ref":"aiobungie.crate.PostActivity.starting_phase",
"url":2,
"doc":"The postt activity starting phase index. For an example if it was 0 that means it's a fresh run"
},
{
"ref":"aiobungie.crate.Clan",
"url":2,
"doc":"Represents a Bungie clan. Method generated by attrs for class Clan."
},
{
"ref":"aiobungie.crate.Clan.fetch_member",
"url":2,
"doc":"Fetch a specific clan member by their name and membership type. if the memberhship type is None we will try to return the first member matches the name. its also better to leave this parameter on None since usually only one player has this name. Parameters      name:  builtins.str The clan member name. type:  aiobungie.MembershipType The member's membership type. Default is 0 which returns any member matches the name. Returns      ClanMember Raises     aiobungie.ClanNotFound The clan was not found.  aiobungie.NotFound The member was not found",
"func":1
},
{
"ref":"aiobungie.crate.Clan.fetch_members",
"url":2,
"doc":"Fetch the members of the clan. if the memberhship type is None it will All membership types. Parameters      type:  aiobungie.MembershipType Filters the membership types to return. Default is  aiobungie.MembershipType.NONE which returns all membership types. Returns      typing.Sequence[ClanMember] A sequence of the clan members found in this clan. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.crate.Clan.fetch_banned_members",
"url":2,
"doc":"Fetch members who has been banned from the clan. Returns      typing.Sequence[aiobungie.crate.clans.ClanMember] A sequence of clan members or are banned.",
"func":1
},
{
"ref":"aiobungie.crate.Clan.fetch_pending_members",
"url":2,
"doc":"Fetch members who are waiting to get accepted. Returns      typing.Sequence[aiobungie.crate.clans.ClanMember] A sequence of clan members who are awaiting to get accepted to the clan.",
"func":1
},
{
"ref":"aiobungie.crate.Clan.fetch_invited_members",
"url":2,
"doc":"Fetch members who has been invited. Returns      typing.Sequence[aiobungie.crate.clans.ClanMember] A sequence of members who have been invited.",
"func":1
},
{
"ref":"aiobungie.crate.Clan.url",
"url":2,
"doc":""
},
{
"ref":"aiobungie.crate.Clan.about",
"url":2,
"doc":"Clan's about title."
},
{
"ref":"aiobungie.crate.Clan.avatar",
"url":2,
"doc":"Clan's avatar"
},
{
"ref":"aiobungie.crate.Clan.banner",
"url":2,
"doc":"Clan's banner"
},
{
"ref":"aiobungie.crate.Clan.created_at",
"url":2,
"doc":"Clan's creation date time in UTC."
},
{
"ref":"aiobungie.crate.Clan.features",
"url":2,
"doc":"The clan features."
},
{
"ref":"aiobungie.crate.Clan.id",
"url":2,
"doc":"The clan id"
},
{
"ref":"aiobungie.crate.Clan.is_public",
"url":2,
"doc":"Clan's privacy status."
},
{
"ref":"aiobungie.crate.Clan.member_count",
"url":2,
"doc":"Clan's member count."
},
{
"ref":"aiobungie.crate.Clan.motto",
"url":2,
"doc":"Clan's motto."
},
{
"ref":"aiobungie.crate.Clan.name",
"url":2,
"doc":"The clan's name"
},
{
"ref":"aiobungie.crate.Clan.net",
"url":2,
"doc":"A network state used for making external requests."
},
{
"ref":"aiobungie.crate.Clan.owner",
"url":2,
"doc":"The clan owner."
},
{
"ref":"aiobungie.crate.Clan.tags",
"url":2,
"doc":"A list of the clan's tags."
},
{
"ref":"aiobungie.crate.Clan.type",
"url":2,
"doc":"The clan type."
},
{
"ref":"aiobungie.crate.Player",
"url":2,
"doc":"Represents a Bungie Destiny 2 Player. Method generated by attrs for class Player."
},
{
"ref":"aiobungie.crate.Player.unique_name",
"url":2,
"doc":"The user's unique name.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.Player.id",
"url":2,
"doc":"The player's id."
},
{
"ref":"aiobungie.crate.Player.name",
"url":2,
"doc":"The player's name"
},
{
"ref":"aiobungie.crate.Player.type",
"url":2,
"doc":"The profile's membership type."
},
{
"ref":"aiobungie.crate.Player.types",
"url":2,
"doc":"A list of the player's membership types.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.Player.icon",
"url":2,
"doc":"The player's icon."
},
{
"ref":"aiobungie.crate.Player.code",
"url":2,
"doc":"The clan member's bungie display name code. This can be  None if not found.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.Player.is_public",
"url":2,
"doc":"The player's profile privacy."
},
{
"ref":"aiobungie.crate.Player.crossave_override",
"url":2,
"doc":"Returns  1 if the user has a cross save override in effect and 0 if not.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.Player.last_seen_name",
"url":3,
"doc":"The member's last seen display name. You may use this field if  DestinyUser.name is  Undefined ."
},
{
"ref":"aiobungie.crate.Player.link",
"url":3,
"doc":"The user like's profile link."
},
{
"ref":"aiobungie.crate.Character",
"url":2,
"doc":"An implementation for a Bungie character. Method generated by attrs for class Character."
},
{
"ref":"aiobungie.crate.Character.url",
"url":2,
"doc":"A url for the character at bungie.net."
},
{
"ref":"aiobungie.crate.Character.class_type",
"url":2,
"doc":"Character's class."
},
{
"ref":"aiobungie.crate.Character.emblem",
"url":2,
"doc":"Character's emblem"
},
{
"ref":"aiobungie.crate.Character.emblem_hash",
"url":2,
"doc":"Character's emblem hash."
},
{
"ref":"aiobungie.crate.Character.emblem_icon",
"url":2,
"doc":"Character's emblem icon"
},
{
"ref":"aiobungie.crate.Character.gender",
"url":2,
"doc":"Character's gender"
},
{
"ref":"aiobungie.crate.Character.id",
"url":2,
"doc":"Character's id"
},
{
"ref":"aiobungie.crate.Character.last_played",
"url":2,
"doc":"Character's last played date."
},
{
"ref":"aiobungie.crate.Character.level",
"url":2,
"doc":"Character's base level."
},
{
"ref":"aiobungie.crate.Character.light",
"url":2,
"doc":"Character's light"
},
{
"ref":"aiobungie.crate.Character.member_id",
"url":2,
"doc":"The character's member id."
},
{
"ref":"aiobungie.crate.Character.member_type",
"url":2,
"doc":"The character's memberhip type."
},
{
"ref":"aiobungie.crate.Character.race",
"url":2,
"doc":"Character's race"
},
{
"ref":"aiobungie.crate.Character.stats",
"url":2,
"doc":"Character stats."
},
{
"ref":"aiobungie.crate.Character.title_hash",
"url":2,
"doc":"Character's equipped title hash."
},
{
"ref":"aiobungie.crate.Character.total_played_time",
"url":2,
"doc":"Character's total plyed time minutes."
},
{
"ref":"aiobungie.crate.Character.equip",
"url":4,
"doc":"Equip an item to this character. This requires the OAuth2: MoveEquipDestinyItems scope. Also You must have a valid Destiny account, and either be in a social space, in orbit or offline. Parameters      item:  builtins.int The item id you want to equip for this character. Returns    -  builtins.None . Raises     NotImplementedError This endpoint is currently not implemented.",
"func":1
},
{
"ref":"aiobungie.crate.Character.equip_items",
"url":4,
"doc":"Equip multiple items to this character. This requires the OAuth2: MoveEquipDestinyItems scope. Also You must have a valid Destiny account, and either be in a social space, in orbit or offline. Parameters      items:  typing.List[builtins.int] A list of item ids you want to equip for this character. Returns    -  builtins.None . Raises     NotImplementedError This endpoint is currently not implemented.",
"func":1
},
{
"ref":"aiobungie.crate.Activity",
"url":2,
"doc":"Represents a Bungie Activity. Method generated by attrs for class Activity."
},
{
"ref":"aiobungie.crate.Activity.post_report",
"url":2,
"doc":"Get activity's data after its finished. Returns    -  .PostActivity ",
"func":1
},
{
"ref":"aiobungie.crate.Activity.assists",
"url":2,
"doc":"Activity's assists"
},
{
"ref":"aiobungie.crate.Activity.completion_reason",
"url":2,
"doc":"The reason why the activity was completed. usually its Unknown."
},
{
"ref":"aiobungie.crate.Activity.deaths",
"url":2,
"doc":"Activity's deaths."
},
{
"ref":"aiobungie.crate.Activity.duration",
"url":2,
"doc":"A string of The activity's duration, Example format  7m 42s "
},
{
"ref":"aiobungie.crate.Activity.efficiency",
"url":2,
"doc":"Activity's efficienty."
},
{
"ref":"aiobungie.crate.Activity.hash",
"url":2,
"doc":"The activity's hash."
},
{
"ref":"aiobungie.crate.Activity.instance_id",
"url":2,
"doc":"The activity's instance id."
},
{
"ref":"aiobungie.crate.Activity.is_completed",
"url":2,
"doc":"Check if the activity was completed or no."
},
{
"ref":"aiobungie.crate.Activity.kd",
"url":2,
"doc":"Activity's kill/death ratio."
},
{
"ref":"aiobungie.crate.Activity.kills",
"url":2,
"doc":"Activity's kills."
},
{
"ref":"aiobungie.crate.Activity.member_type",
"url":2,
"doc":"The activity player's membership type."
},
{
"ref":"aiobungie.crate.Activity.mode",
"url":2,
"doc":"The activity mode or type."
},
{
"ref":"aiobungie.crate.Activity.modes",
"url":2,
"doc":"A list of the post activity's game mode."
},
{
"ref":"aiobungie.crate.Activity.net",
"url":2,
"doc":"A network state used for making external requests."
},
{
"ref":"aiobungie.crate.Activity.opponents_defeated",
"url":2,
"doc":"Activity's opponents kills."
},
{
"ref":"aiobungie.crate.Activity.period",
"url":2,
"doc":"When did the activity occurred in UTC datetime."
},
{
"ref":"aiobungie.crate.Activity.player_count",
"url":2,
"doc":"Activity's player count."
},
{
"ref":"aiobungie.crate.Activity.score",
"url":2,
"doc":"Activity's score."
},
{
"ref":"aiobungie.crate.User",
"url":2,
"doc":"Concrete representtion of a Bungie user. This includes both Bungie net and Destiny memberships information. Method generated by attrs for class User."
},
{
"ref":"aiobungie.crate.User.bungie",
"url":2,
"doc":"The user's bungie net membership.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.User.destiny",
"url":2,
"doc":"A sequence of the user's Destiny memberships.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.ClanOwner",
"url":2,
"doc":"Represents a Bungie clan owner. Method generated by attrs for class ClanOwner."
},
{
"ref":"aiobungie.crate.ClanOwner.unique_name",
"url":2,
"doc":"The user's unique name which includes their unique code. This field could be None if no unique name found.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.ClanOwner.link",
"url":2,
"doc":"Returns the user's profile link."
},
{
"ref":"aiobungie.crate.ClanOwner.clan_id",
"url":2,
"doc":"Owner's current clan id."
},
{
"ref":"aiobungie.crate.ClanOwner.code",
"url":2,
"doc":"The user's unique display name code. This can be None if the user hasn't logged in after season of the lost update.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.ClanOwner.icon",
"url":2,
"doc":"Owner's profile icom"
},
{
"ref":"aiobungie.crate.ClanOwner.id",
"url":2,
"doc":"The user id."
},
{
"ref":"aiobungie.crate.ClanOwner.is_public",
"url":2,
"doc":"Returns if the user profile is public or no."
},
{
"ref":"aiobungie.crate.ClanOwner.joined_at",
"url":2,
"doc":"Owner's bungie join date."
},
{
"ref":"aiobungie.crate.ClanOwner.last_online",
"url":2,
"doc":"An aware  datetime.datetime object of the user's last online date UTC."
},
{
"ref":"aiobungie.crate.ClanOwner.last_seen_name",
"url":2,
"doc":"The clan member's last seen display name"
},
{
"ref":"aiobungie.crate.ClanOwner.name",
"url":2,
"doc":"The user name."
},
{
"ref":"aiobungie.crate.ClanOwner.type",
"url":2,
"doc":"Returns the membership type of the user."
},
{
"ref":"aiobungie.crate.ClanOwner.types",
"url":2,
"doc":"Returns a list of the member ship's membership types."
},
{
"ref":"aiobungie.crate.ClanMember",
"url":2,
"doc":"Represents a Destiny 2 clan member. Method generated by attrs for class ClanMember."
},
{
"ref":"aiobungie.crate.ClanMember.unique_name",
"url":2,
"doc":"The user's unique name which includes their unique code.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.ClanMember.link",
"url":2,
"doc":"Clan member's profile link."
},
{
"ref":"aiobungie.crate.ClanMember.ban",
"url":2,
"doc":"Bans a clan member from the clan. This requires OAuth2: AdminGroups scope.",
"func":1
},
{
"ref":"aiobungie.crate.ClanMember.unban",
"url":2,
"doc":"Unbans a clan member clan. This requires OAuth2: AdminGroups scope.",
"func":1
},
{
"ref":"aiobungie.crate.ClanMember.kick",
"url":2,
"doc":"Kicks a clan member from the clan. The requires OAuth2: AdminsGroup scope.",
"func":1
},
{
"ref":"aiobungie.crate.ClanMember.code",
"url":2,
"doc":"The clan member's bungie display name code This is new and was added in Season of the lost update  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.ClanMember.group_id",
"url":2,
"doc":"The member's group id."
},
{
"ref":"aiobungie.crate.ClanMember.icon",
"url":2,
"doc":"Clan member's icon"
},
{
"ref":"aiobungie.crate.ClanMember.id",
"url":2,
"doc":"Clan member's id"
},
{
"ref":"aiobungie.crate.ClanMember.is_online",
"url":2,
"doc":"True if the clan member is online or not."
},
{
"ref":"aiobungie.crate.ClanMember.is_public",
"url":2,
"doc":" builtins.True if the clan member is public."
},
{
"ref":"aiobungie.crate.ClanMember.joined_at",
"url":2,
"doc":"The clan member's join date in UTC time zone."
},
{
"ref":"aiobungie.crate.ClanMember.last_online",
"url":2,
"doc":"The date of the clan member's last online in UTC time zone."
},
{
"ref":"aiobungie.crate.ClanMember.last_seen_name",
"url":2,
"doc":"The clan member's last seen display name"
},
{
"ref":"aiobungie.crate.ClanMember.name",
"url":2,
"doc":"Clan member's name. This can be  UNDEFINED if not found."
},
{
"ref":"aiobungie.crate.ClanMember.net",
"url":2,
"doc":"A network state used for making external requests."
},
{
"ref":"aiobungie.crate.ClanMember.type",
"url":2,
"doc":"Clan member's membership type."
},
{
"ref":"aiobungie.crate.ClanMember.types",
"url":2,
"doc":"A sequence of the available clan member membership types."
},
{
"ref":"aiobungie.crate.ApplicationOwner",
"url":2,
"doc":"Represents a Bungie Application owner. Method generated by attrs for class ApplicationOwner."
},
{
"ref":"aiobungie.crate.ApplicationOwner.unique_name",
"url":2,
"doc":"The application owner's unique name."
},
{
"ref":"aiobungie.crate.ApplicationOwner.last_seen_name",
"url":2,
"doc":"The user like's last seen name."
},
{
"ref":"aiobungie.crate.ApplicationOwner.link",
"url":2,
"doc":"The user like's profile link."
},
{
"ref":"aiobungie.crate.ApplicationOwner.code",
"url":2,
"doc":"The user like's unique display name code. This can be None if the user hasn't logged in after season of the lost update.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.ApplicationOwner.icon",
"url":2,
"doc":"The application owner's icon."
},
{
"ref":"aiobungie.crate.ApplicationOwner.id",
"url":2,
"doc":"The application owner's id."
},
{
"ref":"aiobungie.crate.ApplicationOwner.is_public",
"url":2,
"doc":"The application owner's profile privacy."
},
{
"ref":"aiobungie.crate.ApplicationOwner.name",
"url":2,
"doc":"The application owner name. This can be  UNDEFINED if not found."
},
{
"ref":"aiobungie.crate.ApplicationOwner.type",
"url":2,
"doc":"The membership of the application owner."
},
{
"ref":"aiobungie.crate.Profile",
"url":2,
"doc":"Represents a Bungie member Profile. Bungie profiles requires components. But its kinda boring to pass multiple components to a parameter. So. The  .Profile crate will include all Bungie components. to be accessiable as a crate. How?. For an example: to access the  Characters component you'll need to pass  ?component=200 . But here you can just return the character itself from the profile using  await .Profile.titan() and the other character methods which returns a  aiobungie.crate.Character crate. crates are basically classes/objects. Example    -   client = aiobungie.Client( .) profile = await client.fetch_profile(\"Fate\")  access the character component and get my warlock. warlock = await profile.warlock() assert warlock.light  1320   Method generated by attrs for class Profile."
},
{
"ref":"aiobungie.crate.Profile.titan_id",
"url":2,
"doc":"The titan id of the profile player."
},
{
"ref":"aiobungie.crate.Profile.hunter_id",
"url":2,
"doc":"The huter id of the profile player."
},
{
"ref":"aiobungie.crate.Profile.warlock_id",
"url":2,
"doc":"The warlock id of the profile player."
},
{
"ref":"aiobungie.crate.Profile.character_ids",
"url":2,
"doc":"A list of the profile's character ids."
},
{
"ref":"aiobungie.crate.Profile.id",
"url":2,
"doc":"Profile's id"
},
{
"ref":"aiobungie.crate.Profile.is_public",
"url":2,
"doc":"Profile's privacy status."
},
{
"ref":"aiobungie.crate.Profile.last_played",
"url":2,
"doc":"Profile's last played Destiny 2 played date."
},
{
"ref":"aiobungie.crate.Profile.name",
"url":2,
"doc":"Profile's name."
},
{
"ref":"aiobungie.crate.Profile.net",
"url":2,
"doc":"A network state used for making external requests."
},
{
"ref":"aiobungie.crate.Profile.power_cap",
"url":2,
"doc":"The profile's current seaspn power cap."
},
{
"ref":"aiobungie.crate.Profile.type",
"url":2,
"doc":"Profile's type."
},
{
"ref":"aiobungie.crate.Profile.titan",
"url":5,
"doc":"Returns the titan character of the profile owner.",
"func":1
},
{
"ref":"aiobungie.crate.Profile.hunter",
"url":5,
"doc":"Returns the hunter character of the profile owner.",
"func":1
},
{
"ref":"aiobungie.crate.Profile.warlock",
"url":5,
"doc":"Returns the Warlock character of the profile owner.",
"func":1
},
{
"ref":"aiobungie.crate.InventoryEntity",
"url":2,
"doc":"Represents a bungie inventory item entity. This derives from  DestinyInventoryItemDefinition definition. Method generated by attrs for class InventoryEntity."
},
{
"ref":"aiobungie.crate.InventoryEntity.about",
"url":2,
"doc":"Entity's about."
},
{
"ref":"aiobungie.crate.InventoryEntity.ammo_type",
"url":2,
"doc":"Entity's ammo type if it was a wepon, otherwise it will return None"
},
{
"ref":"aiobungie.crate.InventoryEntity.banner",
"url":2,
"doc":"Entity's banner."
},
{
"ref":"aiobungie.crate.InventoryEntity.bucket_type",
"url":2,
"doc":"The entity's bucket type, None if unknown"
},
{
"ref":"aiobungie.crate.InventoryEntity.damage",
"url":2,
"doc":"Entity's damage type. Only works for weapons."
},
{
"ref":"aiobungie.crate.InventoryEntity.description",
"url":2,
"doc":"Entity's description."
},
{
"ref":"aiobungie.crate.InventoryEntity.has_icon",
"url":2,
"doc":"A boolean that returns True if the entity has an icon."
},
{
"ref":"aiobungie.crate.InventoryEntity.hash",
"url":2,
"doc":"Entity's hash."
},
{
"ref":"aiobungie.crate.InventoryEntity.icon",
"url":2,
"doc":"Entity's icon"
},
{
"ref":"aiobungie.crate.InventoryEntity.index",
"url":2,
"doc":"Entity's index."
},
{
"ref":"aiobungie.crate.InventoryEntity.is_equippable",
"url":2,
"doc":"True if the entity can be equipped or False."
},
{
"ref":"aiobungie.crate.InventoryEntity.item_class",
"url":2,
"doc":"The entity's class type."
},
{
"ref":"aiobungie.crate.InventoryEntity.lore_hash",
"url":2,
"doc":"The entity's lore hash. Can be undefined if no lore hash found."
},
{
"ref":"aiobungie.crate.InventoryEntity.name",
"url":2,
"doc":"Entity's name. This can be  UNDEFINED if not found."
},
{
"ref":"aiobungie.crate.InventoryEntity.net",
"url":2,
"doc":"A network state used for making external requests."
},
{
"ref":"aiobungie.crate.InventoryEntity.stats",
"url":2,
"doc":"Entity's stats. this currently returns a dict object of the stats."
},
{
"ref":"aiobungie.crate.InventoryEntity.sub_type",
"url":2,
"doc":"The subtype of the entity. A type is a weapon or armor. A subtype is a handcannonn or leg armor for an example."
},
{
"ref":"aiobungie.crate.InventoryEntity.summary_hash",
"url":2,
"doc":"Entity's summary hash."
},
{
"ref":"aiobungie.crate.InventoryEntity.tier",
"url":2,
"doc":"Entity's \"tier."
},
{
"ref":"aiobungie.crate.InventoryEntity.tier_name",
"url":2,
"doc":"A string version of the item tier."
},
{
"ref":"aiobungie.crate.InventoryEntity.type",
"url":2,
"doc":"Entity's type. Can be undefined if nothing was found."
},
{
"ref":"aiobungie.crate.InventoryEntity.type_name",
"url":2,
"doc":"Entity's type name. i.e.,  Grenade Launcher "
},
{
"ref":"aiobungie.crate.InventoryEntity.water_mark",
"url":2,
"doc":"Entity's water mark."
},
{
"ref":"aiobungie.crate.Entity",
"url":2,
"doc":"An interface of a Bungie Definition Entity. This is the main entity which all other entities should inherit from. it holds core information that all bungie entities has."
},
{
"ref":"aiobungie.crate.Entity.net",
"url":2,
"doc":"A network state used for making external requests."
},
{
"ref":"aiobungie.crate.Entity.name",
"url":2,
"doc":"Entity's name. This can be  UNDEFINED if not found."
},
{
"ref":"aiobungie.crate.Entity.icon",
"url":2,
"doc":"An optional entity's icon if its filled."
},
{
"ref":"aiobungie.crate.Entity.has_icon",
"url":2,
"doc":"A boolean that returns True if the entity has an icon."
},
{
"ref":"aiobungie.crate.Entity.description",
"url":2,
"doc":"Entity's description"
},
{
"ref":"aiobungie.crate.Entity.index",
"url":2,
"doc":"The entity's index."
},
{
"ref":"aiobungie.crate.Entity.hash",
"url":2,
"doc":"Entity's hash."
},
{
"ref":"aiobungie.crate.HardLinkedMembership",
"url":2,
"doc":"Represents hard linked Bungie user membership. This currently only supports SteamID which's a public credenitial. Also Cross-Save Aware. Method generated by attrs for class HardLinkedMembership."
},
{
"ref":"aiobungie.crate.HardLinkedMembership.cross_save_type",
"url":2,
"doc":"The hard link user's crpss save membership type. Default is set to None-0"
},
{
"ref":"aiobungie.crate.HardLinkedMembership.id",
"url":2,
"doc":"The hard link user id"
},
{
"ref":"aiobungie.crate.HardLinkedMembership.type",
"url":2,
"doc":"The hard link user membership type."
},
{
"ref":"aiobungie.crate.Friend",
"url":2,
"doc":"Represents a bungie friend in your account  versionadded 0.2.5 Method generated by attrs for class Friend."
},
{
"ref":"aiobungie.crate.Friend.unique_name",
"url":2,
"doc":"The friend's global unique display name. This field could be None if the player hasn't logged in yet."
},
{
"ref":"aiobungie.crate.Friend.accept",
"url":2,
"doc":"Accepts a friend request. Parameters      id :  builtins.int The friend's id you want to accept. Returns    -  builtins.NoneType None Raises     aiobungie.NotFound The friend was not found in your pending requests.",
"func":1
},
{
"ref":"aiobungie.crate.Friend.decline",
"url":2,
"doc":"Decline a friend request. Parameters      id :  builtins.int The friend's id you want to decline. Returns    -  builtins.NoneType None Raises     aiobungie.NotFound The friend was not found in your pending requests.",
"func":1
},
{
"ref":"aiobungie.crate.Friend.add",
"url":2,
"doc":"Adds a bungie member to your friend list. Parameters      id :  builtins.int The friend's id you want to add. Returns    -  builtins.NoneType None Raises     aiobungie.NotFound The player was not found.",
"func":1
},
{
"ref":"aiobungie.crate.Friend.remove",
"url":2,
"doc":"Removed an existing friend from your friend list. Parameters      id :  builtins.int The friend's id you want to remove. Returns    -  builtins.NoneType None Raises     aiobungie.NotFound The friend was not found in your friend list.",
"func":1
},
{
"ref":"aiobungie.crate.Friend.pending",
"url":2,
"doc":"Returns the pending friend requests. Parameters      id :  builtins.int The friend's id you want to remove. Returns    -  typing.Sequence[Friend] A sequence of pending friend requests.",
"func":1
},
{
"ref":"aiobungie.crate.Friend.remove_request",
"url":2,
"doc":"Removed an existing friend request.  note The friend request must be on your friend request list. Parameters      id :  builtins.int The friend's id you want to remove. Returns    -  builtins.NoneType None",
"func":1
},
{
"ref":"aiobungie.crate.Friend.fetch_platform_friends",
"url":2,
"doc":"Gets the platform friend of the requested type. Parameters      platform :  aiobungie.MembershipType The friend memebrship type. Raises     aiobungie.NotFound The requested friend was not found.",
"func":1
},
{
"ref":"aiobungie.crate.Friend.is_pending",
"url":2,
"doc":"",
"func":1
},
{
"ref":"aiobungie.crate.Friend.code",
"url":2,
"doc":"The friend's last seen global code. This field could be None if the player hasn't logged in yet."
},
{
"ref":"aiobungie.crate.Friend.id",
"url":2,
"doc":"The friend's last seen at id."
},
{
"ref":"aiobungie.crate.Friend.name",
"url":2,
"doc":"The friend's last seen global display name. This field could be Undefined if the player hasn't logged in yet."
},
{
"ref":"aiobungie.crate.Friend.net",
"url":2,
"doc":"A network state we use to make external requests."
},
{
"ref":"aiobungie.crate.Friend.online_status",
"url":2,
"doc":"The friend's online status."
},
{
"ref":"aiobungie.crate.Friend.online_title",
"url":2,
"doc":"The friend's online title."
},
{
"ref":"aiobungie.crate.Friend.relationship",
"url":2,
"doc":"The friend's relationship type."
},
{
"ref":"aiobungie.crate.Friend.type",
"url":2,
"doc":"The friend's last seen membership type."
},
{
"ref":"aiobungie.crate.Friend.user",
"url":2,
"doc":"The friend's bungie user account. This field is optional and can be None in some states."
},
{
"ref":"aiobungie.crate.Friend.last_seen_name",
"url":3,
"doc":"The user like's last seen name."
},
{
"ref":"aiobungie.crate.Friend.is_public",
"url":3,
"doc":"True if the user profile is public or no."
},
{
"ref":"aiobungie.crate.Friend.icon",
"url":3,
"doc":"The user like's icon."
},
{
"ref":"aiobungie.crate.Friend.link",
"url":3,
"doc":"The user like's profile link."
},
{
"ref":"aiobungie.crate.UserThemes",
"url":2,
"doc":"Represents a Bungie User theme. Method generated by attrs for class UserThemes."
},
{
"ref":"aiobungie.crate.UserThemes.description",
"url":2,
"doc":"An optional theme description. This field could be  None if no description found."
},
{
"ref":"aiobungie.crate.UserThemes.id",
"url":2,
"doc":"The theme id."
},
{
"ref":"aiobungie.crate.UserThemes.name",
"url":2,
"doc":"An optional theme name. if not found this field will be  None "
},
{
"ref":"aiobungie.crate.DestinyUser",
"url":2,
"doc":"Represents a Bungie user's Destiny memberships.  versionadded 0.2.5 Method generated by attrs for class DestinyUser."
},
{
"ref":"aiobungie.crate.DestinyUser.unique_name",
"url":2,
"doc":"The member's unique name. This field may be  Undefined if not found."
},
{
"ref":"aiobungie.crate.DestinyUser.code",
"url":2,
"doc":"The member's name code. This field may be  None if not found."
},
{
"ref":"aiobungie.crate.DestinyUser.crossave_override",
"url":2,
"doc":"The member's corssave override membership type."
},
{
"ref":"aiobungie.crate.DestinyUser.icon",
"url":2,
"doc":"The member's icon if it was present."
},
{
"ref":"aiobungie.crate.DestinyUser.id",
"url":2,
"doc":"The member's id."
},
{
"ref":"aiobungie.crate.DestinyUser.is_public",
"url":2,
"doc":"The member's profile privacy status."
},
{
"ref":"aiobungie.crate.DestinyUser.last_seen_name",
"url":2,
"doc":"The member's last seen display name. You may use this field if  DestinyUser.name is  Undefined ."
},
{
"ref":"aiobungie.crate.DestinyUser.name",
"url":2,
"doc":"The member's name."
},
{
"ref":"aiobungie.crate.DestinyUser.type",
"url":2,
"doc":"The member's membership type."
},
{
"ref":"aiobungie.crate.DestinyUser.types",
"url":2,
"doc":"A sequence of the member's membership types."
},
{
"ref":"aiobungie.crate.DestinyUser.link",
"url":3,
"doc":"The user like's profile link."
},
{
"ref":"aiobungie.crate.BungieUser",
"url":2,
"doc":"Represents a Bungie user. Method generated by attrs for class BungieUser."
},
{
"ref":"aiobungie.crate.BungieUser.about",
"url":2,
"doc":"The user's about, Default is None if nothing is Found."
},
{
"ref":"aiobungie.crate.BungieUser.blizzard_name",
"url":2,
"doc":"The user's blizzard name if it exists."
},
{
"ref":"aiobungie.crate.BungieUser.code",
"url":2,
"doc":"The user's unique display name code. This can be None if the user hasn't logged in after season of the lost update.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.BungieUser.created_at",
"url":2,
"doc":"The user's creation date in UTC timezone."
},
{
"ref":"aiobungie.crate.BungieUser.display_title",
"url":2,
"doc":"User's display title.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.BungieUser.id",
"url":2,
"doc":"The user's id"
},
{
"ref":"aiobungie.crate.BungieUser.is_deleted",
"url":2,
"doc":"True if the user is deleted"
},
{
"ref":"aiobungie.crate.BungieUser.locale",
"url":2,
"doc":"The user's locale."
},
{
"ref":"aiobungie.crate.BungieUser.name",
"url":2,
"doc":"The user's name."
},
{
"ref":"aiobungie.crate.BungieUser.picture",
"url":2,
"doc":"The user's profile picture."
},
{
"ref":"aiobungie.crate.BungieUser.psn_name",
"url":2,
"doc":"The user's psn id if it exists."
},
{
"ref":"aiobungie.crate.BungieUser.show_activity",
"url":2,
"doc":" True if the user is showing their activity status and  False if not.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.BungieUser.stadia_name",
"url":2,
"doc":"The user's stadia name if it exists  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.BungieUser.status",
"url":2,
"doc":"The user's bungie status text"
},
{
"ref":"aiobungie.crate.BungieUser.steam_name",
"url":2,
"doc":"The user's steam name if it exists"
},
{
"ref":"aiobungie.crate.BungieUser.theme_id",
"url":2,
"doc":"User profile's theme id.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.BungieUser.theme_name",
"url":2,
"doc":"User's profile theme name.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.BungieUser.twitch_name",
"url":2,
"doc":"The user's twitch name if it exists."
},
{
"ref":"aiobungie.crate.BungieUser.unique_name",
"url":2,
"doc":"The user's unique name which includes their unique code. This field could be None if no unique name found.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.BungieUser.updated_at",
"url":2,
"doc":"The user's last updated om UTC date."
},
{
"ref":"aiobungie.crate.ClanFeatures",
"url":2,
"doc":"Represents Bungie clan features. Method generated by attrs for class ClanFeatures."
},
{
"ref":"aiobungie.crate.ClanFeatures.capabilities",
"url":2,
"doc":"An int that represents the clan's capabilities."
},
{
"ref":"aiobungie.crate.ClanFeatures.invite_permissions",
"url":2,
"doc":"True if the clan has permissions to invite."
},
{
"ref":"aiobungie.crate.ClanFeatures.join_level",
"url":2,
"doc":"The clan's join level."
},
{
"ref":"aiobungie.crate.ClanFeatures.max_members",
"url":2,
"doc":"The maximum members the clan can have"
},
{
"ref":"aiobungie.crate.ClanFeatures.max_membership_types",
"url":2,
"doc":"The maximum membership types the clan can have"
},
{
"ref":"aiobungie.crate.ClanFeatures.membership_types",
"url":2,
"doc":"The clan's membership types."
},
{
"ref":"aiobungie.crate.ClanFeatures.update_banner_permissions",
"url":2,
"doc":"True if the clan has permissions to updates its banner."
},
{
"ref":"aiobungie.crate.ClanFeatures.update_culture_permissions",
"url":2,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.crate.activity",
"url":6,
"doc":"Basic implementation for a Bungie a activity. NOTE that this is still under development ages, and you might face some major bugs."
},
{
"ref":"aiobungie.crate.activity.Activity",
"url":6,
"doc":"Represents a Bungie Activity. Method generated by attrs for class Activity."
},
{
"ref":"aiobungie.crate.activity.Activity.post_report",
"url":6,
"doc":"Get activity's data after its finished. Returns    -  .PostActivity ",
"func":1
},
{
"ref":"aiobungie.crate.activity.Activity.assists",
"url":6,
"doc":"Activity's assists"
},
{
"ref":"aiobungie.crate.activity.Activity.completion_reason",
"url":6,
"doc":"The reason why the activity was completed. usually its Unknown."
},
{
"ref":"aiobungie.crate.activity.Activity.deaths",
"url":6,
"doc":"Activity's deaths."
},
{
"ref":"aiobungie.crate.activity.Activity.duration",
"url":6,
"doc":"A string of The activity's duration, Example format  7m 42s "
},
{
"ref":"aiobungie.crate.activity.Activity.efficiency",
"url":6,
"doc":"Activity's efficienty."
},
{
"ref":"aiobungie.crate.activity.Activity.hash",
"url":6,
"doc":"The activity's hash."
},
{
"ref":"aiobungie.crate.activity.Activity.instance_id",
"url":6,
"doc":"The activity's instance id."
},
{
"ref":"aiobungie.crate.activity.Activity.is_completed",
"url":6,
"doc":"Check if the activity was completed or no."
},
{
"ref":"aiobungie.crate.activity.Activity.kd",
"url":6,
"doc":"Activity's kill/death ratio."
},
{
"ref":"aiobungie.crate.activity.Activity.kills",
"url":6,
"doc":"Activity's kills."
},
{
"ref":"aiobungie.crate.activity.Activity.member_type",
"url":6,
"doc":"The activity player's membership type."
},
{
"ref":"aiobungie.crate.activity.Activity.mode",
"url":6,
"doc":"The activity mode or type."
},
{
"ref":"aiobungie.crate.activity.Activity.modes",
"url":6,
"doc":"A list of the post activity's game mode."
},
{
"ref":"aiobungie.crate.activity.Activity.net",
"url":6,
"doc":"A network state used for making external requests."
},
{
"ref":"aiobungie.crate.activity.Activity.opponents_defeated",
"url":6,
"doc":"Activity's opponents kills."
},
{
"ref":"aiobungie.crate.activity.Activity.period",
"url":6,
"doc":"When did the activity occurred in UTC datetime."
},
{
"ref":"aiobungie.crate.activity.Activity.player_count",
"url":6,
"doc":"Activity's player count."
},
{
"ref":"aiobungie.crate.activity.Activity.score",
"url":6,
"doc":"Activity's score."
},
{
"ref":"aiobungie.crate.activity.PostActivity",
"url":6,
"doc":"Represents a Destiny 2 post activity details. Method generated by attrs for class PostActivity."
},
{
"ref":"aiobungie.crate.activity.PostActivity.get_players",
"url":6,
"doc":"Returns a sequence of the players that were in this activity. Returns    -  typing.Sequence[aiobungie.crate.Player] the players that were in this activity.",
"func":1
},
{
"ref":"aiobungie.crate.activity.PostActivity.is_fresh",
"url":6,
"doc":"Determines if the activity was fresh or no."
},
{
"ref":"aiobungie.crate.activity.PostActivity.membership_type",
"url":6,
"doc":"The post activity's membership type."
},
{
"ref":"aiobungie.crate.activity.PostActivity.mode",
"url":6,
"doc":"The post activity's game mode, Can be  Undefined if unknown."
},
{
"ref":"aiobungie.crate.activity.PostActivity.modes",
"url":6,
"doc":"A list of the post activity's game mode."
},
{
"ref":"aiobungie.crate.activity.PostActivity.period",
"url":6,
"doc":"The post activity's period utc date."
},
{
"ref":"aiobungie.crate.activity.PostActivity.players",
"url":6,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.crate.activity.PostActivity.reference_id",
"url":6,
"doc":"The post activity reference id. AKA the activity hash."
},
{
"ref":"aiobungie.crate.activity.PostActivity.starting_phase",
"url":6,
"doc":"The postt activity starting phase index. For an example if it was 0 that means it's a fresh run"
},
{
"ref":"aiobungie.crate.application",
"url":7,
"doc":"Basic implementation for a Bungie a application."
},
{
"ref":"aiobungie.crate.application.Application",
"url":7,
"doc":"Represents a Bungie developer application. Method generated by attrs for class Application."
},
{
"ref":"aiobungie.crate.application.Application.created_at",
"url":7,
"doc":"App creation date in UTC timezone"
},
{
"ref":"aiobungie.crate.application.Application.id",
"url":7,
"doc":"App id"
},
{
"ref":"aiobungie.crate.application.Application.link",
"url":7,
"doc":"App's link"
},
{
"ref":"aiobungie.crate.application.Application.name",
"url":7,
"doc":"App name"
},
{
"ref":"aiobungie.crate.application.Application.owner",
"url":7,
"doc":"App's owner"
},
{
"ref":"aiobungie.crate.application.Application.published_at",
"url":7,
"doc":"App's publish date in UTC timezone"
},
{
"ref":"aiobungie.crate.application.Application.redirect_url",
"url":7,
"doc":"App redirect url"
},
{
"ref":"aiobungie.crate.application.Application.scope",
"url":7,
"doc":"App's scope"
},
{
"ref":"aiobungie.crate.application.Application.status",
"url":7,
"doc":"App's status"
},
{
"ref":"aiobungie.crate.application.ApplicationOwner",
"url":7,
"doc":"Represents a Bungie Application owner. Method generated by attrs for class ApplicationOwner."
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.unique_name",
"url":7,
"doc":"The application owner's unique name."
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.last_seen_name",
"url":7,
"doc":"The user like's last seen name."
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.link",
"url":7,
"doc":"The user like's profile link."
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.code",
"url":7,
"doc":"The user like's unique display name code. This can be None if the user hasn't logged in after season of the lost update.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.icon",
"url":7,
"doc":"The application owner's icon."
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.id",
"url":7,
"doc":"The application owner's id."
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.is_public",
"url":7,
"doc":"The application owner's profile privacy."
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.name",
"url":7,
"doc":"The application owner name. This can be  UNDEFINED if not found."
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.type",
"url":7,
"doc":"The membership of the application owner."
},
{
"ref":"aiobungie.crate.character",
"url":4,
"doc":"Basic Implementation of a Bungie Character."
},
{
"ref":"aiobungie.crate.character.CharacterComponent",
"url":4,
"doc":"An interface for a Bungie character component."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.member_type",
"url":4,
"doc":"The character's membership type."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.member_id",
"url":4,
"doc":"The profile's member id."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.id",
"url":4,
"doc":"The character's member id."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.light",
"url":4,
"doc":"The character's light."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.stats",
"url":4,
"doc":"The character's stats."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.url",
"url":4,
"doc":"The character's url at bungie.net."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.emblem",
"url":4,
"doc":"The character's current equipped emblem."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.last_played",
"url":4,
"doc":"The character's last played time."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.emblem_icon",
"url":4,
"doc":"The character's current equipped emblem icon."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.emblem_hash",
"url":4,
"doc":"The character's current equipped emblem hash."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.race",
"url":4,
"doc":"The character's race."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.gender",
"url":4,
"doc":"The character's gender."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.total_played_time",
"url":4,
"doc":"Character's total played time in hours."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.class_type",
"url":4,
"doc":"The character's class."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.title_hash",
"url":4,
"doc":"The character's title hash. This is Optional and can be None if no title was found."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.equip",
"url":4,
"doc":"Equip an item to this character. This requires the OAuth2: MoveEquipDestinyItems scope. Also You must have a valid Destiny account, and either be in a social space, in orbit or offline. Parameters      item:  builtins.int The item id you want to equip for this character. Returns    -  builtins.None . Raises     NotImplementedError This endpoint is currently not implemented.",
"func":1
},
{
"ref":"aiobungie.crate.character.CharacterComponent.equip_items",
"url":4,
"doc":"Equip multiple items to this character. This requires the OAuth2: MoveEquipDestinyItems scope. Also You must have a valid Destiny account, and either be in a social space, in orbit or offline. Parameters      items:  typing.List[builtins.int] A list of item ids you want to equip for this character. Returns    -  builtins.None . Raises     NotImplementedError This endpoint is currently not implemented.",
"func":1
},
{
"ref":"aiobungie.crate.character.Character",
"url":4,
"doc":"An implementation for a Bungie character. Method generated by attrs for class Character."
},
{
"ref":"aiobungie.crate.character.Character.url",
"url":4,
"doc":"A url for the character at bungie.net."
},
{
"ref":"aiobungie.crate.character.Character.class_type",
"url":4,
"doc":"Character's class."
},
{
"ref":"aiobungie.crate.character.Character.emblem",
"url":4,
"doc":"Character's emblem"
},
{
"ref":"aiobungie.crate.character.Character.emblem_hash",
"url":4,
"doc":"Character's emblem hash."
},
{
"ref":"aiobungie.crate.character.Character.emblem_icon",
"url":4,
"doc":"Character's emblem icon"
},
{
"ref":"aiobungie.crate.character.Character.gender",
"url":4,
"doc":"Character's gender"
},
{
"ref":"aiobungie.crate.character.Character.id",
"url":4,
"doc":"Character's id"
},
{
"ref":"aiobungie.crate.character.Character.last_played",
"url":4,
"doc":"Character's last played date."
},
{
"ref":"aiobungie.crate.character.Character.level",
"url":4,
"doc":"Character's base level."
},
{
"ref":"aiobungie.crate.character.Character.light",
"url":4,
"doc":"Character's light"
},
{
"ref":"aiobungie.crate.character.Character.member_id",
"url":4,
"doc":"The character's member id."
},
{
"ref":"aiobungie.crate.character.Character.member_type",
"url":4,
"doc":"The character's memberhip type."
},
{
"ref":"aiobungie.crate.character.Character.race",
"url":4,
"doc":"Character's race"
},
{
"ref":"aiobungie.crate.character.Character.stats",
"url":4,
"doc":"Character stats."
},
{
"ref":"aiobungie.crate.character.Character.title_hash",
"url":4,
"doc":"Character's equipped title hash."
},
{
"ref":"aiobungie.crate.character.Character.total_played_time",
"url":4,
"doc":"Character's total plyed time minutes."
},
{
"ref":"aiobungie.crate.character.Character.equip",
"url":4,
"doc":"Equip an item to this character. This requires the OAuth2: MoveEquipDestinyItems scope. Also You must have a valid Destiny account, and either be in a social space, in orbit or offline. Parameters      item:  builtins.int The item id you want to equip for this character. Returns    -  builtins.None . Raises     NotImplementedError This endpoint is currently not implemented.",
"func":1
},
{
"ref":"aiobungie.crate.character.Character.equip_items",
"url":4,
"doc":"Equip multiple items to this character. This requires the OAuth2: MoveEquipDestinyItems scope. Also You must have a valid Destiny account, and either be in a social space, in orbit or offline. Parameters      items:  typing.List[builtins.int] A list of item ids you want to equip for this character. Returns    -  builtins.None . Raises     NotImplementedError This endpoint is currently not implemented.",
"func":1
},
{
"ref":"aiobungie.crate.clans",
"url":8,
"doc":"Basic implementation for a Bungie a clan."
},
{
"ref":"aiobungie.crate.clans.Clan",
"url":8,
"doc":"Represents a Bungie clan. Method generated by attrs for class Clan."
},
{
"ref":"aiobungie.crate.clans.Clan.fetch_member",
"url":8,
"doc":"Fetch a specific clan member by their name and membership type. if the memberhship type is None we will try to return the first member matches the name. its also better to leave this parameter on None since usually only one player has this name. Parameters      name:  builtins.str The clan member name. type:  aiobungie.MembershipType The member's membership type. Default is 0 which returns any member matches the name. Returns      ClanMember Raises     aiobungie.ClanNotFound The clan was not found.  aiobungie.NotFound The member was not found",
"func":1
},
{
"ref":"aiobungie.crate.clans.Clan.fetch_members",
"url":8,
"doc":"Fetch the members of the clan. if the memberhship type is None it will All membership types. Parameters      type:  aiobungie.MembershipType Filters the membership types to return. Default is  aiobungie.MembershipType.NONE which returns all membership types. Returns      typing.Sequence[ClanMember] A sequence of the clan members found in this clan. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.crate.clans.Clan.fetch_banned_members",
"url":8,
"doc":"Fetch members who has been banned from the clan. Returns      typing.Sequence[aiobungie.crate.clans.ClanMember] A sequence of clan members or are banned.",
"func":1
},
{
"ref":"aiobungie.crate.clans.Clan.fetch_pending_members",
"url":8,
"doc":"Fetch members who are waiting to get accepted. Returns      typing.Sequence[aiobungie.crate.clans.ClanMember] A sequence of clan members who are awaiting to get accepted to the clan.",
"func":1
},
{
"ref":"aiobungie.crate.clans.Clan.fetch_invited_members",
"url":8,
"doc":"Fetch members who has been invited. Returns      typing.Sequence[aiobungie.crate.clans.ClanMember] A sequence of members who have been invited.",
"func":1
},
{
"ref":"aiobungie.crate.clans.Clan.url",
"url":8,
"doc":""
},
{
"ref":"aiobungie.crate.clans.Clan.about",
"url":8,
"doc":"Clan's about title."
},
{
"ref":"aiobungie.crate.clans.Clan.avatar",
"url":8,
"doc":"Clan's avatar"
},
{
"ref":"aiobungie.crate.clans.Clan.banner",
"url":8,
"doc":"Clan's banner"
},
{
"ref":"aiobungie.crate.clans.Clan.created_at",
"url":8,
"doc":"Clan's creation date time in UTC."
},
{
"ref":"aiobungie.crate.clans.Clan.features",
"url":8,
"doc":"The clan features."
},
{
"ref":"aiobungie.crate.clans.Clan.id",
"url":8,
"doc":"The clan id"
},
{
"ref":"aiobungie.crate.clans.Clan.is_public",
"url":8,
"doc":"Clan's privacy status."
},
{
"ref":"aiobungie.crate.clans.Clan.member_count",
"url":8,
"doc":"Clan's member count."
},
{
"ref":"aiobungie.crate.clans.Clan.motto",
"url":8,
"doc":"Clan's motto."
},
{
"ref":"aiobungie.crate.clans.Clan.name",
"url":8,
"doc":"The clan's name"
},
{
"ref":"aiobungie.crate.clans.Clan.net",
"url":8,
"doc":"A network state used for making external requests."
},
{
"ref":"aiobungie.crate.clans.Clan.owner",
"url":8,
"doc":"The clan owner."
},
{
"ref":"aiobungie.crate.clans.Clan.tags",
"url":8,
"doc":"A list of the clan's tags."
},
{
"ref":"aiobungie.crate.clans.Clan.type",
"url":8,
"doc":"The clan type."
},
{
"ref":"aiobungie.crate.clans.ClanOwner",
"url":8,
"doc":"Represents a Bungie clan owner. Method generated by attrs for class ClanOwner."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.unique_name",
"url":8,
"doc":"The user's unique name which includes their unique code. This field could be None if no unique name found.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.clans.ClanOwner.link",
"url":8,
"doc":"Returns the user's profile link."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.clan_id",
"url":8,
"doc":"Owner's current clan id."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.code",
"url":8,
"doc":"The user's unique display name code. This can be None if the user hasn't logged in after season of the lost update.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.clans.ClanOwner.icon",
"url":8,
"doc":"Owner's profile icom"
},
{
"ref":"aiobungie.crate.clans.ClanOwner.id",
"url":8,
"doc":"The user id."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.is_public",
"url":8,
"doc":"Returns if the user profile is public or no."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.joined_at",
"url":8,
"doc":"Owner's bungie join date."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.last_online",
"url":8,
"doc":"An aware  datetime.datetime object of the user's last online date UTC."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.last_seen_name",
"url":8,
"doc":"The clan member's last seen display name"
},
{
"ref":"aiobungie.crate.clans.ClanOwner.name",
"url":8,
"doc":"The user name."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.type",
"url":8,
"doc":"Returns the membership type of the user."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.types",
"url":8,
"doc":"Returns a list of the member ship's membership types."
},
{
"ref":"aiobungie.crate.clans.ClanMember",
"url":8,
"doc":"Represents a Destiny 2 clan member. Method generated by attrs for class ClanMember."
},
{
"ref":"aiobungie.crate.clans.ClanMember.unique_name",
"url":8,
"doc":"The user's unique name which includes their unique code.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.clans.ClanMember.link",
"url":8,
"doc":"Clan member's profile link."
},
{
"ref":"aiobungie.crate.clans.ClanMember.ban",
"url":8,
"doc":"Bans a clan member from the clan. This requires OAuth2: AdminGroups scope.",
"func":1
},
{
"ref":"aiobungie.crate.clans.ClanMember.unban",
"url":8,
"doc":"Unbans a clan member clan. This requires OAuth2: AdminGroups scope.",
"func":1
},
{
"ref":"aiobungie.crate.clans.ClanMember.kick",
"url":8,
"doc":"Kicks a clan member from the clan. The requires OAuth2: AdminsGroup scope.",
"func":1
},
{
"ref":"aiobungie.crate.clans.ClanMember.code",
"url":8,
"doc":"The clan member's bungie display name code This is new and was added in Season of the lost update  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.clans.ClanMember.group_id",
"url":8,
"doc":"The member's group id."
},
{
"ref":"aiobungie.crate.clans.ClanMember.icon",
"url":8,
"doc":"Clan member's icon"
},
{
"ref":"aiobungie.crate.clans.ClanMember.id",
"url":8,
"doc":"Clan member's id"
},
{
"ref":"aiobungie.crate.clans.ClanMember.is_online",
"url":8,
"doc":"True if the clan member is online or not."
},
{
"ref":"aiobungie.crate.clans.ClanMember.is_public",
"url":8,
"doc":" builtins.True if the clan member is public."
},
{
"ref":"aiobungie.crate.clans.ClanMember.joined_at",
"url":8,
"doc":"The clan member's join date in UTC time zone."
},
{
"ref":"aiobungie.crate.clans.ClanMember.last_online",
"url":8,
"doc":"The date of the clan member's last online in UTC time zone."
},
{
"ref":"aiobungie.crate.clans.ClanMember.last_seen_name",
"url":8,
"doc":"The clan member's last seen display name"
},
{
"ref":"aiobungie.crate.clans.ClanMember.name",
"url":8,
"doc":"Clan member's name. This can be  UNDEFINED if not found."
},
{
"ref":"aiobungie.crate.clans.ClanMember.net",
"url":8,
"doc":"A network state used for making external requests."
},
{
"ref":"aiobungie.crate.clans.ClanMember.type",
"url":8,
"doc":"Clan member's membership type."
},
{
"ref":"aiobungie.crate.clans.ClanMember.types",
"url":8,
"doc":"A sequence of the available clan member membership types."
},
{
"ref":"aiobungie.crate.clans.ClanFeatures",
"url":8,
"doc":"Represents Bungie clan features. Method generated by attrs for class ClanFeatures."
},
{
"ref":"aiobungie.crate.clans.ClanFeatures.capabilities",
"url":8,
"doc":"An int that represents the clan's capabilities."
},
{
"ref":"aiobungie.crate.clans.ClanFeatures.invite_permissions",
"url":8,
"doc":"True if the clan has permissions to invite."
},
{
"ref":"aiobungie.crate.clans.ClanFeatures.join_level",
"url":8,
"doc":"The clan's join level."
},
{
"ref":"aiobungie.crate.clans.ClanFeatures.max_members",
"url":8,
"doc":"The maximum members the clan can have"
},
{
"ref":"aiobungie.crate.clans.ClanFeatures.max_membership_types",
"url":8,
"doc":"The maximum membership types the clan can have"
},
{
"ref":"aiobungie.crate.clans.ClanFeatures.membership_types",
"url":8,
"doc":"The clan's membership types."
},
{
"ref":"aiobungie.crate.clans.ClanFeatures.update_banner_permissions",
"url":8,
"doc":"True if the clan has permissions to updates its banner."
},
{
"ref":"aiobungie.crate.clans.ClanFeatures.update_culture_permissions",
"url":8,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.crate.entity",
"url":9,
"doc":"Bungie entity definitions implementation. This is still not fully implemented and you may experince bugs. This will include all Bungie Definitions."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity",
"url":9,
"doc":"Represents a bungie inventory item entity. This derives from  DestinyInventoryItemDefinition definition. Method generated by attrs for class InventoryEntity."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.about",
"url":9,
"doc":"Entity's about."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.ammo_type",
"url":9,
"doc":"Entity's ammo type if it was a wepon, otherwise it will return None"
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.banner",
"url":9,
"doc":"Entity's banner."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.bucket_type",
"url":9,
"doc":"The entity's bucket type, None if unknown"
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.damage",
"url":9,
"doc":"Entity's damage type. Only works for weapons."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.description",
"url":9,
"doc":"Entity's description."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.has_icon",
"url":9,
"doc":"A boolean that returns True if the entity has an icon."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.hash",
"url":9,
"doc":"Entity's hash."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.icon",
"url":9,
"doc":"Entity's icon"
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.index",
"url":9,
"doc":"Entity's index."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.is_equippable",
"url":9,
"doc":"True if the entity can be equipped or False."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.item_class",
"url":9,
"doc":"The entity's class type."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.lore_hash",
"url":9,
"doc":"The entity's lore hash. Can be undefined if no lore hash found."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.name",
"url":9,
"doc":"Entity's name. This can be  UNDEFINED if not found."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.net",
"url":9,
"doc":"A network state used for making external requests."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.stats",
"url":9,
"doc":"Entity's stats. this currently returns a dict object of the stats."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.sub_type",
"url":9,
"doc":"The subtype of the entity. A type is a weapon or armor. A subtype is a handcannonn or leg armor for an example."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.summary_hash",
"url":9,
"doc":"Entity's summary hash."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.tier",
"url":9,
"doc":"Entity's \"tier."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.tier_name",
"url":9,
"doc":"A string version of the item tier."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.type",
"url":9,
"doc":"Entity's type. Can be undefined if nothing was found."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.type_name",
"url":9,
"doc":"Entity's type name. i.e.,  Grenade Launcher "
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.water_mark",
"url":9,
"doc":"Entity's water mark."
},
{
"ref":"aiobungie.crate.entity.Entity",
"url":9,
"doc":"An interface of a Bungie Definition Entity. This is the main entity which all other entities should inherit from. it holds core information that all bungie entities has."
},
{
"ref":"aiobungie.crate.entity.Entity.net",
"url":9,
"doc":"A network state used for making external requests."
},
{
"ref":"aiobungie.crate.entity.Entity.name",
"url":9,
"doc":"Entity's name. This can be  UNDEFINED if not found."
},
{
"ref":"aiobungie.crate.entity.Entity.icon",
"url":9,
"doc":"An optional entity's icon if its filled."
},
{
"ref":"aiobungie.crate.entity.Entity.has_icon",
"url":9,
"doc":"A boolean that returns True if the entity has an icon."
},
{
"ref":"aiobungie.crate.entity.Entity.description",
"url":9,
"doc":"Entity's description"
},
{
"ref":"aiobungie.crate.entity.Entity.index",
"url":9,
"doc":"The entity's index."
},
{
"ref":"aiobungie.crate.entity.Entity.hash",
"url":9,
"doc":"Entity's hash."
},
{
"ref":"aiobungie.crate.friends",
"url":10,
"doc":"Bungie social and friends crate."
},
{
"ref":"aiobungie.crate.friends.Friend",
"url":10,
"doc":"Represents a bungie friend in your account  versionadded 0.2.5 Method generated by attrs for class Friend."
},
{
"ref":"aiobungie.crate.friends.Friend.unique_name",
"url":10,
"doc":"The friend's global unique display name. This field could be None if the player hasn't logged in yet."
},
{
"ref":"aiobungie.crate.friends.Friend.accept",
"url":10,
"doc":"Accepts a friend request. Parameters      id :  builtins.int The friend's id you want to accept. Returns    -  builtins.NoneType None Raises     aiobungie.NotFound The friend was not found in your pending requests.",
"func":1
},
{
"ref":"aiobungie.crate.friends.Friend.decline",
"url":10,
"doc":"Decline a friend request. Parameters      id :  builtins.int The friend's id you want to decline. Returns    -  builtins.NoneType None Raises     aiobungie.NotFound The friend was not found in your pending requests.",
"func":1
},
{
"ref":"aiobungie.crate.friends.Friend.add",
"url":10,
"doc":"Adds a bungie member to your friend list. Parameters      id :  builtins.int The friend's id you want to add. Returns    -  builtins.NoneType None Raises     aiobungie.NotFound The player was not found.",
"func":1
},
{
"ref":"aiobungie.crate.friends.Friend.remove",
"url":10,
"doc":"Removed an existing friend from your friend list. Parameters      id :  builtins.int The friend's id you want to remove. Returns    -  builtins.NoneType None Raises     aiobungie.NotFound The friend was not found in your friend list.",
"func":1
},
{
"ref":"aiobungie.crate.friends.Friend.pending",
"url":10,
"doc":"Returns the pending friend requests. Parameters      id :  builtins.int The friend's id you want to remove. Returns    -  typing.Sequence[Friend] A sequence of pending friend requests.",
"func":1
},
{
"ref":"aiobungie.crate.friends.Friend.remove_request",
"url":10,
"doc":"Removed an existing friend request.  note The friend request must be on your friend request list. Parameters      id :  builtins.int The friend's id you want to remove. Returns    -  builtins.NoneType None",
"func":1
},
{
"ref":"aiobungie.crate.friends.Friend.fetch_platform_friends",
"url":10,
"doc":"Gets the platform friend of the requested type. Parameters      platform :  aiobungie.MembershipType The friend memebrship type. Raises     aiobungie.NotFound The requested friend was not found.",
"func":1
},
{
"ref":"aiobungie.crate.friends.Friend.is_pending",
"url":10,
"doc":"",
"func":1
},
{
"ref":"aiobungie.crate.friends.Friend.code",
"url":10,
"doc":"The friend's last seen global code. This field could be None if the player hasn't logged in yet."
},
{
"ref":"aiobungie.crate.friends.Friend.id",
"url":10,
"doc":"The friend's last seen at id."
},
{
"ref":"aiobungie.crate.friends.Friend.name",
"url":10,
"doc":"The friend's last seen global display name. This field could be Undefined if the player hasn't logged in yet."
},
{
"ref":"aiobungie.crate.friends.Friend.net",
"url":10,
"doc":"A network state we use to make external requests."
},
{
"ref":"aiobungie.crate.friends.Friend.online_status",
"url":10,
"doc":"The friend's online status."
},
{
"ref":"aiobungie.crate.friends.Friend.online_title",
"url":10,
"doc":"The friend's online title."
},
{
"ref":"aiobungie.crate.friends.Friend.relationship",
"url":10,
"doc":"The friend's relationship type."
},
{
"ref":"aiobungie.crate.friends.Friend.type",
"url":10,
"doc":"The friend's last seen membership type."
},
{
"ref":"aiobungie.crate.friends.Friend.user",
"url":10,
"doc":"The friend's bungie user account. This field is optional and can be None in some states."
},
{
"ref":"aiobungie.crate.friends.Friend.last_seen_name",
"url":3,
"doc":"The user like's last seen name."
},
{
"ref":"aiobungie.crate.friends.Friend.is_public",
"url":3,
"doc":"True if the user profile is public or no."
},
{
"ref":"aiobungie.crate.friends.Friend.icon",
"url":3,
"doc":"The user like's icon."
},
{
"ref":"aiobungie.crate.friends.Friend.link",
"url":3,
"doc":"The user like's profile link."
},
{
"ref":"aiobungie.crate.members",
"url":11,
"doc":"A collection and entities of Bungie's Destiny players memberships."
},
{
"ref":"aiobungie.crate.members.StadiaMember",
"url":11,
"doc":"Represent a Stadia membership for a bungie user.  versionadded 0.2.5 Method generated by attrs for class StadiaMember."
},
{
"ref":"aiobungie.crate.members.StadiaMember.unique_name",
"url":11,
"doc":"Member's unique name."
},
{
"ref":"aiobungie.crate.members.StadiaMember.code",
"url":11,
"doc":"The member's name code. This field may be  None if not found."
},
{
"ref":"aiobungie.crate.members.StadiaMember.icon",
"url":11,
"doc":"The profile's icon if it was present."
},
{
"ref":"aiobungie.crate.members.StadiaMember.id",
"url":11,
"doc":"The member's id."
},
{
"ref":"aiobungie.crate.members.StadiaMember.is_public",
"url":11,
"doc":"The member's profile privacy status."
},
{
"ref":"aiobungie.crate.members.StadiaMember.last_seen_name",
"url":11,
"doc":"The member's last seen display name. You may use this field if  StadiaMember.name is  Undefined ."
},
{
"ref":"aiobungie.crate.members.StadiaMember.name",
"url":11,
"doc":"The member's name. This can be  UNDEFINED if not found."
},
{
"ref":"aiobungie.crate.members.StadiaMember.type",
"url":11,
"doc":"The member's membership type."
},
{
"ref":"aiobungie.crate.members.StadiaMember.types",
"url":11,
"doc":"A sequence of the member's membership types."
},
{
"ref":"aiobungie.crate.members.StadiaMember.link",
"url":3,
"doc":"The user like's profile link."
},
{
"ref":"aiobungie.crate.members.XboxMember",
"url":11,
"doc":"Represent an Xbox membership for a bungie user.  versionadded 0.2.5 Method generated by attrs for class XboxMember."
},
{
"ref":"aiobungie.crate.members.XboxMember.unique_name",
"url":11,
"doc":"Member's unique name."
},
{
"ref":"aiobungie.crate.members.XboxMember.code",
"url":11,
"doc":"The member's name code. This field may be  None if not found."
},
{
"ref":"aiobungie.crate.members.XboxMember.icon",
"url":11,
"doc":"The profile's icon if it was present."
},
{
"ref":"aiobungie.crate.members.XboxMember.id",
"url":11,
"doc":"The member's id."
},
{
"ref":"aiobungie.crate.members.XboxMember.is_public",
"url":11,
"doc":"The member's profile privacy status."
},
{
"ref":"aiobungie.crate.members.XboxMember.last_seen_name",
"url":11,
"doc":"The member's last seen display name. You may use this field if  XboxMember.name is  Undefined ."
},
{
"ref":"aiobungie.crate.members.XboxMember.name",
"url":11,
"doc":"The member's name. This can be  UNDEFINED if not found."
},
{
"ref":"aiobungie.crate.members.XboxMember.type",
"url":11,
"doc":"The member's membership type."
},
{
"ref":"aiobungie.crate.members.XboxMember.types",
"url":11,
"doc":"A sequence of the member's membership types."
},
{
"ref":"aiobungie.crate.members.XboxMember.link",
"url":3,
"doc":"The user like's profile link."
},
{
"ref":"aiobungie.crate.members.PSNMember",
"url":11,
"doc":"Represent a PSN membership for a bungie user.  versionadded 0.2.5 Method generated by attrs for class PSNMember."
},
{
"ref":"aiobungie.crate.members.PSNMember.unique_name",
"url":11,
"doc":"Member's unique name."
},
{
"ref":"aiobungie.crate.members.PSNMember.code",
"url":11,
"doc":"The member's name code. This field may be  None if not found."
},
{
"ref":"aiobungie.crate.members.PSNMember.icon",
"url":11,
"doc":"The profile's icon if it was present."
},
{
"ref":"aiobungie.crate.members.PSNMember.id",
"url":11,
"doc":"The member's id."
},
{
"ref":"aiobungie.crate.members.PSNMember.is_public",
"url":11,
"doc":"The member's profile privacy status."
},
{
"ref":"aiobungie.crate.members.PSNMember.last_seen_name",
"url":11,
"doc":"The member's last seen display name. You may use this field if  PSNMember.name is  Undefined ."
},
{
"ref":"aiobungie.crate.members.PSNMember.name",
"url":11,
"doc":"The member's name. This can be  UNDEFINED if not found."
},
{
"ref":"aiobungie.crate.members.PSNMember.type",
"url":11,
"doc":"The member's membership type."
},
{
"ref":"aiobungie.crate.members.PSNMember.types",
"url":11,
"doc":"A sequence of the member's membership types."
},
{
"ref":"aiobungie.crate.members.PSNMember.link",
"url":3,
"doc":"The user like's profile link."
},
{
"ref":"aiobungie.crate.members.SteamMember",
"url":11,
"doc":"Represent a Steam membership for a bungie user.  versionadded 0.2.5 Method generated by attrs for class SteamMember."
},
{
"ref":"aiobungie.crate.members.SteamMember.unique_name",
"url":11,
"doc":"Member's unique name."
},
{
"ref":"aiobungie.crate.members.SteamMember.code",
"url":11,
"doc":"The member's name code. This field may be  None if not found."
},
{
"ref":"aiobungie.crate.members.SteamMember.icon",
"url":11,
"doc":"The profile's icon if it was present."
},
{
"ref":"aiobungie.crate.members.SteamMember.id",
"url":11,
"doc":"The member's id."
},
{
"ref":"aiobungie.crate.members.SteamMember.is_public",
"url":11,
"doc":"The member's profile privacy status."
},
{
"ref":"aiobungie.crate.members.SteamMember.last_seen_name",
"url":11,
"doc":"The member's last seen display name. You may use this field if  SteamMember.name is  Undefined ."
},
{
"ref":"aiobungie.crate.members.SteamMember.name",
"url":11,
"doc":"The member's name. This can be  UNDEFINED if not found."
},
{
"ref":"aiobungie.crate.members.SteamMember.type",
"url":11,
"doc":"The member's membership type."
},
{
"ref":"aiobungie.crate.members.SteamMember.types",
"url":11,
"doc":"A sequence of the member's membership types."
},
{
"ref":"aiobungie.crate.members.SteamMember.link",
"url":3,
"doc":"The user like's profile link."
},
{
"ref":"aiobungie.crate.player",
"url":12,
"doc":"Basic implementation for a Bungie a player."
},
{
"ref":"aiobungie.crate.player.Player",
"url":12,
"doc":"Represents a Bungie Destiny 2 Player. Method generated by attrs for class Player."
},
{
"ref":"aiobungie.crate.player.Player.unique_name",
"url":12,
"doc":"The user's unique name.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.player.Player.id",
"url":12,
"doc":"The player's id."
},
{
"ref":"aiobungie.crate.player.Player.name",
"url":12,
"doc":"The player's name"
},
{
"ref":"aiobungie.crate.player.Player.type",
"url":12,
"doc":"The profile's membership type."
},
{
"ref":"aiobungie.crate.player.Player.types",
"url":12,
"doc":"A list of the player's membership types.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.player.Player.icon",
"url":12,
"doc":"The player's icon."
},
{
"ref":"aiobungie.crate.player.Player.code",
"url":12,
"doc":"The clan member's bungie display name code. This can be  None if not found.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.player.Player.is_public",
"url":12,
"doc":"The player's profile privacy."
},
{
"ref":"aiobungie.crate.player.Player.crossave_override",
"url":12,
"doc":"Returns  1 if the user has a cross save override in effect and 0 if not.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.player.Player.last_seen_name",
"url":3,
"doc":"The member's last seen display name. You may use this field if  DestinyUser.name is  Undefined ."
},
{
"ref":"aiobungie.crate.player.Player.link",
"url":3,
"doc":"The user like's profile link."
},
{
"ref":"aiobungie.crate.profile",
"url":5,
"doc":"Implementation for a Bungie a Profile."
},
{
"ref":"aiobungie.crate.profile.Profile",
"url":5,
"doc":"Represents a Bungie member Profile. Bungie profiles requires components. But its kinda boring to pass multiple components to a parameter. So. The  .Profile crate will include all Bungie components. to be accessiable as a crate. How?. For an example: to access the  Characters component you'll need to pass  ?component=200 . But here you can just return the character itself from the profile using  await .Profile.titan() and the other character methods which returns a  aiobungie.crate.Character crate. crates are basically classes/objects. Example    -   client = aiobungie.Client( .) profile = await client.fetch_profile(\"Fate\")  access the character component and get my warlock. warlock = await profile.warlock() assert warlock.light  1320   Method generated by attrs for class Profile."
},
{
"ref":"aiobungie.crate.profile.Profile.titan_id",
"url":5,
"doc":"The titan id of the profile player."
},
{
"ref":"aiobungie.crate.profile.Profile.hunter_id",
"url":5,
"doc":"The huter id of the profile player."
},
{
"ref":"aiobungie.crate.profile.Profile.warlock_id",
"url":5,
"doc":"The warlock id of the profile player."
},
{
"ref":"aiobungie.crate.profile.Profile.character_ids",
"url":5,
"doc":"A list of the profile's character ids."
},
{
"ref":"aiobungie.crate.profile.Profile.id",
"url":5,
"doc":"Profile's id"
},
{
"ref":"aiobungie.crate.profile.Profile.is_public",
"url":5,
"doc":"Profile's privacy status."
},
{
"ref":"aiobungie.crate.profile.Profile.last_played",
"url":5,
"doc":"Profile's last played Destiny 2 played date."
},
{
"ref":"aiobungie.crate.profile.Profile.name",
"url":5,
"doc":"Profile's name."
},
{
"ref":"aiobungie.crate.profile.Profile.net",
"url":5,
"doc":"A network state used for making external requests."
},
{
"ref":"aiobungie.crate.profile.Profile.power_cap",
"url":5,
"doc":"The profile's current seaspn power cap."
},
{
"ref":"aiobungie.crate.profile.Profile.type",
"url":5,
"doc":"Profile's type."
},
{
"ref":"aiobungie.crate.profile.Profile.titan",
"url":5,
"doc":"Returns the titan character of the profile owner.",
"func":1
},
{
"ref":"aiobungie.crate.profile.Profile.hunter",
"url":5,
"doc":"Returns the hunter character of the profile owner.",
"func":1
},
{
"ref":"aiobungie.crate.profile.Profile.warlock",
"url":5,
"doc":"Returns the Warlock character of the profile owner.",
"func":1
},
{
"ref":"aiobungie.crate.profile.ProfileComponent",
"url":5,
"doc":"An interface that include all bungie profile components. Some fields may or may not be available here."
},
{
"ref":"aiobungie.crate.profile.ProfileComponent.net",
"url":5,
"doc":"A network state used for making external requests."
},
{
"ref":"aiobungie.crate.profile.ProfileComponent.name",
"url":5,
"doc":"Profile's name"
},
{
"ref":"aiobungie.crate.profile.ProfileComponent.type",
"url":5,
"doc":"Profile's membership type."
},
{
"ref":"aiobungie.crate.profile.ProfileComponent.last_played",
"url":5,
"doc":"The profile user's last played date time."
},
{
"ref":"aiobungie.crate.profile.ProfileComponent.is_public",
"url":5,
"doc":"Profile's privacy status."
},
{
"ref":"aiobungie.crate.profile.ProfileComponent.character_ids",
"url":5,
"doc":"A list of the profile's character ids."
},
{
"ref":"aiobungie.crate.profile.ProfileComponent.id",
"url":5,
"doc":"The profile's id."
},
{
"ref":"aiobungie.crate.profile.ProfileComponent.titan",
"url":5,
"doc":"Returns the titan character of the profile owner.",
"func":1
},
{
"ref":"aiobungie.crate.profile.ProfileComponent.hunter",
"url":5,
"doc":"Returns the hunter character of the profile owner.",
"func":1
},
{
"ref":"aiobungie.crate.profile.ProfileComponent.warlock",
"url":5,
"doc":"Returns the Warlock character of the profile owner.",
"func":1
},
{
"ref":"aiobungie.crate.season",
"url":13,
"doc":"A basic implementations of stuff that a Destiny 2 season contains. This includes all season that can be found in a regular season i.e, season artifact, season content, season pass, etc."
},
{
"ref":"aiobungie.crate.user",
"url":3,
"doc":"Basic implementation for a Bungie a user."
},
{
"ref":"aiobungie.crate.user.User",
"url":3,
"doc":"Concrete representtion of a Bungie user. This includes both Bungie net and Destiny memberships information. Method generated by attrs for class User."
},
{
"ref":"aiobungie.crate.user.User.bungie",
"url":3,
"doc":"The user's bungie net membership.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.user.User.destiny",
"url":3,
"doc":"A sequence of the user's Destiny memberships.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.user.UserLike",
"url":3,
"doc":"An ABC that's used for all userlike objects."
},
{
"ref":"aiobungie.crate.user.UserLike.id",
"url":3,
"doc":"The user like's id."
},
{
"ref":"aiobungie.crate.user.UserLike.name",
"url":3,
"doc":"The user like's name."
},
{
"ref":"aiobungie.crate.user.UserLike.last_seen_name",
"url":3,
"doc":"The user like's last seen name."
},
{
"ref":"aiobungie.crate.user.UserLike.is_public",
"url":3,
"doc":"True if the user profile is public or no."
},
{
"ref":"aiobungie.crate.user.UserLike.type",
"url":3,
"doc":"The user type of the user."
},
{
"ref":"aiobungie.crate.user.UserLike.icon",
"url":3,
"doc":"The user like's icon."
},
{
"ref":"aiobungie.crate.user.UserLike.code",
"url":3,
"doc":"The user like's unique display name code. This can be None if the user hasn't logged in after season of the lost update.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.user.UserLike.unique_name",
"url":3,
"doc":"The user like's display name. This includes the full name with the user name code.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.user.UserLike.link",
"url":3,
"doc":"The user like's profile link."
},
{
"ref":"aiobungie.crate.user.HardLinkedMembership",
"url":3,
"doc":"Represents hard linked Bungie user membership. This currently only supports SteamID which's a public credenitial. Also Cross-Save Aware. Method generated by attrs for class HardLinkedMembership."
},
{
"ref":"aiobungie.crate.user.HardLinkedMembership.cross_save_type",
"url":3,
"doc":"The hard link user's crpss save membership type. Default is set to None-0"
},
{
"ref":"aiobungie.crate.user.HardLinkedMembership.id",
"url":3,
"doc":"The hard link user id"
},
{
"ref":"aiobungie.crate.user.HardLinkedMembership.type",
"url":3,
"doc":"The hard link user membership type."
},
{
"ref":"aiobungie.crate.user.UserThemes",
"url":3,
"doc":"Represents a Bungie User theme. Method generated by attrs for class UserThemes."
},
{
"ref":"aiobungie.crate.user.UserThemes.description",
"url":3,
"doc":"An optional theme description. This field could be  None if no description found."
},
{
"ref":"aiobungie.crate.user.UserThemes.id",
"url":3,
"doc":"The theme id."
},
{
"ref":"aiobungie.crate.user.UserThemes.name",
"url":3,
"doc":"An optional theme name. if not found this field will be  None "
},
{
"ref":"aiobungie.crate.user.BungieUser",
"url":3,
"doc":"Represents a Bungie user. Method generated by attrs for class BungieUser."
},
{
"ref":"aiobungie.crate.user.BungieUser.about",
"url":3,
"doc":"The user's about, Default is None if nothing is Found."
},
{
"ref":"aiobungie.crate.user.BungieUser.blizzard_name",
"url":3,
"doc":"The user's blizzard name if it exists."
},
{
"ref":"aiobungie.crate.user.BungieUser.code",
"url":3,
"doc":"The user's unique display name code. This can be None if the user hasn't logged in after season of the lost update.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.user.BungieUser.created_at",
"url":3,
"doc":"The user's creation date in UTC timezone."
},
{
"ref":"aiobungie.crate.user.BungieUser.display_title",
"url":3,
"doc":"User's display title.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.user.BungieUser.id",
"url":3,
"doc":"The user's id"
},
{
"ref":"aiobungie.crate.user.BungieUser.is_deleted",
"url":3,
"doc":"True if the user is deleted"
},
{
"ref":"aiobungie.crate.user.BungieUser.locale",
"url":3,
"doc":"The user's locale."
},
{
"ref":"aiobungie.crate.user.BungieUser.name",
"url":3,
"doc":"The user's name."
},
{
"ref":"aiobungie.crate.user.BungieUser.picture",
"url":3,
"doc":"The user's profile picture."
},
{
"ref":"aiobungie.crate.user.BungieUser.psn_name",
"url":3,
"doc":"The user's psn id if it exists."
},
{
"ref":"aiobungie.crate.user.BungieUser.show_activity",
"url":3,
"doc":" True if the user is showing their activity status and  False if not.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.user.BungieUser.stadia_name",
"url":3,
"doc":"The user's stadia name if it exists  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.user.BungieUser.status",
"url":3,
"doc":"The user's bungie status text"
},
{
"ref":"aiobungie.crate.user.BungieUser.steam_name",
"url":3,
"doc":"The user's steam name if it exists"
},
{
"ref":"aiobungie.crate.user.BungieUser.theme_id",
"url":3,
"doc":"User profile's theme id.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.user.BungieUser.theme_name",
"url":3,
"doc":"User's profile theme name.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.user.BungieUser.twitch_name",
"url":3,
"doc":"The user's twitch name if it exists."
},
{
"ref":"aiobungie.crate.user.BungieUser.unique_name",
"url":3,
"doc":"The user's unique name which includes their unique code. This field could be None if no unique name found.  versionadded 0.2.5"
},
{
"ref":"aiobungie.crate.user.BungieUser.updated_at",
"url":3,
"doc":"The user's last updated om UTC date."
},
{
"ref":"aiobungie.crate.user.PartialBungieUser",
"url":3,
"doc":"Represents partial bungie user. This is usually used for bungie user info for destiny member objects. Like Clan members, owners, moderators for an example. Method generated by attrs for class PartialBungieUser."
},
{
"ref":"aiobungie.crate.user.PartialBungieUser.crossave_override",
"url":3,
"doc":"The user's crossave override membership."
},
{
"ref":"aiobungie.crate.user.PartialBungieUser.icon",
"url":3,
"doc":"The user's icon."
},
{
"ref":"aiobungie.crate.user.PartialBungieUser.id",
"url":3,
"doc":"The user's id."
},
{
"ref":"aiobungie.crate.user.PartialBungieUser.is_public",
"url":3,
"doc":"The user's privacy."
},
{
"ref":"aiobungie.crate.user.PartialBungieUser.name",
"url":3,
"doc":"The user's name. Field may be undefined if not found."
},
{
"ref":"aiobungie.crate.user.PartialBungieUser.type",
"url":3,
"doc":"The user's membership type."
},
{
"ref":"aiobungie.crate.user.DestinyUser",
"url":3,
"doc":"Represents a Bungie user's Destiny memberships.  versionadded 0.2.5 Method generated by attrs for class DestinyUser."
},
{
"ref":"aiobungie.crate.user.DestinyUser.unique_name",
"url":3,
"doc":"The member's unique name. This field may be  Undefined if not found."
},
{
"ref":"aiobungie.crate.user.DestinyUser.code",
"url":3,
"doc":"The member's name code. This field may be  None if not found."
},
{
"ref":"aiobungie.crate.user.DestinyUser.crossave_override",
"url":3,
"doc":"The member's corssave override membership type."
},
{
"ref":"aiobungie.crate.user.DestinyUser.icon",
"url":3,
"doc":"The member's icon if it was present."
},
{
"ref":"aiobungie.crate.user.DestinyUser.id",
"url":3,
"doc":"The member's id."
},
{
"ref":"aiobungie.crate.user.DestinyUser.is_public",
"url":3,
"doc":"The member's profile privacy status."
},
{
"ref":"aiobungie.crate.user.DestinyUser.last_seen_name",
"url":3,
"doc":"The member's last seen display name. You may use this field if  DestinyUser.name is  Undefined ."
},
{
"ref":"aiobungie.crate.user.DestinyUser.name",
"url":3,
"doc":"The member's name."
},
{
"ref":"aiobungie.crate.user.DestinyUser.type",
"url":3,
"doc":"The member's membership type."
},
{
"ref":"aiobungie.crate.user.DestinyUser.types",
"url":3,
"doc":"A sequence of the member's membership types."
},
{
"ref":"aiobungie.crate.user.DestinyUser.link",
"url":3,
"doc":"The user like's profile link."
},
{
"ref":"aiobungie.error",
"url":14,
"doc":"aiobungie Exceptions."
},
{
"ref":"aiobungie.error.AiobungieError",
"url":14,
"doc":"The base exception class that all other errors inherit from."
},
{
"ref":"aiobungie.error.PlayerNotFound",
"url":14,
"doc":"Raised when a  aiobungie.crate.Player is not found."
},
{
"ref":"aiobungie.error.ActivityNotFound",
"url":14,
"doc":"Raised when a  aiobungie.crate.Activity not found."
},
{
"ref":"aiobungie.error.ClanNotFound",
"url":14,
"doc":"Raised when a  aiobungie.crate.Clan not found."
},
{
"ref":"aiobungie.error.CharacterError",
"url":14,
"doc":"Raised when a  aiobungie.crate.Character not found. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.CharacterError.message",
"url":14,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.CharacterError.long_message",
"url":14,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.NotFound",
"url":14,
"doc":"Raised when an unknown request was not found."
},
{
"ref":"aiobungie.error.HTTPException",
"url":14,
"doc":"Exception for handling  aiobungie.rest.RESTClient requests errors. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.HTTPException.long_message",
"url":14,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.HTTPException.message",
"url":14,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.UserNotFound",
"url":14,
"doc":"Raised when a  aiobungie.crate.User not found."
},
{
"ref":"aiobungie.error.ComponentError",
"url":14,
"doc":"Raised when someone uses the wrong  aiobungie.internal.enums.Component. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.ComponentError.message",
"url":14,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.ComponentError.long_message",
"url":14,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.MembershipTypeError",
"url":14,
"doc":"Raised when the memberhsip type is invalid. or The crate you're trying to fetch doesn't have The requested membership type. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.MembershipTypeError.message",
"url":14,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.MembershipTypeError.long_message",
"url":14,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.Forbidden",
"url":14,
"doc":"Exception that's raised for when status code 403 occurs. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.Forbidden.message",
"url":14,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.Forbidden.long_message",
"url":14,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.Unauthorized",
"url":14,
"doc":"Unauthorized access. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.Unauthorized.message",
"url":14,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.Unauthorized.long_message",
"url":14,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.ResponseError",
"url":14,
"doc":"Typical Responses error."
},
{
"ref":"aiobungie.ext",
"url":15,
"doc":"aiobungie extensions."
},
{
"ref":"aiobungie.ext.Manifest",
"url":15,
"doc":""
},
{
"ref":"aiobungie.ext.Manifest.download",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.ext.Manifest.version",
"url":15,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.ext.meta",
"url":16,
"doc":"A very basic helper for the bungie Manifest."
},
{
"ref":"aiobungie.ext.meta.Manifest",
"url":16,
"doc":""
},
{
"ref":"aiobungie.ext.meta.Manifest.download",
"url":16,
"doc":"",
"func":1
},
{
"ref":"aiobungie.ext.meta.Manifest.version",
"url":16,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.interfaces",
"url":17,
"doc":"Aiobungie Interfaces provides abstracted objects for implementations."
},
{
"ref":"aiobungie.interfaces.RESTInterface",
"url":17,
"doc":"An interface for a rest only client implementation."
},
{
"ref":"aiobungie.interfaces.RESTInterface.static_search",
"url":17,
"doc":"Raw http search given a valid bungie endpoint. Parameters      path:  builtins.str The bungie endpoint or path. A path must look something like this \"Destiny2/3/Profile/46111239123/ .\" kwargs:  typing.Any Any other key words you'd like to pass through. Returns    -  typing.Any Any object.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.fetch_manifest",
"url":17,
"doc":"Access The bungie Manifest. Returns    -  builtins.bytes The bytes to read and write the manifest database.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.fetch_manifest_path",
"url":17,
"doc":"Return a string of the bungie manifest database url. Returns    -  builtins.str A downloadable url for the bungie manifest database.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.fetch_user",
"url":17,
"doc":"Fetch a Bungie user by their id. Parameters      id:  builtins.int The user id. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of users objects. Raises     aiobungie.error.UserNotFound The user was not found.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.search_users",
"url":17,
"doc":"Search for users by their global name and return all users who share this name. Parameters      name :  str The user name. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonArray] A JSON array of the found users. Raises     aiobungie.NotFound The user(s) was not found.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.fetch_user_themes",
"url":17,
"doc":"Fetch all available user themes. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonArray] A JSON array of user themes.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.fetch_hard_linked",
"url":17,
"doc":"Gets any hard linked membership given a credential. Only works for credentials that are public just  aiobungie.CredentialType.STEAMID right now. Cross Save aware. Parameters      credential:  builtins.int A valid SteamID64 type:  aiobungie.CredentialType The crededntial type. This must not be changed Since its only credential that works \"currently\" Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the found user hard linked types.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.fetch_membership_from_id",
"url":17,
"doc":"Fetch Bungie user's memberships from their id. Parameters      id :  builtins.int The user's id. type :  aiobungie.MembershipType The user's membership type. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the found user. Raises    aiobungie.UserNotFound The requested user was not found.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.fetch_profile",
"url":17,
"doc":"Fetche a bungie profile. Parameters      memberid:  builtins.int The member's id. type:  aiobungie.MembershipType A valid membership type. Returns      ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the found profile. Raises     aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.fetch_player",
"url":17,
"doc":"Fetch a Destiny 2 Player. Parameters      - name:  builtins.str The Player's Name.  note You must also pass the player's unique code. A full name parameter should look like this  Fate\u6012 4275 type:  aiobungie.internal.enums.MembershipType The player's membership type, e,g. XBOX, STEAM, PSN Returns      ResponseSig[aiobungie.internal.helpers.JsonArray] A JSON array of the found players. Raises     aiobungie.PlayerNotFound The player was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.fetch_character",
"url":17,
"doc":"Fetch a Destiny 2 player's characters. Parameters      memberid:  builtins.int A valid bungie member id. type:  aiobungie.internal.enums.MembershipType The member's membership type. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the requested character. Raises     aiobungie.error.CharacterError raised if the Character was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.fetch_activity",
"url":17,
"doc":"Fetch a Destiny 2 activity for the specified user id and character. Parameters      member_id:  builtins.int The user id that starts with  4611 . character_id:  builtins.int The id of the character to retrieve. mode:  aiobungie.internal.enums.GameMode This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc. membership_type:  aiobungie.internal.enums.MembershipType The Member ship type, if nothing was passed than it will return all. page: typing.Optional[builtins.int] The page number limit: typing.Optional[builtins.int] Limit the returned result. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the player's activities. Raises     aiobungie.error.ActivityNotFound The activity was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.fetch_post_activity",
"url":17,
"doc":"Fetch a post activity details.  warning This http request is not implemented yet and it will raise  NotImplementedError Parameters      instance:  builtins.int The activity instance id. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the post activity.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.fetch_clan_from_id",
"url":17,
"doc":"Fetch a Bungie Clan by its id. Parameters      - id:  builtins.int The clan id. Returns      ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the clan. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.fetch_clan",
"url":17,
"doc":"Fetch a Clan by its name. This method will return the first clan found with given name name. Parameters      name:  builtins.str The clan name type  aiobungie.GroupType The group type, Default is one. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the clan. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.fetch_clan_members",
"url":17,
"doc":"Fetch all Bungie Clan members. Parameters      clan_id :  builsins.int The clans id type :  aiobungie.MembershipType An optional clan member's membership type. Default is set to  aiobungie.MembershipType.NONE Which returns the first matched clan member by their name. name :  builtins.str This parameter is only provided here to keep the signature with the main client implementation, Which only works with the non-rest clients. It returns a specific clan member by their name. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonArray] A JSON array of clan members. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.fetch_inventory_item",
"url":17,
"doc":"Fetch a static inventory item entity given a its hash. Parameters      type:  builtins.str Entity's type definition. hash:  builtins.int Entity's hash. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON array object of the inventory item.",
"func":1
},
{
"ref":"aiobungie.interfaces.RESTInterface.fetch_app",
"url":17,
"doc":"Fetch a Bungie Application. Parameters      - appid:  builtins.int The application id. Returns      ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the application.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest",
"url":18,
"doc":"An interface for the rest client."
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface",
"url":18,
"doc":"An interface for a rest only client implementation."
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.static_search",
"url":18,
"doc":"Raw http search given a valid bungie endpoint. Parameters      path:  builtins.str The bungie endpoint or path. A path must look something like this \"Destiny2/3/Profile/46111239123/ .\" kwargs:  typing.Any Any other key words you'd like to pass through. Returns    -  typing.Any Any object.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.fetch_manifest",
"url":18,
"doc":"Access The bungie Manifest. Returns    -  builtins.bytes The bytes to read and write the manifest database.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.fetch_manifest_path",
"url":18,
"doc":"Return a string of the bungie manifest database url. Returns    -  builtins.str A downloadable url for the bungie manifest database.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.fetch_user",
"url":18,
"doc":"Fetch a Bungie user by their id. Parameters      id:  builtins.int The user id. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of users objects. Raises     aiobungie.error.UserNotFound The user was not found.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.search_users",
"url":18,
"doc":"Search for users by their global name and return all users who share this name. Parameters      name :  str The user name. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonArray] A JSON array of the found users. Raises     aiobungie.NotFound The user(s) was not found.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.fetch_user_themes",
"url":18,
"doc":"Fetch all available user themes. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonArray] A JSON array of user themes.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.fetch_hard_linked",
"url":18,
"doc":"Gets any hard linked membership given a credential. Only works for credentials that are public just  aiobungie.CredentialType.STEAMID right now. Cross Save aware. Parameters      credential:  builtins.int A valid SteamID64 type:  aiobungie.CredentialType The crededntial type. This must not be changed Since its only credential that works \"currently\" Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the found user hard linked types.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.fetch_membership_from_id",
"url":18,
"doc":"Fetch Bungie user's memberships from their id. Parameters      id :  builtins.int The user's id. type :  aiobungie.MembershipType The user's membership type. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the found user. Raises    aiobungie.UserNotFound The requested user was not found.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.fetch_profile",
"url":18,
"doc":"Fetche a bungie profile. Parameters      memberid:  builtins.int The member's id. type:  aiobungie.MembershipType A valid membership type. Returns      ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the found profile. Raises     aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.fetch_player",
"url":18,
"doc":"Fetch a Destiny 2 Player. Parameters      - name:  builtins.str The Player's Name.  note You must also pass the player's unique code. A full name parameter should look like this  Fate\u6012 4275 type:  aiobungie.internal.enums.MembershipType The player's membership type, e,g. XBOX, STEAM, PSN Returns      ResponseSig[aiobungie.internal.helpers.JsonArray] A JSON array of the found players. Raises     aiobungie.PlayerNotFound The player was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.fetch_character",
"url":18,
"doc":"Fetch a Destiny 2 player's characters. Parameters      memberid:  builtins.int A valid bungie member id. type:  aiobungie.internal.enums.MembershipType The member's membership type. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the requested character. Raises     aiobungie.error.CharacterError raised if the Character was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.fetch_activity",
"url":18,
"doc":"Fetch a Destiny 2 activity for the specified user id and character. Parameters      member_id:  builtins.int The user id that starts with  4611 . character_id:  builtins.int The id of the character to retrieve. mode:  aiobungie.internal.enums.GameMode This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc. membership_type:  aiobungie.internal.enums.MembershipType The Member ship type, if nothing was passed than it will return all. page: typing.Optional[builtins.int] The page number limit: typing.Optional[builtins.int] Limit the returned result. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the player's activities. Raises     aiobungie.error.ActivityNotFound The activity was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.fetch_post_activity",
"url":18,
"doc":"Fetch a post activity details.  warning This http request is not implemented yet and it will raise  NotImplementedError Parameters      instance:  builtins.int The activity instance id. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the post activity.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.fetch_clan_from_id",
"url":18,
"doc":"Fetch a Bungie Clan by its id. Parameters      - id:  builtins.int The clan id. Returns      ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the clan. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.fetch_clan",
"url":18,
"doc":"Fetch a Clan by its name. This method will return the first clan found with given name name. Parameters      name:  builtins.str The clan name type  aiobungie.GroupType The group type, Default is one. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the clan. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.fetch_clan_members",
"url":18,
"doc":"Fetch all Bungie Clan members. Parameters      clan_id :  builsins.int The clans id type :  aiobungie.MembershipType An optional clan member's membership type. Default is set to  aiobungie.MembershipType.NONE Which returns the first matched clan member by their name. name :  builtins.str This parameter is only provided here to keep the signature with the main client implementation, Which only works with the non-rest clients. It returns a specific clan member by their name. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonArray] A JSON array of clan members. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.fetch_inventory_item",
"url":18,
"doc":"Fetch a static inventory item entity given a its hash. Parameters      type:  builtins.str Entity's type definition. hash:  builtins.int Entity's hash. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON array object of the inventory item.",
"func":1
},
{
"ref":"aiobungie.interfaces.rest.RESTInterface.fetch_app",
"url":18,
"doc":"Fetch a Bungie Application. Parameters      - appid:  builtins.int The application id. Returns      ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the application.",
"func":1
},
{
"ref":"aiobungie.internal",
"url":19,
"doc":"Package contains internal and helpers for aiobungie."
},
{
"ref":"aiobungie.internal.Image",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.Image.url",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.Image.is_jpg",
"url":19,
"doc":"Checks if the given path for the image is a JPEG type."
},
{
"ref":"aiobungie.internal.Image.partial",
"url":19,
"doc":"A partial image that just returns undefined.",
"func":1
},
{
"ref":"aiobungie.internal.deprecated",
"url":19,
"doc":"functions with this decorator will not work or is not implemented yet.",
"func":1
},
{
"ref":"aiobungie.internal.assets",
"url":20,
"doc":"aiobungie assets module for API Image hash and path linking."
},
{
"ref":"aiobungie.internal.assets.Image",
"url":20,
"doc":""
},
{
"ref":"aiobungie.internal.assets.Image.url",
"url":20,
"doc":""
},
{
"ref":"aiobungie.internal.assets.Image.is_jpg",
"url":20,
"doc":"Checks if the given path for the image is a JPEG type."
},
{
"ref":"aiobungie.internal.assets.Image.partial",
"url":20,
"doc":"A partial image that just returns undefined.",
"func":1
},
{
"ref":"aiobungie.internal.assets.MaybeImage",
"url":20,
"doc":"A type hint for images that may or may not exists in the api. Images returned from the api as None will be replaced with  Image.partial ."
},
{
"ref":"aiobungie.internal.enums",
"url":21,
"doc":"Bungie enums impl for aiobungie."
},
{
"ref":"aiobungie.internal.enums.GameMode",
"url":21,
"doc":"An Enum for all available gamemodes in Destiny 2."
},
{
"ref":"aiobungie.internal.enums.GameMode.NONE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.STORY",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.STRIKE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.RAID",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.ALLPVP",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.PATROL",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.ALLPVE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.TOF",
"url":21,
"doc":"Trials Of Osiris"
},
{
"ref":"aiobungie.internal.enums.GameMode.CONTROL",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.NIGHTFALL",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.IRONBANER",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.ALLSTRIKES",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.DUNGEON",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.GAMBIT",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.EMIPIRE_HUNT",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.RUMBLE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.CLASSIC_MIX",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.COUNTDOWN",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.DOUBLES",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.CLASH",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.MAYHEM",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.SURVIVAL",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType",
"url":21,
"doc":"An Enum for Bungie membership types."
},
{
"ref":"aiobungie.internal.enums.MembershipType.NONE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.XBOX",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.PSN",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.STEAM",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.BLIZZARD",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.STADIA",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.BUNGIE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.ALL",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Class",
"url":21,
"doc":"An Enum for Destiny character classes."
},
{
"ref":"aiobungie.internal.enums.Class.TITAN",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Class.HUNTER",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Class.WARLOCK",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Class.UNKNOWN",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType",
"url":21,
"doc":"An Enum for Destiny 2 milestone types."
},
{
"ref":"aiobungie.internal.enums.MilestoneType.UNKNOWN",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType.TUTORIAL",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType.ONETIME",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType.WEEKLY",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType.DAILY",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType.SPECIAL",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Race",
"url":21,
"doc":"An Enum for Destiny races."
},
{
"ref":"aiobungie.internal.enums.Race.HUMAN",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Race.AWOKEN",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Race.EXO",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Race.UNKNOWN",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor",
"url":21,
"doc":"An Enum for all available vendors in Destiny 2."
},
{
"ref":"aiobungie.internal.enums.Vendor.ZAVALA",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.XUR",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.BANSHE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.SPIDER",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.SHAXX",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.KADI",
"url":21,
"doc":"Postmaster exo."
},
{
"ref":"aiobungie.internal.enums.Vendor.YUNA",
"url":21,
"doc":"Asia servers only."
},
{
"ref":"aiobungie.internal.enums.Vendor.EVERVERSE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.AMANDA",
"url":21,
"doc":"Amanda holiday"
},
{
"ref":"aiobungie.internal.enums.Vendor.CROW",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.HAWTHORNE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.ADA1",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.DRIFTER",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.IKORA",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.SAINT",
"url":21,
"doc":"Saint-14"
},
{
"ref":"aiobungie.internal.enums.Vendor.ERIS_MORN",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.SHAW_HAWN",
"url":21,
"doc":"COSMODROME Guy"
},
{
"ref":"aiobungie.internal.enums.Vendor.VARIKS",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Raid",
"url":21,
"doc":"An Enum for all available raids in Destiny 2."
},
{
"ref":"aiobungie.internal.enums.Raid.DSC",
"url":21,
"doc":"Deep Stone Crypt"
},
{
"ref":"aiobungie.internal.enums.Raid.LW",
"url":21,
"doc":"Last Wish"
},
{
"ref":"aiobungie.internal.enums.Raid.VOG",
"url":21,
"doc":"Normal Valut of Glass"
},
{
"ref":"aiobungie.internal.enums.Raid.GOS",
"url":21,
"doc":"Garden Of Salvation"
},
{
"ref":"aiobungie.internal.enums.Dungeon",
"url":21,
"doc":"An Enum for all available Dungeon/Like missions in Destiny 2."
},
{
"ref":"aiobungie.internal.enums.Dungeon.NORMAL_PRESAGE",
"url":21,
"doc":"Normal Presage"
},
{
"ref":"aiobungie.internal.enums.Dungeon.MASTER_PRESAGE",
"url":21,
"doc":"Master Presage"
},
{
"ref":"aiobungie.internal.enums.Dungeon.HARBINGER",
"url":21,
"doc":"Harbinger"
},
{
"ref":"aiobungie.internal.enums.Dungeon.PROPHECY",
"url":21,
"doc":"Prophecy"
},
{
"ref":"aiobungie.internal.enums.Dungeon.MASTER_POH",
"url":21,
"doc":"Master Pit of Heresy?"
},
{
"ref":"aiobungie.internal.enums.Dungeon.LEGEND_POH",
"url":21,
"doc":"Legend Pit of Heresy?"
},
{
"ref":"aiobungie.internal.enums.Dungeon.POH",
"url":21,
"doc":"Normal Pit of Heresy."
},
{
"ref":"aiobungie.internal.enums.Dungeon.SHATTERED",
"url":21,
"doc":"Shattered Throne"
},
{
"ref":"aiobungie.internal.enums.Gender",
"url":21,
"doc":"An Enum for Destiny Genders."
},
{
"ref":"aiobungie.internal.enums.Gender.MALE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Gender.FEMALE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Gender.UNKNOWN",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component",
"url":21,
"doc":"An Enum for Destiny 2 Components."
},
{
"ref":"aiobungie.internal.enums.Component.NONE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.PROFILE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.SILVER",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.PROGRESSION",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.INVENTORIES",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.CHARACTERS",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.CHAR_INVENTORY",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.CHARECTER_PROGRESSION",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.EQUIPED_ITEMS",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.VENDORS",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.RECORDS",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.VENDOR_SALES",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Planet",
"url":21,
"doc":"An Enum for all available planets in Destiny 2."
},
{
"ref":"aiobungie.internal.enums.Planet.UNKNOWN",
"url":21,
"doc":"Unknown space"
},
{
"ref":"aiobungie.internal.enums.Planet.EARTH",
"url":21,
"doc":"Earth"
},
{
"ref":"aiobungie.internal.enums.Planet.DREAMING_CITY",
"url":21,
"doc":"The Dreaming city."
},
{
"ref":"aiobungie.internal.enums.Planet.NESSUS",
"url":21,
"doc":"Nessus"
},
{
"ref":"aiobungie.internal.enums.Planet.MOON",
"url":21,
"doc":"The Moon"
},
{
"ref":"aiobungie.internal.enums.Planet.COSMODROME",
"url":21,
"doc":"The Cosmodrome"
},
{
"ref":"aiobungie.internal.enums.Planet.TANGLED_SHORE",
"url":21,
"doc":"The Tangled Shore"
},
{
"ref":"aiobungie.internal.enums.Planet.VENUS",
"url":21,
"doc":"Venus"
},
{
"ref":"aiobungie.internal.enums.Planet.EAZ",
"url":21,
"doc":"European Aerial Zone"
},
{
"ref":"aiobungie.internal.enums.Planet.EUROPA",
"url":21,
"doc":"Europa"
},
{
"ref":"aiobungie.internal.enums.Stat",
"url":21,
"doc":"An Enum for Destiny 2 character stats."
},
{
"ref":"aiobungie.internal.enums.Stat.NONE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.MOBILITY",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.RESILIENCE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.RECOVERY",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.DISCIPLINE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.INTELLECT",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.STRENGTH",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.WeaponType",
"url":21,
"doc":"Enums for The three Destiny Weapon Types"
},
{
"ref":"aiobungie.internal.enums.WeaponType.NONE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.WeaponType.KINETIC",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.WeaponType.ENERGY",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.WeaponType.POWER",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType",
"url":21,
"doc":"Enums for Destiny Damage types"
},
{
"ref":"aiobungie.internal.enums.DamageType.NONE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.KINETIC",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.SOLAR",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.VOID",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.ARC",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.STASIS",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.RAID",
"url":21,
"doc":"This is a special damage type reserved for some raid activity encounters."
},
{
"ref":"aiobungie.internal.enums.Item",
"url":21,
"doc":"Enums for Destiny2's inventory bucket items"
},
{
"ref":"aiobungie.internal.enums.Item.NONE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.ARMOR",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.WEAPON",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.AUTO_RIFLE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SHOTGUN",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.MACHINE_GUN",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.HANDCANNON",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.ROCKET_LAUNCHER",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.FUSION_RIFLE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SNIPER_RIFLE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.PULSE_RIFLE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SCOUT_RIFLE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SIDEARM",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SWORD",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.MASK",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SHADER",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.ORNAMENT",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.FUSION_RIFLELINE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.GRENADE_LAUNCHER",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SUBMACHINE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.TRACE_RIFLE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.HELMET_ARMOR",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.GAUNTLET_ARMOR",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.CHEST_ARMOR",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.LEG_ARMOR",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.CLASS_ARMOR",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.HELMET",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.GAUNTLET",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.CHEST",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.LEG",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.CLASS",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.BOW",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.EMBLEMS",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.LEGENDRY_SHARDS",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.GHOST",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SUBCLASS",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SEASONAL_ARTIFACT",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.EMOTES",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SYNTHWAEV_TEMPLATE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.KINETIC",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.ENERGY",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.POWER",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Place",
"url":21,
"doc":"An Enum for Destiny 2 Places and NOT Planets"
},
{
"ref":"aiobungie.internal.enums.Place.ORBIT",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Place.SOCIAL",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Place.LIGHT_HOUSE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Place.EXPLORE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier",
"url":21,
"doc":"An enum for a Destiny 2 item tier."
},
{
"ref":"aiobungie.internal.enums.ItemTier.NONE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier.BASIC",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier.COMMON",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier.RARE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier.LEGENDERY",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier.EXOTIC",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.AmmoType",
"url":21,
"doc":"AN enum for Detyiny 2 ammo types."
},
{
"ref":"aiobungie.internal.enums.AmmoType.NONE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.AmmoType.PRIMARY",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.AmmoType.SPECIAL",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.AmmoType.HEAVY",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GroupType",
"url":21,
"doc":"An enums for the known bungie group types."
},
{
"ref":"aiobungie.internal.enums.GroupType.GENERAL",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GroupType.CLAN",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType",
"url":21,
"doc":"The types of the accounts system supports at bungie."
},
{
"ref":"aiobungie.internal.enums.CredentialType.NONE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.XUID",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.PSNID",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.WILD",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.FAKE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.FACEBOOK",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.GOOGLE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.WINDOWS",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.DEMONID",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.STEAMID",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.BATTLENETID",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.STADIAID",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.TWITCHID",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Presence",
"url":21,
"doc":"An enum for a bungie friend status."
},
{
"ref":"aiobungie.internal.enums.Presence.OFFLINE_OR_UNKNOWN",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Presence.ONLINE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Relationship",
"url":21,
"doc":"An enum for bungie friends relationship types."
},
{
"ref":"aiobungie.internal.enums.Relationship.UNKNOWN",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Relationship.FRIEND",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Relationship.INCOMING_REQUEST",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Relationship.OUTGOING_REQUEST",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ClanMemberType",
"url":21,
"doc":"An enumeration."
},
{
"ref":"aiobungie.internal.enums.ClanMemberType.NONE",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ClanMemberType.BEGINNER",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ClanMemberType.MEMBER",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ClanMemberType.ADMIN",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ClanMemberType.ACTING_FOUNDER",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ClanMemberType.FOUNDER",
"url":21,
"doc":""
},
{
"ref":"aiobungie.internal.helpers",
"url":22,
"doc":"A module for helper functions and types."
},
{
"ref":"aiobungie.internal.helpers.deprecated",
"url":22,
"doc":"functions with this decorator will not work or is not implemented yet.",
"func":1
},
{
"ref":"aiobungie.internal.helpers.JsonObject",
"url":22,
"doc":"A json like dict of string key and any value. i.e., {\"Key\": 1, \"Key2\": \"Value\"}"
},
{
"ref":"aiobungie.internal.helpers.JsonArray",
"url":22,
"doc":"A json like list of any data type. i.e., [{\"Key\": 1}, {\"Key2\": \"Value\"}]"
},
{
"ref":"aiobungie.internal.helpers.Undefined",
"url":22,
"doc":"An undefined type for attribs that may be undefined and not None."
},
{
"ref":"aiobungie.internal.helpers.UndefinedOr",
"url":22,
"doc":"A union version of the Undefined type which can be undefined or any other type."
},
{
"ref":"aiobungie.internal.helpers.UndefinedType",
"url":22,
"doc":"An  UNDEFINED type."
},
{
"ref":"aiobungie.internal.helpers.Unknown",
"url":22,
"doc":"Stuff that are empty strings."
},
{
"ref":"aiobungie.internal.helpers.just",
"url":22,
"doc":"A helper function that takes a list of dicts and return a list of all keys found inside the dict",
"func":1
},
{
"ref":"aiobungie.internal.helpers.NoneOr",
"url":22,
"doc":"A Union type that's similar to to  Optional[T] "
},
{
"ref":"aiobungie.internal.helpers.get_or_make_loop",
"url":22,
"doc":"Get the current usable event loop or create a new one. Returns    - asyncio.AbstractEventLoop",
"func":1
},
{
"ref":"aiobungie.internal.serialize",
"url":23,
"doc":"Deserialization for all bungie incoming json payloads."
},
{
"ref":"aiobungie.internal.serialize.Factory",
"url":23,
"doc":"The base Deserialization factory class for all aiobungie objects."
},
{
"ref":"aiobungie.internal.serialize.Factory.deserialize_bungie_user",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deserialize_partial_bungie_user",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deserialize_destiny_user",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deserialize_destiny_members",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deserialize_user",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deseialize_found_users",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.set_themese_attrs",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deserialize_user_themes",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deserialize_player",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deseialize_clan_owner",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deseialize_clan",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deserialize_clan_member",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deserialize_clan_members",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deserialize_app_owner",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deserialize_app",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deserialize_character",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deserialize_profile",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deserialize_inventory_entity",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Factory.deserialize_activity",
"url":23,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.time",
"url":24,
"doc":"Time formatting module."
},
{
"ref":"aiobungie.internal.time.format_played",
"url":24,
"doc":"Converts A Bungie's total played time in minutes to a a readable time.",
"func":1
},
{
"ref":"aiobungie.internal.time.from_timestamp",
"url":24,
"doc":"Converts timestamp to  datetime.datetime ",
"func":1
},
{
"ref":"aiobungie.internal.time.clean_date",
"url":24,
"doc":"Formats  datetime.datetime to a readable date.",
"func":1
},
{
"ref":"aiobungie.internal.time.to_timestamp",
"url":24,
"doc":"Converts datetime.datetime.utctimetuple() to timestamp.",
"func":1
},
{
"ref":"aiobungie.internal.traits",
"url":25,
"doc":"Module for all client interfaces."
},
{
"ref":"aiobungie.internal.traits.RESTful",
"url":25,
"doc":"A RESTful, serializble and netrunner client protocol."
},
{
"ref":"aiobungie.internal.traits.RESTful.run",
"url":25,
"doc":"Runs a Coro function until its complete. This is equivalent to asyncio.get_event_loop().run_until_complete( .) Parameters      future:  typing.Coroutine[typing.Any, typing.Any, typing.Any] Your coro function. Example    -   async def main() -> None: player = await client.fetch_player(\"Fate\") print(player.name) client.run(main(  ",
"func":1
},
{
"ref":"aiobungie.internal.traits.RESTful.rest",
"url":25,
"doc":"The rest client we make the http request to the API with."
},
{
"ref":"aiobungie.internal.traits.RESTful.request",
"url":25,
"doc":"Returns a client network state for making external requests."
},
{
"ref":"aiobungie.internal.traits.RESTful.serialize",
"url":25,
"doc":"A property that returns a deserializer object for the client."
},
{
"ref":"aiobungie.internal.traits.Netrunner",
"url":25,
"doc":"A protocol represents The main client That's only used for making external requests."
},
{
"ref":"aiobungie.internal.traits.Netrunner.request",
"url":25,
"doc":"Returns a client network state for making external requests."
},
{
"ref":"aiobungie.internal.traits.Serializable",
"url":25,
"doc":"A protocol that uses  aiobungie.internal.serialize.Factory for deseializing objects."
},
{
"ref":"aiobungie.internal.traits.Serializable.serialize",
"url":25,
"doc":"A property that returns a deserializer object for the client."
},
{
"ref":"aiobungie.rest",
"url":26,
"doc":"A basic REST only client to interact with Bungie's REST API."
},
{
"ref":"aiobungie.rest.RESTClient",
"url":26,
"doc":"A REST only client implementation for interacting with Bungie's REST API. Attributes      token :  builtins.str A valid application token from Bungie's developer portal."
},
{
"ref":"aiobungie.rest.RESTClient.fetch_user",
"url":26,
"doc":"Fetch a Bungie user by their id. Parameters      id:  builtins.int The user id. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of users objects. Raises     aiobungie.error.UserNotFound The user was not found.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_user_themes",
"url":26,
"doc":"Fetch all available user themes. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonArray] A JSON array of user themes.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_membership_from_id",
"url":26,
"doc":"Fetch Bungie user's memberships from their id. Parameters      id :  builtins.int The user's id. type :  aiobungie.MembershipType The user's membership type. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the found user. Raises    aiobungie.UserNotFound The requested user was not found.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.static_search",
"url":26,
"doc":"Raw http search given a valid bungie endpoint. Parameters      path:  builtins.str The bungie endpoint or path. A path must look something like this \"Destiny2/3/Profile/46111239123/ .\" kwargs:  typing.Any Any other key words you'd like to pass through. Returns    -  typing.Any Any object.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_player",
"url":26,
"doc":"Fetch a Destiny 2 Player. Parameters      - name:  builtins.str The Player's Name.  note You must also pass the player's unique code. A full name parameter should look like this  Fate\u6012 4275 type:  aiobungie.internal.enums.MembershipType The player's membership type, e,g. XBOX, STEAM, PSN Returns      ResponseSig[aiobungie.internal.helpers.JsonArray] A JSON array of the found players. Raises     aiobungie.PlayerNotFound The player was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.search_users",
"url":26,
"doc":"Search for users by their global name and return all users who share this name. Parameters      name :  str The user name. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonArray] A JSON array of the found users. Raises     aiobungie.NotFound The user(s) was not found.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_clan_from_id",
"url":26,
"doc":"Fetch a Bungie Clan by its id. Parameters      - id:  builtins.int The clan id. Returns      ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the clan. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_clan",
"url":26,
"doc":"Fetch a Clan by its name. This method will return the first clan found with given name name. Parameters      name:  builtins.str The clan name type  aiobungie.GroupType The group type, Default is one. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the clan. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_app",
"url":26,
"doc":"Fetch a Bungie Application. Parameters      - appid:  builtins.int The application id. Returns      ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the application.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_character",
"url":26,
"doc":"Fetch a Destiny 2 player's characters. Parameters      memberid:  builtins.int A valid bungie member id. type:  aiobungie.internal.enums.MembershipType The member's membership type. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the requested character. Raises     aiobungie.error.CharacterError raised if the Character was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_activity",
"url":26,
"doc":"Fetch a Destiny 2 activity for the specified user id and character. Parameters      member_id:  builtins.int The user id that starts with  4611 . character_id:  builtins.int The id of the character to retrieve. mode:  aiobungie.internal.enums.GameMode This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc. membership_type:  aiobungie.internal.enums.MembershipType The Member ship type, if nothing was passed than it will return all. page: typing.Optional[builtins.int] The page number limit: typing.Optional[builtins.int] Limit the returned result. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the player's activities. Raises     aiobungie.error.ActivityNotFound The activity was not found.  aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_post_activity",
"url":26,
"doc":"Fetch a post activity details.  warning This http request is not implemented yet and it will raise  NotImplementedError Parameters      instance:  builtins.int The activity instance id. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the post activity.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_vendor_sales",
"url":26,
"doc":"",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_profile",
"url":26,
"doc":"Fetche a bungie profile. Parameters      memberid:  builtins.int The member's id. type:  aiobungie.MembershipType A valid membership type. Returns      ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the found profile. Raises     aiobungie.MembershipTypeError The provided membership type was invalid.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_entity",
"url":26,
"doc":"",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_inventory_item",
"url":26,
"doc":"Fetch a static inventory item entity given a its hash. Parameters      type:  builtins.str Entity's type definition. hash:  builtins.int Entity's hash. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON array object of the inventory item.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_clan_members",
"url":26,
"doc":"Fetch all Bungie Clan members. Parameters      clan_id :  builsins.int The clans id type :  aiobungie.MembershipType An optional clan member's membership type. Default is set to  aiobungie.MembershipType.NONE Which returns the first matched clan member by their name. name :  builtins.str This parameter is only provided here to keep the signature with the main client implementation, Which only works with the non-rest clients. It returns a specific clan member by their name. Returns    -  ResponseSig[aiobungie.internal.helpers.JsonArray] A JSON array of clan members. Raises     aiobungie.ClanNotFound The clan was not found.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_hard_linked",
"url":26,
"doc":"Gets any hard linked membership given a credential. Only works for credentials that are public just  aiobungie.CredentialType.STEAMID right now. Cross Save aware. Parameters      credential:  builtins.int A valid SteamID64 type:  aiobungie.CredentialType The crededntial type. This must not be changed Since its only credential that works \"currently\" Returns    -  ResponseSig[aiobungie.internal.helpers.JsonObject] A JSON object of the found user hard linked types.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_manifest_path",
"url":26,
"doc":"Return a string of the bungie manifest database url. Returns    -  builtins.str A downloadable url for the bungie manifest database.",
"func":1
},
{
"ref":"aiobungie.rest.RESTClient.fetch_manifest",
"url":26,
"doc":"Access The bungie Manifest. Returns    -  builtins.bytes The bytes to read and write the manifest database.",
"func":1
},
{
"ref":"aiobungie.url",
"url":27,
"doc":"Bungie API endpoint urls."
},
{
"ref":"aiobungie.url.BASE",
"url":27,
"doc":"Base bungie url"
},
{
"ref":"aiobungie.url.REST_EP",
"url":27,
"doc":"REST API endpoint"
},
{
"ref":"aiobungie.url.OAUTH_EP",
"url":27,
"doc":"OAuth endpoint"
},
{
"ref":"aiobungie.url.TOKEN_EP",
"url":27,
"doc":"OAuth token endpoint"
}
]