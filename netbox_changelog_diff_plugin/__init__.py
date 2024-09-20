"""Top-level package for NetBox ChangeLog Diff Plugin."""

__author__ = """Jamie Murphy"""
__email__ = "git@jam.ie"
__version__ = "0.2.1"


from netbox.plugins import PluginConfig


class ChangeLogDiffConfig(PluginConfig):
    name = "netbox_changelog_diff_plugin"
    verbose_name = "NetBox ChangeLog Diff Plugin"
    description = "NetBox plugin for more detailed changlog diffs"
    version = __version__
    base_url = "netbox_changelog_diff_plugin"
    default_settings = {
        "change_log_format": "yaml",
        "hide_native_diff": False,
    }


config = ChangeLogDiffConfig
