import pytest
from tickets.models.ticket import Ticket
from tickets.models.ticket_comment import TicketComment
from tests.pytest.users.conftest import *
from tests.pytest.tickets.conftest import *
from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_notify_support_on_new_ticket(mocker, create_user, ticket_category):
    mock_task = mocker.patch("tickets.signals.notify_support_on_new_ticket_task.delay")

    ticket = Ticket.objects.create(
        subject="Test ticket",
        user=create_user,
        category=ticket_category,
    )

    mock_task.assert_called_once()
    args, kwargs = mock_task.call_args
    assert args[0]["id"] == ticket.pk
    assert args[0]["user"]["id"] == create_user.id


@pytest.mark.django_db
def test_notify_ticket_author_on_assignment(mocker, create_ticket, create_support_user):
    mock_task = mocker.patch("tickets.signals.send_user_ticket_assigned_to_notification.delay")

    ticket = create_ticket
    support_user = create_support_user

    ticket.assigned_to = support_user
    ticket.save()

    mock_task.assert_called_once()
    args, kwargs = mock_task.call_args
    assert kwargs["user_id"] == ticket.user.id
    assert kwargs["ticket_id"] == ticket.id
    assert "Назначен ответственный" in kwargs["task_data"]["title"]


@pytest.mark.django_db
def test_notify_about_new_comment_public(mocker, create_ticket, create_support_user):
    mock_task = mocker.patch("tickets.signals.notify_about_new_ticket_comment.delay")

    comment = TicketComment.objects.create(
        ticket=create_ticket,
        user=create_support_user,
        message="Это публичный комментарий",
        is_internal=False,
    )

    mock_task.assert_called_once_with(
        user_id=create_ticket.user.id,
        ticket_id=create_ticket.id,
        author=create_support_user.username,
        text="Это публичный комментарий",
    )


@pytest.mark.django_db
def test_notify_about_new_comment_internal_skipped(mocker, create_ticket, create_support_user):
    mock_task = mocker.patch("tickets.signals.notify_about_new_ticket_comment.delay")

    TicketComment.objects.create(
        ticket=create_ticket,
        user=create_support_user,
        message="Это внутренний комментарий",
        is_internal=True,
    )

    mock_task.assert_not_called()


@pytest.mark.django_db
def test_clear_ticket_cache_on_save_and_delete(mocker, create_ticket):
    cache_keys = [
        f"tickets_support_detail:{create_ticket.pk}",
        f"tickets_user_detail:{create_ticket.pk}",
        "tickets_support_list",
        "tickets_user_list",
    ]

    # Установим фейковые значения в кэш
    for key in cache_keys:
        cache.set(key, "dummy")

    # Проверка что значения установлены
    for key in cache_keys:
        assert cache.get(key) == "dummy"

    # Триггерим сигнал post_save
    create_ticket.subject = "Updated subject"
    create_ticket.save()

    # Проверяем, что кэш сброшен
    for key in cache_keys:
        assert cache.get(key) is None

    # Устанавливаем снова и проверяем, что post_delete тоже чистит
    for key in cache_keys:
        cache.set(key, "dummy")

    create_ticket.delete()

    for key in cache_keys:
        assert cache.get(key) is None
