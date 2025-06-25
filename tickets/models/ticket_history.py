from django.db import models
from django.conf import settings
from tickets.models.ticket import Ticket


class TicketHistory(models.Model):
    ticket = models.ForeignKey(
        Ticket, 
        on_delete=models.CASCADE, 
        related_name='history',
        verbose_name='Обращение'
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name='Кем изменено'
    )
    field = models.CharField(max_length=100, verbose_name='Поле')
    old_value = models.TextField(null=True, blank=True, verbose_name='Старое значение')
    new_value = models.TextField(null=True, blank=True, verbose_name='Новое значение')
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    
    class Meta:
        verbose_name = 'История обращения'
        verbose_name_plural = 'История обращений'
        ordering = ['-changed_at']
    
    def __str__(self):
        return f"Изменение {self.field} для {self.ticket}"