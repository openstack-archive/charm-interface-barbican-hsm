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


class BarbicanProvides(reactive.RelationBase):
    """This is the barbican-{type}hsm end of the relation

    The HSM provider needs to set it's name (which may be relevant) and
    also provide any plugin data to Barbican.

    The plugin data is:

    {
         "library_path": <library path of PKCS#11 libary>,
         "login": the pin/password for accessing the PKCS#11 token,
         "slot_id": <int: slot_id of the token for barbican to use>
    }
    """
    scope = reactive.scopes.GLOBAL

    # These remote data fields will be automatically mapped to accessors
    # with a basic documentation string provided.
    auto_accessors = []

    @reactive.hook('{provides:barbican-hsm}-relation-joined')
    def joined(self):
        self.set_state('{relation_name}.connected')
        self.set_state('{relation_name}.available')

    @reactive.hook('{provides:barbican-hsm}-relation-changed')
    def changed(self):
        pass

    @reactive.hook('{provides:barbican-hsm}-relation-{broken,departed}')
    def departed(self):
        self.remove_state('{relation_name}.available')
        self.remove_state('{relation_name}.connected')

    def set_name(self, name):
        """Set the name of the plugin.

        :param name: string
        """
        self.set_remote(_name=name)

    def set_plugin_data(self, data):
        """Set the plugin data for the remote (Barbican charm) to be able to
        configure barbican to use the HSM that is installed alongside it.

        NOTE that the data is wrapped in a dictionary, converted to JSON and
        then placed in the juju remote variable.  The other 'end' unpacks this
        and provides the original data to Barbican charm.

        Thus data has to be JSONable.

        :param data: object that describes the plugin data to be sent.
        """
        self.set_remote(_plugin_data=json.dumps({"data": data}))
