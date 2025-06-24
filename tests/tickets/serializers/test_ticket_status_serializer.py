from datetime import datetime
import pytest
from tickets.models.ticket import Ticket
from tickets.serializers.tickets import TicketStatusSerializer
from tests.users.conftest import *
from django.utils import timezone


@pytest.mark.django_db
def test_ticket_close(api_client, create_ticket, create_support_user):
    user = create_support_user
    ticket = create_ticket
    serializer = TicketStatusSerializer(
        instance=ticket,
        data={'status': Ticket.Status.CLOSED},
        context={'request': type('Request', (), {'user': user})()}
    )

    assert serializer.is_valid(), serializer.errors
    serializer.save()

    ticket.refresh_from_db()
    assert ticket.status == Ticket.Status.CLOSED
    assert ticket.closed_by == user
    assert ticket.closed_at is not None
    assert isinstance(ticket.closed_at, timezone.datetime)


@pytest.mark.django_db
def test_ticket_status_change(api_client, create_ticket, create_support_user):
    user = create_support_user
    ticket = create_ticket
    ticket.status = Ticket.Status.CLOSED
    ticket.closed_at = timezone.now()
    ticket.closed_by = user
    ticket.save()

    serializer = TicketStatusSerializer(
        instance=ticket,
        data={'status': Ticket.Status.IN_PROGRESS},
        # создание контекста c фейковым объектом request, который содержит поле user
        context={'request': type('Request', (), {'user': user})()}
    )

    assert serializer.is_valid(), serializer.errors
    serializer.save()

    ticket.refresh_from_db()
    assert ticket.status == Ticket.Status.IN_PROGRESS
    assert ticket.closed_by is None
    assert ticket.closed_at is None


@pytest.mark.django_db
def test_ticket_status_logs_history(mocker, create_ticket, create_support_user):
    user = create_support_user
    ticket = create_ticket

    # мок log_history
    mock_log = mocker.patch("tickets.serializers.tickets.TicketHistoryMixin.log_history")

    serializer = TicketStatusSerializer(
        instance=ticket,
        data={'status': Ticket.Status.CLOSED},
        context={'request': type('Request', (), {'user': user})()}
    )
    assert serializer.is_valid(), serializer.errors
    serializer.save()

    mock_log.assert_called_once_with(ticket, {'status': Ticket.Status.CLOSED})