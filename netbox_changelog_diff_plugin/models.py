from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel

class ChangeLogSummary(NetBoxModel):
    """Model to store human-readable summaries of changelogs"""
    
    changelog = models.ForeignKey(
        to='extras.ObjectChange',
        on_delete=models.CASCADE,
        related_name='summaries'
    )
    
    summary = models.TextField(
        help_text="Human readable summary of the changes made"
    )

    class Meta:
        verbose_name = "Changelog Summary"
        verbose_name_plural = "Changelog Summaries"
        ordering = ['-changelog__time']

    def __str__(self):
        return f"Summary for change {self.changelog.id}"

    def get_absolute_url(self):
        return reverse('plugins:netbox_changelog_diff_plugin:changelogsummary', args=[self.pk])
