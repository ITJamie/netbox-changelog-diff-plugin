import django_tables2
from django.utils.translation import gettext_lazy as _

from .models import ChangeLogSummary
from core.tables.change_logging import ObjectChangeTable
from utilities.tables import register_table_column

mycol_2 = django_tables2.Column(
    verbose_name=_('Change Summary'),
    accessor=django_tables2.A('human_summary'),
    default="- -"
)

def register_changelog():
    register_table_column(mycol_2, 'human_summary', ObjectChangeTable)
