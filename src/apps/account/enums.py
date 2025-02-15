from django.utils.translation import gettext_lazy as _
from django.db.models import TextChoices


# UserAccess Enums
class UserAccessEnum(TextChoices):

    VIEWER = 'viewer', _('Viewer')
    GENERAL_ADMIN = 'general_admin', _('General admin')
    PROJECT_ADMIN = 'project_admin', _('Project admin')
    PROJECT_MEMBER = 'project_member', _('Project member')


# UserGender Enums
class UserGenderEnum(TextChoices):

    MALE = 'm', _('Male')
    FEMALE = 'f', _('Female')
