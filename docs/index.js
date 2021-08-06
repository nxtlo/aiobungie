URLS=[
"aiobungie/index.html",
"aiobungie/client.html",
"aiobungie/error.html",
"aiobungie/ext/index.html",
"aiobungie/ext/meta.html",
"aiobungie/http.html",
"aiobungie/internal/index.html",
"aiobungie/internal/assets.html",
"aiobungie/internal/cache.html",
"aiobungie/internal/db.html",
"aiobungie/internal/enums.html",
"aiobungie/internal/helpers.html",
"aiobungie/internal/impl.html",
"aiobungie/internal/serialize.html",
"aiobungie/internal/time.html",
"aiobungie/objects/index.html",
"aiobungie/objects/user.html",
"aiobungie/objects/character.html",
"aiobungie/objects/activity.html",
"aiobungie/objects/application.html",
"aiobungie/objects/clans.html",
"aiobungie/objects/entity.html",
"aiobungie/objects/player.html",
"aiobungie/objects/profile.html",
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
"ref":"aiobungie.Client.cache",
"url":0,
"doc":"A redis hash cache for testing purposes."
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
"doc":"Access The bungie Manifest. Returns    -  aiobungie.ext.Manifest A Manifest object.",
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
"ref":"aiobungie.Client.fetch_profile",
"url":0,
"doc":"Fetches a bungie profile. See  aiobungie.objects.Profile to access other components. Paramaters      memberid:  builtins.int The member's id. type:  aiobungie.MembershipType A valid membership type. Returns      aiobungie.objects.Profile An aiobungie member profile.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_player",
"url":0,
"doc":"Fetches a Destiny2 Player. Parameters      - name:  builtins.str The Player's Name type:  aiobungie.internal.enums.MembershipType The player's membership type, e,g. XBOX, STEAM, PSN position:  builtins.int Which player position to return, first player will return if None. Returns      aiobungie.objects.Player An aiobungie Destiny 2 Player object",
"func":1
},
{
"ref":"aiobungie.Client.fetch_character",
"url":0,
"doc":"Fetches a Destiny 2 character. Parameters      memberid:  builtins.int A valid bungie member id. character:  aiobungie.internal.enums.Class The Destiny character to retrieve. type:  aiobungie.internal.enums.MembershipType The member's membership type. Returns    -  aiobungie.objects.Character An aiobungie character object. Raises     aiobungie.error.CharacterError raised if the Character was not found.",
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
"doc":"Fetches a Destiny 2 activity for the specified user id and character. Parameters      userid:  builtins.int The user id that starts with  4611 . charaid:  builtins.int The id of the character to retrieve. mode:  aiobungie.internal.enums.GameMode This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc. memtype:  aiobungie.internal.enums.MembershipType The Member ship type, if nothing was passed than it will return all. page: typing.Optional[builtins.int] The page number limit: typing.Optional[builtins.int] Limit the returned result. Returns    -  aiobungie.objects.Activity An aiobungie Activity object. Raises     AttributeError Using  aiobungie.objects.Activity.hash for non raid activies.  aiobungie.error.ActivityNotFound Any other errors occures during the response.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_app",
"url":0,
"doc":"Fetches a Bungie Application. Parameters      - appid:  builtins.int The application id. Returns      aiobungie.objects.Application An aiobungie application object.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_clan_from_id",
"url":0,
"doc":"Fetches a Bungie Clan by its id. Parameters      - id:  builtins.int The clan id. Returns      aiobungie.objects.Clan An aioungie clan object",
"func":1
},
{
"ref":"aiobungie.Client.fetch_clan",
"url":0,
"doc":"Fetches a Clan by its name and returns the first result. Parameters      name:  builtins.str The clan name type  builtins.int The group type, Default is one. Returns    -  aiobungie.objects.Clan An aiobungie clan object.",
"func":1
},
{
"ref":"aiobungie.Client.fetch_entity",
"url":0,
"doc":"Fetches a static definition of an entity given a type and its hash. Paramaters      type:  builtins.str Entity's type definition. hash:  builtins.int Entity's hash. Returns    -  aiobungie.objects.Entity An aiobungie entity object.",
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
"doc":"Raised when a  aiobungie.objects.Player is not found."
},
{
"ref":"aiobungie.ActivityNotFound",
"url":0,
"doc":"Raised when a  aiobungie.objects.Activity not found."
},
{
"ref":"aiobungie.ClanNotFound",
"url":0,
"doc":"Raised when a  aiobungie.objects.Clan not found."
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
"doc":"Raised when a  aiobungie.objects.User not found."
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
"doc":"Raised when the memberhsip type is invalid. or The object you're trying to fetch doesn't have The requested membership type. Method generated by attrs for class HTTPException."
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
"ref":"aiobungie.client.Client.cache",
"url":1,
"doc":"A redis hash cache for testing purposes."
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
"doc":"Access The bungie Manifest. Returns    -  aiobungie.ext.Manifest A Manifest object.",
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
"ref":"aiobungie.client.Client.fetch_profile",
"url":1,
"doc":"Fetches a bungie profile. See  aiobungie.objects.Profile to access other components. Paramaters      memberid:  builtins.int The member's id. type:  aiobungie.MembershipType A valid membership type. Returns      aiobungie.objects.Profile An aiobungie member profile.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_player",
"url":1,
"doc":"Fetches a Destiny2 Player. Parameters      - name:  builtins.str The Player's Name type:  aiobungie.internal.enums.MembershipType The player's membership type, e,g. XBOX, STEAM, PSN position:  builtins.int Which player position to return, first player will return if None. Returns      aiobungie.objects.Player An aiobungie Destiny 2 Player object",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_character",
"url":1,
"doc":"Fetches a Destiny 2 character. Parameters      memberid:  builtins.int A valid bungie member id. character:  aiobungie.internal.enums.Class The Destiny character to retrieve. type:  aiobungie.internal.enums.MembershipType The member's membership type. Returns    -  aiobungie.objects.Character An aiobungie character object. Raises     aiobungie.error.CharacterError raised if the Character was not found.",
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
"doc":"Fetches a Destiny 2 activity for the specified user id and character. Parameters      userid:  builtins.int The user id that starts with  4611 . charaid:  builtins.int The id of the character to retrieve. mode:  aiobungie.internal.enums.GameMode This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc. memtype:  aiobungie.internal.enums.MembershipType The Member ship type, if nothing was passed than it will return all. page: typing.Optional[builtins.int] The page number limit: typing.Optional[builtins.int] Limit the returned result. Returns    -  aiobungie.objects.Activity An aiobungie Activity object. Raises     AttributeError Using  aiobungie.objects.Activity.hash for non raid activies.  aiobungie.error.ActivityNotFound Any other errors occures during the response.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_app",
"url":1,
"doc":"Fetches a Bungie Application. Parameters      - appid:  builtins.int The application id. Returns      aiobungie.objects.Application An aiobungie application object.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_clan_from_id",
"url":1,
"doc":"Fetches a Bungie Clan by its id. Parameters      - id:  builtins.int The clan id. Returns      aiobungie.objects.Clan An aioungie clan object",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_clan",
"url":1,
"doc":"Fetches a Clan by its name and returns the first result. Parameters      name:  builtins.str The clan name type  builtins.int The group type, Default is one. Returns    -  aiobungie.objects.Clan An aiobungie clan object.",
"func":1
},
{
"ref":"aiobungie.client.Client.fetch_entity",
"url":1,
"doc":"Fetches a static definition of an entity given a type and its hash. Paramaters      type:  builtins.str Entity's type definition. hash:  builtins.int Entity's hash. Returns    -  aiobungie.objects.Entity An aiobungie entity object.",
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
"ref":"aiobungie.error",
"url":2,
"doc":"aiobungie Exceptions."
},
{
"ref":"aiobungie.error.AiobungieError",
"url":2,
"doc":"The base exception class that all other errors inherit from."
},
{
"ref":"aiobungie.error.PlayerNotFound",
"url":2,
"doc":"Raised when a  aiobungie.objects.Player is not found."
},
{
"ref":"aiobungie.error.ActivityNotFound",
"url":2,
"doc":"Raised when a  aiobungie.objects.Activity not found."
},
{
"ref":"aiobungie.error.ClanNotFound",
"url":2,
"doc":"Raised when a  aiobungie.objects.Clan not found."
},
{
"ref":"aiobungie.error.CharacterError",
"url":2,
"doc":"Raised when a  aiobungie.objects.Character not found. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.CharacterError.message",
"url":2,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.NotFound",
"url":2,
"doc":"Raised when an unknown request was not found."
},
{
"ref":"aiobungie.error.HTTPException",
"url":2,
"doc":"Exception for handling  aiobungie.http.HTTPClient requests errors. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.HTTPException.message",
"url":2,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.UserNotFound",
"url":2,
"doc":"Raised when a  aiobungie.objects.User not found."
},
{
"ref":"aiobungie.error.ComponentError",
"url":2,
"doc":"Raised when someone uses the wrong  aiobungie.internal.enums.Component. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.ComponentError.message",
"url":2,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.MembershipTypeError",
"url":2,
"doc":"Raised when the memberhsip type is invalid. or The object you're trying to fetch doesn't have The requested membership type. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.MembershipTypeError.message",
"url":2,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.Forbidden",
"url":2,
"doc":"Exception that's raised for when status code 403 occurs. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.Forbidden.message",
"url":2,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.Unauthorized",
"url":2,
"doc":"Unauthorized access. Method generated by attrs for class HTTPException."
},
{
"ref":"aiobungie.error.Unauthorized.message",
"url":2,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.error.ResponseError",
"url":2,
"doc":"Typical Responses error."
},
{
"ref":"aiobungie.ext",
"url":3,
"doc":"aiobungie extensions."
},
{
"ref":"aiobungie.ext.Manifest",
"url":3,
"doc":""
},
{
"ref":"aiobungie.ext.Manifest.download",
"url":3,
"doc":"",
"func":1
},
{
"ref":"aiobungie.ext.Manifest.get_raid_image",
"url":3,
"doc":"",
"func":1
},
{
"ref":"aiobungie.ext.Manifest.fetch",
"url":3,
"doc":"Fetch something from the manifest databse. This returns a  typing.Dict[typing.Any, typing.Any] Parameters      definition:  builtins.str The definition you want to fetch from. id:  builtins.int The id of the entity. item:  typing.Optional[builsint.str] An item to get from the dict. Returns    -  typing.Optional[typing.Dict[typing.Any, typing.Any  ",
"func":1
},
{
"ref":"aiobungie.ext.Manifest.db",
"url":3,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.ext.Manifest.version",
"url":3,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.ext.meta",
"url":4,
"doc":"A very basic helper for the bungie Manifest."
},
{
"ref":"aiobungie.ext.meta.Manifest",
"url":4,
"doc":""
},
{
"ref":"aiobungie.ext.meta.Manifest.download",
"url":4,
"doc":"",
"func":1
},
{
"ref":"aiobungie.ext.meta.Manifest.get_raid_image",
"url":4,
"doc":"",
"func":1
},
{
"ref":"aiobungie.ext.meta.Manifest.fetch",
"url":4,
"doc":"Fetch something from the manifest databse. This returns a  typing.Dict[typing.Any, typing.Any] Parameters      definition:  builtins.str The definition you want to fetch from. id:  builtins.int The id of the entity. item:  typing.Optional[builsint.str] An item to get from the dict. Returns    -  typing.Optional[typing.Dict[typing.Any, typing.Any  ",
"func":1
},
{
"ref":"aiobungie.ext.meta.Manifest.db",
"url":4,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.ext.meta.Manifest.version",
"url":4,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.http",
"url":5,
"doc":"An HTTPClient for sending requests to the Bungie API and Where all the magic happenes."
},
{
"ref":"aiobungie.http.HTTPClient",
"url":5,
"doc":"An HTTP Client for sending http requests to the Bungie API"
},
{
"ref":"aiobungie.http.HTTPClient.fetch",
"url":5,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_user",
"url":5,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_user_from_id",
"url":5,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_manifest",
"url":5,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.static_search",
"url":5,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_player",
"url":5,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_clan_from_id",
"url":5,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_clan",
"url":5,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_app",
"url":5,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_character",
"url":5,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_activity",
"url":5,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_vendor_sales",
"url":5,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_profile",
"url":5,
"doc":"",
"func":1
},
{
"ref":"aiobungie.http.HTTPClient.fetch_entity",
"url":5,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal",
"url":6,
"doc":"Package contains internal and helpers for aiobungie."
},
{
"ref":"aiobungie.internal.Time",
"url":6,
"doc":""
},
{
"ref":"aiobungie.internal.Time.format_played",
"url":6,
"doc":"Converts A Bungie's total played time in minutes to a a readble time.",
"func":1
},
{
"ref":"aiobungie.internal.Time.from_timestamp",
"url":6,
"doc":"Converts timestamp to  datetime.datetime ",
"func":1
},
{
"ref":"aiobungie.internal.Time.clean_date",
"url":6,
"doc":"Formats  datetime.datetime to a readble date.",
"func":1
},
{
"ref":"aiobungie.internal.Time.to_timestamp",
"url":6,
"doc":"Converts datetime.datetime.utctimetuple() to timestamp.",
"func":1
},
{
"ref":"aiobungie.internal.Time.human_timedelta",
"url":6,
"doc":"Rapptz :>)",
"func":1
},
{
"ref":"aiobungie.internal.Image",
"url":6,
"doc":""
},
{
"ref":"aiobungie.internal.Image.BASE",
"url":6,
"doc":""
},
{
"ref":"aiobungie.internal.deprecated",
"url":6,
"doc":"functions with this decorator will not work or is not implemented yet.",
"func":1
},
{
"ref":"aiobungie.internal.assets",
"url":7,
"doc":"aiobungie assets module for API Image hash and path linking."
},
{
"ref":"aiobungie.internal.assets.Image",
"url":7,
"doc":""
},
{
"ref":"aiobungie.internal.assets.Image.BASE",
"url":7,
"doc":""
},
{
"ref":"aiobungie.internal.cache",
"url":8,
"doc":"aiobungie Redis and Memory cache."
},
{
"ref":"aiobungie.internal.cache.Cache",
"url":8,
"doc":"Redis Cache for interacting with aiobungie."
},
{
"ref":"aiobungie.internal.cache.Cache.set_user",
"url":8,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.cache.Cache.get_user",
"url":8,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.cache.Cache.flush",
"url":8,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.cache.Cache.ttl",
"url":8,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.cache.Cache.get",
"url":8,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.cache.Cache.put",
"url":8,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.cache.Cache.remove",
"url":8,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.cache.Cache.expire",
"url":8,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.cache.Cache.hash",
"url":8,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.internal.cache.Hash",
"url":8,
"doc":"Implementation of redis hash. Attributes      - inject:  aredis.StrictRedis an Injector for your redis client."
},
{
"ref":"aiobungie.internal.cache.Hash.set",
"url":8,
"doc":"Creates a new hash with field name and a value. Parameters      - hash:  builtins.str The hash name. field:  typing.Any The field name. value:  typing.Any The value for the field.",
"func":1
},
{
"ref":"aiobungie.internal.cache.Hash.setx",
"url":8,
"doc":"A method thats similar to  Hash.set but will not replace the value if one is already exists. Parameters      hash:  builtins.str The hash name. field:  typing.Any The field name value:  typing.Any The value of the field.",
"func":1
},
{
"ref":"aiobungie.internal.cache.Hash.flush",
"url":8,
"doc":"Removes a hash. Parameters      - hashes:  typing.Sequence[builtins.str] The hashes you desire to delete.",
"func":1
},
{
"ref":"aiobungie.internal.cache.Hash.len",
"url":8,
"doc":"Returns the length of the hash. Parameters      - hash:  builtins.str The hash name.",
"func":1
},
{
"ref":"aiobungie.internal.cache.Hash.hashes",
"url":8,
"doc":"Returns all hashes in the cache.",
"func":1
},
{
"ref":"aiobungie.internal.cache.Hash.all",
"url":8,
"doc":"Returns all values from a hash. Parameters      - hash:  builtins.str The hash name. Returns    -  typing.List[builtins.str] A list of string values.",
"func":1
},
{
"ref":"aiobungie.internal.cache.Hash.delete",
"url":8,
"doc":"Deletes a field from the provided hash. Parameters      hash:  builtins.str The hash name. field:  typing.Any The field you want to delete.",
"func":1
},
{
"ref":"aiobungie.internal.cache.Hash.exists",
"url":8,
"doc":"Returns True if the field exists in the hash. Parameters      hash:  builtins.str The hash name. field:  typing.Any The field name Returns:  builtins.bool True if field exists in hash and False if not.",
"func":1
},
{
"ref":"aiobungie.internal.cache.Hash.get",
"url":8,
"doc":"Returns the value associated with field in the hash stored at key. Parameters      hash:  builtins.str The hash name. field:  typing.Any The field name",
"func":1
},
{
"ref":"aiobungie.internal.db",
"url":9,
"doc":"A small sqlite3 database for the bungie manifest."
},
{
"ref":"aiobungie.internal.db.Database",
"url":9,
"doc":""
},
{
"ref":"aiobungie.internal.db.Database.commit",
"url":9,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.db.Database.fetch",
"url":9,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.db.Database.fetchrow",
"url":9,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.db.Database.create_table",
"url":9,
"doc":"Creates a table with one column, this is only used for the versions.",
"func":1
},
{
"ref":"aiobungie.internal.db.Database.insert_version",
"url":9,
"doc":"Insertes the manifest version.",
"func":1
},
{
"ref":"aiobungie.internal.db.Database.execute",
"url":9,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.db.Database.get_version",
"url":9,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.db.Database.version",
"url":9,
"doc":""
},
{
"ref":"aiobungie.internal.db.Database.path",
"url":9,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.internal.enums",
"url":10,
"doc":"Bungie enums impl for aiobungie."
},
{
"ref":"aiobungie.internal.enums.GameMode",
"url":10,
"doc":"An Enum for all available gamemodes in Destiny 2."
},
{
"ref":"aiobungie.internal.enums.GameMode.NONE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.STORY",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.STRIKE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.RAID",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.ALLPVP",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.PATROL",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.ALLPVE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.TOF",
"url":10,
"doc":"Trials Of Osiris"
},
{
"ref":"aiobungie.internal.enums.GameMode.CONTROL",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.NIGHTFALL",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.IRONBANER",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.ALLSTRIKES",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.DUNGEON",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.GAMBIT",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.EMIPIRE_HUNT",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.RUMBLE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.CLASSIC_MIX",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.COUNTDOWN",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.DOUBLES",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.CLASH",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.MAYHEM",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.GameMode.SURVIVAL",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType",
"url":10,
"doc":"An Enum for Bungie membership types."
},
{
"ref":"aiobungie.internal.enums.MembershipType.NONE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.XBOX",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.PSN",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.STEAM",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.BLIZZARD",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.STADIA",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.BUNGIE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MembershipType.ALL",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Class",
"url":10,
"doc":"An Enum for Destiny character classes."
},
{
"ref":"aiobungie.internal.enums.Class.TITAN",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Class.HUNTER",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Class.WARLOCK",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Class.UNKNOWN",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType",
"url":10,
"doc":"An Enum for Destiny 2 milestone types."
},
{
"ref":"aiobungie.internal.enums.MilestoneType.UNKNOWN",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType.TUTORIAL",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType.ONETIME",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType.WEEKLY",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType.DAILY",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.MilestoneType.SPECIAL",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Race",
"url":10,
"doc":"An Enum for Destiny races."
},
{
"ref":"aiobungie.internal.enums.Race.HUMAN",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Race.AWOKEN",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Race.EXO",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Race.UNKNOWN",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor",
"url":10,
"doc":"An Enum for all available vendors in Destiny 2."
},
{
"ref":"aiobungie.internal.enums.Vendor.ZAVALA",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.XUR",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.BANSHE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.SPIDER",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.SHAXX",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.KADI",
"url":10,
"doc":"Postmaster exo."
},
{
"ref":"aiobungie.internal.enums.Vendor.YUNA",
"url":10,
"doc":"Asia servers only."
},
{
"ref":"aiobungie.internal.enums.Vendor.EVERVERSE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.AMANDA",
"url":10,
"doc":"Amanda holiday"
},
{
"ref":"aiobungie.internal.enums.Vendor.CROW",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.HAWTHORNE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.ADA1",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.DRIFTER",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.IKORA",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.SAINT",
"url":10,
"doc":"Saint-14"
},
{
"ref":"aiobungie.internal.enums.Vendor.ERIS_MORN",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Vendor.SHAW_HAWN",
"url":10,
"doc":"COSMODROME Guy"
},
{
"ref":"aiobungie.internal.enums.Vendor.VARIKS",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Raid",
"url":10,
"doc":"An Enum for all available raids in Destiny 2."
},
{
"ref":"aiobungie.internal.enums.Raid.DSC",
"url":10,
"doc":"Deep Stone Crypt"
},
{
"ref":"aiobungie.internal.enums.Raid.LW",
"url":10,
"doc":"Last Wish"
},
{
"ref":"aiobungie.internal.enums.Raid.VOG",
"url":10,
"doc":"Normal Valut of Glass"
},
{
"ref":"aiobungie.internal.enums.Raid.GOS",
"url":10,
"doc":"Garden Of Salvation"
},
{
"ref":"aiobungie.internal.enums.Dungeon",
"url":10,
"doc":"An Enum for all available Dungeon/Like missions in Destiny 2."
},
{
"ref":"aiobungie.internal.enums.Dungeon.NORMAL_PRESAGE",
"url":10,
"doc":"Normal Presage"
},
{
"ref":"aiobungie.internal.enums.Dungeon.MASTER_PRESAGE",
"url":10,
"doc":"Master Presage"
},
{
"ref":"aiobungie.internal.enums.Dungeon.HARBINGER",
"url":10,
"doc":"Harbinger"
},
{
"ref":"aiobungie.internal.enums.Dungeon.PROPHECY",
"url":10,
"doc":"Prophecy"
},
{
"ref":"aiobungie.internal.enums.Dungeon.MASTER_POH",
"url":10,
"doc":"Master Pit of Heresy?"
},
{
"ref":"aiobungie.internal.enums.Dungeon.LEGEND_POH",
"url":10,
"doc":"Legend Pit of Heresy?"
},
{
"ref":"aiobungie.internal.enums.Dungeon.POH",
"url":10,
"doc":"Normal Pit of Heresy."
},
{
"ref":"aiobungie.internal.enums.Dungeon.SHATTERED",
"url":10,
"doc":"Shattered Throne"
},
{
"ref":"aiobungie.internal.enums.Gender",
"url":10,
"doc":"An Enum for Destiny Genders."
},
{
"ref":"aiobungie.internal.enums.Gender.MALE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Gender.FEMALE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Gender.UNKNOWN",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component",
"url":10,
"doc":"An Enum for Destiny 2 Components."
},
{
"ref":"aiobungie.internal.enums.Component.NONE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.PROFILE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.SILVER",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.PROGRESSION",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.INVENTORIES",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.CHARECTERS",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.CHAR_INVENTORY",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.CHARECTER_PROGRESSION",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.EQUIPED_ITEMS",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.VENDORS",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.RECORDS",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Component.VENDOR_SALES",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Planet",
"url":10,
"doc":"An Enum for all available planets in Destiny 2."
},
{
"ref":"aiobungie.internal.enums.Planet.UNKNOWN",
"url":10,
"doc":"Unknown space"
},
{
"ref":"aiobungie.internal.enums.Planet.EARTH",
"url":10,
"doc":"Earth"
},
{
"ref":"aiobungie.internal.enums.Planet.DREAMING_CITY",
"url":10,
"doc":"The Dreaming city."
},
{
"ref":"aiobungie.internal.enums.Planet.NESSUS",
"url":10,
"doc":"Nessus"
},
{
"ref":"aiobungie.internal.enums.Planet.MOON",
"url":10,
"doc":"The Moon"
},
{
"ref":"aiobungie.internal.enums.Planet.COSMODROME",
"url":10,
"doc":"The Cosmodrome"
},
{
"ref":"aiobungie.internal.enums.Planet.TANGLED_SHORE",
"url":10,
"doc":"The Tangled Shore"
},
{
"ref":"aiobungie.internal.enums.Planet.VENUS",
"url":10,
"doc":"Venus"
},
{
"ref":"aiobungie.internal.enums.Planet.EAZ",
"url":10,
"doc":"European Aerial Zone"
},
{
"ref":"aiobungie.internal.enums.Planet.EUROPA",
"url":10,
"doc":"Europa"
},
{
"ref":"aiobungie.internal.enums.Stat",
"url":10,
"doc":"An Enum for Destiny 2 character stats."
},
{
"ref":"aiobungie.internal.enums.Stat.NONE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.MOBILITY",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.RESILIENCE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.RECOVERY",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.DISCIPLINE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.INTELLECT",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Stat.STRENGTH",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.WeaponType",
"url":10,
"doc":"Enums for The three Destiny Weapon Types"
},
{
"ref":"aiobungie.internal.enums.WeaponType.NONE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.WeaponType.KINETIC",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.WeaponType.ENERGY",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.WeaponType.POWER",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType",
"url":10,
"doc":"Enums for Destiny Damage types"
},
{
"ref":"aiobungie.internal.enums.DamageType.NONE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.KINETIC",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.SOLAR",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.VOID",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.ARC",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.STASIS",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.DamageType.RAID",
"url":10,
"doc":"This is a special damage type reserved for some raid activity encounters."
},
{
"ref":"aiobungie.internal.enums.Item",
"url":10,
"doc":"Enums for Destiny2's inventory bucket items"
},
{
"ref":"aiobungie.internal.enums.Item.NONE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.ARMOR",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.WEAPON",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.AUTO_RIFLE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SHOTGUN",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.MACHINE_GUN",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.HANDCANNON",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.ROCKET_LAUNCHER",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.FUSION_RIFLE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SNIPER_RIFLE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.PULSE_RIFLE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SCOUT_RIFLE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SIDEARM",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SWORD",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.MASK",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SHADER",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.ORNAMENT",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.FUSION_RIFLELINE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.GRENADE_LAUNCHER",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SUBMACHINE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.TRACE_RIFLE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.HELMET_ARMOR",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.GAUNTLET_ARMOR",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.CHEST_ARMOR",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.LEG_ARMOR",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.CLASS_ARMOR",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.HELMET",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.GAUNTLET",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.CHEST",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.LEG",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.CLASS",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.BOW",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.EMBLEMS",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.LEGENDRY_SHARDS",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.GHOST",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SUBCLASS",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SEASONAL_ARTIFACT",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.EMOTES",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.SYNTHWAEV_TEMPLATE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.KINETIC",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.ENERGY",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Item.POWER",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Place",
"url":10,
"doc":"An Enum for Destiny 2 Places and NOT Planets"
},
{
"ref":"aiobungie.internal.enums.Place.ORBIT",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Place.SOCIAL",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Place.LIGHT_HOUSE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.Place.EXPLORE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier",
"url":10,
"doc":"An enum for a Destiny 2 item tier."
},
{
"ref":"aiobungie.internal.enums.ItemTier.NONE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier.BASIC",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier.COMMON",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier.RARE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier.LEGENDERY",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.ItemTier.EXOTIC",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.AmmoType",
"url":10,
"doc":"AN enum for Detyiny 2 ammo types."
},
{
"ref":"aiobungie.internal.enums.AmmoType.NONE",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.AmmoType.PRIMARY",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.AmmoType.SPECIAL",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.enums.AmmoType.HEAVY",
"url":10,
"doc":""
},
{
"ref":"aiobungie.internal.helpers",
"url":11,
"doc":"A helper module for useful decorators and other stuff."
},
{
"ref":"aiobungie.internal.helpers.deprecated",
"url":11,
"doc":"functions with this decorator will not work or is not implemented yet.",
"func":1
},
{
"ref":"aiobungie.internal.impl",
"url":12,
"doc":"A base module for all client implementation."
},
{
"ref":"aiobungie.internal.impl.BaseCache",
"url":12,
"doc":"Base class for protocol classes. Protocol classes are defined as class Proto(Protocol): def meth(self) -> int:  . Such classes are primarily used with static type checkers that recognize structural subtyping (static duck-typing), for example class C: def meth(self) -> int: return 0 def func(x: Proto) -> int: return x.meth() func(C(  Passes static type check See PEP 544 for details. Protocol classes decorated with @typing.runtime_checkable act as simple-minded runtime protocols that check only the presence of given attributes, ignoring their type signatures. Protocol classes can be generic, they are defined as class GenProto(Protocol[T]): def meth(self) -> T:  ."
},
{
"ref":"aiobungie.internal.impl.BaseCache.cache",
"url":12,
"doc":"A redis hash cache for testing purposes."
},
{
"ref":"aiobungie.internal.impl.BaseClient",
"url":12,
"doc":"Base class for protocol classes. Protocol classes are defined as class Proto(Protocol): def meth(self) -> int:  . Such classes are primarily used with static type checkers that recognize structural subtyping (static duck-typing), for example class C: def meth(self) -> int: return 0 def func(x: Proto) -> int: return x.meth() func(C(  Passes static type check See PEP 544 for details. Protocol classes decorated with @typing.runtime_checkable act as simple-minded runtime protocols that check only the presence of given attributes, ignoring their type signatures. Protocol classes can be generic, they are defined as class GenProto(Protocol[T]): def meth(self) -> T:  ."
},
{
"ref":"aiobungie.internal.impl.BaseClient.run",
"url":12,
"doc":"Runs a Coro function until its complete. This is equivalent to asyncio.get_event_loop().run_until_complete( .) Parameters      future:  typing.Coroutine[typing.Any, typing.Any, typing.Any] Your coro function. Example    -   async def main() -> None: player = await client.fetch_player(\"Fate\") print(player.name) client.run(main(  ",
"func":1
},
{
"ref":"aiobungie.internal.impl.BaseClient.cache",
"url":12,
"doc":"A redis hash cache for testing purposes."
},
{
"ref":"aiobungie.internal.impl.BaseClient.rest",
"url":12,
"doc":"Returns resful of the client instance for other requests."
},
{
"ref":"aiobungie.internal.impl.RESTful",
"url":12,
"doc":"Base class for protocol classes. Protocol classes are defined as class Proto(Protocol): def meth(self) -> int:  . Such classes are primarily used with static type checkers that recognize structural subtyping (static duck-typing), for example class C: def meth(self) -> int: return 0 def func(x: Proto) -> int: return x.meth() func(C(  Passes static type check See PEP 544 for details. Protocol classes decorated with @typing.runtime_checkable act as simple-minded runtime protocols that check only the presence of given attributes, ignoring their type signatures. Protocol classes can be generic, they are defined as class GenProto(Protocol[T]): def meth(self) -> T:  ."
},
{
"ref":"aiobungie.internal.impl.RESTful.rest",
"url":12,
"doc":"Returns resful of the client instance for other requests."
},
{
"ref":"aiobungie.internal.serialize",
"url":13,
"doc":"Deserialization for all bungie incoming json payloads."
},
{
"ref":"aiobungie.internal.serialize.Deserialize",
"url":13,
"doc":"The base Deserialization class for all aiobungie objects."
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_user",
"url":13,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_player",
"url":13,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deseialize_clan_owner",
"url":13,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deseialize_clan",
"url":13,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_app_owner",
"url":13,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_app",
"url":13,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_character",
"url":13,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_profile",
"url":13,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.serialize.Deserialize.deserialize_entity",
"url":13,
"doc":"",
"func":1
},
{
"ref":"aiobungie.internal.time",
"url":14,
"doc":"Time formating module."
},
{
"ref":"aiobungie.internal.time.Time",
"url":14,
"doc":""
},
{
"ref":"aiobungie.internal.time.Time.format_played",
"url":14,
"doc":"Converts A Bungie's total played time in minutes to a a readble time.",
"func":1
},
{
"ref":"aiobungie.internal.time.Time.from_timestamp",
"url":14,
"doc":"Converts timestamp to  datetime.datetime ",
"func":1
},
{
"ref":"aiobungie.internal.time.Time.clean_date",
"url":14,
"doc":"Formats  datetime.datetime to a readble date.",
"func":1
},
{
"ref":"aiobungie.internal.time.Time.to_timestamp",
"url":14,
"doc":"Converts datetime.datetime.utctimetuple() to timestamp.",
"func":1
},
{
"ref":"aiobungie.internal.time.Time.human_timedelta",
"url":14,
"doc":"Rapptz :>)",
"func":1
},
{
"ref":"aiobungie.objects",
"url":15,
"doc":"Basic aiobungie objects implementation."
},
{
"ref":"aiobungie.objects.Application",
"url":15,
"doc":"Represents a Bungie developer application. Attributes      - name:  builtins.str The app's name id:  builtins.int The app's id. redirect_url: typing.Optional[ builtins.str ]: The app's redirect url, None if not Found. created_at:  datetime.datetime The application's creation date in UTC time. published_at:  datetime.datetime The application's publish date in UTC time. link:  builtins.str The app's link if it exists. status:  builtins.str The app's status. owner:  aiobungie.objects.ApplicationOwner An object of The application owner. scope:  builtins.str The app's scope Method generated by attrs for class Application."
},
{
"ref":"aiobungie.objects.Application.human_timedelta",
"url":15,
"doc":"Returns a human readble date of the app's creation date."
},
{
"ref":"aiobungie.objects.Application.as_dict",
"url":15,
"doc":"Returns a dict object of the application, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.objects.Application.created_at",
"url":15,
"doc":"App creation date in UTC timezone"
},
{
"ref":"aiobungie.objects.Application.id",
"url":15,
"doc":"App id"
},
{
"ref":"aiobungie.objects.Application.link",
"url":15,
"doc":"App's link"
},
{
"ref":"aiobungie.objects.Application.name",
"url":15,
"doc":"App name"
},
{
"ref":"aiobungie.objects.Application.owner",
"url":15,
"doc":"App's owner"
},
{
"ref":"aiobungie.objects.Application.published_at",
"url":15,
"doc":"App's publish date in UTC timezone"
},
{
"ref":"aiobungie.objects.Application.redirect_url",
"url":15,
"doc":"App redirect url"
},
{
"ref":"aiobungie.objects.Application.scope",
"url":15,
"doc":"App's scope"
},
{
"ref":"aiobungie.objects.Application.status",
"url":15,
"doc":"App's status"
},
{
"ref":"aiobungie.objects.Clan",
"url":15,
"doc":"Represents a Bungie clan object. Attributes      - name:  builtins.str The clan's name id:  builtins.int The clans's id created_at:  datetime.datetime Returns the clan's creation date in UTC time. description:  builtins.str The clan's description. is_public:  builtins.bool Returns True if the clan is public and False if not. banner:  aiobungie.internal.assets.Image Returns the clan's banner avatar:  aiobungie.internal.assets.Image Returns the clan's avatar about:  builtins.str The clan's about. tags:  builtins.str The clan's tags owner:  aiobungie.objects.ClanOwner Returns an object of the clan's owner. See  aiobungie.objects.ClanOwner for info. Method generated by attrs for class Clan."
},
{
"ref":"aiobungie.objects.Clan.human_timedelta",
"url":15,
"doc":"Returns a human readble date of the clan's creation date."
},
{
"ref":"aiobungie.objects.Clan.url",
"url":15,
"doc":""
},
{
"ref":"aiobungie.objects.Clan.as_dict",
"url":15,
"doc":"Returns an instance of the object as a dict"
},
{
"ref":"aiobungie.objects.Clan.about",
"url":15,
"doc":"Clan's about title."
},
{
"ref":"aiobungie.objects.Clan.avatar",
"url":15,
"doc":"Clan's avatar"
},
{
"ref":"aiobungie.objects.Clan.banner",
"url":15,
"doc":"Clan's banner"
},
{
"ref":"aiobungie.objects.Clan.created_at",
"url":15,
"doc":"Clan's creation date time in UTC."
},
{
"ref":"aiobungie.objects.Clan.description",
"url":15,
"doc":"Clan's description"
},
{
"ref":"aiobungie.objects.Clan.id",
"url":15,
"doc":"The clan id"
},
{
"ref":"aiobungie.objects.Clan.is_public",
"url":15,
"doc":"Clan's privacy status."
},
{
"ref":"aiobungie.objects.Clan.member_count",
"url":15,
"doc":"Clan's member count."
},
{
"ref":"aiobungie.objects.Clan.name",
"url":15,
"doc":"The clan's name"
},
{
"ref":"aiobungie.objects.Clan.owner",
"url":15,
"doc":"The clan owner."
},
{
"ref":"aiobungie.objects.Clan.tags",
"url":15,
"doc":"A list of the clan's tags."
},
{
"ref":"aiobungie.objects.Player",
"url":15,
"doc":"Represents a Bungie Destiny 2 Player. Attributes      icon:  aiobungie.internal.Image The player's icon. id:  builtins.int The player's id. name:  builtins.str The player's name. is_public:  builtins.bool A boolean True if the user's profile is public and False if not. type:  aiobungie.internal.enums.MembershipType The player's membership type. Method generated by attrs for class Player."
},
{
"ref":"aiobungie.objects.Player.as_dict",
"url":15,
"doc":"Returns a dict object of the player, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.objects.Player.icon",
"url":15,
"doc":"The player's icon."
},
{
"ref":"aiobungie.objects.Player.id",
"url":15,
"doc":"The player's id."
},
{
"ref":"aiobungie.objects.Player.is_public",
"url":15,
"doc":"The player's profile privacy."
},
{
"ref":"aiobungie.objects.Player.name",
"url":15,
"doc":"The player's name"
},
{
"ref":"aiobungie.objects.Player.type",
"url":15,
"doc":"The profile's membership type."
},
{
"ref":"aiobungie.objects.Player.link",
"url":16,
"doc":"Returns the user's profile link."
},
{
"ref":"aiobungie.objects.Character",
"url":15,
"doc":"An implementation for a Bungie character. A Bungie character object can be a Warlock, Titan or a Hunter. This can only be accessed using the  aiobungie.Component CHARACTERS component. Attributes      - light:  builtins.int The character's light id:  builtins.int The character's id gender:  aiobungie.internal.enums.Gender The character's gender race:  aiobungie.internal.enums.Race The character's race emblem:  aiobungie.internal.assets.Image The character's currnt equipped emblem. emblem_icon:  aiobungie.internal.assets.Image The character's current icon for the equipped emblem. emblem_hash:  builtins.int Character's emblem hash. last_played:  datetime.datetime When was this character last played date in UTC. total_played:  builtins.int Returns the total played time in seconds for the chosen character. member_id:  builtins.int The character's member id. class_type:  aiobungie.internal.enums.Class The character's class. level:  builtins.int Character's base level. stats:  aiobungie.internal.enums.Stat Character's current stats. title_hash:  typing.Optional[builtins.int] The hash of the character's equipped title, Returns  builtins.NoneType if no title is equipped. Method generated by attrs for class Character."
},
{
"ref":"aiobungie.objects.Character.url",
"url":15,
"doc":"A url for the character at bungie.net."
},
{
"ref":"aiobungie.objects.Character.as_dict",
"url":15,
"doc":"Returns a dict object of the character, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.objects.Character.class_type",
"url":15,
"doc":"Character's class."
},
{
"ref":"aiobungie.objects.Character.emblem",
"url":15,
"doc":"Character's emblem"
},
{
"ref":"aiobungie.objects.Character.emblem_hash",
"url":15,
"doc":"Character's emblem hash."
},
{
"ref":"aiobungie.objects.Character.emblem_icon",
"url":15,
"doc":"Character's emblem icon"
},
{
"ref":"aiobungie.objects.Character.gender",
"url":15,
"doc":"Character's gender"
},
{
"ref":"aiobungie.objects.Character.id",
"url":15,
"doc":"Character's id"
},
{
"ref":"aiobungie.objects.Character.last_played",
"url":15,
"doc":"Character's last played date."
},
{
"ref":"aiobungie.objects.Character.level",
"url":15,
"doc":"Character's base level."
},
{
"ref":"aiobungie.objects.Character.light",
"url":15,
"doc":"Character's light"
},
{
"ref":"aiobungie.objects.Character.member_id",
"url":15,
"doc":"The character's member id."
},
{
"ref":"aiobungie.objects.Character.member_type",
"url":15,
"doc":"The character's memberhip type."
},
{
"ref":"aiobungie.objects.Character.race",
"url":15,
"doc":"Character's race"
},
{
"ref":"aiobungie.objects.Character.stats",
"url":15,
"doc":"Character stats."
},
{
"ref":"aiobungie.objects.Character.title_hash",
"url":15,
"doc":"Character's equipped title hash."
},
{
"ref":"aiobungie.objects.Character.total_played_time",
"url":15,
"doc":"Character's total plyed time minutes."
},
{
"ref":"aiobungie.objects.Character.human_timedelta",
"url":17,
"doc":"The player's last played time in a human readble date."
},
{
"ref":"aiobungie.objects.Activity",
"url":15,
"doc":"Represents a Bungie Activity object. An activity can be one of  aiobungie.internal.enums.GameMode . Attributes      - mode:  aiobungie.internal.enums.GameMode The activity mode or type. is_completed:  builtins.str Check if the activity was completed or no. hash:  builtins.int The activity's hash. duration:  builtins.str A string of The activity's duration, Example format  7m 42s kills:  builtins.int Activity's Total kills deaths:  builtins.int Activity's total deaths. assists:  builtins.int Activity's Total assists kd:  builtins.int Activity's kd ration. member_type:  aiobungie.internal.enums.MembershipType The activity member's membership type. players_count:  builtins.int Total players in the activity. when: typing.Optional[datetime.datetime] When did the activity occurred in UTC datetime. Method generated by attrs for class Activity."
},
{
"ref":"aiobungie.objects.Activity.as_dict",
"url":15,
"doc":"Returns a dict object of the Activity, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.objects.Activity.assists",
"url":15,
"doc":"Activity's total assists."
},
{
"ref":"aiobungie.objects.Activity.deaths",
"url":15,
"doc":"Activity's total deaths."
},
{
"ref":"aiobungie.objects.Activity.duration",
"url":15,
"doc":"A string of The activity's duration, Example format  7m 42s "
},
{
"ref":"aiobungie.objects.Activity.hash",
"url":15,
"doc":"The activity's hash."
},
{
"ref":"aiobungie.objects.Activity.is_completed",
"url":15,
"doc":"Returns  Ok if the activity is completed and 'No' if not."
},
{
"ref":"aiobungie.objects.Activity.kd",
"url":15,
"doc":"Activity's kill/death ration."
},
{
"ref":"aiobungie.objects.Activity.kills",
"url":15,
"doc":"Activity's total kills."
},
{
"ref":"aiobungie.objects.Activity.member_type",
"url":15,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.objects.Activity.mode",
"url":15,
"doc":"Activity's game mode."
},
{
"ref":"aiobungie.objects.Activity.player_count",
"url":15,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.objects.Activity.when",
"url":15,
"doc":"A UTC datetime object of when was the activivy started."
},
{
"ref":"aiobungie.objects.User",
"url":15,
"doc":"Represents Bungie User object. Attributes      id:  builtins.int The user's id name:  builtins.str The user's name. is_deleted:  builtins.bool Returns True if the user is deleted about: typing.Optional[builtins.str] The user's about, Default is None if nothing is Found. created_at:  datetime.datetime The user's creation date in UTC date. updated_at:  datetime.datetime The user's last updated om UTC date. psn_name: typing.Optional[builtins.str] The user's psn id if it exists. twitch_name: typing.Optional[builtins.str] The user's twitch name if it exists. blizzard_name: typing.Optional[builtins.str] The user's blizzard name if it exists. steam_name: typing.Optional[builtins.str] The user's steam name if it exists status: typing.Optional[builtins.str] The user's bungie status text locale: typing.Optional[builtins.str] The user's locale. picture: aiobungie.internal.assets.Image The user's avatar. Method generated by attrs for class User."
},
{
"ref":"aiobungie.objects.User.as_dict",
"url":15,
"doc":"Returns a dict object of the user, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.objects.User.about",
"url":15,
"doc":"The user's about, Default is None if nothing is Found."
},
{
"ref":"aiobungie.objects.User.blizzard_name",
"url":15,
"doc":"The user's blizzard name if it exists."
},
{
"ref":"aiobungie.objects.User.created_at",
"url":15,
"doc":"The user's creation date in UTC timezone."
},
{
"ref":"aiobungie.objects.User.id",
"url":15,
"doc":"The user's id"
},
{
"ref":"aiobungie.objects.User.is_deleted",
"url":15,
"doc":"Returns True if the user is deleted"
},
{
"ref":"aiobungie.objects.User.locale",
"url":15,
"doc":"The user's locale."
},
{
"ref":"aiobungie.objects.User.name",
"url":15,
"doc":"The user's name."
},
{
"ref":"aiobungie.objects.User.picture",
"url":15,
"doc":"The user's profile picture."
},
{
"ref":"aiobungie.objects.User.psn_name",
"url":15,
"doc":"The user's psn id if it exists."
},
{
"ref":"aiobungie.objects.User.status",
"url":15,
"doc":"The user's bungie status text"
},
{
"ref":"aiobungie.objects.User.steam_name",
"url":15,
"doc":"The user's steam name if it exists"
},
{
"ref":"aiobungie.objects.User.twitch_name",
"url":15,
"doc":"The user's twitch name if it exists."
},
{
"ref":"aiobungie.objects.User.updated_at",
"url":15,
"doc":"The user's last updated om UTC date."
},
{
"ref":"aiobungie.objects.ClanOwner",
"url":15,
"doc":"Represents a Bungie clan owner. Attributes      - id:  builtins.int The clan owner's membership id name:  builtins.str The clan owner's display name last_online:  builtins.str An aware  builtins.str version of a  datetime.datetime object. type:  aiobungie.internal.enums.MembershipType Returns the clan owner's membership type. This could be Xbox, Steam, PSN, Blizzard or ALL, if the membership type is not recognized it will return  builtins.NoneType . clan_id:  builtins.int The clan owner's clan id joined_at: Optional[datetime.datetime]: The clan owner's join date in UTC. icon:  aiobungie.internal.assets.Image Returns the clan owner's icon from Image. is_public:  builtins.bool Returns True if the clan's owner profile is public or False if not. types: typing.List[builtins.int]: returns a List of  builtins.int of the clan owner's types. Method generated by attrs for class ClanOwner."
},
{
"ref":"aiobungie.objects.ClanOwner.human_timedelta",
"url":15,
"doc":"Returns a human readble date of the clan owner's last login."
},
{
"ref":"aiobungie.objects.ClanOwner.link",
"url":15,
"doc":"Returns the user's profile link."
},
{
"ref":"aiobungie.objects.ClanOwner.as_dict",
"url":15,
"doc":"Returns a dict object of the clan owner, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.objects.ClanOwner.clan_id",
"url":15,
"doc":"Owner's current clan id."
},
{
"ref":"aiobungie.objects.ClanOwner.icon",
"url":15,
"doc":"Owner's profile icom"
},
{
"ref":"aiobungie.objects.ClanOwner.id",
"url":15,
"doc":"The user id."
},
{
"ref":"aiobungie.objects.ClanOwner.is_public",
"url":15,
"doc":"Returns if the user profile is public or no."
},
{
"ref":"aiobungie.objects.ClanOwner.joined_at",
"url":15,
"doc":"Owner's bungie join date."
},
{
"ref":"aiobungie.objects.ClanOwner.last_online",
"url":15,
"doc":"An aware  datetime.datetime object of the user's last online date UTC."
},
{
"ref":"aiobungie.objects.ClanOwner.name",
"url":15,
"doc":"The user name."
},
{
"ref":"aiobungie.objects.ClanOwner.type",
"url":15,
"doc":"Returns the membership type of the user."
},
{
"ref":"aiobungie.objects.ClanOwner.types",
"url":15,
"doc":"Returns a list of the member ship's membership types."
},
{
"ref":"aiobungie.objects.ApplicationOwner",
"url":15,
"doc":"Represents a Bungie Application owner. Attributes      - name:  builtins.str The application owner name. id:  builtins.int The application owner bungie id. icon:  aiobungie.internal.assets.Image The application owner profile icon. is_public:  builtins.bool Determines if the application owner's profile was public or private type:  aiobungie.internal.enums.MembershipType The application owner's bungie membership type. Method generated by attrs for class ApplicationOwner."
},
{
"ref":"aiobungie.objects.ApplicationOwner.link",
"url":15,
"doc":"Returns the user's profile link."
},
{
"ref":"aiobungie.objects.ApplicationOwner.as_dict",
"url":15,
"doc":"Returns a dict object of the application owner, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.objects.ApplicationOwner.icon",
"url":15,
"doc":"The application owner's icon."
},
{
"ref":"aiobungie.objects.ApplicationOwner.id",
"url":15,
"doc":"The application owner's id."
},
{
"ref":"aiobungie.objects.ApplicationOwner.is_public",
"url":15,
"doc":"The application owner's profile privacy."
},
{
"ref":"aiobungie.objects.ApplicationOwner.name",
"url":15,
"doc":"The application owner name."
},
{
"ref":"aiobungie.objects.ApplicationOwner.type",
"url":15,
"doc":"The membership of the application owner."
},
{
"ref":"aiobungie.objects.Profile",
"url":15,
"doc":"Represents a Bungie member Profile. Bungie profiles requires components. but in aiobungie you don't need to select a specific component since they will all/will be implemented. for an example: to access the  Character component you'll need to pass  ?component=200 right?. in aiobungie you can just do this.   profile = await client.fetch_profile(\"Fate\")  access the character component and get my warlock. warlock = await profile.warlock() assert warlock.light  1320   Attributes      id:  builtins.int Profile's id name:  builtins.str Profile's name type:  aiobungie.internal.enums.MembershipType The profile's membership type. last_played:  datetime.datetime The profile owner's last played date in UTC character_ids:  typing.List[builtins.int] A list of the profile's character ids. power_cap:  builtins.int The profile's current season power cap. Method generated by attrs for class Profile."
},
{
"ref":"aiobungie.objects.Profile.as_dict",
"url":15,
"doc":"Returns a dict object of the profile, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.objects.Profile.human_timedelta",
"url":15,
"doc":"Returns last_played attr but in human delta date."
},
{
"ref":"aiobungie.objects.Profile.app",
"url":15,
"doc":"A client that we may to make rest requests."
},
{
"ref":"aiobungie.objects.Profile.character_ids",
"url":15,
"doc":"A list of the profile's character ids."
},
{
"ref":"aiobungie.objects.Profile.id",
"url":15,
"doc":"Profile's id"
},
{
"ref":"aiobungie.objects.Profile.is_public",
"url":15,
"doc":"Profile's privacy status."
},
{
"ref":"aiobungie.objects.Profile.last_played",
"url":15,
"doc":"Profile's last played Destiny 2 played date."
},
{
"ref":"aiobungie.objects.Profile.name",
"url":15,
"doc":"Profile's name."
},
{
"ref":"aiobungie.objects.Profile.power_cap",
"url":15,
"doc":"The profile's current seaspn power cap."
},
{
"ref":"aiobungie.objects.Profile.type",
"url":15,
"doc":"Profile's type."
},
{
"ref":"aiobungie.objects.Entity",
"url":15,
"doc":"A concrate implementation of a Bungie Item Definition Entity. As bungie says. using this endpoint is still in beta and may experience rough edges and bugs. Method generated by attrs for class Entity."
},
{
"ref":"aiobungie.objects.Entity.as_dict",
"url":15,
"doc":"Returns an instance of the object as a dict"
},
{
"ref":"aiobungie.objects.Entity.about",
"url":15,
"doc":"Entity's about."
},
{
"ref":"aiobungie.objects.Entity.ammo_type",
"url":15,
"doc":"Entity's ammo type if it was a wepon, otherwise it will return None"
},
{
"ref":"aiobungie.objects.Entity.app",
"url":15,
"doc":"A client that we may use to make rest calls."
},
{
"ref":"aiobungie.objects.Entity.banner",
"url":15,
"doc":"Entity's banner."
},
{
"ref":"aiobungie.objects.Entity.bucket_type",
"url":15,
"doc":"The entity's bucket type, None if unknown"
},
{
"ref":"aiobungie.objects.Entity.damage",
"url":15,
"doc":"Entity's damage type. Only works for weapons."
},
{
"ref":"aiobungie.objects.Entity.description",
"url":15,
"doc":"Entity's description. most entities don't use this so consider using  Entity.about if you found an empty string."
},
{
"ref":"aiobungie.objects.Entity.has_icon",
"url":15,
"doc":"A boolean that returns True if the entity has an icon."
},
{
"ref":"aiobungie.objects.Entity.hash",
"url":15,
"doc":"Entity's hash."
},
{
"ref":"aiobungie.objects.Entity.icon",
"url":15,
"doc":"Entity's icon"
},
{
"ref":"aiobungie.objects.Entity.index",
"url":15,
"doc":"Entity's index."
},
{
"ref":"aiobungie.objects.Entity.is_equippable",
"url":15,
"doc":"True if the entity can be equipped or False."
},
{
"ref":"aiobungie.objects.Entity.item_class",
"url":15,
"doc":"The entity's class type."
},
{
"ref":"aiobungie.objects.Entity.lore_hash",
"url":15,
"doc":"The entity's lore hash"
},
{
"ref":"aiobungie.objects.Entity.name",
"url":15,
"doc":"Entity's name"
},
{
"ref":"aiobungie.objects.Entity.stats",
"url":15,
"doc":"Entity's stats. this currently returns a dict object of the stats."
},
{
"ref":"aiobungie.objects.Entity.sub_type",
"url":15,
"doc":"The subtype of the entity. A type is a weapon or armor. A subtype is a handcannonn or leg armor for an example."
},
{
"ref":"aiobungie.objects.Entity.summary_hash",
"url":15,
"doc":"Entity's summary hash."
},
{
"ref":"aiobungie.objects.Entity.tier",
"url":15,
"doc":"Entity's \"tier."
},
{
"ref":"aiobungie.objects.Entity.tier_name",
"url":15,
"doc":"A string version of the item tier."
},
{
"ref":"aiobungie.objects.Entity.type",
"url":15,
"doc":"Entity's type."
},
{
"ref":"aiobungie.objects.Entity.type_name",
"url":15,
"doc":"Entity's type name. i.e.,  Grenade Launcher "
},
{
"ref":"aiobungie.objects.Entity.water_mark",
"url":15,
"doc":"Entity's water mark."
},
{
"ref":"aiobungie.objects.activity",
"url":18,
"doc":"Basic implementation for a Bungie a activity."
},
{
"ref":"aiobungie.objects.activity.Activity",
"url":18,
"doc":"Represents a Bungie Activity object. An activity can be one of  aiobungie.internal.enums.GameMode . Attributes      - mode:  aiobungie.internal.enums.GameMode The activity mode or type. is_completed:  builtins.str Check if the activity was completed or no. hash:  builtins.int The activity's hash. duration:  builtins.str A string of The activity's duration, Example format  7m 42s kills:  builtins.int Activity's Total kills deaths:  builtins.int Activity's total deaths. assists:  builtins.int Activity's Total assists kd:  builtins.int Activity's kd ration. member_type:  aiobungie.internal.enums.MembershipType The activity member's membership type. players_count:  builtins.int Total players in the activity. when: typing.Optional[datetime.datetime] When did the activity occurred in UTC datetime. Method generated by attrs for class Activity."
},
{
"ref":"aiobungie.objects.activity.Activity.as_dict",
"url":18,
"doc":"Returns a dict object of the Activity, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.objects.activity.Activity.assists",
"url":18,
"doc":"Activity's total assists."
},
{
"ref":"aiobungie.objects.activity.Activity.deaths",
"url":18,
"doc":"Activity's total deaths."
},
{
"ref":"aiobungie.objects.activity.Activity.duration",
"url":18,
"doc":"A string of The activity's duration, Example format  7m 42s "
},
{
"ref":"aiobungie.objects.activity.Activity.hash",
"url":18,
"doc":"The activity's hash."
},
{
"ref":"aiobungie.objects.activity.Activity.is_completed",
"url":18,
"doc":"Returns  Ok if the activity is completed and 'No' if not."
},
{
"ref":"aiobungie.objects.activity.Activity.kd",
"url":18,
"doc":"Activity's kill/death ration."
},
{
"ref":"aiobungie.objects.activity.Activity.kills",
"url":18,
"doc":"Activity's total kills."
},
{
"ref":"aiobungie.objects.activity.Activity.member_type",
"url":18,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.objects.activity.Activity.mode",
"url":18,
"doc":"Activity's game mode."
},
{
"ref":"aiobungie.objects.activity.Activity.player_count",
"url":18,
"doc":"Return an attribute of instance, which is of type owner."
},
{
"ref":"aiobungie.objects.activity.Activity.when",
"url":18,
"doc":"A UTC datetime object of when was the activivy started."
},
{
"ref":"aiobungie.objects.application",
"url":19,
"doc":"Basic implementation for a Bungie a application."
},
{
"ref":"aiobungie.objects.application.Application",
"url":19,
"doc":"Represents a Bungie developer application. Attributes      - name:  builtins.str The app's name id:  builtins.int The app's id. redirect_url: typing.Optional[ builtins.str ]: The app's redirect url, None if not Found. created_at:  datetime.datetime The application's creation date in UTC time. published_at:  datetime.datetime The application's publish date in UTC time. link:  builtins.str The app's link if it exists. status:  builtins.str The app's status. owner:  aiobungie.objects.ApplicationOwner An object of The application owner. scope:  builtins.str The app's scope Method generated by attrs for class Application."
},
{
"ref":"aiobungie.objects.application.Application.human_timedelta",
"url":19,
"doc":"Returns a human readble date of the app's creation date."
},
{
"ref":"aiobungie.objects.application.Application.as_dict",
"url":19,
"doc":"Returns a dict object of the application, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.objects.application.Application.created_at",
"url":19,
"doc":"App creation date in UTC timezone"
},
{
"ref":"aiobungie.objects.application.Application.id",
"url":19,
"doc":"App id"
},
{
"ref":"aiobungie.objects.application.Application.link",
"url":19,
"doc":"App's link"
},
{
"ref":"aiobungie.objects.application.Application.name",
"url":19,
"doc":"App name"
},
{
"ref":"aiobungie.objects.application.Application.owner",
"url":19,
"doc":"App's owner"
},
{
"ref":"aiobungie.objects.application.Application.published_at",
"url":19,
"doc":"App's publish date in UTC timezone"
},
{
"ref":"aiobungie.objects.application.Application.redirect_url",
"url":19,
"doc":"App redirect url"
},
{
"ref":"aiobungie.objects.application.Application.scope",
"url":19,
"doc":"App's scope"
},
{
"ref":"aiobungie.objects.application.Application.status",
"url":19,
"doc":"App's status"
},
{
"ref":"aiobungie.objects.application.ApplicationOwner",
"url":19,
"doc":"Represents a Bungie Application owner. Attributes      - name:  builtins.str The application owner name. id:  builtins.int The application owner bungie id. icon:  aiobungie.internal.assets.Image The application owner profile icon. is_public:  builtins.bool Determines if the application owner's profile was public or private type:  aiobungie.internal.enums.MembershipType The application owner's bungie membership type. Method generated by attrs for class ApplicationOwner."
},
{
"ref":"aiobungie.objects.application.ApplicationOwner.link",
"url":19,
"doc":"Returns the user's profile link."
},
{
"ref":"aiobungie.objects.application.ApplicationOwner.as_dict",
"url":19,
"doc":"Returns a dict object of the application owner, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.objects.application.ApplicationOwner.icon",
"url":19,
"doc":"The application owner's icon."
},
{
"ref":"aiobungie.objects.application.ApplicationOwner.id",
"url":19,
"doc":"The application owner's id."
},
{
"ref":"aiobungie.objects.application.ApplicationOwner.is_public",
"url":19,
"doc":"The application owner's profile privacy."
},
{
"ref":"aiobungie.objects.application.ApplicationOwner.name",
"url":19,
"doc":"The application owner name."
},
{
"ref":"aiobungie.objects.application.ApplicationOwner.type",
"url":19,
"doc":"The membership of the application owner."
},
{
"ref":"aiobungie.objects.character",
"url":17,
"doc":"Basic Implementation for a Bungie Character."
},
{
"ref":"aiobungie.objects.character.CharacterComponent",
"url":17,
"doc":"An interface for a Bungie character component. Method generated by attrs for class CharacterComponent."
},
{
"ref":"aiobungie.objects.character.CharacterComponent.member_type",
"url":17,
"doc":"The character's membership type."
},
{
"ref":"aiobungie.objects.character.CharacterComponent.id",
"url":17,
"doc":"The character's member id."
},
{
"ref":"aiobungie.objects.character.CharacterComponent.light",
"url":17,
"doc":"The character's light."
},
{
"ref":"aiobungie.objects.character.CharacterComponent.stats",
"url":17,
"doc":"The character's stats."
},
{
"ref":"aiobungie.objects.character.CharacterComponent.url",
"url":17,
"doc":"The character's url at bungie.net."
},
{
"ref":"aiobungie.objects.character.CharacterComponent.emblem",
"url":17,
"doc":"The character's current equipped emblem."
},
{
"ref":"aiobungie.objects.character.CharacterComponent.last_played",
"url":17,
"doc":"The character's last played time."
},
{
"ref":"aiobungie.objects.character.CharacterComponent.emblem_icon",
"url":17,
"doc":"The character's current equipped emblem icon."
},
{
"ref":"aiobungie.objects.character.CharacterComponent.emblem_hash",
"url":17,
"doc":"The character's current equipped emblem hash."
},
{
"ref":"aiobungie.objects.character.CharacterComponent.race",
"url":17,
"doc":"The character's race."
},
{
"ref":"aiobungie.objects.character.CharacterComponent.gender",
"url":17,
"doc":"The character's gender."
},
{
"ref":"aiobungie.objects.character.CharacterComponent.total_played_time",
"url":17,
"doc":"Character's total played time in hours."
},
{
"ref":"aiobungie.objects.character.CharacterComponent.class_type",
"url":17,
"doc":"The character's class."
},
{
"ref":"aiobungie.objects.character.CharacterComponent.title_hash",
"url":17,
"doc":"The character's title hash. This is Optional and can be None if no title was found."
},
{
"ref":"aiobungie.objects.character.CharacterComponent.human_timedelta",
"url":17,
"doc":"The player's last played time in a human readble date."
},
{
"ref":"aiobungie.objects.character.Character",
"url":17,
"doc":"An implementation for a Bungie character. A Bungie character object can be a Warlock, Titan or a Hunter. This can only be accessed using the  aiobungie.Component CHARACTERS component. Attributes      - light:  builtins.int The character's light id:  builtins.int The character's id gender:  aiobungie.internal.enums.Gender The character's gender race:  aiobungie.internal.enums.Race The character's race emblem:  aiobungie.internal.assets.Image The character's currnt equipped emblem. emblem_icon:  aiobungie.internal.assets.Image The character's current icon for the equipped emblem. emblem_hash:  builtins.int Character's emblem hash. last_played:  datetime.datetime When was this character last played date in UTC. total_played:  builtins.int Returns the total played time in seconds for the chosen character. member_id:  builtins.int The character's member id. class_type:  aiobungie.internal.enums.Class The character's class. level:  builtins.int Character's base level. stats:  aiobungie.internal.enums.Stat Character's current stats. title_hash:  typing.Optional[builtins.int] The hash of the character's equipped title, Returns  builtins.NoneType if no title is equipped. Method generated by attrs for class Character."
},
{
"ref":"aiobungie.objects.character.Character.url",
"url":17,
"doc":"A url for the character at bungie.net."
},
{
"ref":"aiobungie.objects.character.Character.as_dict",
"url":17,
"doc":"Returns a dict object of the character, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.objects.character.Character.class_type",
"url":17,
"doc":"Character's class."
},
{
"ref":"aiobungie.objects.character.Character.emblem",
"url":17,
"doc":"Character's emblem"
},
{
"ref":"aiobungie.objects.character.Character.emblem_hash",
"url":17,
"doc":"Character's emblem hash."
},
{
"ref":"aiobungie.objects.character.Character.emblem_icon",
"url":17,
"doc":"Character's emblem icon"
},
{
"ref":"aiobungie.objects.character.Character.gender",
"url":17,
"doc":"Character's gender"
},
{
"ref":"aiobungie.objects.character.Character.id",
"url":17,
"doc":"Character's id"
},
{
"ref":"aiobungie.objects.character.Character.last_played",
"url":17,
"doc":"Character's last played date."
},
{
"ref":"aiobungie.objects.character.Character.level",
"url":17,
"doc":"Character's base level."
},
{
"ref":"aiobungie.objects.character.Character.light",
"url":17,
"doc":"Character's light"
},
{
"ref":"aiobungie.objects.character.Character.member_id",
"url":17,
"doc":"The character's member id."
},
{
"ref":"aiobungie.objects.character.Character.member_type",
"url":17,
"doc":"The character's memberhip type."
},
{
"ref":"aiobungie.objects.character.Character.race",
"url":17,
"doc":"Character's race"
},
{
"ref":"aiobungie.objects.character.Character.stats",
"url":17,
"doc":"Character stats."
},
{
"ref":"aiobungie.objects.character.Character.title_hash",
"url":17,
"doc":"Character's equipped title hash."
},
{
"ref":"aiobungie.objects.character.Character.total_played_time",
"url":17,
"doc":"Character's total plyed time minutes."
},
{
"ref":"aiobungie.objects.character.Character.human_timedelta",
"url":17,
"doc":"The player's last played time in a human readble date."
},
{
"ref":"aiobungie.objects.clans",
"url":20,
"doc":"Basic implementation for a Bungie a clan."
},
{
"ref":"aiobungie.objects.clans.Clan",
"url":20,
"doc":"Represents a Bungie clan object. Attributes      - name:  builtins.str The clan's name id:  builtins.int The clans's id created_at:  datetime.datetime Returns the clan's creation date in UTC time. description:  builtins.str The clan's description. is_public:  builtins.bool Returns True if the clan is public and False if not. banner:  aiobungie.internal.assets.Image Returns the clan's banner avatar:  aiobungie.internal.assets.Image Returns the clan's avatar about:  builtins.str The clan's about. tags:  builtins.str The clan's tags owner:  aiobungie.objects.ClanOwner Returns an object of the clan's owner. See  aiobungie.objects.ClanOwner for info. Method generated by attrs for class Clan."
},
{
"ref":"aiobungie.objects.clans.Clan.human_timedelta",
"url":20,
"doc":"Returns a human readble date of the clan's creation date."
},
{
"ref":"aiobungie.objects.clans.Clan.url",
"url":20,
"doc":""
},
{
"ref":"aiobungie.objects.clans.Clan.as_dict",
"url":20,
"doc":"Returns an instance of the object as a dict"
},
{
"ref":"aiobungie.objects.clans.Clan.about",
"url":20,
"doc":"Clan's about title."
},
{
"ref":"aiobungie.objects.clans.Clan.avatar",
"url":20,
"doc":"Clan's avatar"
},
{
"ref":"aiobungie.objects.clans.Clan.banner",
"url":20,
"doc":"Clan's banner"
},
{
"ref":"aiobungie.objects.clans.Clan.created_at",
"url":20,
"doc":"Clan's creation date time in UTC."
},
{
"ref":"aiobungie.objects.clans.Clan.description",
"url":20,
"doc":"Clan's description"
},
{
"ref":"aiobungie.objects.clans.Clan.id",
"url":20,
"doc":"The clan id"
},
{
"ref":"aiobungie.objects.clans.Clan.is_public",
"url":20,
"doc":"Clan's privacy status."
},
{
"ref":"aiobungie.objects.clans.Clan.member_count",
"url":20,
"doc":"Clan's member count."
},
{
"ref":"aiobungie.objects.clans.Clan.name",
"url":20,
"doc":"The clan's name"
},
{
"ref":"aiobungie.objects.clans.Clan.owner",
"url":20,
"doc":"The clan owner."
},
{
"ref":"aiobungie.objects.clans.Clan.tags",
"url":20,
"doc":"A list of the clan's tags."
},
{
"ref":"aiobungie.objects.clans.ClanOwner",
"url":20,
"doc":"Represents a Bungie clan owner. Attributes      - id:  builtins.int The clan owner's membership id name:  builtins.str The clan owner's display name last_online:  builtins.str An aware  builtins.str version of a  datetime.datetime object. type:  aiobungie.internal.enums.MembershipType Returns the clan owner's membership type. This could be Xbox, Steam, PSN, Blizzard or ALL, if the membership type is not recognized it will return  builtins.NoneType . clan_id:  builtins.int The clan owner's clan id joined_at: Optional[datetime.datetime]: The clan owner's join date in UTC. icon:  aiobungie.internal.assets.Image Returns the clan owner's icon from Image. is_public:  builtins.bool Returns True if the clan's owner profile is public or False if not. types: typing.List[builtins.int]: returns a List of  builtins.int of the clan owner's types. Method generated by attrs for class ClanOwner."
},
{
"ref":"aiobungie.objects.clans.ClanOwner.human_timedelta",
"url":20,
"doc":"Returns a human readble date of the clan owner's last login."
},
{
"ref":"aiobungie.objects.clans.ClanOwner.link",
"url":20,
"doc":"Returns the user's profile link."
},
{
"ref":"aiobungie.objects.clans.ClanOwner.as_dict",
"url":20,
"doc":"Returns a dict object of the clan owner, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.objects.clans.ClanOwner.clan_id",
"url":20,
"doc":"Owner's current clan id."
},
{
"ref":"aiobungie.objects.clans.ClanOwner.icon",
"url":20,
"doc":"Owner's profile icom"
},
{
"ref":"aiobungie.objects.clans.ClanOwner.id",
"url":20,
"doc":"The user id."
},
{
"ref":"aiobungie.objects.clans.ClanOwner.is_public",
"url":20,
"doc":"Returns if the user profile is public or no."
},
{
"ref":"aiobungie.objects.clans.ClanOwner.joined_at",
"url":20,
"doc":"Owner's bungie join date."
},
{
"ref":"aiobungie.objects.clans.ClanOwner.last_online",
"url":20,
"doc":"An aware  datetime.datetime object of the user's last online date UTC."
},
{
"ref":"aiobungie.objects.clans.ClanOwner.name",
"url":20,
"doc":"The user name."
},
{
"ref":"aiobungie.objects.clans.ClanOwner.type",
"url":20,
"doc":"Returns the membership type of the user."
},
{
"ref":"aiobungie.objects.clans.ClanOwner.types",
"url":20,
"doc":"Returns a list of the member ship's membership types."
},
{
"ref":"aiobungie.objects.entity",
"url":21,
"doc":"A basic bungie entity definition implementation. This is still not fully implemented and you may experince bugs."
},
{
"ref":"aiobungie.objects.entity.PartialEntity",
"url":21,
"doc":"A partial interface for a bungie entity All bungie entities has a hash and an index. but other fields are optional. it may or may not be present. Method generated by attrs for class PartialEntity."
},
{
"ref":"aiobungie.objects.entity.PartialEntity.app",
"url":21,
"doc":"A client that we may use to make rest calls."
},
{
"ref":"aiobungie.objects.entity.PartialEntity.name",
"url":21,
"doc":"Entity's name"
},
{
"ref":"aiobungie.objects.entity.PartialEntity.icon",
"url":21,
"doc":"An optional entity's icon if its filled."
},
{
"ref":"aiobungie.objects.entity.PartialEntity.banner",
"url":21,
"doc":"An optional benner of the entity if its filled."
},
{
"ref":"aiobungie.objects.entity.PartialEntity.has_icon",
"url":21,
"doc":"A boolean that returns True if the entity has an icon."
},
{
"ref":"aiobungie.objects.entity.PartialEntity.description",
"url":21,
"doc":"Entity's description"
},
{
"ref":"aiobungie.objects.entity.PartialEntity.type_name",
"url":21,
"doc":"Entity's type name. i.e.,  Grenade Launcher "
},
{
"ref":"aiobungie.objects.entity.PartialEntity.water_mark",
"url":21,
"doc":"Entity's water mark."
},
{
"ref":"aiobungie.objects.entity.PartialEntity.tier",
"url":21,
"doc":"Entity's \"tier."
},
{
"ref":"aiobungie.objects.entity.PartialEntity.tier_name",
"url":21,
"doc":"A  builtins.str version of the entity's tier and name."
},
{
"ref":"aiobungie.objects.entity.PartialEntity.type",
"url":21,
"doc":"The entity's type, None if unknown"
},
{
"ref":"aiobungie.objects.entity.PartialEntity.bucket_type",
"url":21,
"doc":"Entity's bucket type."
},
{
"ref":"aiobungie.objects.entity.PartialEntity.stats",
"url":21,
"doc":"Entity's stats. this currently returns a dict object of the stats."
},
{
"ref":"aiobungie.objects.entity.PartialEntity.ammo_type",
"url":21,
"doc":"Entity's ammo type if it was a wepon, otherwise it will return None"
},
{
"ref":"aiobungie.objects.entity.PartialEntity.lore_hash",
"url":21,
"doc":"The entity's lore hash"
},
{
"ref":"aiobungie.objects.entity.PartialEntity.item_class",
"url":21,
"doc":"The entity's class type."
},
{
"ref":"aiobungie.objects.entity.PartialEntity.sub_type",
"url":21,
"doc":"The subtype of the entity. A type is a weapon or armor. A subtype is a handcannonn or leg armor for an example."
},
{
"ref":"aiobungie.objects.entity.PartialEntity.is_equippable",
"url":21,
"doc":"True if the entity can be equipped or False."
},
{
"ref":"aiobungie.objects.entity.PartialEntity.summary_hash",
"url":21,
"doc":"Entity's summary hash."
},
{
"ref":"aiobungie.objects.entity.PartialEntity.damage",
"url":21,
"doc":"Entity's damage type. Only works for weapons."
},
{
"ref":"aiobungie.objects.entity.PartialEntity.about",
"url":21,
"doc":"Entity's about. you probably wanna use this instaed  Entity.description "
},
{
"ref":"aiobungie.objects.entity.Entity",
"url":21,
"doc":"A concrate implementation of a Bungie Item Definition Entity. As bungie says. using this endpoint is still in beta and may experience rough edges and bugs. Method generated by attrs for class Entity."
},
{
"ref":"aiobungie.objects.entity.Entity.as_dict",
"url":21,
"doc":"Returns an instance of the object as a dict"
},
{
"ref":"aiobungie.objects.entity.Entity.about",
"url":21,
"doc":"Entity's about."
},
{
"ref":"aiobungie.objects.entity.Entity.ammo_type",
"url":21,
"doc":"Entity's ammo type if it was a wepon, otherwise it will return None"
},
{
"ref":"aiobungie.objects.entity.Entity.app",
"url":21,
"doc":"A client that we may use to make rest calls."
},
{
"ref":"aiobungie.objects.entity.Entity.banner",
"url":21,
"doc":"Entity's banner."
},
{
"ref":"aiobungie.objects.entity.Entity.bucket_type",
"url":21,
"doc":"The entity's bucket type, None if unknown"
},
{
"ref":"aiobungie.objects.entity.Entity.damage",
"url":21,
"doc":"Entity's damage type. Only works for weapons."
},
{
"ref":"aiobungie.objects.entity.Entity.description",
"url":21,
"doc":"Entity's description. most entities don't use this so consider using  Entity.about if you found an empty string."
},
{
"ref":"aiobungie.objects.entity.Entity.has_icon",
"url":21,
"doc":"A boolean that returns True if the entity has an icon."
},
{
"ref":"aiobungie.objects.entity.Entity.hash",
"url":21,
"doc":"Entity's hash."
},
{
"ref":"aiobungie.objects.entity.Entity.icon",
"url":21,
"doc":"Entity's icon"
},
{
"ref":"aiobungie.objects.entity.Entity.index",
"url":21,
"doc":"Entity's index."
},
{
"ref":"aiobungie.objects.entity.Entity.is_equippable",
"url":21,
"doc":"True if the entity can be equipped or False."
},
{
"ref":"aiobungie.objects.entity.Entity.item_class",
"url":21,
"doc":"The entity's class type."
},
{
"ref":"aiobungie.objects.entity.Entity.lore_hash",
"url":21,
"doc":"The entity's lore hash"
},
{
"ref":"aiobungie.objects.entity.Entity.name",
"url":21,
"doc":"Entity's name"
},
{
"ref":"aiobungie.objects.entity.Entity.stats",
"url":21,
"doc":"Entity's stats. this currently returns a dict object of the stats."
},
{
"ref":"aiobungie.objects.entity.Entity.sub_type",
"url":21,
"doc":"The subtype of the entity. A type is a weapon or armor. A subtype is a handcannonn or leg armor for an example."
},
{
"ref":"aiobungie.objects.entity.Entity.summary_hash",
"url":21,
"doc":"Entity's summary hash."
},
{
"ref":"aiobungie.objects.entity.Entity.tier",
"url":21,
"doc":"Entity's \"tier."
},
{
"ref":"aiobungie.objects.entity.Entity.tier_name",
"url":21,
"doc":"A string version of the item tier."
},
{
"ref":"aiobungie.objects.entity.Entity.type",
"url":21,
"doc":"Entity's type."
},
{
"ref":"aiobungie.objects.entity.Entity.type_name",
"url":21,
"doc":"Entity's type name. i.e.,  Grenade Launcher "
},
{
"ref":"aiobungie.objects.entity.Entity.water_mark",
"url":21,
"doc":"Entity's water mark."
},
{
"ref":"aiobungie.objects.player",
"url":22,
"doc":"Basic implementation for a Bungie a player."
},
{
"ref":"aiobungie.objects.player.Player",
"url":22,
"doc":"Represents a Bungie Destiny 2 Player. Attributes      icon:  aiobungie.internal.Image The player's icon. id:  builtins.int The player's id. name:  builtins.str The player's name. is_public:  builtins.bool A boolean True if the user's profile is public and False if not. type:  aiobungie.internal.enums.MembershipType The player's membership type. Method generated by attrs for class Player."
},
{
"ref":"aiobungie.objects.player.Player.as_dict",
"url":22,
"doc":"Returns a dict object of the player, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.objects.player.Player.icon",
"url":22,
"doc":"The player's icon."
},
{
"ref":"aiobungie.objects.player.Player.id",
"url":22,
"doc":"The player's id."
},
{
"ref":"aiobungie.objects.player.Player.is_public",
"url":22,
"doc":"The player's profile privacy."
},
{
"ref":"aiobungie.objects.player.Player.name",
"url":22,
"doc":"The player's name"
},
{
"ref":"aiobungie.objects.player.Player.type",
"url":22,
"doc":"The profile's membership type."
},
{
"ref":"aiobungie.objects.player.Player.link",
"url":16,
"doc":"Returns the user's profile link."
},
{
"ref":"aiobungie.objects.profile",
"url":23,
"doc":"Implementation for a Bungie a Profile."
},
{
"ref":"aiobungie.objects.profile.Profile",
"url":23,
"doc":"Represents a Bungie member Profile. Bungie profiles requires components. but in aiobungie you don't need to select a specific component since they will all/will be implemented. for an example: to access the  Character component you'll need to pass  ?component=200 right?. in aiobungie you can just do this.   profile = await client.fetch_profile(\"Fate\")  access the character component and get my warlock. warlock = await profile.warlock() assert warlock.light  1320   Attributes      id:  builtins.int Profile's id name:  builtins.str Profile's name type:  aiobungie.internal.enums.MembershipType The profile's membership type. last_played:  datetime.datetime The profile owner's last played date in UTC character_ids:  typing.List[builtins.int] A list of the profile's character ids. power_cap:  builtins.int The profile's current season power cap. Method generated by attrs for class Profile."
},
{
"ref":"aiobungie.objects.profile.Profile.as_dict",
"url":23,
"doc":"Returns a dict object of the profile, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.objects.profile.Profile.human_timedelta",
"url":23,
"doc":"Returns last_played attr but in human delta date."
},
{
"ref":"aiobungie.objects.profile.Profile.app",
"url":23,
"doc":"A client that we may to make rest requests."
},
{
"ref":"aiobungie.objects.profile.Profile.character_ids",
"url":23,
"doc":"A list of the profile's character ids."
},
{
"ref":"aiobungie.objects.profile.Profile.id",
"url":23,
"doc":"Profile's id"
},
{
"ref":"aiobungie.objects.profile.Profile.is_public",
"url":23,
"doc":"Profile's privacy status."
},
{
"ref":"aiobungie.objects.profile.Profile.last_played",
"url":23,
"doc":"Profile's last played Destiny 2 played date."
},
{
"ref":"aiobungie.objects.profile.Profile.name",
"url":23,
"doc":"Profile's name."
},
{
"ref":"aiobungie.objects.profile.Profile.power_cap",
"url":23,
"doc":"The profile's current seaspn power cap."
},
{
"ref":"aiobungie.objects.profile.Profile.type",
"url":23,
"doc":"Profile's type."
},
{
"ref":"aiobungie.objects.user",
"url":16,
"doc":"Basic implementation for a Bungie a user."
},
{
"ref":"aiobungie.objects.user.User",
"url":16,
"doc":"Represents Bungie User object. Attributes      id:  builtins.int The user's id name:  builtins.str The user's name. is_deleted:  builtins.bool Returns True if the user is deleted about: typing.Optional[builtins.str] The user's about, Default is None if nothing is Found. created_at:  datetime.datetime The user's creation date in UTC date. updated_at:  datetime.datetime The user's last updated om UTC date. psn_name: typing.Optional[builtins.str] The user's psn id if it exists. twitch_name: typing.Optional[builtins.str] The user's twitch name if it exists. blizzard_name: typing.Optional[builtins.str] The user's blizzard name if it exists. steam_name: typing.Optional[builtins.str] The user's steam name if it exists status: typing.Optional[builtins.str] The user's bungie status text locale: typing.Optional[builtins.str] The user's locale. picture: aiobungie.internal.assets.Image The user's avatar. Method generated by attrs for class User."
},
{
"ref":"aiobungie.objects.user.User.as_dict",
"url":16,
"doc":"Returns a dict object of the user, This function is useful if you're binding to other REST apis."
},
{
"ref":"aiobungie.objects.user.User.about",
"url":16,
"doc":"The user's about, Default is None if nothing is Found."
},
{
"ref":"aiobungie.objects.user.User.blizzard_name",
"url":16,
"doc":"The user's blizzard name if it exists."
},
{
"ref":"aiobungie.objects.user.User.created_at",
"url":16,
"doc":"The user's creation date in UTC timezone."
},
{
"ref":"aiobungie.objects.user.User.id",
"url":16,
"doc":"The user's id"
},
{
"ref":"aiobungie.objects.user.User.is_deleted",
"url":16,
"doc":"Returns True if the user is deleted"
},
{
"ref":"aiobungie.objects.user.User.locale",
"url":16,
"doc":"The user's locale."
},
{
"ref":"aiobungie.objects.user.User.name",
"url":16,
"doc":"The user's name."
},
{
"ref":"aiobungie.objects.user.User.picture",
"url":16,
"doc":"The user's profile picture."
},
{
"ref":"aiobungie.objects.user.User.psn_name",
"url":16,
"doc":"The user's psn id if it exists."
},
{
"ref":"aiobungie.objects.user.User.status",
"url":16,
"doc":"The user's bungie status text"
},
{
"ref":"aiobungie.objects.user.User.steam_name",
"url":16,
"doc":"The user's steam name if it exists"
},
{
"ref":"aiobungie.objects.user.User.twitch_name",
"url":16,
"doc":"The user's twitch name if it exists."
},
{
"ref":"aiobungie.objects.user.User.updated_at",
"url":16,
"doc":"The user's last updated om UTC date."
},
{
"ref":"aiobungie.objects.user.PartialUser",
"url":16,
"doc":"The partial user object. Method generated by attrs for class PartialUser."
},
{
"ref":"aiobungie.objects.user.PartialUser.steam_name",
"url":16,
"doc":"The user's steam username or None."
},
{
"ref":"aiobungie.objects.user.PartialUser.twitch_name",
"url":16,
"doc":"The user's twitch username or None."
},
{
"ref":"aiobungie.objects.user.PartialUser.blizzard_name",
"url":16,
"doc":"The user's blizzard username or None."
},
{
"ref":"aiobungie.objects.user.PartialUser.psn_name",
"url":16,
"doc":"The user's psn username or None."
},
{
"ref":"aiobungie.objects.user.PartialUser.about",
"url":16,
"doc":"The user's about section."
},
{
"ref":"aiobungie.objects.user.PartialUser.locale",
"url":16,
"doc":"The user's profile locale."
},
{
"ref":"aiobungie.objects.user.PartialUser.name",
"url":16,
"doc":"The user's name."
},
{
"ref":"aiobungie.objects.user.PartialUser.picture",
"url":16,
"doc":"The user's profile picture if its set."
},
{
"ref":"aiobungie.objects.user.PartialUser.updated_at",
"url":16,
"doc":"The user's last profile update."
},
{
"ref":"aiobungie.objects.user.PartialUser.is_deleted",
"url":16,
"doc":"Determines if the user is deleted or not."
},
{
"ref":"aiobungie.objects.user.PartialUser.status",
"url":16,
"doc":"The user's profile status."
},
{
"ref":"aiobungie.objects.user.PartialUser.created_at",
"url":16,
"doc":"Retruns the user's creation date in UTC timezone."
},
{
"ref":"aiobungie.objects.user.PartialUser.human_timedelta",
"url":16,
"doc":""
},
{
"ref":"aiobungie.objects.user.UserLike",
"url":16,
"doc":"The is meant for any Member / user / like objects."
},
{
"ref":"aiobungie.objects.user.UserLike.name",
"url":16,
"doc":"The user's name."
},
{
"ref":"aiobungie.objects.user.UserLike.is_public",
"url":16,
"doc":"Returns if the user profile is public or no."
},
{
"ref":"aiobungie.objects.user.UserLike.type",
"url":16,
"doc":"Returns the user type of the user."
},
{
"ref":"aiobungie.objects.user.UserLike.icon",
"url":16,
"doc":"The user's icon."
},
{
"ref":"aiobungie.objects.user.UserLike.link",
"url":16,
"doc":"Returns the user's profile link."
},
{
"ref":"aiobungie.objects.user.UserLike.as_dict",
"url":16,
"doc":"Returns an instance of the object attrs as a dict."
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