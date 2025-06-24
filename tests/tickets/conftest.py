import io
import pytest
from tickets.models.ticket import Ticket as TicketModel
from tickets.models.ticket_category import TicketCategory


@pytest.fixture
def ticket_category():
    return TicketCategory.objects.create(name="Ошибка в системе")


@pytest.fixture
def file_payload():
    return [io.BytesIO(b"file_content") for _ in range(2)]


@pytest.fixture
def big_file_list():
    return [io.BytesIO(b"x" * 10) for _ in range(11)]



@pytest.fixture
def create_ticket(create_user, ticket_category):
    return TicketModel.objects.create(
        user=create_user,
        subject="Проблема",
        category=ticket_category,
        description="Что-то пошло не так",
    )


@pytest.fixture
def tickets_list(create_user, ticket_category):
    return [
        TicketModel.objects.create(
            user=create_user,
            subject=f"Проблема {i}",
            category=ticket_category,
            description="Описание тикета",
            status='in_progress' if i % 2 == 0 else 'open'
        )
        for i in range(1, 11)
    ]


@pytest.fixture
def ticket_categories():
    return [
        TicketCategory.objects.create(name=f"Категория {i}")
        for i in range(1, 6)
    ]