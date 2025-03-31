from django.db.models import Manager


class ReportManager(Manager):

    def active_reports(self):
        return self.filter(is_archived=False)

    def archived_reports(self):
        return self.filter(is_archived=True)

    def by_type(self, report_type):
        if not report_type:
            return self.none()
        return self.filter(type=report_type)

    def unsent_reports(self):
        return self.filter(last_send_at__isnull=True)

    def sent_reports(self):
        return self.exclude(last_send_at__isnull=True)