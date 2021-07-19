from typing import TypedDict, List, Optional, Union
from ..utils import Image
from ..utils.enums import MembershipType
from datetime import datetime


class UserCard(TypedDict):
    iconPath: Image
    isPublic: bool
    displayName: str
    applicableMembershipTypes: List[int]
    membershipType: MembershipType
    membershipId: int


class User(UserCard, total=False):
    isDeleted: bool
    about: Optional[str]
    firstAccess: str
    lastUpdate: str
    psnDisplayName: Optional[str]
    locale: str
    profilePicturePath: Optional[Image]
    statusText: Optional[str]
    blizzardDisplayName: Optional[str]
    steamDisplayName: Optional[str]
    twitchDisplayName: Optional[str]
