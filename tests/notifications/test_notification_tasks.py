import pytest
from notifications.models import Notification
from notifications.tasks import (
    send_status_change_notification_email,
    notify_support_on_new_ticket_task,
    send_user_ticket_assigned_to_notification,
    notify_about_new_ticket_comment,
)
from tests.users.conftest import *
from tests.tickets.conftest import *


@pytest.mark.django_db(transaction=True)
def test_send_status_change_notification_email_changed_status(
    create_ticket, mocker
):
    ticket = create_ticket
    ticket.status = 'in_progress'
    ticket.save()

    mocker.patch('notifications.tasks.render_to_string', side_effect=lambda tpl, ctx: f'Rendered {tpl}')
    mock_send_mail = mocker.patch('notifications.tasks.send_mail')

    send_status_change_notification_email(ticket.id, ticket.status, 'resolved')

    assert Notification.objects.filter(user=ticket.user, ticket=ticket).exists()
    mock_send_mail.assert_called_once()
    assert 'Rendered notifications/emails/status_change_notification.txt' in mock_send_mail.call_args[1]['message']


@pytest.mark.django_db(transaction=True)
def test_send_status_change_notification_email_same_status(create_ticket, mocker):
    ticket = create_ticket
    mock_send_mail = mocker.patch('notifications.tasks.send_mail')

    send_status_change_notification_email(ticket.id, ticket.status, ticket.status)

    assert not Notification.objects.filter(user=ticket.user, ticket=ticket).exists()
    mock_send_mail.assert_not_called()


@pytest.mark.django_db(transaction=True)
def test_send_status_change_notification_email_ticket_not_found(caplog):
    send_status_change_notification_email(99999, 'open', 'in_progress')
    assert 'Не удалось найти тикет с id=99999' in caplog.text


@pytest.mark.django_db(transaction=True)
def test_notify_support_on_new_ticket_task(mocker):
    mock_group_send = mocker.Mock()
    mocker.patch('notifications.tasks.async_to_sync', return_value=mock_group_send)
    mocker.patch('notifications.tasks.check_and_get_channel_layer')

    ticket_data = {
        'id': 1,
        'subject': 'Тестовая тема',
        'category': 'Какая-то категория',
        'user': 'user@example.com',
        'created_at': '2025-06-25T12:00:00Z',
        'link': '/tickets/1'
    }

    notify_support_on_new_ticket_task(ticket_data)

    mock_group_send.assert_called_once()
    channel, data = mock_group_send.call_args[0]

    assert channel == 'support'
    assert data['type'] == 'notify_new_ticket'
    assert data['ticket_id'] == ticket_data['id']
    assert data['subject'] == ticket_data['subject']


@pytest.mark.django_db(transaction=True)
def test_send_user_ticket_assigned_to_notification(create_ticket, mocker):
    ticket = create_ticket
    user = ticket.user

    mock_group_send = mocker.Mock()
    mocker.patch('notifications.tasks.async_to_sync', return_value=mock_group_send)
    mocker.patch('notifications.tasks.check_and_get_channel_layer')

    task_data = {'title': 'Назначен сотрудник', 'message': 'Вашей заявке назначен сотрудник'}

    send_user_ticket_assigned_to_notification(user.id, ticket.id, task_data)

    assert Notification.objects.filter(user=user, title=task_data['title']).exists()

    mock_group_send.assert_called_once()
    channel, data = mock_group_send.call_args[0]
    assert channel == f'user_{user.pk}'
    assert data['type'] == 'notify'
    assert data['data']['title'] == task_data['title']
    assert data['data']['message'] == task_data['message']


@pytest.mark.django_db(transaction=True)
def test_notify_about_new_ticket_comment(create_ticket, mocker):
    ticket = create_ticket
    user = ticket.user

    mock_group_send = mocker.Mock()
    mocker.patch('notifications.tasks.async_to_sync', return_value=mock_group_send)
    mocker.patch('notifications.tasks.check_and_get_channel_layer')

    author = 'support@example.com'
    text = 'Текст комментария'

    notify_about_new_ticket_comment(user.id, ticket.id, author, text)

    notification = Notification.objects.get(user=user, ticket=ticket)
    assert author in notification.message
    mock_group_send.assert_called_once()

    channel, data = mock_group_send.call_args[0]
    assert channel == f'user_{user.pk}'
    assert data['type'] == 'notify'
    assert str(user.pk) in data['data']['title']
    assert author in data['data']['message']
    assert text in data['data']['message']
