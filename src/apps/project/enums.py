from django.utils.translation import gettext_lazy as _
from django.db.models import TextChoices

from apps.account.enums import UserAccessEnum


class ProjectStatusEnum(TextChoices):

    ACTIVE = 'active', _('Active')
    IN_PROGRESS = 'in_progress', _('In progress')
    COMPLETED = 'completed', _('Completed')
    CANCELED = 'canceled', _('Canceled')


class ProjectRoleEnum(TextChoices):

    PROJECT_ADMIN = UserAccessEnum.PROJECT_ADMIN, _('Project Admin')
    PROJECT_MEMBER = UserAccessEnum.PROJECT_MEMBER, _('Project Member')