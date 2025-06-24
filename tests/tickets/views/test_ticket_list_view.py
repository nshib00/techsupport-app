from django.urls import reverse
from rest_framework import status
import pytest
from tests.users.conftest import *


@pytest.mark.django_db
def test_ticket_list_view_success(auth_client, create_ticket):
    client, _ = auth_client
    url = reverse('tickets-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_ticket_list_filter_invalid_status(auth_client, tickets_list):
    client, _ = auth_client
    url = reverse('tickets-list')
    response = client.get(url, {'status': 'aaa'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_ticket_list_filter_correct_status(auth_client, tickets_list):
    client, _ = auth_client
    url = reverse('tickets-list')
    response = client.get(url, {'status': 'in_progress'})
    assert response.status_code == status.HTTP_200_OK
    assert all(ticket['status'] == 'in_progress' for ticket in response.data)