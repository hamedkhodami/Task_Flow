from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from apps.core.models import BaseModel
from apps.core.utils import get_jalali_date,get_timesince_persian
from apps.account.enums import UserAccessEnum

from .enums import ReportTypeEnum,ReportScheduleEnum
from .managers import ReportManager
from .validators import validate_schedule


User = get_user_model()


class ReportModel(BaseModel):
    TypeReport = ReportTypeEnum
    UserAccess = UserAccessEnum
    TimeSend = ReportScheduleEnum

    objects = ReportManager

    type = models.CharField(_('Report Type'), max_length=50, choices=TypeReport.choices)
    created_by = models.ForeignKey(User, verbose_name=_('Created By'), on_delete=models.CASCADE, related_name='reports')
    access_level = models.CharField(_('Access level'), max_length=20, choices=UserAccess.choices)

    filters =models.JSONField(_('Filters'), null=True,blank=True, help_text=_('User-defined filters for custom reports'))
    content =models.JSONField(_('Content'), help_text=_('Time report data for later viewing or export'))

    auto_send = models.BooleanField(_('Auto Send'), default=False)
    schedule = models.CharField(_('Send Schedule'), max_length=20, choices=TimeSend.choices, null=True, blank=True, validators=[validate_schedule])
    last_send_at = models.DateTimeField(_('Last Send At'), null=True, blank=True)

    is_archived = models.BooleanField(_('Archived'), default=False)
    archive_at = models.DateTimeField(_('Archive At'), null=True, blank=True)

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')
        ordering = ('-created_at',)


    def __str__(self):
        return f"{self.get_type_display()} - {self.created_by}"


    def should_send_report(self):

        if not self.auto_send or not self.schedule:
            return False

        if self.last_send_at:
            now = timezone.now()
            days_since_last_send = (now - self.last_send_at).days
            if self.schedule == self.TimeSend.DAILY and days_since_last_send >= 1:
                return True
            elif self.schedule == self.TimeSend.WEEKLY and days_since_last_send >= 7:
                return True
            elif self.schedule == self.TimeSend.MONTHLY and days_since_last_send >= 30:
                return True
            return False
        return True

    def archive(self):
        self.is_archived = True
        self.archive_at = timezone.now()
        self.save(update_fields=['is_archived', 'archive_at'])

    def get_archive_at_jalali(self):
        return get_jalali_date(self.archive_at) if self.archive_at else None

    def get_created_at_jalali(self):
        return get_jalali_date(self.created_at)

    def get_last_send_at_jalali(self):
        return get_jalali_date(self.last_send_at) if self.last_send_at else None

    def get_last_send_time_ago(self):
        return get_timesince_persian(self.last_send_at) if self.last_send_at else _('Never Sent')

