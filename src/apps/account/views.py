from django.contrib.auth import login, logout
from django.urls import reverse_lazy,reverse
from django.views.generic import FormView, RedirectView, DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.contrib import messages

from .models import UserProfileModel,UserModel
from .mixins import LogoutRequiredMixin,ProfileCompletedRequiredMixin,AccessRequiredMixin
from .forms import LoginForm, UpdateProfileForm, GetPhoneNumberForm, ResetPassForm, VerifyPhoneNumberForm
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


class GetPhoneNumberView(LogoutRequiredMixin, FormView):
    template_name = 'account/password/get_phone.html'
    form_class = GetPhoneNumberForm

    def get_success_url(self):
        return reverse('account:send_code') + f'?next={reverse("account:reset_pass_confirm")}'

    def form_valid(self, form):
        user = form.cleaned_data.get('user')

        # Create register token and save it in sessions
        token = user.generate_token()
        self.request.session['secret_token'] = token

        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)


class ResetPassConfirmView(LogoutRequiredMixin, FormView):
    template_name = 'account/password/reset_pass_confirm.html'
    form_class = VerifyPhoneNumberForm
    success_url = reverse_lazy('account:reset_pass_complete')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method == 'POST':
            kwargs['data'] = {
                'code': self.request.POST.get('code'),
                'verify_code': self.request.session.get('verify_code'),
                'token': self.request.session.get('secret_token')
            }

        return kwargs

    def form_valid(self, form):
        # Delete code from session
        if 'verify_code' in self.request.session:
            del self.request.session['verify_code']

        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)


class ResetPassCompleteView(LogoutRequiredMixin, FormView):
    template_name = 'account/password/reset_pass_complete.html'
    form_class = ResetPassForm
    success_url = reverse_lazy('account:login')

    def form_valid(self, form):
        password = form.cleaned_data.get('password2')
        token = self.request.session.get('secret_token')

        try:
            user = UserModel.objects.get(token=token)
        except UserModel.DoesNotExist:
            messages.error(self.request, _('There is an issue! please try again'))
            return self.form_invalid(form)

        # Set new password and clear tokens
        user.set_password(password)
        user.is_verified = True
        user.clear_token(self.request)

        messages.success(self.request, _('Password successfully reset'))
        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
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




