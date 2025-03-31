from django import forms
from .models import ReportModel
from .validators import validate_json
from .enums import ReportScheduleEnum


class ReportCreateForm(forms.ModelForm):
    class Meta:
        model = ReportModel
        fields = ['type', 'access_level', 'filters', 'content', 'auto_send', 'schedule']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'access_level': forms.Select(attrs={'class': 'form-control'}),
            'filters': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'auto_send': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'schedule': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_filters(self):
        filters = self.cleaned_data.get('filters')
        if filters:
            validate_json(filters)  # اعتبارسنجی JSON
        return filters

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content:
            validate_json(content)  # اعتبارسنجی JSON
        return content


class ReportUpdateForm(forms.ModelForm):
    class Meta:
        model = ReportModel
        fields = ['filters', 'content', 'auto_send', 'schedule']
        widgets = {
            'filters': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'auto_send': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'schedule': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_filters(self):
        filters = self.cleaned_data.get('filters')
        if filters:
            validate_json(filters)
        return filters

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content:
            validate_json(content)
        return content


class ReportFilterForm(forms.Form):
    type = forms.ChoiceField(choices=[('', 'All')] + ReportModel.TypeReport.choices, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    access_level = forms.ChoiceField(choices=[('', 'All')] + ReportModel.UserAccess.choices, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    is_archived = forms.ChoiceField(choices=[('', 'All'), (True, 'Archived'), (False, 'Active')], required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    schedule = forms.ChoiceField(choices=[('', 'All')] + ReportScheduleEnum.choices, required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    def filter_queryset(self, queryset):
        """فیلتر کردن QuerySet بر اساس داده‌های ورودی"""
        data = self.cleaned_data
        if data.get('type'):
            queryset = queryset.filter(type=data['type'])
        if data.get('access_level'):
            queryset = queryset.filter(access_level=data['access_level'])
        if data.get('is_archived') != '':
            queryset = queryset.filter(is_archived=data['is_archived'])
        if data.get('schedule'):
            queryset = queryset.filter(schedule=data['schedule'])
        return queryset