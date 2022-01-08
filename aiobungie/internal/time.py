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

"""Time helper functions."""


from __future__ import annotations

__all__: list[str] = [
    "format_played",
    "from_timestamp",
    "clean_date",
    "to_timestamp",
]

import calendar
import datetime
import math
import typing

import dateutil.parser


def format_played(mins: int, /, *, suffix: bool = False) -> str:
    """Converts A memberships's total played time from minutes to a readable string."""
    hrs = math.floor(mins // 60)
    seconds = math.floor(mins % 60)
    return f"{hrs} hours{' and' if suffix else ''} {seconds} seconds."


def from_timestamp(timer: typing.Union[int, float], /) -> datetime.datetime:
    """Converts a timestamp to `datetime.datetime`"""
    return datetime.datetime.utcfromtimestamp(timer)


def clean_date(iso_date: str, /) -> datetime.datetime:
    """Parse a Bungie ISO format string date to a Python `datetime.datetime` object."""
    parsed = dateutil.parser.parse(iso_date)
    ts = to_timestamp(parsed)  # had to do it in two ways...
    return from_timestamp(ts)


def to_timestamp(date: datetime.datetime, /) -> int:
    """Converts `datetime.datetime` to timestamp."""
    return calendar.timegm(date.timetuple())
