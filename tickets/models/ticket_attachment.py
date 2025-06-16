from django.db import models
from techsupport import settings
from tickets.models.ticket import Ticket
from os.path import basename


def ticket_attachment_path(instance, filename):
    safe_name = basename(filename)
    return f'ticket-attachments/{instance.ticket.id}/{safe_name}'


class TicketAttachment(models.Model):
    ticket = models.ForeignKey(
        Ticket, 
        on_delete=models.CASCADE, 
        related_name='attachments',
        verbose_name='Обращение'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    file = models.FileField(
        upload_to=ticket_attachment_path,
        verbose_name='Файл'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    
    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'
    
    def __str__(self):
        return f"Вложение к {self.ticket.subject}"