from django.db import models
from django.core.validators import MinLengthValidator


class TicketCategory(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название категории',
        unique=True,
        validators=[MinLengthValidator(3)]
    )
    description = models.TextField(blank=True, max_length=500, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Категория обращения'
        verbose_name_plural = 'Категории обращений'
        ordering = ['name']
    
    def __str__(self):
        return self.name