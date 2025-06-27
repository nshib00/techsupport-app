import pytest
from django.urls import reverse
from rest_framework import status
from tickets.models.ticket_category import TicketCategory
from tests.pytest.users.conftest import *


@pytest.mark.django_db
def test_create_ticket_category_success(auth_admin_client, create_admin):
    client, _ = auth_admin_client

    url = reverse('ticket-category-list')
    payload = {'name': 'Новая категория'}

    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert TicketCategory.objects.filter(name='Новая категория').exists()


@pytest.mark.django_db
def test_create_ticket_category_conflict(auth_admin_client, create_admin):
    client, _ = auth_admin_client
    
    TicketCategory.objects.create(name='Дублирующая категория')

    url = reverse('ticket-category-list')
    payload = {'name': 'Дублирующая категория'}

    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert 'name' in response.data


@pytest.mark.django_db
def test_create_ticket_category_forbidden(auth_client, create_user):
    client, _ = auth_client

    url = reverse('ticket-category-list')
    payload = {'name': 'Недоступная категория'}

    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_partial_update_ticket_category_success(auth_admin_client, create_admin):
    client, _ = auth_admin_client
    
    category = TicketCategory.objects.create(name='Обновить меня')
    url = reverse('ticket-category-detail', kwargs={'pk': category.pk})
    payload = {'name': 'Новое имя'}

    response = client.patch(url, data=payload)
    assert response.status_code == status.HTTP_200_OK
    category.refresh_from_db()
    assert category.name == 'Новое имя'


@pytest.mark.django_db
def test_partial_update_ticket_category_conflict(auth_admin_client, create_admin):
    client, _ = auth_admin_client

    existing = TicketCategory.objects.create(name='Существующая категория')
    to_update = TicketCategory.objects.create(name='Обновляемая категория')

    url = reverse('ticket-category-detail', kwargs={'pk': to_update.pk})
    payload = {'name': 'Существующая категория'}

    response = client.patch(url, data=payload)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert 'name' in response.data


@pytest.mark.django_db
def test_partial_update_ticket_category_not_found(auth_admin_client, create_admin):
    client, _ = auth_admin_client

    url = reverse('ticket-category-detail', kwargs={'pk': 999})
    payload = {'name': 'Несуществующая'}

    response = client.patch(url, data=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_ticket_category_success(auth_admin_client, create_admin):
    client, _ = auth_admin_client

    category = TicketCategory.objects.create(name='Удаляемая')
    url = reverse('ticket-category-detail', kwargs={'pk': category.pk})

    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not TicketCategory.objects.filter(pk=category.pk).exists()


@pytest.mark.django_db
def test_delete_ticket_category_not_found(auth_admin_client, create_admin):
    client, _ = auth_admin_client

    url = reverse('ticket-category-detail', kwargs={'pk': 999})

    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_ticket_category_forbidden(auth_client, create_user):
    client, _ = auth_client

    category = TicketCategory.objects.create(name='Не твоя категория')
    url = reverse('ticket-category-detail', kwargs={'pk': category.pk})

    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
