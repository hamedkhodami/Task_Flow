from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import TaskModel, TaskAssignmentModel, TaskCommentModel
from .forms import TaskForm, TaskCommentForm, TaskAssignmentForm
from .mixins import TaskAssigneeRequiredMixin, TaskCreatorRequiredMixin, ProjectAdminRequiredMixin

from ...apps.core.utils import validate_form


class TaskListView(ListView):

    model = TaskModel
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'
    ordering = 'due_date'

    def get_queryset(self):
        user = self.request.user
        return TaskModel.objects.get_tasks_for_user(user)


class TaskDetailView(DetailView):

    model = TaskModel
    template_name = 'task/task_detail.html'
    context_object_name = 'task'

    def get_object(self):
        user = self.request.user
        return get_object_or_404(TaskModel.objects.get_tasks_for_user(user), pk=self.kwargs.get('pk'))


class TaskCreateView(ProjectAdminRequiredMixin, CreateView):

    model = TaskModel
    form_class = TaskForm
    template_name = 'task/task_form.html'

    def form_valid(self, form):
        if not validate_form(self.request, form):
            return self.form_invalid(form)
        form.instance.created_by(self.request, _('Task created successfully'))
        return super().form_valid(form)


class TaskUpdateView(TaskCreatorRequiredMixin, UpdateView):

    model = TaskModel
    form_class = TaskForm
    template_name = 'task/task_form.html'

    def form_valid(self, form):
        if not validate_form(self.request, form):
            return self.form_invalid(form)
        form.instance.created_by(self.request, _('Task updated successfully'))
        return super().form_valid(form)


class TaskDeleteView(TaskCreatorRequiredMixin, DeleteView):

    model = TaskModel
    template_name = 'task/task_confirm_delete.html'
    success_url = reverse_lazy('task:task_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('Task deleted successfully'))
        return super().delete(request, *args, **kwargs)


class TaskStatusUpdateView(TaskAssigneeRequiredMixin, UpdateView):

    model = TaskModel
    fields = ['status']
    template_name = 'task/task_status_update.html'

    def form_valid(self, form):
        messages.success(self.request, _('Task status updated successfully'))
        return super().form_valid(form)

    def get_object(self):
        user = self.request.user
        return get_object_or_404(TaskModel.objects.get_tasks_for_user(user), pk=self.kwargs.get('pk'))


class TaskCommentCreateView(LoginRequiredMixin, CreateView):

    model = TaskCommentModel
    form_class = TaskCommentForm
    template_name = 'task/task_comment_form.html'

    def form_valid(self, form):
        task = get_object_or_404(TaskModel, pk=self.kwargs.get('task_id'))
        form.instance.task = task
        form.instance.user = self.request.user
        messages.success(self.request, _("Comment added successfully"))
        return super().form_valid(form)


class TaskAssignmentView(ProjectAdminRequiredMixin, CreateView):

    model = TaskAssignmentModel
    form_class = TaskAssignmentForm
    template_name = 'task/task_assignment_form.html'

    def form_valid(self, form):
        messages.success(self.request, _('Task assigned successfully'))


