from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager as DjangoUserManager


class UserManager(DjangoUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('Имя пользователя обязательно')
        email = self.normalize_email(email)
        extra_fields.setdefault('role', 'user')
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)



class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        SUPPORT = 'support', 'Сотрудник поддержки'
        ADMIN = 'admin', 'Администратор'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)

    objects = UserManager()


    def is_support(self) -> bool:
        return self.role == self.Role.SUPPORT
    
    @property
    def roles(self):
        return [role.value for role in self.Role]