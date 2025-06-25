import pytest
from django.urls import reverse
from rest_framework import status
from users.models import User
from tests.users.conftest import *


@pytest.mark.django_db
def test_user_list_view_admin_can_view_all(auth_admin_client, create_user, create_support_user, create_admin):
    client, _ = auth_admin_client
    # создаем пользователей разных ролей
    u1 = create_user
    u2 = create_support_user
    u3 = create_admin
    url = reverse('users-list')

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    # должно вернуть всех трех
    roles = {item['role'] for item in response.data}
    assert roles.issuperset({u1.role, u2.role, u3.role})


@pytest.mark.django_db
def test_user_list_view_filter_by_role(auth_admin_client, create_user_factory):
    admin = create_user_factory(username='admin1', email='a@example.com', role=User.Role.ADMIN)
    user = create_user_factory(username='user1', email='u@example.com', role=User.Role.USER)
    client, _ = auth_admin_client

    url = reverse('users-list')
    response = client.get(url, {'role': User.Role.USER})
    assert response.status_code == status.HTTP_200_OK
    assert all(item['role'] == User.Role.USER for item in response.data)
    assert any(item['username'] == 'user1' for item in response.data)
    assert all(item['username'] != 'admin1' for item in response.data)


@pytest.mark.django_db
def test_user_list_view_filter_invalid_role(auth_admin_client):
    client, _ = auth_admin_client
    url = reverse('users-list')
    response = client.get(url, {'role': 'invalidrole'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'role' in response.data


@pytest.mark.django_db
def test_user_list_view_forbidden_for_non_admin(auth_support_client, auth_client):
    support_client, _ = auth_support_client
    url = reverse('users-list')
    response = support_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    user_client, _ = auth_client
    response2 = user_client.get(url)
    assert response2.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_list_view_unauthorized(api_client):
    url = reverse('users-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
