# NetBox ChangeLog Diff Plugin

NetBox plugin for more detailed changlog diffs


* Free software: Apache-2.0
* Documentation: https://github.com/ITJamie/netbox-changelog-diff-plugin


## Features

The features the plugin provides should be listed here.

## Compatibility

| NetBox Version   | Plugin Version |
|------------------|----------------|
|     4.1.x        |      0.2.0     |
|     4.0.5        |      0.1.0     |

Minium version is 4.0.5 of netbox. Otherwise no changelog diff's will show up

## Screenshot

![gif1](docs/netbox%20changelog%20deepdiff%20plugin.gif)


## Installing

For adding to a NetBox Docker setup see
[the general instructions for using netbox-docker with plugins](https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins).

While this is still in development and not yet on pypi you can install with pip:

```bash
pip install git+https://github.com/ITJamie/netbox-changelog-diff-plugin
```

or by adding to your `local_requirements.txt` or `plugin_requirements.txt` (netbox-docker):

```bash
git+https://github.com/ITJamie/netbox-changelog-diff-plugin
```

Enable the plugin in `/opt/netbox/netbox/netbox/configuration.py`,
 or if you use netbox-docker, your `/configuration/plugins.py` file :

```python
PLUGINS = [
    'netbox_changelog_diff_plugin'
]

PLUGINS_CONFIG = {
    "netbox_changelog_diff_plugin": {},
}
```

## Credits

Diff function based on [https://github.com/wagoodman/diff2HtmlCompare](https://github.com/wagoodman/diff2HtmlCompare)


Based on the NetBox plugin tutorial:

- [demo repository](https://github.com/netbox-community/netbox-plugin-demo)
- [tutorial](https://github.com/netbox-community/netbox-plugin-tutorial)

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`netbox-community/cookiecutter-netbox-plugin`](https://github.com/netbox-community/cookiecutter-netbox-plugin) project template.
