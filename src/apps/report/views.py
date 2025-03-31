from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ReportModel
from .forms import ReportCreateForm, ReportUpdateForm
from .mixins import ReportAccessMixin


class ReportListView(LoginRequiredMixin, ReportAccessMixin, ListView):
    model = ReportModel
    template_name = "report/report_list.html"
    context_object_name = "reports"

    def get_queryset(self):
        return ReportModel.objects.active_reports()


class ReportDetailView(LoginRequiredMixin, ReportAccessMixin, DetailView):
    model = ReportModel
    template_name = "report/report_detail.html"
    context_object_name = "report"


class ReportCreateView(LoginRequiredMixin, ReportAccessMixin, CreateView):
    model = ReportModel
    form_class = ReportCreateForm
    template_name = "report/report_form.html"
    success_url = reverse_lazy("report:list")


class ReportUpdateView(LoginRequiredMixin, ReportAccessMixin, UpdateView):
    model = ReportModel
    form_class = ReportUpdateForm
    template_name = "report/report_form.html"
    success_url = reverse_lazy("report:list")


class ReportArchiveView(LoginRequiredMixin, ReportAccessMixin, View):
    def post(self, request, *args, **kwargs):
        report = get_object_or_404(ReportModel, pk=kwargs["pk"])
        report.archive()
        return JsonResponse({"status": "archived"})