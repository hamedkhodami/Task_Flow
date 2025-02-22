from django import forms
from django.utils.translation import gettext_lazy as _

from .models import TaskModel, TaskCommentModel, TaskAssignmentModel
from .validators import validate_due_date, validate_task_title, validate_comment_content


class TaskForm(forms.ModelForm):

    class Meta:
        model = TaskModel
        fields = ["title", "description", "status", "priority", "due_date", "assigned_to"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}
        labels = {
            "title": _("Task Title"),
            "description": _("Description"),
            "status": _("Status"),
            "priority": _("Priority"),
            "due_date": _("Due Date"),
            "assigned_to": _("Assigned Users"),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        validate_task_title(title)
        return title

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")
        validate_due_date(due_date)
        return due_date


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskCommentModel
        fields = ["content"]
        labels = {
            "content": _("Comment"),
        }

    def clean_content(self):
        content = self.cleaned_data.get("content")
        validate_comment_content(content)
        return content


class TaskAssignmentForm(forms.ModelForm):

    class Meta:
        model = TaskAssignmentModel
        fields = ["task", "user", "assignment_type"]
        labels = {
            "task": _("Task"),
            "user": _("Assigned User"),
            "assignment_type": _("Assignment Type"),
        }