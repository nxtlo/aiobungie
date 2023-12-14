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
import pytest
import attrs.exceptions as attrs

from aiobungie import crate


class TestRecordsComponent:
    @pytest.fixture()
    def model(self):
        return crate.RecordsComponent(
            profile_records=mock.Mock({1234: mock.Mock(crate.Record)}),
            character_records=mock.Mock({1234: mock.Mock(crate.CharacterRecord)}),
        )

    def test_profile_records(self, model: crate.RecordsComponent):
        with pytest.raises(attrs.FrozenInstanceError), mock.patch.object(
            model, "profile_records"
        ) as profile_records:
            assert model.profile_records is not None
            assert profile_records[1234] is model.profile_records[1234]

    def test_character_records(self, model: crate.RecordsComponent):
        with pytest.raises(attrs.FrozenInstanceError), mock.patch.object(
            model, "character_records"
        ) as character_records:
            assert model.character_records is not None
            assert character_records[1234] is model.character_records[1234]


class TestProfileComponent:
    @pytest.fixture()
    def model(self):
        return crate.ProfileComponent(
            profiles=mock.Mock(
                crate.Profile,
            ),
            profile_progression=mock.Mock(crate.ProfileProgression),
            profile_currencies=None,
            profile_inventories=[
                mock.Mock(crate.ProfileItemImpl, crate.ProfileItemImpl)
            ],
        )

    def test_profiles_component(self, model: crate.ProfileComponent):
        with pytest.raises(attrs.FrozenInstanceError), mock.patch.object(
            model, "profiles"
        ) as profiles:
            assert model.profiles is not None
            assert model.profiles is profiles

    def test_profile_progression_component(self, model: crate.ProfileComponent):
        with pytest.raises(attrs.FrozenInstanceError), mock.patch.object(
            model, "profile_progression"
        ) as profile_progression:
            assert model.profile_progression is not None
            assert profile_progression is model.profile_progression

    def test_profile_currencies(self, model: crate.ProfileComponent):
        assert model.profile_currencies is None

    def test_profile_inventories(self, model: crate.ProfileComponent):
        with pytest.raises(attrs.FrozenInstanceError), mock.patch.object(
            model, "profile_inventories"
        ) as profile_inventories:
            assert model.profile_inventories is not None
            assert profile_inventories is model.profile_inventories


class TestUninstancedItemsComponent:
    @pytest.fixture()
    def model(self):
        return crate.UninstancedItemsComponent(
            objectives={0: [mock.Mock(crate.Objective), mock.Mock(crate.Objective)]},
            perks={0: [mock.Mock(crate.ItemPerk)], 1: [mock.Mock(crate.ItemPerk)]},
        )

    def test_objectives(self, model: crate.UninstancedItemsComponent):
        with pytest.raises(attrs.FrozenInstanceError), mock.patch.object(
            model, "objectives"
        ) as objectives:
            assert model.objectives is not None
            assert objectives[0] is model.objectives[0]
            assert objectives[1] is model.objectives[1]

    def test_perks(self, model: crate.UninstancedItemsComponent):
        with pytest.raises(attrs.FrozenInstanceError), mock.patch.object(
            model, "perks"
        ) as perks:
            assert model.perks is not None
            assert perks[0] is model.perks[0]
            assert perks[1] is model.perks[1]


class TestItemsComponent:
    @pytest.fixture()
    def model(self):
        return crate.ItemsComponent(
            instances=[
                {0: mock.Mock(crate.ItemInstance), 1: mock.Mock(crate.ItemInstance)},
            ],
            render_data=None,
            stats={0: mock.Mock(crate.ItemStatsView)},
            sockets={23: [mock.Mock(crate.ItemSocket)]},
            reusable_plugs={0: [mock.Mock(crate.PlugItemState)]},
            plug_objectives=None,
            plug_states=[mock.Mock(crate.PlugItemState)],
            objectives={
                0: [mock.Mock(crate.Objective)],
            },
            perks=None,
        )

    def test_any_meth(self, model: crate.ItemsComponent):
        assert model.any()

    def test_all_meth(self, model: crate.ItemsComponent):
        assert not model.all()

    def test_instances(self, model: crate.ItemsComponent):
        with pytest.raises(attrs.FrozenInstanceError), mock.patch.object(
            model, "instances"
        ) as instances:
            assert model.instances is not None
            assert instances[0] is model.instances[0]
            assert instances[1] is model.instances[1]

    def test_render_data(self, model: crate.ItemsComponent):
        assert model.render_data is None

    def test_stats(self, model: crate.ItemsComponent):
        with pytest.raises(attrs.FrozenInstanceError), mock.patch.object(
            model, "stats"
        ) as stats:
            assert model.stats is not None
            assert stats[0] is model.stats[0]

    def test_sockets(self, model: crate.ItemsComponent):
        with pytest.raises(attrs.FrozenInstanceError), mock.patch.object(
            model, "sockets"
        ) as sockets:
            assert model.sockets is not None
            assert sockets[23] is model.sockets[23]

    def test_reusable_plugs(self, model: crate.ItemsComponent):
        with pytest.raises(attrs.FrozenInstanceError), mock.patch.object(
            model, "reusable_plugs"
        ) as reusable_plugs:
            assert model.reusable_plugs is not None
            assert reusable_plugs[0] is model.reusable_plugs[0]

    def test_plug_objectives(self, model: crate.ItemsComponent):
        assert model.plug_objectives is None

    def test_plug_states(self, model: crate.ItemsComponent):
        with pytest.raises(attrs.FrozenInstanceError), mock.patch.object(
            model, "plug_states"
        ) as plug_states:
            assert model.plug_states is not None
            assert plug_states is model.plug_states

    def test_objectives(self, model: crate.ItemsComponent):
        with pytest.raises(attrs.FrozenInstanceError), mock.patch.object(
            model, "objectives"
        ) as objectives:
            assert model.objectives is not None
            assert objectives[0] is model.objectives[0]

    def test_perks(self, model: crate.ItemsComponent):
        assert model.perks is None


class TestVendorsComponent:
    # TODO.
    ...


class TestStringVariablesComponent:
    @pytest.fixture()
    def model(self):
        return crate.StringVariableComponent(
            profile_string_variables={0: 1, 2: 3},
            character_string_variables={1: {2: 3}},
        )

    def test_profile_string_variables(self, model: crate.StringVariableComponent):
        with pytest.raises(attrs.FrozenInstanceError), mock.patch.object(
            model, "profile_string_variables"
        ) as profile_string_variables:
            assert model.profile_string_variables is not None
            assert profile_string_variables[0] is model.profile_string_variables[0]
            assert profile_string_variables[2] is model.profile_string_variables[2]

    def test_character_string_variables(self, model: crate.StringVariableComponent):
        with pytest.raises(attrs.FrozenInstanceError), mock.patch.object(
            model, "character_string_variables"
        ) as character_string_variables:
            assert model.character_string_variables is not None
            assert character_string_variables[1] is model.character_string_variables[1]
            assert (
                character_string_variables[1][2]
                is model.character_string_variables[1][2]
            )


class TestMetricsComponent:
    # TODO
    ...


class TestCharacterComponent:
    # TODO
    ...


class TestComponent:
    # TODO
    ...
