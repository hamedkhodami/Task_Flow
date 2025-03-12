from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel
from apps.account.models import UserModel

from .enums import MessageTypeEnum
# Create your models here.


class MessageModel(BaseModel):

    MessageType = MessageTypeEnum

    sendr = models.ForeignKey(UserModel, models.CASCADE,related_name='sent_messages' , verbose_name=_("Sender"))
    receiver = models.ForeignKey(UserModel, models.CASCADE,related_name='received_messages' , verbose_name=_("Receiver"))
    message = models.TextField(verbose_name=_('Message'), max_length=500)
    message_type = models.CharField(_('Message Type'), max_length=10, choices=MessageType, default=MessageType.TEXT)
    is_read = models.BooleanField(_('Read'), default=False)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['-created_at']


    def __str__(self):
        return f"From{self.sendr.first_name} to {self.receiver.first_name}: {self.message[:30]}"

    def mark_as_read(self):
        self.is_read = True
        self.save(update_fields=['is_read'])