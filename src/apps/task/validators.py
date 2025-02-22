from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .enums import TaskAssignmentTypeEnum
import re


def validate_due_date(due_date):
    if due_date and due_date < timezone.now().date():
        raise ValidationError(_('Due date cannot be in the past.'))


def validate_task_title(title):
    if len(title) < 5:
        raise ValidationError(_('Task title must be at least 5 characters long.'))


def validate_comment_content(content):
    if not content.strip():
        raise ValidationError(_('Comment cannot be empty or contain only whitespace.'))


def validate_task_assignment(task, user, assignment_type):
    if assignment_type == TaskAssignmentTypeEnum.INDIVIDUAL and not user:
        raise ValidationError(_("An individual task must have an assigned user."))