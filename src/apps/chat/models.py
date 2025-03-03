from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel
from apps.account.models import UserModel
# Create your models here.


class Message(BaseModel):
    auther = models.ForeignKey(UserModel, models.CASCADE, verbose_name=_("Auther"))
    message = models.TextField(verbose_name=_('Message'), max_length=500)


    def __str__(self):
        return self.auther.first_name