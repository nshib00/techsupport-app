from django.utils import timezone
import pytest
from tickets.models.ticket_history import TicketHistory
from tests.tickets.conftest import *


@pytest.fixture
def create_ticket_history(create_admin, create_user, create_ticket):
    """Создаёт несколько записей истории изменений тикета"""
    TicketHistory.objects.bulk_create([
        TicketHistory(
            ticket=create_ticket,
            field='status',
            old_value='open',
            new_value='in_progress',
            changed_by=create_admin,
            changed_at=timezone.now()
        ),
        TicketHistory(
            ticket=create_ticket,
            field='subject',
            old_value='Старая тема',
            new_value='Новая тема',
            changed_by=create_user,
            changed_at=timezone.now()
        ),
    ])
    return TicketHistory.objects.all()