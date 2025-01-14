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

__all__ = (
    "from_timestamp",
    "clean_date",
    "parse_date_range",
    "monotonic",
)

import datetime
import sys as _sys
import time as _time
import warnings

_has_backport = True
if _sys.version_info.minor == 10:
    try:
        from backports.datetime_fromisoformat import MonkeyPatch  # pyright: ignore

        MonkeyPatch.patch_fromisoformat()  # pyright: ignore[reportUnknownMemberType]
    except ModuleNotFoundError:
        _has_backport = False
        warnings.warn(
            "The backports module is required for Python 3.10 compatibility.\n"
            "Please install it with `pip install backports-datetime-fromisoformat`"
        )


def from_timestamp(
    timestamp: int | float, tz: datetime.timezone = datetime.timezone.utc, /
) -> datetime.datetime:
    """Converts a timestamp to `datetime.datetime`"""
    return datetime.datetime.fromtimestamp(float(timestamp), tz=tz)


def clean_date(iso_date: str, /) -> datetime.datetime:
    """Parse an `ISO8601` string datetime into a Python `datetime.datetime` object."""
    # Python 3.10 doesn't parse all ISO8601 formats, Need a backport for that.
    if not _has_backport:
        return datetime.datetime.min

    return datetime.datetime.fromisoformat(iso_date)


def parse_date_range(
    end: datetime.datetime | None = None,
    start: datetime.datetime | None = None,
) -> tuple[str, str]:
    """Parse Bungie's datetime ranges to string."""

    if end is not None:
        end_date = f"{end.year}-{end.month}-{end.day}"
    else:
        now = datetime.datetime.now()
        end_date = f"{now.year}-{now.month}-{now.day}"

    if start is not None:
        start_date = f"{start.year}-{start.month}-{start.day}"
    else:
        last_24_hrs = datetime.datetime.now() - datetime.timedelta(hours=23)
        start_date = f"{last_24_hrs.year}-{last_24_hrs.month}-{last_24_hrs.day}"

    return end_date, start_date


def monotonic() -> float:
    """Returns the monotonic time in seconds."""
    return _time.monotonic()
