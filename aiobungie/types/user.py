from typing import TypedDict, List
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
	lastOnlineStatusChange: str