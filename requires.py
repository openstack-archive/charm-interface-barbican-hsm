import charms.reactive as reactive
import charmhelpers.core.hookenv as hookenv


class BarbicanRequires(reactive.RelationBase):
    scope = reactive.scopes.GLOBAL

    # These remote data fields will be automatically mapped to accessors
    # with a basic documentation string provided.
    auto_accessors = ['name']

    @reactive.hook('{requires:barbican-hsm-plugin}-relation-joined')
    def joined(self):
        self.set_state('{relation_name}.connected')
        hookenv.log("BarbicanRequires.joined() ran")
        self.update_status()

    @reactive.hook('{requires:barbican-hsm-plugin}-relation-changed')
    def changed(self):
        hookenv.log("BarbicanRequires.changed() ran")
        self.update_status()

    @reactive.hook('{requires:barbican-hsm-plugin}-relation-{broken,departed}')
    def departed(self):
        hookenv.log("BarbicanRequires.departed() ran")
        self.remove_state('{relation_name}.connected')
        self.remove_state('{relation_name}.available')

    def update_status(self):
        if self.name is not None:
            self.set_state('{relation_name}.available')
