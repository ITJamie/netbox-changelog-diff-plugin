from django.core.management.base import BaseCommand
from extras.models import ObjectChange
from .models import ChangeLogSummary

class Command(BaseCommand):
    help = 'Creates ChangeLogSummary objects for ObjectChanges that do not have one'

    def handle(self, *args, **options):
        # Get all ObjectChanges that don't have a summary and have action='update'
        object_changes = ObjectChange.objects.filter(
            action='update'
        ).exclude(
            id__in=ChangeLogSummary.objects.values_list('changelog_id', flat=True)
        )

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
            
            ChangeLogSummary.objects.create(
                changelog=change,
                summary=", ".join(summary) if summary else "No changes detected"
            )
            count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} new changelog summaries')
        )
