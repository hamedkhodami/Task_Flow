from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import TaskModel
from apps.project.models import ProjectMemberModel


class TaskCreatorRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        task = get_object_or_404(TaskModel, pk=self.kwargs.get("pk"))

        if task.created_by != request.user:
            messages.error(request, _("You do not have permission to modify this task"))


class TaskAssigneeRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        task = get_object_or_404(TaskModel, pk=self.kwargs.get("pk"))

        if not task.assigned_to.filter(id=request.user.id).exists():
            messages.error(request, _('You are not assigned to this task.'))
            return redirect('task:task_list')
        return super().dispatch(request, *args, **kwargs)


class ProjectAdminRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        task = get_object_or_404(TaskModel, pk=self.kwargs.get("pk"))
        project = task.project
        member = ProjectMemberModel.objects.filter(project=project, user=request.user).first()

        if not member or member.role != ProjectMemberModel.ROLE.PROJECT_ADMIN:
            messages.error(request, _("Only project admins can manage tasks"))
            return redirect('task:task_list')
        return super().dispatch(request, *args, **kwargs)

