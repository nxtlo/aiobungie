URLS=[
"aiobungie/index.html",
"aiobungie/client.html",
"aiobungie/crate/index.html",
"aiobungie/crate/user.html",
"aiobungie/crate/character.html",
"aiobungie/crate/profile.html",
"aiobungie/crate/entity.html",
"aiobungie/crate/activity.html",
"aiobungie/crate/application.html",
"aiobungie/crate/clans.html",
"aiobungie/crate/player.html",
"aiobungie/crate/season.html",
"aiobungie/error.html",
"aiobungie/ext/index.html",
"aiobungie/ext/meta.html",
"aiobungie/http.html",
"aiobungie/internal/index.html",
"aiobungie/internal/assets.html",
"aiobungie/internal/db.html",
"aiobungie/internal/enums.html",
"aiobungie/internal/helpers.html",
"aiobungie/internal/impl.html",
"aiobungie/internal/serialize.html",
"aiobungie/internal/time.html",
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
"doc":"Represents a client that connects to the Bungie API Attributes      - token:  builtins.str Your Bungie's API key or Token from the developer's portal. loop:  asyncio.AbstractEventLoop asyncio event loop."
},
{
"ref":"aiobungie.Client.serialize",
"url":0,
"doc":""
},
{
"ref":"aiobungie.Client.rest",
"url":0,
"doc":"Returns resful of the client instance for other requests."
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
"doc":"Raw http search given a valid bungie endpoint. Parameters      path:  builtins.str The bungie endpoint or path. A path must look something like this \"Destiny2/3/Profile/46111239123/ .\" Returns    -  typing.Any Any object.",
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
"doc":"Fetches a Bungie user by their name. Parameters      name:  builtins.str The user name. position:  builtins.int The user position/index in the list to return, Will returns the first one if not specified. Raises     aiobungie.error.UserNotFound The user wasa not found.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_user_from_id",
"url":0,
"doc":"Fetches a Bungie user by their id. Parameters      id:  builtins.int The user id. position:  builtins.int The user position/index in the list to return, Will returns the first one if not specified. Raises     aiobungie.error.UserNotFound The user wasa not found.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_hard_types",
"url":0,
"doc":"Gets any hard linked membership given a credential. Only works for credentials that are public just STEAMID from  aiobungie.CredentialType right now. Cross Save aware. Parameters      credential:  builtins.int A valid SteamID64 type:  aiobungie.CredentialType The crededntial type. This must not be changed Since its only credential that works \"currently\" Returns    -  aiobungie.crate.user.HardLinkedMembership Information about the hard linked data.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_profile",
"url":0,
"doc":"Fetches a bungie profile. See  aiobungie.crate.Profile to access other components. Paramaters      memberid:  builtins.int The member's id. type:  aiobungie.MembershipType A valid membership type. Returns      aiobungie.crate.Profile An aiobungie member profile.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_player",
"url":0,
"doc":"Fetches a Destiny2 Player. Parameters      - name:  builtins.str The Player's Name type:  aiobungie.internal.enums.MembershipType The player's membership type, e,g. XBOX, STEAM, PSN position:  builtins.int Which player position to return, first player will return if None. Returns      aiobungie.crate.Player An aiobungie Destiny 2 Player crate",
"func":1
},
{
"ref":"aiobungie.Client.fetch_character",
"url":0,
"doc":"Fetches a Destiny 2 character. Parameters      memberid:  builtins.int A valid bungie member id. character:  aiobungie.internal.enums.Class The Destiny character to retrieve. type:  aiobungie.internal.enums.MembershipType The member's membership type. Returns    -  aiobungie.crate.Character An aiobungie character crate. Raises     aiobungie.error.CharacterError raised if the Character was not found.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_vendor_sales",
"url":0,
"doc":"Fetch vendor sales.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_activity",
"url":0,
"doc":"Fetches a Destiny 2 activity for the specified user id and character. Parameters      member_id:  builtins.int The user id that starts with  4611 . character_id:  builtins.int The id of the character to retrieve. mode:  aiobungie.internal.enums.GameMode This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc. membership_type:  aiobungie.internal.enums.MembershipType The Member ship type, if nothing was passed than it will return all. page: typing.Optional[builtins.int] The page number limit: typing.Optional[builtins.int] Limit the returned result. Returns    -  aiobungie.crate.Activity An aiobungie Activity crate. Raises     aiobungie.error.ActivityNotFound The activity was not found.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_post_activity",
"url":0,
"doc":"Fetchs a post activity details. Parameters      instance:  builtins.int The activity instance id. Returns    -  aiobungie.crate.activity.PostActivity Information about the requested post activity.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_app",
"url":0,
"doc":"Fetches a Bungie Application. Parameters      - appid:  builtins.int The application id. Returns      aiobungie.crate.Application An aiobungie application crate.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_clan_from_id",
"url":0,
"doc":"Fetches a Bungie Clan by its id. Parameters      - id:  builtins.int The clan id. Returns      aiobungie.crate.Clan An aioungie clan crate",
"func":1
},
{
"ref":"aiobungie.Client.fetch_clan",
"url":0,
"doc":"Fetches a Clan by its name and returns the first result. Parameters      name:  builtins.str The clan name type  builtins.int The group type, Default is one. Returns    -  aiobungie.crate.Clan An aiobungie clan crate.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_clan_member",
"url":0,
"doc":"",
"func":1
},
{
"ref":"aiobungie.Client.fetch_clan_members",
"url":0,
"doc":"",
"func":1
},
{
"ref":"aiobungie.Client.fetch_inventory_item",
"url":0,
"doc":"Fetches a static inventory item entity given a its hash. Paramaters      type:  builtins.str Entity's type definition. hash:  builtins.int Entity's hash. Returns    -  aiobungie.crate.InventoryEntity A bungie inventory item.",
"func":1
},
{
"ref":"aiobungie.Client.http",
"url":0,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.Client.loop",
"url":0,
"doc":"Return an attribute of instance, which is of type owner."
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
"doc":"Exception for handling  aiobungie.http.HTTPClient requests errors. Method generated by attrs for class HTTPException."
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
"ref":"aiobungie.Component.CHARECTERS",
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
"doc":"The types of the accounts system suports at bungie."
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
"ref":"aiobungie.client",
"url":1,
"doc":"The base aiobungie Client that your should inherit from / use."
},
{
"ref":"aiobungie.client.Client",
"url":1,
"doc":"Represents a client that connects to the Bungie API Attributes      - token:  builtins.str Your Bungie's API key or Token from the developer's portal. loop:  asyncio.AbstractEventLoop asyncio event loop."
},
{
"ref":"aiobungie.client.Client.serialize",
"url":1,
"doc":""
},
{
"ref":"aiobungie.client.Client.rest",
"url":1,
"doc":"Returns resful of the client instance for other requests."
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
"doc":"Raw http search given a valid bungie endpoint. Parameters      path:  builtins.str The bungie endpoint or path. A path must look something like this \"Destiny2/3/Profile/46111239123/ .\" Returns    -  typing.Any Any object.",
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
"doc":"Fetches a Bungie user by their name. Parameters      name:  builtins.str The user name. position:  builtins.int The user position/index in the list to return, Will returns the first one if not specified. Raises     aiobungie.error.UserNotFound The user wasa not found.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_user_from_id",
"url":1,
"doc":"Fetches a Bungie user by their id. Parameters      id:  builtins.int The user id. position:  builtins.int The user position/index in the list to return, Will returns the first one if not specified. Raises     aiobungie.error.UserNotFound The user wasa not found.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_hard_types",
"url":1,
"doc":"Gets any hard linked membership given a credential. Only works for credentials that are public just STEAMID from  aiobungie.CredentialType right now. Cross Save aware. Parameters      credential:  builtins.int A valid SteamID64 type:  aiobungie.CredentialType The crededntial type. This must not be changed Since its only credential that works \"currently\" Returns    -  aiobungie.crate.user.HardLinkedMembership Information about the hard linked data.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_profile",
"url":1,
"doc":"Fetches a bungie profile. See  aiobungie.crate.Profile to access other components. Paramaters      memberid:  builtins.int The member's id. type:  aiobungie.MembershipType A valid membership type. Returns      aiobungie.crate.Profile An aiobungie member profile.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_player",
"url":1,
"doc":"Fetches a Destiny2 Player. Parameters      - name:  builtins.str The Player's Name type:  aiobungie.internal.enums.MembershipType The player's membership type, e,g. XBOX, STEAM, PSN position:  builtins.int Which player position to return, first player will return if None. Returns      aiobungie.crate.Player An aiobungie Destiny 2 Player crate",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_character",
"url":1,
"doc":"Fetches a Destiny 2 character. Parameters      memberid:  builtins.int A valid bungie member id. character:  aiobungie.internal.enums.Class The Destiny character to retrieve. type:  aiobungie.internal.enums.MembershipType The member's membership type. Returns    -  aiobungie.crate.Character An aiobungie character crate. Raises     aiobungie.error.CharacterError raised if the Character was not found.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_vendor_sales",
"url":1,
"doc":"Fetch vendor sales.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_activity",
"url":1,
"doc":"Fetches a Destiny 2 activity for the specified user id and character. Parameters      member_id:  builtins.int The user id that starts with  4611 . character_id:  builtins.int The id of the character to retrieve. mode:  aiobungie.internal.enums.GameMode This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc. membership_type:  aiobungie.internal.enums.MembershipType The Member ship type, if nothing was passed than it will return all. page: typing.Optional[builtins.int] The page number limit: typing.Optional[builtins.int] Limit the returned result. Returns    -  aiobungie.crate.Activity An aiobungie Activity crate. Raises     aiobungie.error.ActivityNotFound The activity was not found.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_post_activity",
"url":1,
"doc":"Fetchs a post activity details. Parameters      instance:  builtins.int The activity instance id. Returns    -  aiobungie.crate.activity.PostActivity Information about the requested post activity.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_app",
"url":1,
"doc":"Fetches a Bungie Application. Parameters      - appid:  builtins.int The application id. Returns      aiobungie.crate.Application An aiobungie application crate.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_clan_from_id",
"url":1,
"doc":"Fetches a Bungie Clan by its id. Parameters      - id:  builtins.int The clan id. Returns      aiobungie.crate.Clan An aioungie clan crate",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_clan",
"url":1,
"doc":"Fetches a Clan by its name and returns the first result. Parameters      name:  builtins.str The clan name type  builtins.int The group type, Default is one. Returns    -  aiobungie.crate.Clan An aiobungie clan crate.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_clan_member",
"url":1,
"doc":"",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_clan_members",
"url":1,
"doc":"",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_inventory_item",
"url":1,
"doc":"Fetches a static inventory item entity given a its hash. Paramaters      type:  builtins.str Entity's type definition. hash:  builtins.int Entity's hash. Returns    -  aiobungie.crate.InventoryEntity A bungie inventory item.",
"func":1
},
{
"ref":"aiobungie.client.Client.http",
"url":1,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.client.Client.loop",
"url":1,
"doc":"Return an attribute of instance, which is of type owner."
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
"ref":"aiobungie.crate.Application.human_timedelta",
"url":2,
"doc":"Returns a human readble date of the app's creation date."
},
{
"ref":"aiobungie.crate.Application.as_dict",
"url":2,
"doc":"Returns a dict crate of the application, This function is useful if you're binding to other REST apis."
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
"doc":"The post activity's memebership type."
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
"doc":"The postt activity starting phase index. for an example if it was 0 that means it's a fresh run"
},
{
"ref":"aiobungie.crate.Clan",
"url":2,
"doc":"Represents a Bungie clan. Method generated by attrs for class Clan."
},
{
"ref":"aiobungie.crate.Clan.fetch_member",
"url":2,
"doc":"Fetch a specific clan member by their name and membership type. if the memberhship type is None we will try to return the first member matches the name. its also better to leave this parameter on None since usually only one player has this name. Parameters      name:  builtins.str The clan member name. type:  aiobungie.MembershipType The member's membership type. Default is 0 which returns any member matches the name. Returns      ClanMember ",
"func":1
},
{
"ref":"aiobungie.crate.Clan.fetch_members",
"url":2,
"doc":"Fetch the members of the clan. if the memberhship type is None it will All membership types. Parameters      type:  aiobungie.MembershipType Filters the membership types to return. Default is 0 which returns all membership types. Returns     typing.Dict[str, tuple[int, aiobungie.MembershipType The clan members in this clan, Represented as a dict of the member name to a tuple of the member id and membership type object.",
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
"ref":"aiobungie.crate.Clan.human_timedelta",
"url":2,
"doc":"Returns a human readble date of the clan's creation date."
},
{
"ref":"aiobungie.crate.Clan.url",
"url":2,
"doc":""
},
{
"ref":"aiobungie.crate.Clan.as_dict",
"url":2,
"doc":"Returns an instance of the clan as a dict"
},
{
"ref":"aiobungie.crate.Clan.about",
"url":2,
"doc":"Clan's about title."
},
{
"ref":"aiobungie.crate.Clan.app",
"url":2,
"doc":"A client app the we may use for external requests."
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
"ref":"aiobungie.crate.Clan.description",
"url":2,
"doc":"Clan's description"
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
"ref":"aiobungie.crate.Clan.name",
"url":2,
"doc":"The clan's name"
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
"ref":"aiobungie.crate.Player.as_dict",
"url":2,
"doc":"Returns a dict object of the player."
},
{
"ref":"aiobungie.crate.Player.app",
"url":2,
"doc":"A client app that we may use for external requests."
},
{
"ref":"aiobungie.crate.Player.icon",
"url":2,
"doc":"The player's icon."
},
{
"ref":"aiobungie.crate.Player.id",
"url":2,
"doc":"The player's id."
},
{
"ref":"aiobungie.crate.Player.is_public",
"url":2,
"doc":"The player's profile privacy."
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
"ref":"aiobungie.crate.Player.link",
"url":3,
"doc":"Returns the user's profile link."
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
"ref":"aiobungie.crate.Character.as_dict",
"url":2,
"doc":"Returns a dict crate of the character."
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
"ref":"aiobungie.crate.Character.human_timedelta",
"url":4,
"doc":"The player's last played time in a human readble date."
},
{
"ref":"aiobungie.crate.CharacterComponent",
"url":2,
"doc":"An interface for a Bungie character component. Method generated by attrs for class CharacterComponent."
},
{
"ref":"aiobungie.crate.CharacterComponent.member_type",
"url":2,
"doc":"The character's membership type."
},
{
"ref":"aiobungie.crate.CharacterComponent.id",
"url":2,
"doc":"The character's member id."
},
{
"ref":"aiobungie.crate.CharacterComponent.light",
"url":2,
"doc":"The character's light."
},
{
"ref":"aiobungie.crate.CharacterComponent.stats",
"url":2,
"doc":"The character's stats."
},
{
"ref":"aiobungie.crate.CharacterComponent.url",
"url":2,
"doc":"The character's url at bungie.net."
},
{
"ref":"aiobungie.crate.CharacterComponent.emblem",
"url":2,
"doc":"The character's current equipped emblem."
},
{
"ref":"aiobungie.crate.CharacterComponent.last_played",
"url":2,
"doc":"The character's last played time."
},
{
"ref":"aiobungie.crate.CharacterComponent.emblem_icon",
"url":2,
"doc":"The character's current equipped emblem icon."
},
{
"ref":"aiobungie.crate.CharacterComponent.emblem_hash",
"url":2,
"doc":"The character's current equipped emblem hash."
},
{
"ref":"aiobungie.crate.CharacterComponent.race",
"url":2,
"doc":"The character's race."
},
{
"ref":"aiobungie.crate.CharacterComponent.gender",
"url":2,
"doc":"The character's gender."
},
{
"ref":"aiobungie.crate.CharacterComponent.total_played_time",
"url":2,
"doc":"Character's total played time in hours."
},
{
"ref":"aiobungie.crate.CharacterComponent.class_type",
"url":2,
"doc":"The character's class."
},
{
"ref":"aiobungie.crate.CharacterComponent.title_hash",
"url":2,
"doc":"The character's title hash. This is Optional and can be None if no title was found."
},
{
"ref":"aiobungie.crate.CharacterComponent.equip",
"url":2,
"doc":"Equip an item to this character. This requires the OAuth2: MoveEquipDestinyItems scope. Also You must have a valid Destiny account, and either be in a social space, in orbit or offline. Parameters      item:  builtins.int The item id you want to equip for this character. Returns    -  builtins.None . Raises     NotImplementedError This endpoint is currently not implemented.",
"func":1
},
{
"ref":"aiobungie.crate.CharacterComponent.equip_items",
"url":2,
"doc":"Equip multiple items to this character. This requires the OAuth2: MoveEquipDestinyItems scope. Also You must have a valid Destiny account, and either be in a social space, in orbit or offline. Parameters      items:  typing.List[builtins.int] A list of item ids you want to equip for this character. Returns    -  builtins.None . Raises     NotImplementedError This endpoint is currently not implemented.",
"func":1
},
{
"ref":"aiobungie.crate.CharacterComponent.human_timedelta",
"url":2,
"doc":"The player's last played time in a human readble date."
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
"ref":"aiobungie.crate.Activity.as_dict",
"url":2,
"doc":"Returns a dict crate of the Activity, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.crate.Activity.app",
"url":2,
"doc":"A client app that we may use to make external calls."
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
"ref":"aiobungie.crate.Activity.id",
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
"doc":"Represents Bungie user. Method generated by attrs for class User."
},
{
"ref":"aiobungie.crate.User.as_dict",
"url":2,
"doc":"Returns a dict object of the user."
},
{
"ref":"aiobungie.crate.User.about",
"url":2,
"doc":"The user's about, Default is None if nothing is Found."
},
{
"ref":"aiobungie.crate.User.blizzard_name",
"url":2,
"doc":"The user's blizzard name if it exists."
},
{
"ref":"aiobungie.crate.User.created_at",
"url":2,
"doc":"The user's creation date in UTC timezone."
},
{
"ref":"aiobungie.crate.User.id",
"url":2,
"doc":"The user's id"
},
{
"ref":"aiobungie.crate.User.is_deleted",
"url":2,
"doc":"Returns True if the user is deleted"
},
{
"ref":"aiobungie.crate.User.locale",
"url":2,
"doc":"The user's locale."
},
{
"ref":"aiobungie.crate.User.name",
"url":2,
"doc":"The user's name."
},
{
"ref":"aiobungie.crate.User.picture",
"url":2,
"doc":"The user's profile picture."
},
{
"ref":"aiobungie.crate.User.psn_name",
"url":2,
"doc":"The user's psn id if it exists."
},
{
"ref":"aiobungie.crate.User.status",
"url":2,
"doc":"The user's bungie status text"
},
{
"ref":"aiobungie.crate.User.steam_name",
"url":2,
"doc":"The user's steam name if it exists"
},
{
"ref":"aiobungie.crate.User.twitch_name",
"url":2,
"doc":"The user's twitch name if it exists."
},
{
"ref":"aiobungie.crate.User.updated_at",
"url":2,
"doc":"The user's last updated om UTC date."
},
{
"ref":"aiobungie.crate.ClanOwner",
"url":2,
"doc":"Represents a Bungie clan owner. Method generated by attrs for class ClanOwner."
},
{
"ref":"aiobungie.crate.ClanOwner.app",
"url":2,
"doc":"A client app that we may use for external requests."
},
{
"ref":"aiobungie.crate.ClanOwner.human_timedelta",
"url":2,
"doc":"Returns a human readble date of the clan owner's last login."
},
{
"ref":"aiobungie.crate.ClanOwner.link",
"url":2,
"doc":"Returns the user's profile link."
},
{
"ref":"aiobungie.crate.ClanOwner.as_dict",
"url":2,
"doc":"Returns a dict object of the clan owner, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.crate.ClanOwner.clan_id",
"url":2,
"doc":"Owner's current clan id."
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
"ref":"aiobungie.crate.ClanMember.app",
"url":2,
"doc":"A client app that we may use for external requests."
},
{
"ref":"aiobungie.crate.ClanMember.link",
"url":2,
"doc":"Clan member's profile link."
},
{
"ref":"aiobungie.crate.ClanMember.as_dict",
"url":2,
"doc":"Returns an instance of the UserLike as a dict."
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
"ref":"aiobungie.crate.ClanMember.name",
"url":2,
"doc":"Clan member's name"
},
{
"ref":"aiobungie.crate.ClanMember.type",
"url":2,
"doc":"Clan member's membership type."
},
{
"ref":"aiobungie.crate.ApplicationOwner",
"url":2,
"doc":"Represents a Bungie Application owner. Method generated by attrs for class ApplicationOwner."
},
{
"ref":"aiobungie.crate.ApplicationOwner.app",
"url":2,
"doc":"A client app that we may use for external requests."
},
{
"ref":"aiobungie.crate.ApplicationOwner.link",
"url":2,
"doc":"Returns the user's profile link."
},
{
"ref":"aiobungie.crate.ApplicationOwner.as_dict",
"url":2,
"doc":"Returns a dict object of the application owner."
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
"doc":"The application owner name."
},
{
"ref":"aiobungie.crate.ApplicationOwner.type",
"url":2,
"doc":"The membership of the application owner."
},
{
"ref":"aiobungie.crate.Profile",
"url":2,
"doc":"Represents a Bungie member Profile. Bungie profiles requires components. but in aiobungie you don't need to select a specific component since they will all/will be implemented. for an example: to access the  Character component you'll need to pass  ?component=200 right?. in aiobungie you can just do this.   profile = await client.fetch_profile(\"Fate\")  access the character component and get my warlock. warlock = await profile.warlock() assert warlock.light  1320   Method generated by attrs for class Profile."
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
"ref":"aiobungie.crate.Profile.as_dict",
"url":2,
"doc":"Returns a dict object of the profile."
},
{
"ref":"aiobungie.crate.Profile.human_timedelta",
"url":2,
"doc":"Returns last_played attr but in human delta date."
},
{
"ref":"aiobungie.crate.Profile.app",
"url":2,
"doc":"A client that we may to make rest requests."
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
"ref":"aiobungie.crate.InventoryEntity.app",
"url":2,
"doc":"A client that we may use to make rest calls."
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
"doc":"The entity's lore hash"
},
{
"ref":"aiobungie.crate.InventoryEntity.name",
"url":2,
"doc":"Entity's name"
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
"doc":"Entity's type."
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
"ref":"aiobungie.crate.InventoryEntity.as_dict",
"url":6,
"doc":"Returns an instance of the entity as a dict"
},
{
"ref":"aiobungie.crate.UserLike",
"url":2,
"doc":"The is meant for any Member / user / like crate. Method generated by attrs for class UserLike."
},
{
"ref":"aiobungie.crate.UserLike.app",
"url":2,
"doc":"A client app that we may use for external requests."
},
{
"ref":"aiobungie.crate.UserLike.name",
"url":2,
"doc":"The user's name."
},
{
"ref":"aiobungie.crate.UserLike.is_public",
"url":2,
"doc":"Returns if the user profile is public or no."
},
{
"ref":"aiobungie.crate.UserLike.type",
"url":2,
"doc":"Returns the user type of the user."
},
{
"ref":"aiobungie.crate.UserLike.icon",
"url":2,
"doc":"The user's icon."
},
{
"ref":"aiobungie.crate.UserLike.link",
"url":2,
"doc":"Returns the user's profile link."
},
{
"ref":"aiobungie.crate.UserLike.as_dict",
"url":2,
"doc":"Returns an instance of the UserLike as a dict."
},
{
"ref":"aiobungie.crate.ProfileComponentImpl",
"url":2,
"doc":"A partial interface that will/include all bungie profile components. Some fields may or may not be available here. Method generated by attrs for class ProfileComponentImpl."
},
{
"ref":"aiobungie.crate.ProfileComponentImpl.app",
"url":2,
"doc":"A client that we may to make rest requests."
},
{
"ref":"aiobungie.crate.ProfileComponentImpl.name",
"url":2,
"doc":"Profile's name"
},
{
"ref":"aiobungie.crate.ProfileComponentImpl.type",
"url":2,
"doc":"Profile's membership type."
},
{
"ref":"aiobungie.crate.ProfileComponentImpl.last_played",
"url":2,
"doc":"The profile user's last played date time."
},
{
"ref":"aiobungie.crate.ProfileComponentImpl.is_public",
"url":2,
"doc":"Profile's privacy status."
},
{
"ref":"aiobungie.crate.ProfileComponentImpl.character_ids",
"url":2,
"doc":"A list of the profile's character ids."
},
{
"ref":"aiobungie.crate.ProfileComponentImpl.id",
"url":2,
"doc":"The profile's id."
},
{
"ref":"aiobungie.crate.ProfileComponentImpl.titan",
"url":2,
"doc":"Returns the titan character of the profile owner.",
"func":1
},
{
"ref":"aiobungie.crate.ProfileComponentImpl.hunter",
"url":2,
"doc":"Returns the hunter character of the profile owner.",
"func":1
},
{
"ref":"aiobungie.crate.ProfileComponentImpl.warlock",
"url":2,
"doc":"Returns the Warlock character of the profile owner.",
"func":1
},
{
"ref":"aiobungie.crate.Entity",
"url":2,
"doc":"An Implementation of a Bungie Item Definition Entity. This is the main entity which all other entities should inherit from. it holds general information that all bungie entities has. Method generated by attrs for class Entity."
},
{
"ref":"aiobungie.crate.Entity.app",
"url":2,
"doc":"A client that we may use to make rest calls."
},
{
"ref":"aiobungie.crate.Entity.name",
"url":2,
"doc":"Entity's name"
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
"ref":"aiobungie.crate.Entity.as_dict",
"url":2,
"doc":"Returns an instance of the entity as a dict"
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
"ref":"aiobungie.crate.activity",
"url":7,
"doc":"Basic implementation for a Bungie a activity. NOTE that this is still under development ages, and you might face some major bugs."
},
{
"ref":"aiobungie.crate.activity.Activity",
"url":7,
"doc":"Represents a Bungie Activity. Method generated by attrs for class Activity."
},
{
"ref":"aiobungie.crate.activity.Activity.post_report",
"url":7,
"doc":"Get activity's data after its finished. Returns    -  .PostActivity ",
"func":1
},
{
"ref":"aiobungie.crate.activity.Activity.as_dict",
"url":7,
"doc":"Returns a dict crate of the Activity, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.crate.activity.Activity.app",
"url":7,
"doc":"A client app that we may use to make external calls."
},
{
"ref":"aiobungie.crate.activity.Activity.assists",
"url":7,
"doc":"Activity's assists"
},
{
"ref":"aiobungie.crate.activity.Activity.completion_reason",
"url":7,
"doc":"The reason why the activity was completed. usually its Unknown."
},
{
"ref":"aiobungie.crate.activity.Activity.deaths",
"url":7,
"doc":"Activity's deaths."
},
{
"ref":"aiobungie.crate.activity.Activity.duration",
"url":7,
"doc":"A string of The activity's duration, Example format  7m 42s "
},
{
"ref":"aiobungie.crate.activity.Activity.efficiency",
"url":7,
"doc":"Activity's efficienty."
},
{
"ref":"aiobungie.crate.activity.Activity.id",
"url":7,
"doc":"The activity's hash."
},
{
"ref":"aiobungie.crate.activity.Activity.instance_id",
"url":7,
"doc":"The activity's instance id."
},
{
"ref":"aiobungie.crate.activity.Activity.is_completed",
"url":7,
"doc":"Check if the activity was completed or no."
},
{
"ref":"aiobungie.crate.activity.Activity.kd",
"url":7,
"doc":"Activity's kill/death ratio."
},
{
"ref":"aiobungie.crate.activity.Activity.kills",
"url":7,
"doc":"Activity's kills."
},
{
"ref":"aiobungie.crate.activity.Activity.member_type",
"url":7,
"doc":"The activity player's membership type."
},
{
"ref":"aiobungie.crate.activity.Activity.mode",
"url":7,
"doc":"The activity mode or type."
},
{
"ref":"aiobungie.crate.activity.Activity.modes",
"url":7,
"doc":"A list of the post activity's game mode."
},
{
"ref":"aiobungie.crate.activity.Activity.opponents_defeated",
"url":7,
"doc":"Activity's opponents kills."
},
{
"ref":"aiobungie.crate.activity.Activity.period",
"url":7,
"doc":"When did the activity occurred in UTC datetime."
},
{
"ref":"aiobungie.crate.activity.Activity.player_count",
"url":7,
"doc":"Activity's player count."
},
{
"ref":"aiobungie.crate.activity.Activity.score",
"url":7,
"doc":"Activity's score."
},
{
"ref":"aiobungie.crate.activity.PostActivity",
"url":7,
"doc":"Represents a Destiny 2 post activity details. Method generated by attrs for class PostActivity."
},
{
"ref":"aiobungie.crate.activity.PostActivity.get_players",
"url":7,
"doc":"Returns a sequence of the players that were in this activity. Returns    -  typing.Sequence[aiobungie.crate.Player] the players that were in this activity.",
"func":1
},
{
"ref":"aiobungie.crate.activity.PostActivity.is_fresh",
"url":7,
"doc":"Determines if the activity was fresh or no."
},
{
"ref":"aiobungie.crate.activity.PostActivity.membership_type",
"url":7,
"doc":"The post activity's memebership type."
},
{
"ref":"aiobungie.crate.activity.PostActivity.mode",
"url":7,
"doc":"The post activity's game mode, Can be  Undefined if unknown."
},
{
"ref":"aiobungie.crate.activity.PostActivity.modes",
"url":7,
"doc":"A list of the post activity's game mode."
},
{
"ref":"aiobungie.crate.activity.PostActivity.period",
"url":7,
"doc":"The post activity's period utc date."
},
{
"ref":"aiobungie.crate.activity.PostActivity.players",
"url":7,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.crate.activity.PostActivity.reference_id",
"url":7,
"doc":"The post activity reference id. AKA the activity hash."
},
{
"ref":"aiobungie.crate.activity.PostActivity.starting_phase",
"url":7,
"doc":"The postt activity starting phase index. for an example if it was 0 that means it's a fresh run"
},
{
"ref":"aiobungie.crate.application",
"url":8,
"doc":"Basic implementation for a Bungie a application."
},
{
"ref":"aiobungie.crate.application.Application",
"url":8,
"doc":"Represents a Bungie developer application. Method generated by attrs for class Application."
},
{
"ref":"aiobungie.crate.application.Application.human_timedelta",
"url":8,
"doc":"Returns a human readble date of the app's creation date."
},
{
"ref":"aiobungie.crate.application.Application.as_dict",
"url":8,
"doc":"Returns a dict crate of the application, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.crate.application.Application.created_at",
"url":8,
"doc":"App creation date in UTC timezone"
},
{
"ref":"aiobungie.crate.application.Application.id",
"url":8,
"doc":"App id"
},
{
"ref":"aiobungie.crate.application.Application.link",
"url":8,
"doc":"App's link"
},
{
"ref":"aiobungie.crate.application.Application.name",
"url":8,
"doc":"App name"
},
{
"ref":"aiobungie.crate.application.Application.owner",
"url":8,
"doc":"App's owner"
},
{
"ref":"aiobungie.crate.application.Application.published_at",
"url":8,
"doc":"App's publish date in UTC timezone"
},
{
"ref":"aiobungie.crate.application.Application.redirect_url",
"url":8,
"doc":"App redirect url"
},
{
"ref":"aiobungie.crate.application.Application.scope",
"url":8,
"doc":"App's scope"
},
{
"ref":"aiobungie.crate.application.Application.status",
"url":8,
"doc":"App's status"
},
{
"ref":"aiobungie.crate.application.ApplicationOwner",
"url":8,
"doc":"Represents a Bungie Application owner. Method generated by attrs for class ApplicationOwner."
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.app",
"url":8,
"doc":"A client app that we may use for external requests."
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.link",
"url":8,
"doc":"Returns the user's profile link."
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.as_dict",
"url":8,
"doc":"Returns a dict object of the application owner."
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.icon",
"url":8,
"doc":"The application owner's icon."
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.id",
"url":8,
"doc":"The application owner's id."
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.is_public",
"url":8,
"doc":"The application owner's profile privacy."
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.name",
"url":8,
"doc":"The application owner name."
},
{
"ref":"aiobungie.crate.application.ApplicationOwner.type",
"url":8,
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
"doc":"An interface for a Bungie character component. Method generated by attrs for class CharacterComponent."
},
{
"ref":"aiobungie.crate.character.CharacterComponent.member_type",
"url":4,
"doc":"The character's membership type."
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
"ref":"aiobungie.crate.character.CharacterComponent.human_timedelta",
"url":4,
"doc":"The player's last played time in a human readble date."
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
"ref":"aiobungie.crate.character.Character.as_dict",
"url":4,
"doc":"Returns a dict crate of the character."
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
"ref":"aiobungie.crate.character.Character.human_timedelta",
"url":4,
"doc":"The player's last played time in a human readble date."
},
{
"ref":"aiobungie.crate.clans",
"url":9,
"doc":"Basic implementation for a Bungie a clan."
},
{
"ref":"aiobungie.crate.clans.Clan",
"url":9,
"doc":"Represents a Bungie clan. Method generated by attrs for class Clan."
},
{
"ref":"aiobungie.crate.clans.Clan.fetch_member",
"url":9,
"doc":"Fetch a specific clan member by their name and membership type. if the memberhship type is None we will try to return the first member matches the name. its also better to leave this parameter on None since usually only one player has this name. Parameters      name:  builtins.str The clan member name. type:  aiobungie.MembershipType The member's membership type. Default is 0 which returns any member matches the name. Returns      ClanMember ",
"func":1
},
{
"ref":"aiobungie.crate.clans.Clan.fetch_members",
"url":9,
"doc":"Fetch the members of the clan. if the memberhship type is None it will All membership types. Parameters      type:  aiobungie.MembershipType Filters the membership types to return. Default is 0 which returns all membership types. Returns     typing.Dict[str, tuple[int, aiobungie.MembershipType The clan members in this clan, Represented as a dict of the member name to a tuple of the member id and membership type object.",
"func":1
},
{
"ref":"aiobungie.crate.clans.Clan.fetch_banned_members",
"url":9,
"doc":"Fetch members who has been banned from the clan. Returns      typing.Sequence[aiobungie.crate.clans.ClanMember] A sequence of clan members or are banned.",
"func":1
},
{
"ref":"aiobungie.crate.clans.Clan.fetch_pending_members",
"url":9,
"doc":"Fetch members who are waiting to get accepted. Returns      typing.Sequence[aiobungie.crate.clans.ClanMember] A sequence of clan members who are awaiting to get accepted to the clan.",
"func":1
},
{
"ref":"aiobungie.crate.clans.Clan.fetch_invited_members",
"url":9,
"doc":"Fetch members who has been invited. Returns      typing.Sequence[aiobungie.crate.clans.ClanMember] A sequence of members who have been invited.",
"func":1
},
{
"ref":"aiobungie.crate.clans.Clan.human_timedelta",
"url":9,
"doc":"Returns a human readble date of the clan's creation date."
},
{
"ref":"aiobungie.crate.clans.Clan.url",
"url":9,
"doc":""
},
{
"ref":"aiobungie.crate.clans.Clan.as_dict",
"url":9,
"doc":"Returns an instance of the clan as a dict"
},
{
"ref":"aiobungie.crate.clans.Clan.about",
"url":9,
"doc":"Clan's about title."
},
{
"ref":"aiobungie.crate.clans.Clan.app",
"url":9,
"doc":"A client app the we may use for external requests."
},
{
"ref":"aiobungie.crate.clans.Clan.avatar",
"url":9,
"doc":"Clan's avatar"
},
{
"ref":"aiobungie.crate.clans.Clan.banner",
"url":9,
"doc":"Clan's banner"
},
{
"ref":"aiobungie.crate.clans.Clan.created_at",
"url":9,
"doc":"Clan's creation date time in UTC."
},
{
"ref":"aiobungie.crate.clans.Clan.description",
"url":9,
"doc":"Clan's description"
},
{
"ref":"aiobungie.crate.clans.Clan.features",
"url":9,
"doc":"The clan features."
},
{
"ref":"aiobungie.crate.clans.Clan.id",
"url":9,
"doc":"The clan id"
},
{
"ref":"aiobungie.crate.clans.Clan.is_public",
"url":9,
"doc":"Clan's privacy status."
},
{
"ref":"aiobungie.crate.clans.Clan.member_count",
"url":9,
"doc":"Clan's member count."
},
{
"ref":"aiobungie.crate.clans.Clan.name",
"url":9,
"doc":"The clan's name"
},
{
"ref":"aiobungie.crate.clans.Clan.owner",
"url":9,
"doc":"The clan owner."
},
{
"ref":"aiobungie.crate.clans.Clan.tags",
"url":9,
"doc":"A list of the clan's tags."
},
{
"ref":"aiobungie.crate.clans.Clan.type",
"url":9,
"doc":"The clan type."
},
{
"ref":"aiobungie.crate.clans.ClanOwner",
"url":9,
"doc":"Represents a Bungie clan owner. Method generated by attrs for class ClanOwner."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.app",
"url":9,
"doc":"A client app that we may use for external requests."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.human_timedelta",
"url":9,
"doc":"Returns a human readble date of the clan owner's last login."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.link",
"url":9,
"doc":"Returns the user's profile link."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.as_dict",
"url":9,
"doc":"Returns a dict object of the clan owner, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.clan_id",
"url":9,
"doc":"Owner's current clan id."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.icon",
"url":9,
"doc":"Owner's profile icom"
},
{
"ref":"aiobungie.crate.clans.ClanOwner.id",
"url":9,
"doc":"The user id."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.is_public",
"url":9,
"doc":"Returns if the user profile is public or no."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.joined_at",
"url":9,
"doc":"Owner's bungie join date."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.last_online",
"url":9,
"doc":"An aware  datetime.datetime object of the user's last online date UTC."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.name",
"url":9,
"doc":"The user name."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.type",
"url":9,
"doc":"Returns the membership type of the user."
},
{
"ref":"aiobungie.crate.clans.ClanOwner.types",
"url":9,
"doc":"Returns a list of the member ship's membership types."
},
{
"ref":"aiobungie.crate.clans.ClanMember",
"url":9,
"doc":"Represents a Destiny 2 clan member. Method generated by attrs for class ClanMember."
},
{
"ref":"aiobungie.crate.clans.ClanMember.app",
"url":9,
"doc":"A client app that we may use for external requests."
},
{
"ref":"aiobungie.crate.clans.ClanMember.link",
"url":9,
"doc":"Clan member's profile link."
},
{
"ref":"aiobungie.crate.clans.ClanMember.as_dict",
"url":9,
"doc":"Returns an instance of the UserLike as a dict."
},
{
"ref":"aiobungie.crate.clans.ClanMember.ban",
"url":9,
"doc":"Bans a clan member from the clan. This requires OAuth2: AdminGroups scope.",
"func":1
},
{
"ref":"aiobungie.crate.clans.ClanMember.unban",
"url":9,
"doc":"Unbans a clan member clan. This requires OAuth2: AdminGroups scope.",
"func":1
},
{
"ref":"aiobungie.crate.clans.ClanMember.kick",
"url":9,
"doc":"Kicks a clan member from the clan. The requires OAuth2: AdminsGroup scope.",
"func":1
},
{
"ref":"aiobungie.crate.clans.ClanMember.group_id",
"url":9,
"doc":"The member's group id."
},
{
"ref":"aiobungie.crate.clans.ClanMember.icon",
"url":9,
"doc":"Clan member's icon"
},
{
"ref":"aiobungie.crate.clans.ClanMember.id",
"url":9,
"doc":"Clan member's id"
},
{
"ref":"aiobungie.crate.clans.ClanMember.is_online",
"url":9,
"doc":"True if the clan member is online or not."
},
{
"ref":"aiobungie.crate.clans.ClanMember.is_public",
"url":9,
"doc":" builtins.True if the clan member is public."
},
{
"ref":"aiobungie.crate.clans.ClanMember.joined_at",
"url":9,
"doc":"The clan member's join date in UTC time zone."
},
{
"ref":"aiobungie.crate.clans.ClanMember.last_online",
"url":9,
"doc":"The date of the clan member's last online in UTC time zone."
},
{
"ref":"aiobungie.crate.clans.ClanMember.name",
"url":9,
"doc":"Clan member's name"
},
{
"ref":"aiobungie.crate.clans.ClanMember.type",
"url":9,
"doc":"Clan member's membership type."
},
{
"ref":"aiobungie.crate.clans.ClanFeatures",
"url":9,
"doc":"Represents Bungie clan features. Method generated by attrs for class ClanFeatures."
},
{
"ref":"aiobungie.crate.clans.ClanFeatures.capabilities",
"url":9,
"doc":"An int that represents the clan's capabilities."
},
{
"ref":"aiobungie.crate.clans.ClanFeatures.invite_permissions",
"url":9,
"doc":"True if the clan has permissions to invite."
},
{
"ref":"aiobungie.crate.clans.ClanFeatures.join_level",
"url":9,
"doc":"The clan's join level."
},
{
"ref":"aiobungie.crate.clans.ClanFeatures.max_members",
"url":9,
"doc":"The maximum members the clan can have"
},
{
"ref":"aiobungie.crate.clans.ClanFeatures.max_membership_types",
"url":9,
"doc":"The maximum membership types the clan can have"
},
{
"ref":"aiobungie.crate.clans.ClanFeatures.membership_types",
"url":9,
"doc":"The clan's membership types."
},
{
"ref":"aiobungie.crate.clans.ClanFeatures.update_banner_permissions",
"url":9,
"doc":"True if the clan has permissions to updates its banner."
},
{
"ref":"aiobungie.crate.clans.ClanFeatures.update_culture_permissions",
"url":9,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.crate.entity",
"url":6,
"doc":"Bungie entity definitions implementation. This is still not fully implemented and you may experince bugs. This will include all Bungie Definitions."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity",
"url":6,
"doc":"Represents a bungie inventory item entity. This derives from  DestinyInventoryItemDefinition definition. Method generated by attrs for class InventoryEntity."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.about",
"url":6,
"doc":"Entity's about."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.ammo_type",
"url":6,
"doc":"Entity's ammo type if it was a wepon, otherwise it will return None"
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.app",
"url":6,
"doc":"A client that we may use to make rest calls."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.banner",
"url":6,
"doc":"Entity's banner."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.bucket_type",
"url":6,
"doc":"The entity's bucket type, None if unknown"
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.damage",
"url":6,
"doc":"Entity's damage type. Only works for weapons."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.description",
"url":6,
"doc":"Entity's description."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.has_icon",
"url":6,
"doc":"A boolean that returns True if the entity has an icon."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.hash",
"url":6,
"doc":"Entity's hash."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.icon",
"url":6,
"doc":"Entity's icon"
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.index",
"url":6,
"doc":"Entity's index."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.is_equippable",
"url":6,
"doc":"True if the entity can be equipped or False."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.item_class",
"url":6,
"doc":"The entity's class type."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.lore_hash",
"url":6,
"doc":"The entity's lore hash"
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.name",
"url":6,
"doc":"Entity's name"
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.stats",
"url":6,
"doc":"Entity's stats. this currently returns a dict object of the stats."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.sub_type",
"url":6,
"doc":"The subtype of the entity. A type is a weapon or armor. A subtype is a handcannonn or leg armor for an example."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.summary_hash",
"url":6,
"doc":"Entity's summary hash."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.tier",
"url":6,
"doc":"Entity's \"tier."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.tier_name",
"url":6,
"doc":"A string version of the item tier."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.type",
"url":6,
"doc":"Entity's type."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.type_name",
"url":6,
"doc":"Entity's type name. i.e.,  Grenade Launcher "
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.water_mark",
"url":6,
"doc":"Entity's water mark."
},
{
"ref":"aiobungie.crate.entity.InventoryEntity.as_dict",
"url":6,
"doc":"Returns an instance of the entity as a dict"
},
{
"ref":"aiobungie.crate.entity.Entity",
"url":6,
"doc":"An Implementation of a Bungie Item Definition Entity. This is the main entity which all other entities should inherit from. it holds general information that all bungie entities has. Method generated by attrs for class Entity."
},
{
"ref":"aiobungie.crate.entity.Entity.app",
"url":6,
"doc":"A client that we may use to make rest calls."
},
{
"ref":"aiobungie.crate.entity.Entity.name",
"url":6,
"doc":"Entity's name"
},
{
"ref":"aiobungie.crate.entity.Entity.icon",
"url":6,
"doc":"An optional entity's icon if its filled."
},
{
"ref":"aiobungie.crate.entity.Entity.has_icon",
"url":6,
"doc":"A boolean that returns True if the entity has an icon."
},
{
"ref":"aiobungie.crate.entity.Entity.description",
"url":6,
"doc":"Entity's description"
},
{
"ref":"aiobungie.crate.entity.Entity.index",
"url":6,
"doc":"The entity's index."
},
{
"ref":"aiobungie.crate.entity.Entity.hash",
"url":6,
"doc":"Entity's hash."
},
{
"ref":"aiobungie.crate.entity.Entity.as_dict",
"url":6,
"doc":"Returns an instance of the entity as a dict"
},
{
"ref":"aiobungie.crate.player",
"url":10,
"doc":"Basic implementation for a Bungie a player."
},
{
"ref":"aiobungie.crate.player.Player",
"url":10,
"doc":"Represents a Bungie Destiny 2 Player. Method generated by attrs for class Player."
},
{
"ref":"aiobungie.crate.player.Player.as_dict",
"url":10,
"doc":"Returns a dict object of the player."
},
{
"ref":"aiobungie.crate.player.Player.app",
"url":10,
"doc":"A client app that we may use for external requests."
},
{
"ref":"aiobungie.crate.player.Player.icon",
"url":10,
"doc":"The player's icon."
},
{
"ref":"aiobungie.crate.player.Player.id",
"url":10,
"doc":"The player's id."
},
{
"ref":"aiobungie.crate.player.Player.is_public",
"url":10,
"doc":"The player's profile privacy."
},
{
"ref":"aiobungie.crate.player.Player.name",
"url":10,
"doc":"The player's name"
},
{
"ref":"aiobungie.crate.player.Player.type",
"url":10,
"doc":"The profile's membership type."
},
{
"ref":"aiobungie.crate.player.Player.link",
"url":3,
"doc":"Returns the user's profile link."
},
{
"ref":"aiobungie.crate.profile",
"url":5,
"doc":"Implementation for a Bungie a Profile."
},
{
"ref":"aiobungie.crate.profile.Profile",
"url":5,
"doc":"Represents a Bungie member Profile. Bungie profiles requires components. but in aiobungie you don't need to select a specific component since they will all/will be implemented. for an example: to access the  Character component you'll need to pass  ?component=200 right?. in aiobungie you can just do this.   profile = await client.fetch_profile(\"Fate\")  access the character component and get my warlock. warlock = await profile.warlock() assert warlock.light  1320   Method generated by attrs for class Profile."
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
"ref":"aiobungie.crate.profile.Profile.as_dict",
"url":5,
"doc":"Returns a dict object of the profile."
},
{
"ref":"aiobungie.crate.profile.Profile.human_timedelta",
"url":5,
"doc":"Returns last_played attr but in human delta date."
},
{
"ref":"aiobungie.crate.profile.Profile.app",
"url":5,
"doc":"A client that we may to make rest requests."
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
"ref":"aiobungie.crate.profile.ProfileComponentImpl",
"url":5,
"doc":"A partial interface that will/include all bungie profile components. Some fields may or may not be available here. Method generated by attrs for class ProfileComponentImpl."
},
{
"ref":"aiobungie.crate.profile.ProfileComponentImpl.app",
"url":5,
"doc":"A client that we may to make rest requests."
},
{
"ref":"aiobungie.crate.profile.ProfileComponentImpl.name",
"url":5,
"doc":"Profile's name"
},
{
"ref":"aiobungie.crate.profile.ProfileComponentImpl.type",
"url":5,
"doc":"Profile's membership type."
},
{
"ref":"aiobungie.crate.profile.ProfileComponentImpl.last_played",
"url":5,
"doc":"The profile user's last played date time."
},
{
"ref":"aiobungie.crate.profile.ProfileComponentImpl.is_public",
"url":5,
"doc":"Profile's privacy status."
},
{
"ref":"aiobungie.crate.profile.ProfileComponentImpl.character_ids",
"url":5,
"doc":"A list of the profile's character ids."
},
{
"ref":"aiobungie.crate.profile.ProfileComponentImpl.id",
"url":5,
"doc":"The profile's id."
},
{
"ref":"aiobungie.crate.profile.ProfileComponentImpl.titan",
"url":5,
"doc":"Returns the titan character of the profile owner.",
"func":1
},
{
"ref":"aiobungie.crate.profile.ProfileComponentImpl.hunter",
"url":5,
"doc":"Returns the hunter character of the profile owner.",
"func":1
},
{
"ref":"aiobungie.crate.profile.ProfileComponentImpl.warlock",
"url":5,
"doc":"Returns the Warlock character of the profile owner.",
"func":1
},
{
"ref":"aiobungie.crate.season",
"url":11,
"doc":"A basic implementations of a destiny 2 season. This includes all season that can be found in a regular season i.e, season artifact, season content etc."
},
{
"ref":"aiobungie.crate.season.Artifact",
"url":11,
"doc":"Concrate interface of a Destiny 2 Season artifact. Method generated by attrs for class Artifact."
},
{
"ref":"aiobungie.crate.season.Artifact.acquired_points",
"url":11,
"doc":"The total acquired artifact points"
},
{
"ref":"aiobungie.crate.season.Artifact.app",
"url":11,
"doc":"A client app we may use to make external requests."
},
{
"ref":"aiobungie.crate.season.Artifact.bonus",
"url":11,
"doc":"Information about the artifact's power bonus."
},
{
"ref":"aiobungie.crate.season.Artifact.hash",
"url":11,
"doc":"The season artifact's hash."
},
{
"ref":"aiobungie.crate.season.Artifact.points",
"url":11,
"doc":"Information about the artifact's power points"
},
{
"ref":"aiobungie.crate.season.Artifact.power_bonus",
"url":11,
"doc":"Season artifact's power bonus."
},
{
"ref":"aiobungie.crate.season.PowerBonus",
"url":11,
"doc":"Represents a Destiny 2 artifact power bonus information. Method generated by attrs for class PowerBonus."
},
{
"ref":"aiobungie.crate.season.PowerBonus.cap",
"url":11,
"doc":"The cap of the power bonus."
},
{
"ref":"aiobungie.crate.season.PowerBonus.current_progress",
"url":11,
"doc":"Power bonus's current progress."
},
{
"ref":"aiobungie.crate.season.PowerBonus.daily_limit",
"url":11,
"doc":"Power bonus's daily limit."
},
{
"ref":"aiobungie.crate.season.PowerBonus.daily_progress",
"url":11,
"doc":"Power bonus's daily progress."
},
{
"ref":"aiobungie.crate.season.PowerBonus.level",
"url":11,
"doc":"Power bonus's current level aka The total earned bonus."
},
{
"ref":"aiobungie.crate.season.PowerBonus.needed",
"url":11,
"doc":"The needed progress to earn the next level."
},
{
"ref":"aiobungie.crate.season.PowerBonus.next_level",
"url":11,
"doc":"Power bonus's next level at."
},
{
"ref":"aiobungie.crate.season.PowerBonus.progression_hash",
"url":11,
"doc":"The hash of the power bonus."
},
{
"ref":"aiobungie.crate.season.PowerBonus.weekly_limit",
"url":11,
"doc":"Power bonus's weekly limit."
},
{
"ref":"aiobungie.crate.user",
"url":3,
"doc":"Basic implementation for a Bungie a user."
},
{
"ref":"aiobungie.crate.user.User",
"url":3,
"doc":"Represents Bungie user. Method generated by attrs for class User."
},
{
"ref":"aiobungie.crate.user.User.as_dict",
"url":3,
"doc":"Returns a dict object of the user."
},
{
"ref":"aiobungie.crate.user.User.about",
"url":3,
"doc":"The user's about, Default is None if nothing is Found."
},
{
"ref":"aiobungie.crate.user.User.blizzard_name",
"url":3,
"doc":"The user's blizzard name if it exists."
},
{
"ref":"aiobungie.crate.user.User.created_at",
"url":3,
"doc":"The user's creation date in UTC timezone."
},
{
"ref":"aiobungie.crate.user.User.id",
"url":3,
"doc":"The user's id"
},
{
"ref":"aiobungie.crate.user.User.is_deleted",
"url":3,
"doc":"Returns True if the user is deleted"
},
{
"ref":"aiobungie.crate.user.User.locale",
"url":3,
"doc":"The user's locale."
},
{
"ref":"aiobungie.crate.user.User.name",
"url":3,
"doc":"The user's name."
},
{
"ref":"aiobungie.crate.user.User.picture",
"url":3,
"doc":"The user's profile picture."
},
{
"ref":"aiobungie.crate.user.User.psn_name",
"url":3,
"doc":"The user's psn id if it exists."
},
{
"ref":"aiobungie.crate.user.User.status",
"url":3,
"doc":"The user's bungie status text"
},
{
"ref":"aiobungie.crate.user.User.steam_name",
"url":3,
"doc":"The user's steam name if it exists"
},
{
"ref":"aiobungie.crate.user.User.twitch_name",
"url":3,
"doc":"The user's twitch name if it exists."
},
{
"ref":"aiobungie.crate.user.User.updated_at",
"url":3,
"doc":"The user's last updated om UTC date."
},
{
"ref":"aiobungie.crate.user.PartialUser",
"url":3,
"doc":"A partial user crate. Method generated by attrs for class PartialUser."
},
{
"ref":"aiobungie.crate.user.PartialUser.steam_name",
"url":3,
"doc":"The user's steam username or None."
},
{
"ref":"aiobungie.crate.user.PartialUser.twitch_name",
"url":3,
"doc":"The user's twitch username or None."
},
{
"ref":"aiobungie.crate.user.PartialUser.blizzard_name",
"url":3,
"doc":"The user's blizzard username or None."
},
{
"ref":"aiobungie.crate.user.PartialUser.psn_name",
"url":3,
"doc":"The user's psn username or None."
},
{
"ref":"aiobungie.crate.user.PartialUser.about",
"url":3,
"doc":"The user's about section."
},
{
"ref":"aiobungie.crate.user.PartialUser.locale",
"url":3,
"doc":"The user's profile locale."
},
{
"ref":"aiobungie.crate.user.PartialUser.name",
"url":3,
"doc":"The user's name."
},
{
"ref":"aiobungie.crate.user.PartialUser.picture",
"url":3,
"doc":"The user's profile picture if its set."
},
{
"ref":"aiobungie.crate.user.PartialUser.updated_at",
"url":3,
"doc":"The user's last profile update."
},
{
"ref":"aiobungie.crate.user.PartialUser.is_deleted",
"url":3,
"doc":"Determines if the user is deleted or not."
},
{
"ref":"aiobungie.crate.user.PartialUser.status",
"url":3,
"doc":"The user's profile status."
},
{
"ref":"aiobungie.crate.user.PartialUser.created_at",
"url":3,
"doc":"Retruns the user's creation date in UTC timezone."
},
{
"ref":"aiobungie.crate.user.PartialUser.human_timedelta",
"url":3,
"doc":""
},
{
"ref":"aiobungie.crate.user.UserLike",
"url":3,
"doc":"The is meant for any Member / user / like crate. Method generated by attrs for class UserLike."
},
{
"ref":"aiobungie.crate.user.UserLike.app",
"url":3,
"doc":"A client app that we may use for external requests."
},
{
"ref":"aiobungie.crate.user.UserLike.name",
"url":3,
"doc":"The user's name."
},
{
"ref":"aiobungie.crate.user.UserLike.is_public",
"url":3,
"doc":"Returns if the user profile is public or no."
},
{
"ref":"aiobungie.crate.user.UserLike.type",
"url":3,
"doc":"Returns the user type of the user."
},
{
"ref":"aiobungie.crate.user.UserLike.icon",
"url":3,
"doc":"The user's icon."
},
{
"ref":"aiobungie.crate.user.UserLike.link",
"url":3,
"doc":"Returns the user's profile link."
},
{
"ref":"aiobungie.crate.user.UserLike.as_dict",
"url":3,
"doc":"Returns an instance of the UserLike as a dict."
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
"ref":"aiobungie.error",
"url":12,
"doc":"aiobungie Exceptions."
},
{
"ref":"aiobungie.error.AiobungieError",
"url":12,
"doc":"The base exception class that all other errors inherit from."
},
{
"ref":"aiobungie.error.PlayerNotFound",
"url":12,
"doc":"Raised when a  aiobungie.crate.Player is not found."
},
{
"ref":"aiobungie.error.ActivityNotFound",
"url":12,
"doc":"Raised when a  aiobungie.crate.Activity not found."
},
{
"ref":"aiobungie.error.ClanNotFound",
"url":12,
"doc":"Raised when a  aiobungie.crate.Clan not found."
},
{
"ref":"aiobungie.error.CharacterError",
"url":12,
"doc":"Raised when a  aiobungie.crate.Character not found. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.CharacterError.message",
"url":12,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.NotFound",
"url":12,
"doc":"Raised when an unknown request was not found."
},
{
"ref":"aiobungie.error.HTTPException",
"url":12,
"doc":"Exception for handling  aiobungie.http.HTTPClient requests errors. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.HTTPException.message",
"url":12,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.UserNotFound",
"url":12,
"doc":"Raised when a  aiobungie.crate.User not found."
},
{
"ref":"aiobungie.error.ComponentError",
"url":12,
"doc":"Raised when someone uses the wrong  aiobungie.internal.enums.Component. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.ComponentError.message",
"url":12,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.MembershipTypeError",
"url":12,
"doc":"Raised when the memberhsip type is invalid. or The crate you're trying to fetch doesn't have The requested membership type. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.MembershipTypeError.message",
"url":12,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.Forbidden",
"url":12,
"doc":"Exception that's raised for when status code 403 occurs. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.Forbidden.message",
"url":12,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.Unauthorized",
"url":12,
"doc":"Unauthorized access. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.Unauthorized.message",
"url":12,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.ResponseError",
"url":12,
"doc":"Typical Responses error."
},
{
"ref":"aiobungie.ext",
"url":13,
"doc":"aiobungie extensions."
},
{
"ref":"aiobungie.ext.Manifest",
"url":13,
"doc":""
},
{
"ref":"aiobungie.ext.Manifest.download",
"url":13,
"doc":"",
"func":1
},
{
"ref":"aiobungie.ext.Manifest.get_raid_image",
"url":13,
"doc":"",
"func":1
},
{
"ref":"aiobungie.ext.Manifest.fetch",
"url":13,
"doc":"Fetch something from the manifest databse. This returns a  typing.Dict[typing.Any, typing.Any] Parameters      definition:  builtins.str The definition you want to fetch from. id:  builtins.int The id of the entity. item:  typing.Optional[builsint.str] An item to get from the dict. Returns    -  typing.Optional[typing.Dict[typing.Any, typing.Any  ",
"func":1
},
{
"ref":"aiobungie.ext.Manifest.db",
"url":13,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.ext.Manifest.version",
"url":13,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.ext.meta",
"url":14,
"doc":"A very basic helper for the bungie Manifest."
},
{
"ref":"aiobungie.ext.meta.Manifest",
"url":14,
"doc":""
},
{
"ref":"aiobungie.ext.meta.Manifest.download",
"url":14,
"doc":"",
"func":1
},
{
"ref":"aiobungie.ext.meta.Manifest.get_raid_image",
"url":14,
"doc":"",
"func":1
},
{
"ref":"aiobungie.ext.meta.Manifest.fetch",
"url":14,
"doc":"Fetch something from the manifest databse. This returns a  typing.Dict[typing.Any, typing.Any] Parameters      definition:  builtins.str The definition you want to fetch from. id:  builtins.int The id of the entity. item:  typing.Optional[builsint.str] An item to get from the dict. Returns    -  typing.Optional[typing.Dict[typing.Any, typing.Any  ",
"func":1
},
{
"ref":"aiobungie.ext.meta.Manifest.db",
"url":14,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.ext.meta.Manifest.version",
"url":14,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.http",
"url":15,
"doc":"An HTTPClient for sending requests to the Bungie API and Where all the magic happenes."
},
{
"ref":"aiobungie.http.HTTPClient",
"url":15,
"doc":"An HTTP Client for sending http requests to the Bungie API"
},
{
"ref":"aiobungie.http.HTTPClient.fetch",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_user",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_user_from_id",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_manifest",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.static_search",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_player",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_clan_from_id",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_clan",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_app",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_character",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_activity",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_post_activity",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_vendor_sales",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_profile",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_entity",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_inventory_item",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_clan_members",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_hard_linked",
"url":15,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal",
"url":16,
"doc":"Package contains internal and helpers for aiobungie."
},
{
"ref":"aiobungie.internal.Time",
"url":16,
"doc":""
},
{
"ref":"aiobungie.internal.Time.format_played",
"url":16,
"doc":"Converts A Bungie's total played time in minutes to a a readble time.",
"func":1
},
{
"ref":"aiobungie.internal.Time.from_timestamp",
"url":16,
"doc":"Converts timestamp to  datetime.datetime ",
"func":1
},
{
"ref":"aiobungie.internal.Time.clean_date",
"url":16,
"doc":"Formats  datetime.datetime to a readble date.",
"func":1
},
{
"ref":"aiobungie.internal.Time.to_timestamp",
"url":16,
"doc":"Converts datetime.datetime.utctimetuple() to timestamp.",
"func":1
},
{
"ref":"aiobungie.internal.Time.human_timedelta",
"url":16,
"doc":"Rapptz :>)",
"func":1
},
{
"ref":"aiobungie.internal.Image",
"url":16,
"doc":""
},
{
"ref":"aiobungie.internal.Image.BASE",
"url":16,
"doc":""
},
{
"ref":"aiobungie.internal.deprecated",
"url":16,
"doc":"functions with this decorator will not work or is not implemented yet.",
"func":1
},
{
"ref":"aiobungie.internal.assets",
"url":17,
"doc":"aiobungie assets module for API Image hash and path linking."
},
{
"ref":"aiobungie.internal.assets.Image",
"url":17,
"doc":""
},
{
"ref":"aiobungie.internal.assets.Image.BASE",
"url":17,
"doc":""
},
{
"ref":"aiobungie.internal.db",
"url":18,
"doc":"A small sqlite3 database for the bungie manifest."
},
{
"ref":"aiobungie.internal.db.Database",
"url":18,
"doc":""
},
{
"ref":"aiobungie.internal.db.Database.commit",
"url":18,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.db.Database.fetch",
"url":18,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.db.Database.fetchrow",
"url":18,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.db.Database.create_table",
"url":18,
"doc":"Creates a table with one column, this is only used for the versions.",
"func":1
},
{
"ref":"aiobungie.internal.db.Database.insert_version",
"url":18,
"doc":"Insertes the manifest version.",
"func":1
},
{
"ref":"aiobungie.internal.db.Database.execute",
"url":18,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.db.Database.get_version",
"url":18,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.db.Database.version",
"url":18,
"doc":""
},
{
"ref":"aiobungie.internal.db.Database.path",
"url":18,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.internal.enums",
"url":19,
"doc":"Bungie enums impl for aiobungie."
},
{
"ref":"aiobungie.internal.enums.GameMode",
"url":19,
"doc":"An Enum for all available gamemodes in Destiny 2."
},
{
"ref":"aiobungie.internal.enums.GameMode.NONE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.STORY",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.STRIKE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.RAID",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.ALLPVP",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.PATROL",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.ALLPVE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.TOF",
"url":19,
"doc":"Trials Of Osiris"
},
{
"ref":"aiobungie.internal.enums.GameMode.CONTROL",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.NIGHTFALL",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.IRONBANER",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.ALLSTRIKES",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.DUNGEON",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.GAMBIT",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.EMIPIRE_HUNT",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.RUMBLE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.CLASSIC_MIX",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.COUNTDOWN",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.DOUBLES",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.CLASH",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.MAYHEM",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.SURVIVAL",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType",
"url":19,
"doc":"An Enum for Bungie membership types."
},
{
"ref":"aiobungie.internal.enums.MembershipType.NONE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.XBOX",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.PSN",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.STEAM",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.BLIZZARD",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.STADIA",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.BUNGIE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.ALL",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Class",
"url":19,
"doc":"An Enum for Destiny character classes."
},
{
"ref":"aiobungie.internal.enums.Class.TITAN",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Class.HUNTER",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Class.WARLOCK",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Class.UNKNOWN",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType",
"url":19,
"doc":"An Enum for Destiny 2 milestone types."
},
{
"ref":"aiobungie.internal.enums.MilestoneType.UNKNOWN",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType.TUTORIAL",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType.ONETIME",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType.WEEKLY",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType.DAILY",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType.SPECIAL",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Race",
"url":19,
"doc":"An Enum for Destiny races."
},
{
"ref":"aiobungie.internal.enums.Race.HUMAN",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Race.AWOKEN",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Race.EXO",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Race.UNKNOWN",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor",
"url":19,
"doc":"An Enum for all available vendors in Destiny 2."
},
{
"ref":"aiobungie.internal.enums.Vendor.ZAVALA",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.XUR",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.BANSHE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.SPIDER",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.SHAXX",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.KADI",
"url":19,
"doc":"Postmaster exo."
},
{
"ref":"aiobungie.internal.enums.Vendor.YUNA",
"url":19,
"doc":"Asia servers only."
},
{
"ref":"aiobungie.internal.enums.Vendor.EVERVERSE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.AMANDA",
"url":19,
"doc":"Amanda holiday"
},
{
"ref":"aiobungie.internal.enums.Vendor.CROW",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.HAWTHORNE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.ADA1",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.DRIFTER",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.IKORA",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.SAINT",
"url":19,
"doc":"Saint-14"
},
{
"ref":"aiobungie.internal.enums.Vendor.ERIS_MORN",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.SHAW_HAWN",
"url":19,
"doc":"COSMODROME Guy"
},
{
"ref":"aiobungie.internal.enums.Vendor.VARIKS",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Raid",
"url":19,
"doc":"An Enum for all available raids in Destiny 2."
},
{
"ref":"aiobungie.internal.enums.Raid.DSC",
"url":19,
"doc":"Deep Stone Crypt"
},
{
"ref":"aiobungie.internal.enums.Raid.LW",
"url":19,
"doc":"Last Wish"
},
{
"ref":"aiobungie.internal.enums.Raid.VOG",
"url":19,
"doc":"Normal Valut of Glass"
},
{
"ref":"aiobungie.internal.enums.Raid.GOS",
"url":19,
"doc":"Garden Of Salvation"
},
{
"ref":"aiobungie.internal.enums.Dungeon",
"url":19,
"doc":"An Enum for all available Dungeon/Like missions in Destiny 2."
},
{
"ref":"aiobungie.internal.enums.Dungeon.NORMAL_PRESAGE",
"url":19,
"doc":"Normal Presage"
},
{
"ref":"aiobungie.internal.enums.Dungeon.MASTER_PRESAGE",
"url":19,
"doc":"Master Presage"
},
{
"ref":"aiobungie.internal.enums.Dungeon.HARBINGER",
"url":19,
"doc":"Harbinger"
},
{
"ref":"aiobungie.internal.enums.Dungeon.PROPHECY",
"url":19,
"doc":"Prophecy"
},
{
"ref":"aiobungie.internal.enums.Dungeon.MASTER_POH",
"url":19,
"doc":"Master Pit of Heresy?"
},
{
"ref":"aiobungie.internal.enums.Dungeon.LEGEND_POH",
"url":19,
"doc":"Legend Pit of Heresy?"
},
{
"ref":"aiobungie.internal.enums.Dungeon.POH",
"url":19,
"doc":"Normal Pit of Heresy."
},
{
"ref":"aiobungie.internal.enums.Dungeon.SHATTERED",
"url":19,
"doc":"Shattered Throne"
},
{
"ref":"aiobungie.internal.enums.Gender",
"url":19,
"doc":"An Enum for Destiny Genders."
},
{
"ref":"aiobungie.internal.enums.Gender.MALE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Gender.FEMALE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Gender.UNKNOWN",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component",
"url":19,
"doc":"An Enum for Destiny 2 Components."
},
{
"ref":"aiobungie.internal.enums.Component.NONE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.PROFILE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.SILVER",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.PROGRESSION",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.INVENTORIES",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.CHARECTERS",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.CHAR_INVENTORY",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.CHARECTER_PROGRESSION",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.EQUIPED_ITEMS",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.VENDORS",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.RECORDS",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.VENDOR_SALES",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Planet",
"url":19,
"doc":"An Enum for all available planets in Destiny 2."
},
{
"ref":"aiobungie.internal.enums.Planet.UNKNOWN",
"url":19,
"doc":"Unknown space"
},
{
"ref":"aiobungie.internal.enums.Planet.EARTH",
"url":19,
"doc":"Earth"
},
{
"ref":"aiobungie.internal.enums.Planet.DREAMING_CITY",
"url":19,
"doc":"The Dreaming city."
},
{
"ref":"aiobungie.internal.enums.Planet.NESSUS",
"url":19,
"doc":"Nessus"
},
{
"ref":"aiobungie.internal.enums.Planet.MOON",
"url":19,
"doc":"The Moon"
},
{
"ref":"aiobungie.internal.enums.Planet.COSMODROME",
"url":19,
"doc":"The Cosmodrome"
},
{
"ref":"aiobungie.internal.enums.Planet.TANGLED_SHORE",
"url":19,
"doc":"The Tangled Shore"
},
{
"ref":"aiobungie.internal.enums.Planet.VENUS",
"url":19,
"doc":"Venus"
},
{
"ref":"aiobungie.internal.enums.Planet.EAZ",
"url":19,
"doc":"European Aerial Zone"
},
{
"ref":"aiobungie.internal.enums.Planet.EUROPA",
"url":19,
"doc":"Europa"
},
{
"ref":"aiobungie.internal.enums.Stat",
"url":19,
"doc":"An Enum for Destiny 2 character stats."
},
{
"ref":"aiobungie.internal.enums.Stat.NONE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.MOBILITY",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.RESILIENCE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.RECOVERY",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.DISCIPLINE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.INTELLECT",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.STRENGTH",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.WeaponType",
"url":19,
"doc":"Enums for The three Destiny Weapon Types"
},
{
"ref":"aiobungie.internal.enums.WeaponType.NONE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.WeaponType.KINETIC",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.WeaponType.ENERGY",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.WeaponType.POWER",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType",
"url":19,
"doc":"Enums for Destiny Damage types"
},
{
"ref":"aiobungie.internal.enums.DamageType.NONE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.KINETIC",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.SOLAR",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.VOID",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.ARC",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.STASIS",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.RAID",
"url":19,
"doc":"This is a special damage type reserved for some raid activity encounters."
},
{
"ref":"aiobungie.internal.enums.Item",
"url":19,
"doc":"Enums for Destiny2's inventory bucket items"
},
{
"ref":"aiobungie.internal.enums.Item.NONE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.ARMOR",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.WEAPON",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.AUTO_RIFLE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SHOTGUN",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.MACHINE_GUN",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.HANDCANNON",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.ROCKET_LAUNCHER",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.FUSION_RIFLE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SNIPER_RIFLE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.PULSE_RIFLE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SCOUT_RIFLE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SIDEARM",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SWORD",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.MASK",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SHADER",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.ORNAMENT",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.FUSION_RIFLELINE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.GRENADE_LAUNCHER",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SUBMACHINE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.TRACE_RIFLE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.HELMET_ARMOR",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.GAUNTLET_ARMOR",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.CHEST_ARMOR",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.LEG_ARMOR",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.CLASS_ARMOR",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.HELMET",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.GAUNTLET",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.CHEST",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.LEG",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.CLASS",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.BOW",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.EMBLEMS",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.LEGENDRY_SHARDS",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.GHOST",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SUBCLASS",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SEASONAL_ARTIFACT",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.EMOTES",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SYNTHWAEV_TEMPLATE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.KINETIC",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.ENERGY",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.POWER",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Place",
"url":19,
"doc":"An Enum for Destiny 2 Places and NOT Planets"
},
{
"ref":"aiobungie.internal.enums.Place.ORBIT",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Place.SOCIAL",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Place.LIGHT_HOUSE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Place.EXPLORE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier",
"url":19,
"doc":"An enum for a Destiny 2 item tier."
},
{
"ref":"aiobungie.internal.enums.ItemTier.NONE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier.BASIC",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier.COMMON",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier.RARE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier.LEGENDERY",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier.EXOTIC",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.AmmoType",
"url":19,
"doc":"AN enum for Detyiny 2 ammo types."
},
{
"ref":"aiobungie.internal.enums.AmmoType.NONE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.AmmoType.PRIMARY",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.AmmoType.SPECIAL",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.AmmoType.HEAVY",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GroupType",
"url":19,
"doc":"An enums for the known bungie group types."
},
{
"ref":"aiobungie.internal.enums.GroupType.GENERAL",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GroupType.CLAN",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType",
"url":19,
"doc":"The types of the accounts system suports at bungie."
},
{
"ref":"aiobungie.internal.enums.CredentialType.NONE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.XUID",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.PSNID",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.WILD",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.FAKE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.FACEBOOK",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.GOOGLE",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.WINDOWS",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.DEMONID",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.STEAMID",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.BATTLENETID",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.STADIAID",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.enums.CredentialType.TWITCHID",
"url":19,
"doc":""
},
{
"ref":"aiobungie.internal.helpers",
"url":20,
"doc":"A helper module for useful decorators and other stuff."
},
{
"ref":"aiobungie.internal.helpers.deprecated",
"url":20,
"doc":"functions with this decorator will not work or is not implemented yet.",
"func":1
},
{
"ref":"aiobungie.internal.impl",
"url":21,
"doc":"A base module for all client implementation."
},
{
"ref":"aiobungie.internal.impl.BaseClient",
"url":21,
"doc":"Base class for protocol classes. Protocol classes are defined as class Proto(Protocol): def meth(self) -> int:  . Such classes are primarily used with static type checkers that recognize structural subtyping (static duck-typing), for example class C: def meth(self) -> int: return 0 def func(x: Proto) -> int: return x.meth() func(C(  Passes static type check See PEP 544 for details. Protocol classes decorated with @typing.runtime_checkable act as simple-minded runtime protocols that check only the presence of given attributes, ignoring their type signatures. Protocol classes can be generic, they are defined as class GenProto(Protocol[T]): def meth(self) -> T:  ."
},
{
"ref":"aiobungie.internal.impl.BaseClient.run",
"url":21,
"doc":"Runs a Coro function until its complete. This is equivalent to asyncio.get_event_loop().run_until_complete( .) Parameters      future:  typing.Coroutine[typing.Any, typing.Any, typing.Any] Your coro function. Example    -   async def main() -> None: player = await client.fetch_player(\"Fate\") print(player.name) client.run(main(  ",
"func":1
},
{
"ref":"aiobungie.internal.impl.BaseClient.rest",
"url":21,
"doc":"Returns resful of the client instance for other requests."
},
{
"ref":"aiobungie.internal.impl.RESTful",
"url":21,
"doc":"Base class for protocol classes. Protocol classes are defined as class Proto(Protocol): def meth(self) -> int:  . Such classes are primarily used with static type checkers that recognize structural subtyping (static duck-typing), for example class C: def meth(self) -> int: return 0 def func(x: Proto) -> int: return x.meth() func(C(  Passes static type check See PEP 544 for details. Protocol classes decorated with @typing.runtime_checkable act as simple-minded runtime protocols that check only the presence of given attributes, ignoring their type signatures. Protocol classes can be generic, they are defined as class GenProto(Protocol[T]): def meth(self) -> T:  ."
},
{
"ref":"aiobungie.internal.impl.RESTful.rest",
"url":21,
"doc":"Returns resful of the client instance for other requests."
},
{
"ref":"aiobungie.internal.serialize",
"url":22,
"doc":"Deserialization for all bungie incoming json payloads."
},
{
"ref":"aiobungie.internal.serialize.Deserialize",
"url":22,
"doc":"The base Deserialization class for all aiobungie crate."
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_user",
"url":22,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_player",
"url":22,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deseialize_clan_owner",
"url":22,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deseialize_clan",
"url":22,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_clan_member",
"url":22,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_clan_members",
"url":22,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_app_owner",
"url":22,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_app",
"url":22,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_character",
"url":22,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_profile",
"url":22,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_inventory_entity",
"url":22,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_activity",
"url":22,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.time",
"url":23,
"doc":"Time formating module."
},
{
"ref":"aiobungie.internal.time.Time",
"url":23,
"doc":""
},
{
"ref":"aiobungie.internal.time.Time.format_played",
"url":23,
"doc":"Converts A Bungie's total played time in minutes to a a readble time.",
"func":1
},
{
"ref":"aiobungie.internal.time.Time.from_timestamp",
"url":23,
"doc":"Converts timestamp to  datetime.datetime ",
"func":1
},
{
"ref":"aiobungie.internal.time.Time.clean_date",
"url":23,
"doc":"Formats  datetime.datetime to a readble date.",
"func":1
},
{
"ref":"aiobungie.internal.time.Time.to_timestamp",
"url":23,
"doc":"Converts datetime.datetime.utctimetuple() to timestamp.",
"func":1
},
{
"ref":"aiobungie.internal.time.Time.human_timedelta",
"url":23,
"doc":"Rapptz :>)",
"func":1
},
{
"ref":"aiobungie.url",
"url":24,
"doc":"Bungie API endpoint urls."
},
{
"ref":"aiobungie.url.BASE",
"url":24,
"doc":"Base bungie url"
},
{
"ref":"aiobungie.url.REST_EP",
"url":24,
"doc":"REST API endpoint"
},
{
"ref":"aiobungie.url.OAUTH_EP",
"url":24,
"doc":"OAuth endpoint"
},
{
"ref":"aiobungie.url.TOKEN_EP",
"url":24,
"doc":"OAuth token endpoint"
}
]