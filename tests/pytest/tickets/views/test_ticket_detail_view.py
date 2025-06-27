from django.urls import reverse
from rest_framework import status
import pytest
from tests.pytest.users.conftest import *


@pytest.mark.django_db
def test_get_ticket_detail_success(auth_client, create_ticket):
    client, _ = auth_client
    url = reverse('ticket-detail', kwargs={'pk': create_ticket.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == create_ticket.id


@pytest.mark.django_db
def test_ticket_detail_unauthenticated(api_client, create_ticket):
    url = reverse('ticket-detail', kwargs={'pk': create_ticket.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_ticket_detail_not_found(auth_client):
    client, _ = auth_client
    url = reverse('ticket-detail', kwargs={'pk': 9999})
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_ticket_detail_not_owner(api_client, create_user, create_ticket):
    other_user = User.objects.create_user(username='other', password='Password123')
    access_token = AccessToken.for_user(other_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    url = reverse('ticket-detail', kwargs={'pk': create_ticket.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND