from django.utils.translation import gettext_lazy as _
from django.db.models import TextChoices


class ReportScheduleEnum(TextChoices):
    DAILY = 'daily', _('Daily')
    WEEKLY = 'weekly', _('Weekly')
    MONTHLY = 'monthly', _('Monthly')

class ReportTypeEnum(TextChoices):
    PROJECT_STATUS = "PROJECT_STATUS", _("Project Status")
    USER_PERFORMANCE = "USER_PERFORMANCE", _("User Performance")
    TASK_OVERVIEW = "TASK_OVERVIEW", _("Task Overview")
    TIME_TRACKING = "TIME_TRACKING", _("Time Tracking")
    CUSTOM = "CUSTOM", _("Custom Report")