import pytest
from django.urls import reverse
from rest_framework import status
from tests.pytest.users.conftest import *
from tickets.models.ticket import Ticket


@pytest.mark.django_db
def test_ticket_list_retrieve_filters_and_cache(auth_support_client, create_support_user, create_ticket):
    client, _ = auth_support_client
    support = create_support_user
    # создаем тикеты с разными статусами и assigned_to
    t1 = create_ticket
    t2 = Ticket.objects.create(
        subject="Другой",
        description="",
        user=create_support_user,
        category=t1.category,
        assigned_to=support,
        status=Ticket.Status.IN_PROGRESS
    )

    url_for_list = reverse('ticket-list')
    response = client.get(url_for_list, data={'status': Ticket.Status.IN_PROGRESS})
    assert response.status_code == status.HTTP_200_OK
    assert all(item['status'] == Ticket.Status.IN_PROGRESS for item in response.data)

    url_for_detail = reverse('ticket-retrieve', kwargs={'pk': t2.pk})
    # первый вызов — кешируется
    r1 = client.get(url_for_detail)
    assert r1.status_code == status.HTTP_200_OK
    # обновление поля в БД. второй запрос вернет закешированные данные
    Ticket.objects.filter(pk=t2.pk).update(subject="Изменён")
    r2 = client.get(url_for_detail)
    assert r2.data['subject'] == r1.data['subject']


@pytest.mark.django_db
def test_ticket_list_retrieve_not_found(auth_support_client):
    client, _ = auth_support_client
    url = reverse('ticket-retrieve', kwargs={'pk': 999})
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_ticket_list_retrieve_forbidden_user(auth_client, create_ticket):
    client, _ = auth_client

    url_for_list = reverse('ticket-list')
    response = client.get(url_for_list)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    url_for_detail = reverse('ticket-retrieve', kwargs={'pk': create_ticket.pk})
    response = client.get(url_for_detail)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_ticket_list_unauthorized(api_client, create_ticket):
    url_for_list = reverse('ticket-list')
    response = api_client.get(url_for_list)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url_for_detail = reverse('ticket-retrieve', kwargs={'pk': create_ticket.pk})
    response = api_client.get(url_for_detail)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED