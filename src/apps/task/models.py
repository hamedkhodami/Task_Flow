from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .enums import TaskStatusEnum, TaskPriorityEnum, TaskAssignmentTypeEnum
from .validators import validate_due_date, validate_task_title, validate_task_assignment, validate_comment_content
from .managers import TaskManager

from apps.core.models import BaseModel
from apps.account.models import UserModel
from apps.project.models import ProjectModel
from apps.core.utils import get_jalali_date


class TaskModel(BaseModel):

    STATUS = TaskStatusEnum
    PRIORITY = TaskPriorityEnum

    title = models.CharField(_("Task Title"), max_length=255, validators=[validate_task_title])
    description = models.TextField(_("Description"), max_length=1000, blank=True, null=True)
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE, related_name="tasks", verbose_name=_("Project"))
    status = models.CharField(_("Status"), max_length=20, choices=STATUS.choices, default=STATUS.PENDING)
    priority = models.CharField(_("Priority"), max_length=10, choices=PRIORITY.choices, default=PRIORITY.MEDIUM)
    due_date = models.DateField(_("Due Date"), blank=True, null=True, validators=[validate_due_date])
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="created_tasks", verbose_name=_("Created By"))
    assigned_to = models.ManyToManyField(UserModel, through="TaskAssignmentModel", related_name="assigned_tasks", verbose_name=_("Assigned To"))

    objects = TaskManager()

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self):
        return self.title

    def is_overdue(self):
        if self.due_date and self.status not in [self.STATUS.COMPLETED, self.STATUS.CANCELLED]:
            return self.due_date < timezone.now().date()
        return False

    def get_jalali_due_date(self):
        return get_jalali_date(self.due_date)

    def get_status_label(self):
        return self.STATUS(self.status).label

    def get_priority_label(self):
        return self.PRIORITY(self.priority).label

    def get_total_tasks_in_project(self):
        return TaskModel.objects.filter(project=self.project).count()


class TaskCommentModel(BaseModel):

    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE, related_name="comments", verbose_name=_("Task"))
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="task_comments", verbose_name=_("User"))
    content = models.TextField(_("Comment Content"), max_length=1000, validators=[validate_comment_content])

    class Meta:
        verbose_name = _("Task Comment")
        verbose_name_plural = _("Task Comments")

    def __str__(self):
        return f"Comment by {self.user.get_full_name()} on {self.task.title}"


class TaskAssignmentModel(BaseModel):

    ASSIGNMENT_TYPE = TaskAssignmentTypeEnum

    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE, related_name="assignments", verbose_name=_("Task"))
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="task_assignments_as_user", verbose_name=_("Assigned User"), blank=True, null=True)
    assignment_type = models.CharField(_("Assignment Type"), max_length=20, choices=ASSIGNMENT_TYPE.choices, default=ASSIGNMENT_TYPE.INDIVIDUAL)

    class Meta:
        verbose_name = _("Task Assignment")
        verbose_name_plural = _("Task Assignments")

    def __str__(self):
        return f"Assignment for {self.task.title}"

    def clean(self):
        validate_task_assignment(self.task, self.user, self.assignment_type)
