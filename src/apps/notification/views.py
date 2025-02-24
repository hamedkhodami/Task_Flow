from django.shortcuts import render, HttpResponse


def ChatView(request):
    return render(request, 'notification/chat.html')

