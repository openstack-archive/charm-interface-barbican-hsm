import charms.reactive as reactive
import charmhelpers.core.hookenv as hookenv


class BarbicanProvides(reactive.RelationBase):
    scope = reactive.scopes.GLOBAL

    # These remote data fields will be automatically mapped to accessors
    # with a basic documentation string provided.
    auto_accessors = ['test']

    @reactive.hook('{provides:barbican-hsm-plugin}-relation-joined')
    def joined(self):
        self.set_state('{relation_name}.connected')
        hookenv.log("BarbicanProvides.joined() ran")

    @reactive.hook('{provides:barbican-hsm-plugin}-relation-changed')
    def changed(self):
        hookenv.log("BarbicanProvides.changed() ran")

    @reactive.hook('{provides:barbican-hsm-plugin}-relation-{broken,departed}')
    def departed(self):
        hookenv.log("BarbicanProvides.departed() ran")
        self.remove_state('{relation_name}.connected')
        self.remove_state('{relation_name}.available')

    def set_name(self, name):
        self.set_remote(name=name)
