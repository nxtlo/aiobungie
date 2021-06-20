'''
MIT License

Copyright (c) 2020 - Present nxtlo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import typing
import types

__all__: typing.Sequence[str] = (
    'GameMode',
    'MembershipType',
    'DestinyCharecter',
    'DestinyMilestoneType',
    'DestinyRace',
    'Vendor',
    'Raid',
    'Dungeon'
)


class Raid:
    def __init__(self, *, raid: int = None) -> None:
        self.raid = raid
        super().__init__()
    DSC     = 910380154
    LW      = 2122313384
    VOG     = 3881495763
    GOS     = 3458480158
    
    def __str__(self):
        if self.raid == self.DSC:
            return 'Deep Stone Crypt'
        elif self.raid == self.LW:
            return 'Last Wish'
        elif self.raid == self.VOG:
            return 'Vault of Glass'
        elif self.raid == self.GOS:
            return 'Garden of Salvation'
        return self

class Dungeon:
    PRESAGE     = ...
    HARBINGER   = ...
    PROPHECY    = ...
    POH         = ...
    SHATTERED   = ...
    ZEROHOUR    = ...
    WHISPER     = ...


class Vendor:
    ZAVALA  = 69482069
    XUR     = 2190858386
    BANSHE  = 672118013
    SPIDER  = 863940356

class GameMode:
    NOTHING = None
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


class MembershipType:
    NONE        = 0
    XBOX        = 1
    PSN         = 2
    STEAM       = 3
    BLIZZARD    = 4
    ALL         = -1


class DestinyCharecter:
    TITAN   = 0
    HUNTER  = 1
    WARLOCK = 2
    UNKNOWN = 3


class DestinyRace:
    HUMAN   = 0
    AWOKEN  = 1
    EXO     = 2
    UNKNOWN = 3


class DestinyMilestoneType:
    UNKNOWN     = 0
    TUTORIAL    = 1
    ONETIME     = 2
    WEEKLY      = 3
    DAILY       = 4
    SPECIAL     = 5