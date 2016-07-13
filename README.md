# Overview

This interface supports the integration between Barbican and HSM devices.

# Usage

No explicit handler is required to consume this interface in charms
that consume this interface.

The interface provides `hsm.connected` and `hsm.available` states.

## For an HSM subordinate charm

The `hsm.connected` state indicates that the Barbican principle charms has been
connected to.  At this point the plugin data required for to configure the HSM
from Barbican should be presented.

# metadata

To consume this interface in your charm or layer, add the following to `layer.yaml`:

```yaml
includes: ['interface:barbican-hsm']
```

and add a provides interface of type `hsm` to your charm or layers
`metadata.yaml`:

```yaml
provides:
  hsm:
    interface: barbican-hsm
    scope: container
```

Please see the example 'Barbican SoftHSM' charm for an example of how to author
an HSM charm.

# Bugs

Please report bugs on [Launchpad](https://bugs.launchpad.net/openstack-charms/+filebug).

For development questions please refer to the OpenStack [Charm Guide](https://github.com/openstack/charm-guide).
