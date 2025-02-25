from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

def validate_digit_type(value):
    if not value.isdigit():
        raise ValidationError(_('Entered value must be a number'))

    return value