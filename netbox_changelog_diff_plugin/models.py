from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
# from netbox.core.models import ObjectChange


class ChangeLogSummary(models.Model):
    """Model to store human-readable summaries of changelogs"""

    changelog = models.OneToOneField(
        to='core.ObjectChange',
        on_delete=models.CASCADE,
        related_name='human_summary',
        unique=True
    )

    summary = models.TextField(
        help_text="Human readable summary of the changes made"
    )

    class Meta:
        verbose_name = "Changelog Summary"
        verbose_name_plural = "Changelog Summaries"
        # ordering = ['-id']

    def __str__(self):
        return f"{self.summary}"

    def get_absolute_url(self):
        return reverse('plugins:netbox_changelog_diff_plugin:changelogsummary', args=[self.pk])
