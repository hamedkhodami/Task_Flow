from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),

    path('password/reset/', views.GetPhoneNumberView.as_view(), name='get_phone_number'),
    path('password/reset/confirm/', views.ResetPassConfirmView.as_view(), name='reset_pass_confirm'),
    path('password/reset/complete/', views.ResetPassCompleteView.as_view(), name='reset_pass_complete'),
]