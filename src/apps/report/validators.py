from django.core.exceptions import ValidationError
import json

def validate_json(value):
    try:
        json.loads(value)
    except ValueError:
        raise ValidationError("Invalid JSON format.")

def validate_schedule(value):
    """بررسی می‌کنه که مقدار زمان‌بندی معتبر باشه"""
    from .enums import ReportScheduleEnum
    if value not in ReportScheduleEnum.values:
        raise ValidationError("Invalid schedule type.")