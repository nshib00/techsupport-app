import pytest
from django.urls import reverse
from rest_framework import status
from users.models import User
from tests.pytest.users.conftest import *


@pytest.mark.django_db
def test_user_update_role_success(auth_admin_client, create_user_factory):
    # админ меняет роль support -> user
    target = create_user_factory(username='target', email='t@example.com', role=User.Role.SUPPORT)
    client, _ = auth_admin_client
    url = reverse('change-user-role', kwargs={'pk': target.pk})
    response = client.patch(url, data={'role': User.Role.USER})
    assert response.status_code == status.HTTP_200_OK
    target.refresh_from_db()
    assert target.role == User.Role.USER


@pytest.mark.django_db
def test_user_update_role_cannot_update_self(auth_admin_client, create_admin):
    # админ хочет изменить свою роль
    self_user = create_admin
    client, _ = auth_admin_client
    url = reverse('change-user-role', kwargs={'pk': self_user.pk})
    response = client.patch(url, data={'role': User.Role.SUPPORT})
    # Django UpdateAPIView не запрещает прямую проверку, но логика в представлении – нет проверки self,
    # Для корректности: считаем, что backend должен вернуть 400 или разрешить — проверяем 400
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_update_role_invalid(auth_admin_client, create_user_factory):
    target = create_user_factory(username='u2', email='u2@example.com', role=User.Role.USER)
    client, _ = auth_admin_client
    url = reverse('change-user-role', kwargs={'pk': target.pk})
    response = client.patch(url, data={'role': 'invalid'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_update_role_not_found(auth_admin_client):
    client, _ = auth_admin_client
    url = reverse('change-user-role', kwargs={'pk': 99999})
    response = client.patch(url, data={'role': User.Role.USER})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_update_role_forbidden_for_non_admin(auth_support_client, create_user_factory):
    target = create_user_factory(username='u3', email='u3@example.com', role=User.Role.USER)
    support_client, _ = auth_support_client
    url = reverse('change-user-role', kwargs={'pk': target.pk})
    response = support_client.patch(url, data={'role': User.Role.ADMIN})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_update_role_unauthorized(api_client, create_user_factory):
    target = create_user_factory(username='u4', email='u4@example.com', role=User.Role.USER)
    url = reverse('change-user-role', kwargs={'pk': target.pk})
    response = api_client.patch(url, data={'role': User.Role.SUPPORT})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED