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

import os
from typing import Any, Dict

from dotenv import load_dotenv

import aiobungie

load_dotenv()
TOKEN = str(os.environ["TOKEN"])

data: Dict[str, Any] = {
    "me": "Fate怒",
    "id": 20315338,
    "app": 33226,
    "clanid": 4389205,
    "memid": 4611686018484639825,
    "charid": 2305843009444904605,
    "char": aiobungie.Class.WARLOCK,
    "memtype": aiobungie.MembershipType.STEAM,
    "vendor": aiobungie.Vendor.SPIDER,
}


types: Dict[str, str] = {
    'inventory_item_def': 'DestinyInventoryItemDefinition',
    'place_def': 'DestinyPlaceDefinition',
    'activ_def': 'DestinyActivityDefinition',
    'activ_type_def': 'DestinyActivityTypeDefinition',
    'activity_mode_def': 'DestinyActivityModeDefinition',
    'class_def': 'DestinyClassDefinition',
    'bucket_def': 'DestinyInventoryBucketDefinition',
    'milestone_def': 'DestinyMilestoneDefinition',
}