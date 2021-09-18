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

"""Time formatting module."""


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

from dateutil.parser import parse

DateSigT = typing.TypeVar("DateSigT", covariant=True)
"""A type hint for the Date type signature."""


def format_played(mins: int, *, suffix: bool = False) -> str:
    """
    Converts A Bungie's total played time in minutes
    to a a readable time.
    """
    hrs = math.floor(mins // 60)
    seconds = math.floor(mins % 60)
    return f"{hrs} hours{' and' if suffix else ''} {seconds} seconds."


def from_timestamp(timer: int) -> datetime.datetime:
    """
    Converts timestamp to `datetime.datetime`
    """
    return datetime.datetime.utcfromtimestamp(timer)


def clean_date(date: str) -> datetime.datetime:
    """Formats `datetime.datetime` to a readable date."""
    parsed = parse(date)
    ts = to_timestamp(parsed)  # had to do it in two ways.
    ft = from_timestamp(ts)
    return ft


def to_timestamp(date: datetime.datetime) -> int:
    """
    Converts datetime.datetime.utctimetuple() to timestamp.
    """
    try:
        return calendar.timegm(date.timetuple())
    except Exception as e:
        raise e


class DateAware(typing.Generic[DateSigT]):
    """A Generic date parser which converts ISO string datetime
    to an aware datetime and from-to timestamp and datetime.
    """

    __slots__: tuple[str, ...] = ("_entry",)

    def __init__(self, entry: DateSigT) -> None:
        self._entry = entry

    @property
    def raw(self) -> DateSigT:
        return self._entry

    def to_datetime(self) -> datetime.datetime:
        if isinstance(self._entry, str):
            if self._entry.endswith(("z", "Z")):
                new = self._entry[:-1]  # type: ignore
                return datetime.datetime.fromisoformat(new)

        elif isinstance(self._entry, (float, int)):
            return datetime.datetime.utcfromtimestamp(self._entry)

        raise TypeError(
            f"Entry must be one of (float, str) not {type(self._entry).__name__}"
        )

    def to_timestamp(self) -> float:
        return datetime.datetime.timestamp(self.to_datetime())

    def timestamp_to_datetime(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self.to_timestamp())
