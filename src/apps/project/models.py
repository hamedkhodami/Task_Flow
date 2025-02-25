from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .enums import ProjectRoleEnum, ProjectStatusEnum
from .validators import validate_project_title, validate_end_date, validate_unique_member
from .managers import ProjectManager,ProjectMemberManager
from apps.core.models import BaseModel
from apps.core.utils import get_jalali_date
from apps.account.models import UserModel



class ProjectModel(BaseModel):

    STATUS = ProjectStatusEnum

    title = models.CharField(_('Project title'), max_length=225, unique=True,validators=[validate_project_title])
    description = models.TextField(_('Description'), blank=True, null=True)
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='owned_project',verbose_name=_('Owner'))
    status = models.CharField(_("Status"), max_length=20, choices=STATUS.choices,default=STATUS.ACTIVE)
    start_date = models.DateField(_("Start Date"), default=timezone.now)
    end_date = models.DateField(_("End Date"), blank=True, null=True)

    objects = ProjectManager()

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.title

    def clean(self):
        validate_end_date(self.start_date, self.end_date)

    def get_jalali_start_date(self):
        return get_jalali_date(self.start_date)

    def get_jalali_end_date(self):
        return get_jalali_date(self.end_date) if self.end_date else _("None Set")

    def get_duration(self):
        if self.end_date and self.start_date:
            return (self.end_date - self.start_date).days
        return None

    def is_active(self):
        today = timezone.now().date()
        if self.end_date:
            return self.start_date <= today <= self.end_date
        return self.start_date <= today

    def get_owner_name(self):
        return self.owner.get_full_name()


class ProjectMemberModel(BaseModel):
    ROLE = ProjectRoleEnum

    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE, related_name="members",verbose_name=_('Project'))
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="projects",verbose_name=_('User'))
    role = models.CharField(_("Role"), max_length=20, choices=ROLE.choices, default=ROLE.PROJECT_MEMBER)
    joined_at = models.DateTimeField(_("Joined At"), auto_now_add=True)

    objects = ProjectMemberManager()

    class Meta:
        unique_together = ("project", "user")
        verbose_name = _("Project Member")
        verbose_name_plural = _("Project Members")

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.project.title}"

    def clean(self):
        validate_unique_member(self.project, self.user)

    def get_role_label(self):
        return self.get_role_display()

    def get_joined_date_jalali(self):
        return get_jalali_date(self.joined_at)

