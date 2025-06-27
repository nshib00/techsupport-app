from django.urls import reverse
from rest_framework import status
import pytest
from tests.pytest.users.conftest import *
from tickets.models.ticket import Ticket
from tickets.models.ticket_comment import TicketComment


@pytest.mark.django_db
def test_list_comments_for_user(auth_client, create_ticket):
    client, _ = auth_client

    TicketComment.objects.create(
        ticket=create_ticket,
        user=create_ticket.user,
        message='Мой комментарий'
    )
    url = reverse('ticket-comments', kwargs={'pk': create_ticket.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['message'] == 'Мой комментарий'


@pytest.mark.django_db
def test_user_cannot_see_foreign_comments(api_client, create_user, create_user_factory, ticket_category):
    other_user = create_user_factory(username='other_user')
    ticket = Ticket.objects.create(user=other_user, subject='Другой тикет', category=ticket_category, description='...')
    TicketComment.objects.create(ticket=ticket, user=other_user, message='Секретный комментарий')

    access_token = AccessToken.for_user(create_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('ticket-comments', kwargs={'pk': ticket.pk})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []
