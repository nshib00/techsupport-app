import logging
from smtplib import SMTPException
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from notifications.utils import check_and_get_channel_layer
from django.conf import settings
from techsupport.common.utils import sanitize_html
from .models import Ticket, Notification


logger = logging.getLogger('celery')


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
        
        if new_status != old_status: 
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
            logger.info(
                f"Email успешно отправлен пользователю {user.email} "
                f"по тикету #{ticket.pk} (статус: {old_status} → {new_status})"
            )
        else:
            logger.warning(
                f"Статус тикета #{ticket.pk} не изменен, email-уведомление пользователю {user.email} "
                "не было сформировано.  "
            )
        
    except Ticket.DoesNotExist:
        logger.error(f"Не удалось найти тикет с id={ticket_id} при попытке отправки уведомления")
    except SMTPException as e:
        logger.error(
            f"SMTP ошибка при отправке уведомления по тикету #{ticket_id} на email {user.email}: {e}"
        )
    except Exception as e:
        logger.error(
            f"Ошибка при отправке уведомления по тикету #{ticket_id}: {e.__class__.__name__}: {e}"
        )


@shared_task
def notify_support_on_new_ticket_task(ticket_data):    
    channel_layer = check_and_get_channel_layer()
    try:
        async_to_sync(channel_layer.group_send)(
            "support",
            {
                "type": "notify_new_ticket",
                "ticket_id": ticket_data["id"],
                "subject": ticket_data["subject"],
                "category": ticket_data["category"],
                "user": ticket_data["user"],
                "created_at": ticket_data["created_at"],
                "link": ticket_data["link"],
            }
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления поддержке о новом тикете: {e.__class__.__name__}: {e}")


@shared_task
def send_user_ticket_assigned_to_notification(user_id, ticket_id, task_data):
    notification_title = task_data["title"]
    notification_message = task_data["message"]

    Notification.objects.create(
        user_id=user_id,
        title=notification_title,
        message=notification_message,
        ticket_id=ticket_id,
        is_read=False
    )

    channel_layer = check_and_get_channel_layer()
    try:
        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "notify",
                "data": {
                    "title": notification_title,
                    "message": notification_message,
                }
            }
        )
    except Exception as e:
        logger.error(
            f"Ошибка при отправке уведомления пользователю о назначении сотрудника на тикет: {e.__class__.__name__}: {e}"
        )


@shared_task
def notify_about_new_ticket_comment(user_id, ticket_id, author, text):
    notification_title = f'Новый комментарий к заявке #{ticket_id}'
    notification_message = f'Пользователь {author} оставил(а) комментарий: "{text}"'

    Notification.objects.create(
        user_id=user_id,
        title=notification_title,
        message=notification_message,
        ticket_id=ticket_id,
        is_read=False
    )

    channel_layer = check_and_get_channel_layer()

    try:
        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "notify",
                "data": {
                    "title": notification_title,
                    "message": notification_message,
                }
            }
        )
    except Exception as e:
        logger.error(
            f"Ошибка при отправке уведомления пользователю о новом комментарии к тикету: {e.__class__.__name__}: {e}"
        )


