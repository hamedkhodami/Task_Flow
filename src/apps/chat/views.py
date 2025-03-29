from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from apps.account.models import UserModel

from .models import MessageModel


def ChatView(request):
    """ نمایش فرم ورود شماره موبایل برای پیدا کردن کاربر و ورود به چت """
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        try:
            receiver = UserModel.objects.get(phone_number=phone_number)
            return redirect("chat:room", user_id=receiver.id)
        except UserModel.DoesNotExist:
            messages.error(request, _("User Not Found"))

    return render(request, "chat/chat.html")


def RoomView(request, user_id):
    """ بررسی و ورود به چت خصوصی بین دو کاربر """
    receiver = get_object_or_404(UserModel, id=user_id)
    sender = request.user  # کاربر لاگین شده

    # بررسی اینکه آیا قبلاً چتی بین این دو نفر بوده یا نه؟
    chat_exists = MessageModel.objects.filter(
        sender=sender, receiver=receiver
    ).exists() or MessageModel.objects.filter(
        sender=receiver, receiver=sender
    ).exists()

    if not chat_exists:
        # اگر چت وجود نداشته باشه، پیام خوش‌آمدگویی ارسال کن
        MessageModel.objects.create(sender=sender, receiver=receiver, message=_("New chat started."))

    return render(request, "chat/room.html", {"receiver": receiver})