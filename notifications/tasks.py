from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from techsupport import settings
from techsupport.common.utils import sanitize_html
from .models import Ticket, Notification


@shared_task
def send_status_change_notification_email(ticket_id, old_status, new_status):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        user = ticket.user
        
        subject = f"Изменение статуса вашей заявки #{ticket.pk}"
        context = {
            'ticket_id': ticket.pk,
            'ticket_subject': sanitize_html(ticket.subject),
            'old_status': ticket.Status(old_status).label,
            'new_status': ticket.Status(new_status).label,
            'username': sanitize_html(user.first_name or user.username),
            'site_name': sanitize_html(settings.SITE_NAME),
        }
        
        text_message = render_to_string('notifications/emails/status_change_notification.txt', context)
        html_message = render_to_string('notifications/emails/status_change_notification.html', context)
        
        Notification.objects.create(
            user=user,
            title=f"Статус заявки #{ticket_id} изменён",
            message=f"Статус изменён с {old_status} на {new_status}",
            ticket=ticket,
            is_read=False
        )
        
        send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False
        )
        
    except Ticket.DoesNotExist:
        print(f"Ticket {ticket_id} not found")
    except Exception as e:
        print(f"Error sending notification: {e.__class__.__name__}: {e}")