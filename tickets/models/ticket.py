from django.db import models
from django.conf import settings
from tickets.models.ticket_category import TicketCategory


class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Открыта'
        IN_PROGRESS = 'in_progress', 'В работе'
        RESOLVED = 'resolved', 'Решена'
        CLOSED = 'closed', 'Закрыта'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='tickets',
        verbose_name='Пользователь'
    )
    category = models.ForeignKey(
        TicketCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Категория'
    )
    subject = models.CharField(max_length=255, verbose_name='Тема')
    description = models.TextField(verbose_name='Описание')
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default='open',
        verbose_name='Статус'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_tickets',
        verbose_name='Ответственный'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата закрытия')
    closed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='closed_tickets',
        verbose_name='Кем закрыта'
    )

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['user']),
            models.Index(fields=['assigned_to']),
        ]
    
    def __str__(self):
        return f"{self.subject} ({self.status})"