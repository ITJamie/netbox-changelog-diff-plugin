from netbox.plugins import PluginTemplateExtension
from .utilities.html_differ import styled_diff
from .utils import get_plugin_setting


class ChangeLogDiffTemplateExtension(PluginTemplateExtension):
    models = ["core.objectchange"]

    def full_width_page(self):
        prechange_data = self.context["object"].prechange_data
        postchange_data = self.context["object"].postchange_data

        leftrightdiffhtml = styled_diff(
            prechange_data or dict(),
            postchange_data or dict(),
        )
        hide_native_diff = get_plugin_setting("hide_native_diff")
        return self.render(
            "netbox_changelog_diff_plugin/changelogdiff.html",
            extra_context={
                "leftrightdiffhtml": leftrightdiffhtml,
                "hide_native_diff": hide_native_diff,
            },
        )


template_extensions = [ChangeLogDiffTemplateExtension]
