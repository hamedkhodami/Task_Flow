from apps.core.utils import send_email

class EmailNotificationHandler:

    @classmethod
    def important_project_message_handler(cls, email_notification, recipient_email):
        subject = "Important Update on Your Project"
        template_name = "email_templates/important_project_message.html"
        context = {
            "user_name": email_notification.to_user.get_full_name(),
            "project_name": email_notification.kwargs.get('project_name'),
            "message": email_notification.description,
        }
        send_email(subject, template_name, [recipient_email], context)

    @classmethod
    def project_report_handler(cls, email_notification, recipient_email):
        subject = "Your Project Report"
        template_name = "email_templates/project_report.html"
        context = {
            "user_name": email_notification.to_user.get_full_name(),
            "project_name": email_notification.kwargs.get('project_name'),
            "report_link": email_notification.kwargs.get('report_link'),
        }
        send_email(subject, template_name, [recipient_email], context)

    @classmethod
    def team_invitation_handler(cls, email_notification, recipient_email):
        subject = "You're Invited to Join a Team"
        template_name = "email_templates/team_invitation.html"
        context = {
            "user_name": email_notification.to_user.get_full_name(),
            "team_name": email_notification.kwargs.get('team_name'),
            "invitation_link": email_notification.kwargs.get('invitation_link'),
        }
        send_email(subject, template_name, [recipient_email], context)

# Add handler mappings
EMAIL_NOTIFICATION_HANDLERS = {
    'IMPORTANT_PROJECT_MESSAGE': EmailNotificationHandler.important_project_message_handler,
    'PROJECT_REPORT': EmailNotificationHandler.project_report_handler,
    'TEAM_INVITATION': EmailNotificationHandler.team_invitation_handler,
}