import pytest
from tests.pytest.users.conftest import *
from tickets.serializers.tickets import TicketAssignSerializer


@pytest.mark.django_db
def test_ticket_assign_success(create_ticket, create_support_user):
    ticket = create_ticket
    support_user = create_support_user

    serializer = TicketAssignSerializer(
        instance=ticket,
        data={'assigned_to': support_user.id},
        context={'request': type('Request', (), {'user': support_user})()}
    )

    assert serializer.is_valid(), serializer.errors
    serializer.save()

    ticket.refresh_from_db()
    assert ticket.assigned_to == support_user


@pytest.mark.django_db
def test_ticket_assign_invalid_user(create_ticket, create_user):
    # попытка присвоения тикета не саппортом, а обычным пользователем

    ticket = create_ticket

    serializer = TicketAssignSerializer(
        instance=ticket,
        data={'assigned_to': create_user.id},
        context={'request': type('Request', (), {'user': create_user})()}
    )

    assert not serializer.is_valid()
    assert 'assigned_to' in serializer.errors
    assert 'Пользователь с таким ID не найден или не является сотрудником поддержки.' in serializer.errors['assigned_to'][0]


@pytest.mark.django_db
def test_ticket_assign_logs_history(mocker, create_ticket, create_support_user):
    ticket = create_ticket
    support_user = create_support_user

    mock_log = mocker.patch("tickets.serializers.tickets.TicketHistoryMixin.log_history")

    serializer = TicketAssignSerializer(
        instance=ticket,
        data={'assigned_to': support_user.id},
        context={'request': type('Request', (), {'user': support_user})()}
    )
    assert serializer.is_valid(), serializer.errors
    serializer.save()

    mock_log.assert_called_once_with(ticket, {'assigned_to': support_user})