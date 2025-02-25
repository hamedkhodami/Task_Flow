from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task_list"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("create/", views.TaskCreateView.as_view(), name="task_create"),
    path("<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task_update"),
    path("<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
    path("<int:pk>/status/", views.TaskStatusUpdateView.as_view(), name="task_status_update"),
    path("<int:task_id>/comment/", views.TaskCommentCreateView.as_view(), name="task_comment"),
    path("<int:task_id>/assign/", views.TaskAssignmentView.as_view(), name="task_assign"),
]