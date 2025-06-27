from django.urls import reverse
from rest_framework import status
import pytest
from tests.pytest.users.conftest import *
from tickets.models.ticket_comment import TicketComment


@pytest.mark.django_db
def test_create_public_comment_success(auth_client, create_ticket):
    client, _ = auth_client
    url = reverse('ticket-comments', kwargs={'pk': create_ticket.id})
    data = {
        'message': 'Публичный комментарий',
        'is_internal': False
    }

    response = client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert TicketComment.objects.filter(ticket=create_ticket, is_internal=False).exists()


@pytest.mark.django_db
def test_create_public_comment_unauthenticated(api_client, create_ticket):
    url = reverse('ticket-comments', kwargs={'pk': create_ticket.id})
    data = {
        'message': 'Публичный комментарий',
        'is_internal': False
    }
    response = api_client.get(url, data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_internal_comment_by_support(api_client, create_user, create_ticket):
    create_user.role = User.Role.SUPPORT
    create_user.save()

    access_token = AccessToken.for_user(create_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    url = reverse('ticket-comments', kwargs={'pk': create_ticket.id})
    data = {
        'message': 'Внутренний комментарий',
        'is_internal': True
    }

    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert TicketComment.objects.filter(ticket=create_ticket, is_internal=True).exists()


@pytest.mark.django_db
def test_create_internal_comment_by_user_forbidden(auth_client, create_ticket):
    client, _ = auth_client
    url = reverse('ticket-comments', kwargs={'pk': create_ticket.id})
    data = {
        'message': 'Нельзя мне такое писать',
        'is_internal': True
    }

    response = client.post(url, data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not TicketComment.objects.filter(ticket=create_ticket, is_internal=True).exists()


