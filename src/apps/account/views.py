from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.contrib import messages

from .models import UserProfileModel,UserModel
from .mixins import LogoutRequiredMixin,ProfileCompletedRequiredMixin,AccessRequiredMixin
from .forms import LoginForm, UpdateProfileForm
from apps.core.utils import validate_form, toast_form_errors



class LoginView(LogoutRequiredMixin, FormView):

    template_name = 'account/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('public:index')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, _('You are successfully logged in.'))
        return super().form_valid(form)

    def form_invalid(self, form):
        validate_form(self.request, form)
        return super().form_invalid(form)


class logoutView(LoginRequiredMixin, RedirectView):

    url = reverse_lazy('account:login')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, _('You have been logged out'))
        return super().get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin,ProfileCompletedRequiredMixin,DetailView):

    template_name = 'account/profile.html'
    model = UserProfileModel

    def get_object(self, queryset=None):
        return self.request.user


class ProfileEditView(LoginRequiredMixin, ProfileCompletedRequiredMixin, UpdateView):

    template_name = 'account/profile_edit.html'
    form_class = UpdateProfileForm
    success_url = reverse_lazy('account:profile')

    def form_valid(self, form):
        messages.success(self.request, _('Your profile has been updated successfully'))
        return super().form_valid(form)

    def form_invalid(self, form):
        validate_form(self.request, form)
        return super().form_invalid(form)


class UserListView(LoginRequiredMixin, AccessRequiredMixin, ListView):

    template_name = 'account/user_list.html'
    model = UserModel
    roles = ['general_admin']

    def get_queryset(self):
        return UserModel.objects.all()


class UserDetailView(LoginRequiredMixin, AccessRequiredMixin, DetailView):

    template_name = 'account/user_detail.html'
    model = UserModel
    roles = ['general_admin']




