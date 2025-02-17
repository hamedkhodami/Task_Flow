from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ProjectModel
from .validators import validate_end_date, validate_project_title


class ProjectForm(forms.ModelForm):

    class Meta:
        model = ProjectModel
        fields = ["title", "description", "status", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "title": _("Project Title"),
            "description": _("Description"),
            "status": _("Status"),
            "start_date": _("Start Date"),
            "end_date": _("End Date"),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        validate_project_title(title)
        return title

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        validate_end_date(start_date, end_date)
        return cleaned_data