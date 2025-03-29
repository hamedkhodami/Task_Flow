from enum import Enum
from django.utils.translation import gettext_lazy as _

# Enum for SMS notifications
class SMSNotificationEnum(Enum):
    ACCOUNT_REGISTRATION = ("ACCOUNT_REGISTRATION", _("Account Registration"))
    PASSWORD_REMINDER = ("PASSWORD_REMINDER", _("Password Reminder"))
    MEETING_REQUEST = ("MEETING_REQUEST", _("Meeting Request"))

# Enum for Email notifications
class EmailNotificationEnum(Enum):
    IMPORTANT_PROJECT_MESSAGE = ("IMPORTANT_PROJECT_MESSAGE", _("Important Project Message"))
    PROJECT_REPORT = ("PROJECT_REPORT", _("Project Report"))
    TEAM_INVITATION = ("TEAM_INVITATION", _("Team Invitation"))

