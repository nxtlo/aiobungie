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

import attrs
import mock
import pytest

import aiobungie
from aiobungie import crates


class TestAppMember:
    @pytest.fixture()
    def obj(self):
        return crates.ApplicationMember(
            role=1,
            api_eula_version=2,
            user=crates.PartialBungieUser(
                name="buh",
                code=9999,
                id=123,
                type=aiobungie.MembershipType.XBOX,
                types=(),
                crossave_override=aiobungie.MembershipType.NONE,
                is_public=True,
                icon=aiobungie.builders.Image(),
            ),
        )

    def test_app_owner_name(self, obj: crates.ApplicationMember):
        with (
            pytest.raises(attrs.exceptions.FrozenInstanceError),
            mock.patch.object(obj.user, "name", new="buh") as name,
        ):
            assert obj.user.name == name

    def test_app_owner_id(self, obj: crates.ApplicationMember):
        with (
            pytest.raises(attrs.exceptions.FrozenInstanceError),
            mock.patch.object(obj.user, "id", new=123) as id,
        ):
            assert obj.user.id == id

    def test_app_owner_type(self, obj: crates.ApplicationMember):
        with (
            pytest.raises(attrs.exceptions.FrozenInstanceError),
            mock.patch.object(
                obj.user, "type", new=aiobungie.MembershipType.XBOX
            ) as type_,
        ):
            assert obj.user.type == type_

    def test_app_owner_is_public(self, obj: crates.ApplicationMember):
        with (
            pytest.raises(attrs.exceptions.FrozenInstanceError),
            mock.patch.object(obj.user, "is_public", new=True) as is_public,
        ):
            assert obj.user.is_public and is_public

    def test_app_owner_icon(self, obj: crates.ApplicationMember):
        with (
            pytest.raises(attrs.exceptions.FrozenInstanceError),
            mock.patch.object(obj.user, "icon", new=aiobungie.builders.Image()) as icon,
        ):
            assert obj.user.icon == icon

    def test_app_owner_code(self, obj: crates.ApplicationMember):
        with (
            pytest.raises(attrs.exceptions.FrozenInstanceError),
            mock.patch.object(obj.user, "code", new=9999) as code,
        ):
            assert obj.user.code == code


class TestApplication:
    @pytest.fixture()
    def team(self) -> tuple[crates.ApplicationMember, ...]:
        return (
            mock.Mock(spec_set=crates.ApplicationMember),
            mock.Mock(spec_set=crates.ApplicationMember),
        )

    @pytest.fixture()
    def app(self, team: tuple[crates.ApplicationMember, ...]) -> crates.Application:
        return crates.Application(
            id=402928,
            name="aiobungie",
            redirect_url=None,
            created_at=datetime(2017, 4, 8),
            published_at=datetime.now(),
            link="this.io",
            scope=None,
            status=1,
            status_changed=datetime.max,
            origin="",
            team=team,
        )

    def test_app_scope(self, app: crates.Application) -> None:
        assert app.scope is None

    def test_app_team(self, app: crates.Application) -> None:
        assert len(app.team) >= 1
