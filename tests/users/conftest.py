import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from users.models import User
from uuid import uuid4


@pytest.fixture(scope='session')
def password():
    return 'Abc_12345'


@pytest.fixture
def user_data():
    # фабрика user_data, нужна для генерации разных данных при каждом вызове для избежания конфликтов,
    # когда в одном тесте вызываются сразу несколько фикстур, использующих одни и те же данные user_data
    def make_data():
        unique_id = uuid4().hex[:10]
        return {
            'username': f'test_user_{unique_id}',
            'email': f'test_{unique_id}@example.com',
            'password': 'Abc_12345',
            're_password': 'Abc_12345',
        }
    return make_data


@pytest.fixture
def create_user(user_data):
    data = user_data()
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
    )
    return user


@pytest.fixture
def create_user_factory():
    def make_user(**kwargs):
        password = kwargs.pop('password', 'Abc_12345')
        user = User.objects.create_user(**kwargs)
        user.set_password(password)
        user.save()
        return user
    return make_user


@pytest.fixture
def create_support_user(user_data):
    data = user_data()
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=User.Role.SUPPORT
    )
    return user


@pytest.fixture
def create_admin(user_data):
    data = user_data()
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=User.Role.ADMIN
    )
    return user


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(api_client, create_user):
    # получение JWT-токенов
    access_token = AccessToken.for_user(user=create_user)
    refresh_token = RefreshToken.for_user(user=create_user)

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client, refresh_token
