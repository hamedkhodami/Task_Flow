from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.core.utils import get_jalali_date
from .models import ProjectModel, ProjectMemberModel


@admin.register(ProjectModel)
class ProjectModelAdmin(admin.ModelAdmin):
    """ مدیریت پروژه‌ها در پنل ادمین """

    list_display = ("title", "owner", "get_status_display", "get_jalali_start", "get_jalali_end")
    list_filter = ("status", "start_date")
    search_fields = ("title", )
    ordering = ("-start_date",)

    def get_status_display(self, obj):
        return obj.get_status_display()

    get_status_display.short_description = _("Status")

    def get_jalali_start(self, obj):
        return get_jalali_date(obj.start_date)

    get_jalali_start.short_description = _("Start Date")

    def get_jalali_end(self, obj):
        return get_jalali_date(obj.end_date) if obj.end_date else _("Not Set")

    get_jalali_end.short_description = _("End Date")


@admin.register(ProjectMemberModel)
class ProjectMemberModelAdmin(admin.ModelAdmin):

    list_display = ("get_user_name", "get_project_name", "get_role_display", "get_jalali_joined")
    list_filter = ("role", "project")
    ordering = ("-joined_at",)

    def get_user_name(self, obj):
        return obj.user.get_full_name()

    get_user_name.short_description = _("User")

    def get_project_name(self, obj):
        return obj.project.title

    get_project_name.short_description = _("Project")

    def get_role_display(self, obj):
        return obj.get_role_display()

    get_role_display.short_description = _("Role")

    def get_jalali_joined(self, obj):
        return get_jalali_date(obj.joined_at)

    get_jalali_joined.short_description = _("Joined Date")