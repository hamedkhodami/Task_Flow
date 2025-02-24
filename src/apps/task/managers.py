from django.db import models
from django.utils import timezone
from .enums import TaskStatusEnum, TaskPriorityEnum


class TaskManager(models.Manager):

    def get_tasks_for_user(self, user):
        return self.filter(assigned_to=user)

