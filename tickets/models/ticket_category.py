from django.db import models


class TicketCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активна ли категория')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Категория обращения'
        verbose_name_plural = 'Категории обращений'
        ordering = ['name']
    
    def __str__(self):
        return self.name