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
from typing import TypedDict, Dict, Any, List, Optional
from ..utils import ImageProtocol
from .user import UserCard
from ..utils.enums import MembershipType
from datetime import datetime

class ClanOwnerResponse(UserCard, total=False):
	groupId: int
	joinDate: datetime

class ClanResponse(TypedDict):
	id: int
	name: str
	created_at: datetime
	edited_at: datetime
	member_count: int
	description: str
	is_public: bool
	banner: ImageProtocol
	avatar: ImageProtocol
	about: str
	tag: str
	owner: str

class ClanOwner(ClanOwnerResponse):
	founder: Dict[str, Any] # TODO: Make this Dict[str, ClanOwnerResponse]

class Clan(ClanResponse, total=False):
	Response: Dict[Any, ClanResponse]