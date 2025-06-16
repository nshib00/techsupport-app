from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        SUPPORT = 'support', 'Сотрудник поддержки'
        ADMIN = 'admin', 'Администратор'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)


    def is_support(self) -> bool:
        return self.role == self.Role.SUPPORT