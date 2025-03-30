from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from ...apps.core.models import BaseModel
from .enums import SMSNotificationEnumTypes, EmailNotificationEnumTypes
# Create your models here.

User = get_user_model()

class SMSNotificationModel(BaseModel):

    SMSType = SMSNotificationEnumTypes

    type = models.CharField(_('sms type'), max_length=130, choices=SMSType)
    title = models.CharField(_('sms title'), max_length=130)
    description = models.TextField(_('description'), max_length=500, null=True, blank=True)

    kwargs = models.JSONField(_('keyword args'), null=True, blank=True)

    send_sms = models.BooleanField(_('send sms'), default=True)
    to_user = models.ForeignKey(User , verbose_name=_('to user'), on_delete=models.CASCADE, related_name='sms')

    is_showing = models.BooleanField(_('Is showing'), default=True)

    class Meta:
        verbose_name = _('SMS Notification')
        verbose_name_plural = _('SMS Notifications')
        ordering = ('-id',)

    def __str__(self):
        return f'Notification for {self.to_user}'

    def get_title(self):
        return self.title or 'sms notification'

    def get_content(self):
        return f"""
            {self.get_title()}
            {self.description}
        """

    def get_link(self):
        return self.kwargs.get('link', '')


class EmailNotificationModel(BaseModel):
    EmailType = EmailNotificationEnumTypes

    type = models.CharField(_('email type'), max_length=130, choices=EmailType)
    title = models.CharField(_('email title'), max_length=130)
    description = models.TextField(_('description'), max_length=500, null=True, blank=True)

    image = models.ImageField(_('images'), upload_to='images/notification/email/', null=True, blank=True)
    kwargs = models.JSONField(_('keyword args'), null=True, blank=True)

    send_email = models.BooleanField(_('send email'), default=True)
    to_user = models.ForeignKey(User, verbose_name=_('to user'), on_delete=models.CASCADE, related_name='email')

    is_showing = models.BooleanField(_('Is showing'), default=True)

    class Meta:
        verbose_name = _('Email Notification')
        verbose_name_plural = _('Email Notifications')
        ordering = ('-id',)

    def __str__(self):
        return f'Notification for {self.to_user}'

    def get_title(self):
        return self.title or 'email notification'

    def get_content(self):
        return f"""
            {self.get_title()}
            {self.description}
        """

    def get_link(self):
        return self.kwargs.get('link', '')

    def get_image_url(self):
        if self.image:
            return self.image.url if self.image else ''