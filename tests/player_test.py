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

import pytest

import aiobungie
from aiobungie import crate
from aiobungie import internal


class TestPlayer:
    @pytest.fixture()
    def model(self):
        return crate.Player(
            name="RoberGamer321",
            id=40001,
            icon=internal.Image("4a2dc9dca0b4.jpg"),
            is_public=True,
            type=aiobungie.MembershipType.STADIA,
        )

    def test_str_op(self, model):
        assert str(model) == "RoberGamer321"

    def test_player_asdict(self, model):
        assert isinstance(model.as_dict, dict)

    def test_player_type(self, model):
        assert (
            isinstance(model.type, aiobungie.MembershipType)
            and model.type is aiobungie.MembershipType.STADIA
        )
