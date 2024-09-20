from netbox.plugins import PluginTemplateExtension
from .utilities.html_differ import styled_diff


class ChangeLogDiffTemplateExtension(PluginTemplateExtension):
    models = ["core.objectchange"]

    def full_width_page(self):
        prechange_data = self.context["object"].prechange_data
        postchange_data = self.context["object"].postchange_data

        leftrightdiffhtml = styled_diff(
            prechange_data or dict(),
            postchange_data or dict(),
        )
        return self.render(
            "netbox_changelog_diff_plugin/changelogdiff.html", extra_context={"leftrightdiffhtml": leftrightdiffhtml}
        )


template_extensions = [ChangeLogDiffTemplateExtension]
