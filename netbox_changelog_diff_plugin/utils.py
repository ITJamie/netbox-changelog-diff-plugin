from django.conf import settings

def get_plugin_setting(setting_name):
    plugin_settings = settings.PLUGINS_CONFIG['netbox_changelog_diff_plugin']
    assert setting_name in plugin_settings, f'Setting {setting_name} not supported'
    return plugin_settings[setting_name]