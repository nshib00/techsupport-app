from notifications.tasks import send_status_change_notification_email
import pytest
from django.urls import reverse
from rest_framework import status
from tests.users.conftest import *
from tickets.models.ticket import Ticket


@pytest.mark.django_db
def test_ticket_update_status_validation_error(auth_support_client, create_ticket):
    client, _ = auth_support_client
    ticket = create_ticket
    url = reverse('ticket-status-update', kwargs={'pk': ticket.pk})
    response = client.patch(url, data={'status': Ticket.Status.IN_PROGRESS})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'assigned_to' in response.data


@pytest.mark.django_db
def test_ticket_update_status_success_and_send_email(mocker, auth_support_client, create_ticket, create_support_user):
    client, _ = auth_support_client
    ticket = create_ticket
    support = create_support_user
    ticket.assigned_to = support
    ticket.save()
    mocker.patch.object(send_status_change_notification_email, 'delay')

    url = reverse('ticket-status-update', kwargs={'pk': ticket.pk})
    response = client.patch(url, data={'status': Ticket.Status.CLOSED})
    assert response.status_code == status.HTTP_200_OK

    ticket.refresh_from_db()
    assert ticket.status == Ticket.Status.CLOSED
    assert ticket.closed_by_id == support.id
    assert ticket.closed_at is not None
    send_status_change_notification_email.delay.assert_called_once()


@pytest.mark.django_db
def test_ticket_update_status_forbidden_user(auth_client, create_ticket):
    client, _ = auth_client
    ticket = create_ticket
    url = reverse('ticket-status-update', kwargs={'pk': ticket.pk})
    response = client.patch(url, data={'status': Ticket.Status.IN_PROGRESS})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_ticket_update_status_not_found(auth_support_client):
    client, _ = auth_support_client
    url = reverse('ticket-status-update', kwargs={'pk': 999})
    response = client.patch(url, data={'status': Ticket.Status.IN_PROGRESS})
    assert response.status_code == status.HTTP_404_NOT_FOUND