from django.urls import reverse
from rest_framework import status
import pytest
from tickets.serializers.ticket_category import TicketCategorySerializer
from tests.users.conftest import *
from django.core.cache import cache


@pytest.mark.django_db
def test_ticket_category_list_unauthenticated(api_client):
    url = reverse('ticket-categories')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_ticket_category_list_success(auth_client, ticket_categories):
    client, _ = auth_client
    url = reverse('ticket-categories')

    cache.clear() # очистка кэша, чтобы полученный список всегда сравнивался с текущим в БД

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected_data = TicketCategorySerializer(ticket_categories, many=True).data
    assert response.data == expected_data