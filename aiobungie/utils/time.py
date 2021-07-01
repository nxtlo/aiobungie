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
from typing import Optional
from datetime import datetime

__all__ = (
    'Time',
)
class Time(object):
    def __init__(self):
        pass


    @staticmethod
    def from_timestamp(timer = None) -> str:
        '''
        Converts timestamp to datetime.utcnow()
        '''
        if not timer:
            return datetime.utcnow().strftime("%c")
        else:
            return time.ctime(timer)

    @staticmethod
    def clean_date(date: datetime) -> datetime:
        '''Converts datetime.utcnow() to a readble date.'''
        return date.strftime('%A, %d/%m/%Y, %H:%M:%S %p')

    @staticmethod
    def to_timestamp(date: datetime) -> int:
        '''
        Converts datetime.utcnow().utctimetuple() to timestamp.
        '''
        try:
            return calendar.timegm(date.timetuple())
        except Exception as e:
            raise e
