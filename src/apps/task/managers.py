from django.db import models
from django.utils import timezone
from .enums import TaskStatusEnum, TaskPriorityEnum

class TaskManager(models.Manager):

    def get_overdue_tasks(self):
        return self.filter(due_date__lt=timezone.now().date(), status__in=[TaskStatusEnum.PENDING, TaskStatusEnum.IN_PROGRESS])

    def get_high_priority_tasks(self):
        return self.filter(priority__in=[TaskPriorityEnum.HIGH, TaskPriorityEnum.CRITICAL])

    def get_tasks_for_user(self, user):
        return self.filter(assigned_to=user)

