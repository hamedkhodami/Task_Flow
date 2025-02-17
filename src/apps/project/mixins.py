from django.shortcuts import redirect,get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ProjectModel, ProjectMemberModel
from apps.account.enums import UserAccessEnum


class ProjectManagerRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        project = get_object_or_404(ProjectModel, pk=self.kwargs.get("pk"))

        if request.user.has_specific_access(UserAccessEnum.GENERAL_ADMIN):
            return super().dispatch(request, *args, **kwargs)

        member = ProjectMemberModel.objects.filter(project=project, user=request.user).first()
        if member and member.role == ProjectMemberModel.ROLE.PROJECT_ADMIN:
            return super().dispatch(request, *args, **kwargs)

        messages.error(request, _("You do not have permission to modify this project."))
        return redirect("project:project_list")

