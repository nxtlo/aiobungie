from enum import Enum


class DestinyRace(Enum):
    HUMAN = 0
    AWOKEN = 1
    EXO = 2
    UNKNOWN = 3



class DestinyMilestoneType(Enum):
    UNKNOWN = 0
    TUTORIAL = 1
    ONETIME = 2
    WEEKLY = 3
    DAILY = 4
    SPECIAL = 5
