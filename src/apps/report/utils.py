from django.utils import timezone
from .models import ReportModel
def get_unsent_reports():
    return ReportModel.objects.unsent_reports()

def get_scheduled_reports():
    now = timezone.now().date()
    return ReportModel.objects.filter(auto_send=True, last_send_atdatelt=now)