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
]