from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('support', 'Сотрудник поддержки'),
        ('admin', 'Администратор')
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')