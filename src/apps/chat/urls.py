from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ChatView, name='chat'),
    path("<str:room_name>/", views.RoomView, name="room"),
]
