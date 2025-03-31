from django.http import HttpResponseForbidden

class ReportAccessMixin:
    required_access = "REPORT_VIEW"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_specific_access(self.required_access):
            return HttpResponseForbidden("You do not have access to this report")
        return super().dispatch(request, *args, **kwargs)