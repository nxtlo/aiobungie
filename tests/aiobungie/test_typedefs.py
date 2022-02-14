# -*- coding: utf-8 -*-

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

from aiobungie.internal import enums
from aiobungie import typedefs

class TestTypedefs:
    def test_json_object(self):
        mock_json_object: typedefs.JSONObject = {"Key": 1}
        assert isinstance(mock_json_object, dict)

    def test_json_array(self):
        mock_json_array: typedefs.JSONArray = [{"Key": 1}, {"Key2": "Value"}]
        assert isinstance(mock_json_array, list)
        assert len(mock_json_array) == 2
        assert 'Key' in mock_json_array[0]
        assert 'Key2' in mock_json_array[1]

    def test_unknown_is_true(self):
        unknwon_str = typedefs.Unknown
        assert typedefs.is_unknown(unknwon_str)

    def test_unknown_is_not_true(self):
        known_str = 'yoyoyo'
        assert not typedefs.is_unknown(known_str)

    def test_none_or_is_true(self):
        optional_field: typedefs.NoneOr[bool] = None
        assert optional_field is None
        optional_field = True
        assert optional_field

    def test_none_or_is_not_true(self):
        optional_field: typedefs.NoneOr[bool] = False
        assert not optional_field
        optional_field = None
        assert optional_field is None

    def test_IntAnd(self):
        int_and: typedefs.IntAnd[enums.MembershipType] = 1
        assert isinstance(int_and, int)
        assert int_and == 1
        int_and = enums.MembershipType.STEAM
        assert isinstance(int_and, enums.MembershipType)
        assert int(int_and) == 3
