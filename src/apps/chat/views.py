from django.shortcuts import render, HttpResponse


def ChatView(request):
    return render(request, 'chat/chat.html')


def RoomView(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

