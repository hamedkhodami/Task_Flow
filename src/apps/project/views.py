from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import ProjectModel
from .forms import ProjectForm
from .mixins import ProjectManagerRequiredMixin
from apps.core.utils import validate_form, toast_form_errors


class ProjectListView(ListView):

    model = ProjectModel
    template_name = "project/project_list.html"
    context_object_name = "projects"
    ordering = ["-start_date"]

    def get_queryset(self):
        return ProjectModel.objects.filter(members__user= self.request.user)


class ProjectDetailView(DetailView):

    model = ProjectModel
    template_name = "project/project_detail.html"
    context_object_name = "project"


class ProjectCreateView(ProjectManagerRequiredMixin, CreateView):

    model = ProjectModel
    form_class = ProjectForm
    template_name = "project/project_form.html"
    success_url = reverse_lazy("project:project_list")

    def form_valid(self, form):
        if not validate_form(self.request, form):
            return self.form_invalid(form)
        form.instance.owner = self.request.user
        messages.success(self.request, _("Project created successfully."))
        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)


class ProjectUpdateView(ProjectManagerRequiredMixin, UpdateView):

    model = ProjectModel
    form_class = ProjectForm
    template_name = "project/project_form.html"

    def form_valid(self, form):
        if not validate_form(self.request, form):
            return self.form_invalid(form)
        messages.success(self.request, _("Project updated successfully."))
        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("project:project_detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(ProjectManagerRequiredMixin, DeleteView):

    model = ProjectModel
    template_name = "project/project_confirm_delete.html"
    success_url = reverse_lazy("project:project_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Project deleted successfully."))
        return super().delete(request, *args, **kwargs)

