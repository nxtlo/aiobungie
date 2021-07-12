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

import calendar
import time
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from datetime import datetime

__all__ = (
    'Time',
)

class plural:
    '''
    Rapptz :>)
    '''
    def __init__(self, value):
        self.value = value
    def __format__(self, format_spec):
        v = self.value
        singular, sep, plural = format_spec.partition('|')
        plural = plural or f'{singular}s'
        if abs(v) != 1:
            return f'{v} {plural}'
        return f'{v} {singular}'


def human_join(seq, delim=', ', final='or') -> str:
    '''
    Rapptz :>)
    '''
    size = len(seq)
    if size == 0:
        return ''

    if size == 1:
        return seq[0]

    if size == 2:
        return f'{seq[0]} {final} {seq[1]}'

    return delim.join(seq[:-1]) + f' {final} {seq[-1]}'


class Time(object):
    def __init__(self):
        pass


    @staticmethod
    def from_timestamp(timer = None) -> datetime:
        '''
        Converts timestamp to datetime.utcnow()
        '''
        return datetime.utcfromtimestamp(timer)

    @staticmethod
    def clean_date(date: str) -> datetime:
        '''Converts datetime.utcnow() to a readble date.'''
        parsed = parse(date)
        ts = Time.to_timestamp(parsed) # had to do it in two ways.
        ft = Time.from_timestamp(ts)
        return ft

    @staticmethod
    def to_timestamp(date: datetime) -> int:
        '''
        Converts datetime.utcnow().utctimetuple() to timestamp.
        '''
        try:
            return calendar.timegm(date.timetuple())
        except Exception as e:
            raise e

    @staticmethod
    def human_timedelta(dt, *, source=None, accuracy=3, brief=False, suffix=True) -> str:
        '''
        Rapptz :>)
        '''
        now = source or datetime.utcnow()
        # Microsecond free zone
        now = now.replace(microsecond=0)
        dt = dt.replace(microsecond=0)

        # This implementation uses relativedelta instead of the much more obvious
        # divmod approach with seconds because the seconds approach is not entirely
        # accurate once you go over 1 week in terms of accuracy since you have to
        # hardcode a month as 30 or 31 days.
        # A query like "11 months" can be interpreted as "!1 months and 6 days"
        if dt > now:
            delta = relativedelta(dt, now)
            suffix = ''
        else:
            delta = relativedelta(now, dt)
            suffix = ' ago' if suffix else ''

        attrs = [
            ('year', 'y'),
            ('month', 'mo'),
            ('day', 'd'),
            ('hour', 'h'),
            ('minute', 'm'),
            ('second', 's'),
        ]

        output = []
        for attr, brief_attr in attrs:
            elem = getattr(delta, attr + 's')
            if not elem:
                continue

            if attr == 'day':
                weeks = delta.weeks
                if weeks:
                    elem -= weeks * 7
                    if not brief:
                        output.append(format(plural(weeks), 'week'))
                    else:
                        output.append(f'{weeks}w')

            if elem <= 0:
                continue

            if brief:
                output.append(f'{elem}{brief_attr}')
            else:
                output.append(format(plural(elem), attr))

        if accuracy is not None:
            output = output[:accuracy]

        if len(output) == 0:
            return 'now'
        else:
            if not brief:
                return human_join(output, final='and') + suffix
            else:
                return ' '.join(output) + suffix