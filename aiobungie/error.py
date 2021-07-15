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

'''aiobungie Exceptions.'''

from __future__ import annotations

__all__: Sequence[str] = (
    'PlayerNotFound', 'HashError',
    'ActivityNotFound', 'CharacterTypeError',
    'JsonError', 'ClanNotFound', 'CharacterNotFound',
    'NotFound', 'HTTPException', 'UserNotFound'
)

from typing import final, Sequence

@final
class PlayerNotFound(Exception):
    """Raised when a :class:`.Player` is not found."""
    pass

@final
class HashError(Exception):
    """Raised when :meth:`.Activity.hash` used for modes that are not raids."""
    pass

@final
class ActivityNotFound(Exception):
    """Raised when a :class:`.Activity` not found."""
    pass

@final
class CharacterTypeError(Exception):
    pass

@final
class JsonError(Exception):
    """Raised when an HTTP request did not return a json response."""
    pass

@final
class CharacterNotFound(Exception):
    """Raised when a :class:`.Character` not found."""
    pass

@final
class HTTPException(Exception):
    """Exception for handling :class:`.HTTPClient` requests errors."""
    pass

@final
class ClanNotFound(Exception):
    """Raised when a :class:`.Clan` not found."""
    pass

@final
class NotFound(Exception):
    """Raised when an unknown request was not found."""
    pass

@final
class UserNotFound(Exception):
    '''Raised when a :class:`.User` not found.'''
    pass