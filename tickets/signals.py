from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@receiver(post_save, sender=Ticket)
def notify_support_on_new_ticket(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        if channel_layer is None:
            raise RuntimeError("Channel layer is not configured.")
        async_to_sync(channel_layer.group_send)(
            "support",
            {
                "type": "notify_new_ticket",
                "ticket_id": instance.id,
                "subject": instance.subject,
                "category": instance.category.name if instance.category else None,
                "user": {
                    "id": instance.user.id,
                    "email": instance.user.email,
                },
                "created_at": instance.created_at.isoformat(),
                "link": f"/support/tickets/{instance.id}/",
            }
        )