from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SMSNotificationModel, EmailNotificationModel
from .sms import SMS_NOTIFICATION_HANDLERS
from .email import EMAIL_NOTIFICATION_HANDLERS


def sms_notify_handler(notification):
    """ Handle SMS notifications based on type """
    handler = SMS_NOTIFICATION_HANDLERS.get(notification.type)
    if handler:
        handler(notification, notification.to_user.phone_number)


def email_notify_handler(notification):
    """ Handle Email notifications based on type """
    handler = EMAIL_NOTIFICATION_HANDLERS.get(notification.type)
    if handler:
        handler(notification, notification.to_user.email)


@receiver(post_save, sender=SMSNotificationModel)
def handle_sms_notification(sender, instance, created, **kwargs):
    """ Send SMS when a new SMSNotificationModel is created """
    if created and instance.send_sms:
        sms_notify_handler(instance)


@receiver(post_save, sender=EmailNotificationModel)
def handle_email_notification(sender, instance, created, **kwargs):
    """ Send Email when a new EmailNotificationModel is created """
    if created and instance.send_email:
        email_notify_handler(instance)