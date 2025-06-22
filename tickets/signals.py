from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from notifications.tasks import (
    notify_about_new_ticket_comment,
    notify_support_on_new_ticket_task,
    send_user_ticket_assigned_to_notification
)
from tickets.models.ticket_comment import TicketComment
from .models import Ticket
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Ticket)
def notify_support_on_new_ticket(sender, instance, created, **kwargs):
    logger.info(f"[SIGNAL] Ticket post_save (created={created}) for ticket #{instance.id}")
    if created:
        ticket_data = {
            "id": instance.id,
            "subject": instance.subject,
            "category": instance.category.name if instance.category else None,
            "user": {
                "id": instance.user.id,
                "email": instance.user.email,
            },
            "created_at": instance.created_at.isoformat(),
            "link": f"/support/tickets/{instance.id}/",
        }
        logger.info(f"[SIGNAL] Dispatching task notify_support_on_new_ticket_task with data: {ticket_data}")
        notify_support_on_new_ticket_task.delay(ticket_data)


@receiver(pre_save, sender=Ticket)
def notify_ticket_author_on_assignment(sender, instance, **kwargs):
    if not instance.pk:
        logger.debug("[SIGNAL] Skipping notify_ticket_author_on_assignment for unsaved instance")
        return

    try:
        old_ticket = Ticket.objects.get(pk=instance.pk)
    except Ticket.DoesNotExist:
        logger.warning(f"[SIGNAL] Old ticket #{instance.pk} not found")
        return

    if old_ticket.assigned_to != instance.assigned_to and instance.assigned_to:
        user = instance.user  # автор тикета
        task_data = {
            "title": f"Назначен ответственный по вашей заявке #{instance.pk}",
            "message": f"На заявку '{instance.subject}' назначен сотрудник поддержки: {instance.assigned_to.first_name or instance.assigned_to.username}",
        }
        logger.info(f"[SIGNAL] Dispatching task send_user_ticket_assigned_to_notification to user {user.id} with data: {task_data}")
        send_user_ticket_assigned_to_notification.delay(
            user_id=user.id,
            ticket_id=instance.pk,
            task_data=task_data
        )
    else:
        logger.debug(f"[SIGNAL] Assigned user not changed for ticket #{instance.pk}")


@receiver(post_save, sender=TicketComment)
def notify_about_new_comment(sender, instance, created, **kwargs):
    logger.info(f"[SIGNAL] TicketComment post_save (created={created}) for comment #{instance.id}")
    if not created or instance.is_internal:
        return # если комментарий не создан или является внутренним, не уведомляем пользователя

    ticket = instance.ticket
    user = ticket.user
    comment_msg = instance.message[:100] + '...' if len(instance.message) > 100 else instance.message

    logger.info(f"[SIGNAL] Dispatching notify_about_new_ticket_comment to user {user.id} for ticket #{ticket.id}")
    notify_about_new_ticket_comment.delay(
        user_id=user.id,
        ticket_id=ticket.id,
        author=instance.user.username,
        text=comment_msg,
    )
