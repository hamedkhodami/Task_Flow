from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import TaskModel, TaskCommentModel, TaskAssignmentModel
from apps.core.utils import get_jalali_date

@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):

    list_display = ("title", "project", "status", "priority", "due_date", "created_by")
    list_filter = ("status", "priority", "project")
    search_fields = ("title", "description", "created_by__phone_number")
    ordering = ("-due_date",)
    date_hierarchy = "due_date"
    list_editable = ("status", "priority")  # تغییر سریع وضعیت و اولویت
    readonly_fields = ("created_by",)

    def get_queryset(self, request):
        """فقط تسک‌های مرتبط با کاربر ادمین را نمایش می‌دهد (اگر نیاز به فیلتر باشد)"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(project__owner=request.user)

    def get_due_date_jalali(self, obj):
        return get_jalali_date(obj.due_date) if obj.end_date else _("Not Set")

    get_due_date_jalali.short_description = _("Due Date")



    def get_comment_count(self, obj):
        return obj.comments.count()

    get_comment_count.short_description = _("Comment Count")


    def get_assigned_users_count(self, obj):
        return obj.assigned_to.count()

    get_assigned_users_count.short_description = _("Assigned Users Count")


    def is_overdue(self, obj):
        return obj.is_overdue()

    is_overdue.boolean = True
    is_overdue.short_description = _("Is Overdue")


@admin.register(TaskCommentModel)
class TaskCommentAdmin(admin.ModelAdmin):

    list_display = ("task", "user", "content", "created_at")
    search_fields = ("tasktitle", "userphone_number", "content")
    ordering = ("-created_at",)


@admin.register(TaskAssignmentModel)
class TaskAssignmentAdmin(admin.ModelAdmin):
    """مدیریت تخصیص وظایف در پنل ادمین"""

    list_display = ("task", "user", "assignment_type")
    list_filter = ("assignment_type",)
    search_fields = ("tasktitle", "userphone_number")

