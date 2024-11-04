from django.core.management.base import BaseCommand
from core.models import ObjectChange
from netbox_changelog_diff_plugin.models import ChangeLogSummary

class Command(BaseCommand):
    help = 'Creates ChangeLogSummary objects for ObjectChanges that do not have one'

    def handle(self, *args, **options):
        # Get all ObjectChanges that don't have a summary and have action='update'
        object_changes = ObjectChange.objects.filter(
            action='update'
        ).exclude(
            id__in=ChangeLogSummary.objects.values_list('changelog', flat=True)
        )
        # for change in object_changes:
        #     print(f"Creating ChangeLogSummary for {change}")
        #     self.stdout.write(
        #         self.style.SUCCESS(f'Successfully created {change.id} change')
        #     )

        count = 0
        for change in object_changes:
            summary = []

            if change.prechange_data and change.postchange_data:
                pre_keys = set(change.prechange_data.keys())
                post_keys = set(change.postchange_data.keys())

                # Find added keys
                added_keys = post_keys - pre_keys
                for key in added_keys:
                    summary.append(f"Added {key}")

                # Find removed keys
                removed_keys = pre_keys - post_keys
                for key in removed_keys:
                    summary.append(f"Removed {key}")

                # Check for updated values in common keys
                common_keys = pre_keys & post_keys
                for key in common_keys:
                    if change.prechange_data[key] != change.postchange_data[key]:
                        summary.append(f"Updated {key}")
            summary_msg = ", ".join(summary) if summary else "No changes detected"
            print(f"summary: `{summary_msg}` for change id: {change.id}")
            obj, created = ChangeLogSummary.objects.get_or_create(
                changelog=change,
                defaults={
                  "summary": summary_msg
                }
            )
        #     count += 1

        # self.stdout.write(
        #     self.style.SUCCESS(f'Successfully created {count} new changelog summaries')
        # )
