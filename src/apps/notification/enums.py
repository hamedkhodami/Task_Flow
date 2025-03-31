from django.db.models import TextChoices
from django.utils.translation import gettext as _

# Enum for SMS notifications
class SMSNotificationEnumTypes(TextChoices):
    ACCOUNT_REGISTRATION = "ACCOUNT_REGISTRATION", _("Account Registration")
    PASSWORD_REMINDER = "PASSWORD_REMINDER", _("Password Reminder")
    MEETING_REQUEST = "MEETING_REQUEST", _("Meeting Request")
    ADDED_TO_PROJECT = "ADDED_TO_PROJECT", _("added to project")

# Enum for Email notifications
class EmailNotificationEnumTypes(TextChoices):
    IMPORTANT_PROJECT_MESSAGE = "IMPORTANT_PROJECT_MESSAGE", _("Important Project Message")
    PROJECT_REPORT = "PROJECT_REPORT", _("Project Report")
    TEAM_INVITATION = "TEAM_INVITATION", _("Team Invitation")

