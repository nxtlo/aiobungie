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

from __future__ import annotations
from datetime import datetime

import pytest

import aiobungie
from aiobungie import crate
from aiobungie.internal import helpers, assets

@pytest.fixture()
def mock_client():
    return mock.Mock(spec_set=aiobungie.Client)

class TestAppOwner:
    @staticmethod
    def init_owner():
        return crate.ApplicationOwner(
            net=mock_client,
            name="rose",
            type=aiobungie.MembershipType.XBOX,
            id=411098,
            is_public=True,
            icon=assets.Image("dndlkwadjnh9.jpg"),
            code=2463,
        )

    @pytest.fixture()
    def obj(self):
        return self.init_owner()

    def test_app_owner(self, obj):
        assert obj.name == "rose"
        assert obj.type is aiobungie.MembershipType.XBOX
        assert isinstance(obj.id, int) and obj.id == 411098
        assert obj.is_public is True
        assert obj.icon is not None and isinstance(obj.icon, assets.Image)

class TestApplication:
    @pytest.fixture()
    def obj(self):
        return crate.Application(
            id=402928,
            name="aiobungie",
            redirect_url=None,
            created_at=datetime(2017, 4, 8),
            published_at=datetime.utcnow(),
            link="warmind.io",
            scope=helpers.Undefined,
            status=1,
            owner=TestAppOwner.init_owner(),
        )

    def test_app_owner(self, obj):
        assert obj.owner.id == 411098
        assert obj.owner.name == "rose"
        assert obj.owner.type is aiobungie.MembershipType.XBOX
        assert obj.owner.is_public is True
        assert obj.owner.icon is not None

    def test_self_app(self, obj):
        app = obj
        assert isinstance(app.id, int) and app.id is not None
        assert app.name == "aiobungie"
        assert app.redirect_url is None
        assert app.owner is not None and isinstance(app.owner, crate.ApplicationOwner)
