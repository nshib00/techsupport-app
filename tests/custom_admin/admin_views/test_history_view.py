import pytest
from django.urls import reverse
from rest_framework import status
from tickets.serializers.ticket_history import TicketHistorySerializer
from tests.users.conftest import *
from tests.custom_admin.conftest import create_ticket_history


@pytest.mark.django_db
def test_ticket_history_view_as_admin(auth_admin_client, create_ticket_history):
    client, _ = auth_admin_client
    url = reverse('ticket-history')

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected_data = TicketHistorySerializer(create_ticket_history, many=True).data
    assert response.data == expected_data


@pytest.mark.django_db
def test_ticket_history_view_forbidden_for_common_user(auth_client):
    client, _ = auth_client
    url = reverse('ticket-history')

    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_ticket_history_view_forbidden_for_support(auth_support_client):
    client, _ = auth_support_client
    url = reverse('ticket-history')

    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_ticket_history_view_filtering(auth_admin_client, create_ticket_history):
    client, _ = auth_admin_client
    ticket_history = list(create_ticket_history)
    ticket_id = ticket_history[0].ticket.id
    user_id = ticket_history[0].changed_by.id
    field = ticket_history[0].field

    url = reverse('ticket-history')
    response = client.get(url, data={
        'ticket': ticket_id,
        'changed_by': user_id,
        'field': field
    })

    assert response.status_code == status.HTTP_200_OK
    assert all(item['ticket'] == ticket_id for item in response.data)
    assert all(item['changed_by'] == user_id for item in response.data)
    assert all(item['field'] == field for item in response.data)


@pytest.mark.django_db
def test_ticket_history_view_unauthorized(api_client):
    url = reverse('ticket-history')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED





