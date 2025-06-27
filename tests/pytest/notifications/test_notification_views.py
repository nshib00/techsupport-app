import pytest
from django.urls import reverse
from rest_framework import status
from notifications.models import Notification
from tests.pytest.users.conftest import *


@pytest.mark.django_db
def test_list_notifications(auth_client, create_user):
    client, _ = auth_client

    user = create_user
    for i in range(1, 4):
        Notification.objects.create(
            user=user,
            message=f"Уведомление {i}"
        )

    url = reverse("notifications-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3


@pytest.mark.django_db
def test_list_notifications_unauthenticated(api_client):
    url = reverse("notifications-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_mark_notification_as_read_success(auth_client, create_user):
    client, _ = auth_client
    user = create_user

    notification = Notification.objects.create(user=user, message="Непрочитанное", is_read=False)
    url = reverse("mark-notification-as-read", args=[notification.pk])

    response = client.patch(url, {"is_read": True}, format="json")

    assert response.status_code == status.HTTP_200_OK
    notification.refresh_from_db()
    assert notification.is_read is True


@pytest.mark.django_db
def test_mark_notification_as_read_unauthorized(api_client, create_user_factory):
    owner = create_user_factory(username="owner", email="owner@example.com")
    other = create_user_factory(username="some_user", email="someuser@example.com")

    notification = Notification.objects.create(user=owner, message="Чужое уведомление", is_read=False)

    access_token = AccessToken.for_user(other)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    url = reverse("mark-notification-as-read", args=[notification.pk])
    response = api_client.patch(url, {"is_read": True}, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    notification.refresh_from_db()
    assert notification.is_read is False
