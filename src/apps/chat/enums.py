from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class MessageTypeEnum(TextChoices):
    TEXT = 'text', _('Text')
    IMAGE = 'image', _('Image')
    FILE = 'file', _('File')


