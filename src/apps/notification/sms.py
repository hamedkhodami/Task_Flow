from apps.core.utils import send_sms


class SMSNotificationHandler:

    @classmethod
    def account_registration_handler(cls, sms_notification, phone_number):
        pattern = ''  # Add your pattern code here later
        send_sms(phone_number, pattern, username=sms_notification.to_user.username)

    @classmethod
    def password_reminder_handler(cls, sms_notification, phone_number):
        pattern = ''  # Add your pattern code here later
        send_sms(phone_number, pattern, reset_code=sms_notification.kwargs['reset_code'])

    @classmethod
    def meeting_request_handler(cls, sms_notification, phone_number):
        pattern = ''  # Add your pattern code here later
        send_sms(phone_number, pattern, meeting_date=sms_notification.kwargs['meeting_date'])

    @classmethod
    def added_to_project_handler(cls, sms_notification, phone_number):
        pattern = ''  # Add your pattern code here later
        send_sms(phone_number, pattern, project_name=sms_notification.kwargs['project_name'])

# Add handler mappings
SMS_NOTIFICATION_HANDLERS = {
    'ACCOUNT_REGISTRATION': SMSNotificationHandler.account_registration_handler,
    'PASSWORD_REMINDER': SMSNotificationHandler.password_reminder_handler,
    'MEETING_REQUEST': SMSNotificationHandler.meeting_request_handler,
    'ADDED_TO_PROJECT': SMSNotificationHandler.added_to_project_handler,
}