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

import mock
from pytest import fixture

import aiobungie
from aiobungie import crate
from aiobungie import internal


@fixture()
def mock_client():
    return mock.Mock(spec_set=aiobungie.Client)


class TestClanFeatures:
    @fixture()
    def obj(self):
        return crate.clans.ClanFeatures(
            max_members=200,
            max_membership_types=5,
            capabilities=3,
            membership_types=[
                aiobungie.MembershipType.STEAM,
                aiobungie.MembershipType.XBOX,
            ],
            invite_permissions=True,
            update_banner_permissions=True,
            update_culture_permissions=False,
            join_level=1,
        )

    def test_clan_has_features(self, obj):
        assert obj.invite_permissions is True
        assert obj.update_banner_permissions is True
        assert obj.update_culture_permissions is False
        assert obj.join_level >= 1

    def test_clan_meta(self, obj):
        assert obj.max_members >= 200
        assert obj.max_membership_types == 5
        assert (
            isinstance(obj.membership_types, list)
            and aiobungie.MembershipType.STEAM in obj.membership_types
        )
        assert obj.capabilities == 3


class TestClanMember:
    @fixture()
    def obj(self):
        # TODO: Finish this.
        ...


class TestClanOwner:
    @fixture()
    def obj(self):
        # TODO: Finish this.
        ...


class TestClan:
    @fixture()
    def obj(self):
        # TODO: Finish this.
        ...
