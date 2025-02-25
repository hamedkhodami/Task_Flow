from django.utils.translation import gettext_lazy as _
from django.db.models import TextChoices


class TaskStatusEnum(TextChoices):
    """وضعیت‌های ممکن برای وظایف"""
    PENDING = "pending", _("Pending")
    IN_PROGRESS = "in_progress", _("In Progress")
    COMPLETED = "completed", _("Completed")
    CANCELLED = "cancelled", _("Cancelled")


class TaskPriorityEnum(TextChoices):
    """اولویت‌های ممکن برای وظایف"""
    LOW = "low", _("Low")
    MEDIUM = "medium", _("Medium")
    HIGH = "high", _("High")
    CRITICAL = "critical", _("Critical")


class TaskAssignmentTypeEnum(TextChoices):
    """نوع تخصیص تسک (فردی یا گروهی)"""
    INDIVIDUAL = "individual", _("Individual")
    TEAM = "team", _("Team")
