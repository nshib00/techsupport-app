import pytest
from channels.testing import WebsocketCommunicator
from channels.layers import BaseChannelLayer
from techsupport.asgi import application
from channels.layers import get_channel_layer
from tests.users.conftest import *
from tests.notifications.conftest import users_notifications_url, support_notifications_url, users_notifications_url_with_token


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_user_notification_connect_and_receive(create_user, users_notifications_url):
    url = users_notifications_url(create_user)
    communicator = WebsocketCommunicator(application, url)

    connected, _ = await communicator.connect()
    assert connected

    channel_layer: BaseChannelLayer = get_channel_layer()  # type: ignore

    # отправка события в группу
    await channel_layer.group_send(
        f"user_{create_user.id}",
        {
            "type": "notify",
            "data": {"message": "Привет!", "type": "info"}
        }
    )

    response = await communicator.receive_json_from()
    assert response == {"message": "Привет!", "type": "info"}

    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_support_notification_connect_and_receive(create_support_user, support_notifications_url):
    url = support_notifications_url(create_support_user)
    communicator = WebsocketCommunicator(application, url)

    connected, _ = await communicator.connect()
    assert connected

    channel_layer: BaseChannelLayer = get_channel_layer()  # type: ignore

    await channel_layer.group_send(
        "support",
        {
            "type": "notify_new_ticket",
            "ticket_id": 1,
            "subject": "Не работает микроволновка",
            "category": "Бытовая техника",
            "user": "user@example.com",
            "created_at": "2025-06-25T12:00:00Z",
            "link": "/tickets/1"
        }
    )

    response = await communicator.receive_json_from()
    assert response["type"] == "new_ticket"
    assert response["ticket_id"] == 1
    assert response["link"] == "/tickets/1"

    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_support_notification_reject_for_user(create_user, support_notifications_url):
    url = support_notifications_url(create_user)
    communicator = WebsocketCommunicator(application, url)

    connected, _ = await communicator.connect()
    assert not connected  # обычный пользователь не должен подключаться

    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_user_notification_reject_no_token(users_notifications_url_with_token):
    url = users_notifications_url_with_token(token="")
    communicator = WebsocketCommunicator(application, url)

    connected, _ = await communicator.connect()
    assert not connected
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_user_notification_reject_invalid_token(users_notifications_url_with_token):
    url = users_notifications_url_with_token(token="invalid.token.value")
    communicator = WebsocketCommunicator(application, url)
    
    connected, _ = await communicator.connect()
    assert not connected
    await communicator.disconnect()
