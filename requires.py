# Copyright 2016 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

import charms.reactive as reactive
import charmhelpers.core.hookenv as hookenv


class BarbicanRequires(reactive.RelationBase):
    """The is the Barbican 'end' of the relation.

    The auto accessors are _name and _plugin_data.  They are underscored as for
    some reason RelationBase only provides these as 'calls'; i.e. they have to
    be used as `self._name()`.  This class therefore provides @properties
    `name` and `plugin_data` that can be used directly.

    The `plugin_data` property also deserialises the _plugin_data from the
    plugin.
    """
    scope = reactive.scopes.GLOBAL

    # These remote data fields will be automatically mapped to accessors
    # with a basic documentation string provided.
    auto_accessors = ['_name', '_plugin_data']

    @reactive.hook('{requires:barbican-hsm-plugin}-relation-joined')
    def joined(self):
        self.set_state('{relation_name}.connected')
        self.update_status()

    @reactive.hook('{requires:barbican-hsm-plugin}-relation-changed')
    def changed(self):
        self.update_status()

    @reactive.hook('{requires:barbican-hsm-plugin}-relation-{broken,departed}')
    def departed(self):
        self.remove_state('{relation_name}.connected')
        self.remove_state('{relation_name}.available')

    def update_status(self):
        if self._name() is not None and self._plugin_data() is not None:
            self.set_state('{relation_name}.available')

    @property
    def name(self):
        """Returns a string of the name or None if it doesn't exist"""
        return self._name()

    @property
    def plugin_data(self):
        """Return the plugin_data from the plugin if it is available.

        The format of the data returned is:
        {
             "library_path": <library path of PKCS#11 libary>,
             "login": the pin/password for accessing the PKCS#11 token,
             "slot_id": <int: slot_id of the token for barbican to use>
        }

        :returns: data object that was passed.
        """
        data = self._plugin_data()
        if data is None:
            return
        return json.loads(data)["data"]
