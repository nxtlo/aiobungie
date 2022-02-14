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
import mock

import aiobungie
from aiobungie import crate
from aiobungie.internal import assets


class TestAppOwner:
    @pytest.fixture()
    def obj(self):
        return crate.ApplicationOwner(
            net=mock.Mock(),
            name="rose",
            type=aiobungie.MembershipType.XBOX,
            id=411098,
            is_public=True,
            icon=assets.Image("dndlkwadjnh9.jpg"),
            code=2463,
        )

    def test_app_owner_name(self, obj: crate.ApplicationOwner):
        with mock.patch.object(crate.ApplicationOwner, "name") as name:
            assert obj.name == name

    def test_app_owner_id(self, obj: crate.ApplicationOwner):
        with mock.patch.object(crate.ApplicationOwner, "id") as id:
            assert obj.id == id

    def test_app_owner_type(self, obj: crate.ApplicationOwner):
        with mock.patch.object(crate.ApplicationOwner, "type") as type:
            assert obj.type == type and int(obj.type) == int(aiobungie.MembershipType.XBOX)

    def test_app_owner_is_public(self, obj: crate.ApplicationOwner):
        with mock.patch.object(crate.ApplicationOwner, "is_public") as is_public:
            assert obj.is_public == is_public

    def test_app_owner_icon(self, obj: crate.ApplicationOwner):
        with mock.patch.object(crate.ApplicationOwner, "icon") as icon:
            assert obj.icon == icon

    def test_app_owner_code(self, obj: crate.ApplicationOwner):
        with mock.patch.object(crate.ApplicationOwner, "code") as code:
            assert obj.code == code


    def test___int__(self, obj: crate.ApplicationOwner) -> None:
        assert int(obj) == obj.id

    def test___str__(self, obj: crate.ApplicationOwner) -> None:
        assert str(obj) == "rose#2463"

class TestApplication:

    @pytest.fixture()
    def owner(self) -> crate.ApplicationOwner:
        return crate.ApplicationOwner(
            name="rose",
            id=411098,
            code=2463,
            net=mock.AsyncMock(),
            type=aiobungie.MembershipType.XBOX,
            is_public=True,
            icon=assets.Image("dndlkwadjnh9.jpg"),
        )

    @pytest.fixture()
    def app(self, owner: crate.ApplicationOwner) -> crate.Application:
        return crate.Application(
            id=402928,
            name="aiobungie",
            redirect_url=None,
            created_at=datetime(2017, 4, 8),
            published_at=datetime.utcnow(),
            link="this.io",
            scope=aiobungie.Undefined,
            status=1,
            owner=owner,
        )

    def test___int__(self, app: crate.Application) -> None:
        assert int(app) == 402928

    def test___str__(self, app: crate.Application) -> None:
        assert str(app) == "aiobungie"

    def test_app_scope(self, app: crate.Application) -> None:
        assert app.scope is aiobungie.Undefined

    def test_app_owner(self, app: crate.Application) -> None:
        assert app.owner.id == 411098
        assert app.owner.name == "rose"
        assert app.owner.code == 2463

    @pytest.mark.asyncio()
    async def test_fetch_self_app_owner_bungie_user(self, owner: crate.ApplicationOwner) -> None:
        owner.net.request.fetch_bungie_user = mock.AsyncMock()

        assert await owner.fetch_self() is owner.net.request.fetch_bungie_user.return_value

        owner.net.request.fetch_bungie_user.assert_called_once_with(411098)