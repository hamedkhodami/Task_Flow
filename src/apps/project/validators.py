from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_end_date(start_date, end_date):
    if end_date and end_date < start_date:
        raise ValidationError(_("End date cannot be before start date."))


def validate_project_title(title):
    if not re.match(r"^[A-Za-z0-9\s\-_.]+$", title):
        raise ValidationError(_("Project title contains invalid characters."))


def validate_unique_member(project, user):
    if project.members.filter(user=user).exists():
        raise ValidationError(_("This user is already a member of this project."))