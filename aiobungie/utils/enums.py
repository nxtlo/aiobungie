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

'''Bungie enums impl for aiobungie.'''


from __future__ import annotations

__all__: typing.Sequence[str] = (
    'GameMode',
    'MembershipType',
    'DestinyCharacter',
    'DestinyMilestoneType',
    'DestinyRace',
    'Vendor',
    'Raid',
    'Dungeon',
    'DestinyGender',
    'Component'
)

import typing
import enum

@typing.final
class Raid(enum.Enum):
    DSC     = 910380154
    LW      = 2122313384
    VOG     = 3881495763
    GOS     = 3458480158

    def __int__(self) -> int:
        return int(self.value)
    
    def __str__(self) -> str:
        return str(self.name)
        
@typing.final
class Dungeon(enum.Enum):
    PRESAGE     = 0
    HARBINGER   = 0
    PROPHECY    = 0
    POH         = 0
    SHATTERED   = 0
    ZEROHOUR    = 0
    WHISPER     = 0
    
    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)


@typing.final
class Vendor(enum.Enum):
    ZAVALA  = 69482069
    XUR     = 2190858386
    BANSHE  = 672118013
    SPIDER  = 863940356

    def __str__(self) -> str:
        return (str(self.name))


    def __int__(self) -> int:
        return int(self.value)
@typing.final
class GameMode(enum.Enum):
    NOTHING = 0
    STORY   = 2
    STRIKE  = 3
    RAID    = 4
    ALLPVP  = 5
    PATROL  = 6
    ALLPVE  = 7
    TOF     = 14
    '''Trials Of Osiris'''
    CONTROL     = 10
    NIGHTFALL   = 16
    IRONBANER   = 19
    ALLSTRIKES  = 18
    DUNGEON     = 82
    GAMBIT      = 63

    def __str__(self) -> str:
        return (str(self.name))


    def __int__(self) -> int:
        return int(self.value)

@typing.final
class Component(enum.Enum):
    NOTHING     = 0
    PROFILE     = 100
    SILVER      = 105
    PROGRESSION = 104
    INVENTORIES = 102
    CHARECTERS  = 200
    CHAR_INVENTORY = 201
    CHARECTER_PROGRESSION = 202
    EQUIPED_ITEMS   = 205
    VENDORS     = 400
    RECORDS     = 900
    VENDOR_SALES    = 402

    def __str__(self) -> str:
        return (str(self.name))

    def __int__(self) -> int:
        return int(self.value)

@typing.final
class MembershipType(enum.Enum):
    NONE        = 0
    XBOX        = 1
    PSN         = 2
    STEAM       = 3
    BLIZZARD    = 4
    ALL         = -1

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)

@typing.final
class DestinyCharacter(enum.Enum):
    TITAN   = 0
    HUNTER  = 1
    WARLOCK = 2
    UNKNOWN = 3

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)

@typing.final
class DestinyGender(enum.Enum):
    MALE    = 0
    FEMALE  = 1
    UNKNOWN = 2

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)

@typing.final
class DestinyRace(enum.Enum):
    HUMAN   = 0
    AWOKEN  = 1
    EXO     = 2
    UNKNOWN = 3

    def __str__(self) -> str:
        return str(self.name)

    def __int__(self) -> int:
        return int(self.value)

@typing.final
class DestinyMilestoneType(enum.Enum):
    UNKNOWN     = 0
    TUTORIAL    = 1
    ONETIME     = 2
    WEEKLY      = 3
    DAILY       = 4
    SPECIAL     = 5
