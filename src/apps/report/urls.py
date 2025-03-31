from django.urls import path
from . import views

app_name = "report"

urlpatterns = [
    path("", views.ReportListView.as_view(), name="list"),
    path("<int:pk>/", views.ReportDetailView.as_view(), name="detail"),
    path("create/", views.ReportCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.ReportUpdateView.as_view(), name="update"),
    path("<int:pk>/archive/", views.ReportArchiveView.as_view(), name="archive"),
]