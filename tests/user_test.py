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

from datetime import datetime

import pytest

import aiobungie
from aiobungie import crate
from aiobungie import internal


class TestHardLinkedUser:
    @pytest.fixture()
    def model(self):
        return crate.HardLinkedMembership(
            type=aiobungie.MembershipType.STEAM,
            id=9909,
            cross_save_type=aiobungie.MembershipType.STADIA,
        )

    def test_user_id(self, model):
        assert model.id == 9909

    def test_user_type(self, model):
        assert model.type is aiobungie.MembershipType.STEAM

    def test_cross_save_type(self, model):
        assert model.cross_save_type is aiobungie.MembershipType.STADIA


class TestUserThemes:
    @pytest.fixture()
    def mod(self):
        return crate.user.UserThemes(id=1122, name="d2_1", description=None)

    @pytest.fixture()
    def list_objs(self):
        return [
            crate.user.UserThemes(id=1, name=None, description=None),
            crate.user.UserThemes(id=239, name=None, description="D2_11"),
            crate.user.UserThemes(
                id=22, name="Ok", description=internal.helpers.Undefined
            ),
        ]

    def test_model_meta(self, mod):
        assert isinstance(mod, crate.user.UserThemes)
        assert mod is not None
        assert mod.description is None

    def test_list_of_objs(self, list_objs):
        assert isinstance(list_objs, list)


class TestUserLike:
    # Not testing ABCs currently.
    @pytest.fixture()
    def model(self):
        assert None
class TestBungieUser:
    @pytest.fixture()
    def model(self):
        return crate.user.BungieUser(
            id=205432,
            name="Fate",
            created_at=datetime.utcnow(),
            is_deleted=True,
            about=None,
            picture=internal.Image("1029312dnoi12.jpg"),
            locale="eu",
            updated_at=datetime(2019, 4, 5),
            status=internal.helpers.Undefined,
            blizzard_name=internal.helpers.Undefined,
            steam_name="Fate",
            psn_name=None,
            twitch_name="fate_ttv",  # Fake o:
            unique_name="Fate怒#4275",
            code=4275,
            theme_id=1234,
            show_activity=True,
            theme_name="some_theme_name",
            display_title='Newbie',
            stadia_name=None
        )

    def test_str_op(self, model):
        assert str(model) == "Fate"

    def test_int_op(self, model):
        assert int(model) == 205432

    def test_user_status_when_None(self, model):
        model.status = None
        assert isinstance(model, crate.user.BungieUser) and model.status is None

class TestDestinyUser:
    @pytest.fixture()
    def obj(self):
        ...
class TestUser:
    @pytest.fixture()
    def obj(self):
        ...
