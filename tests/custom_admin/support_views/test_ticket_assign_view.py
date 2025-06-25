import pytest
from django.urls import reverse
from rest_framework import status
from tests.users.conftest import *


@pytest.mark.django_db
def test_ticket_assign_success(auth_support_client, create_ticket, create_support_user):
    client, _ = auth_support_client
    ticket = create_ticket
    support = create_support_user

    url = reverse('ticket-assign', kwargs={'pk': ticket.pk})
    payload = {'assigned_to': support.id}
    response = client.patch(url, data=payload)
    assert response.status_code == status.HTTP_200_OK

    ticket.refresh_from_db()
    assert ticket.assigned_to_id == support.id


@pytest.mark.django_db
def test_ticket_assign_unauthorized(api_client, create_ticket, create_support_user):
    ticket = create_ticket
    support = create_support_user
    url = reverse('ticket-assign', kwargs={'pk': ticket.pk})
    response = api_client.patch(url, data={'assigned_to': support.id})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_ticket_assign_forbidden_for_user(auth_client, create_ticket, create_support_user):
    client, _ = auth_client
    ticket = create_ticket
    support = create_support_user
    url = reverse('ticket-assign', kwargs={'pk': ticket.pk})
    response = client.patch(url, data={'assigned_to': support.id})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_ticket_assign_not_found(auth_support_client):
    client, _ = auth_support_client
    url = reverse('ticket-assign', kwargs={'pk': 999})
    response = client.patch(url, data={'assigned_to': 1})
    assert response.status_code == status.HTTP_404_NOT_FOUND