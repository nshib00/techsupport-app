from django.db import models
from techsupport import settings
from tickets.models.ticket_category import TicketCategory


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Открыта'),
        ('in_progress', 'В работе'),
        ('resolved', 'Решена'),
        ('closed', 'Закрыта'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
        ('critical', 'Критический'),
    ]

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
        choices=STATUS_CHOICES, 
        default='open',
        verbose_name='Статус'
    )
    priority = models.CharField(
        max_length=20, 
        choices=PRIORITY_CHOICES, 
        default='medium',
        verbose_name='Приоритет'
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
            models.Index(fields=['priority']),
            models.Index(fields=['user']),
            models.Index(fields=['assigned_to']),
        ]
    
    def __str__(self):
        return f"{self.subject} ({self.status})"