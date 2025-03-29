from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ChatView, name='chat'),
    path("room/<int:user_id>/", views.RoomView, name="room"),
]
