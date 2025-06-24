from django.urls import reverse
from rest_framework import status
import pytest
from tests.users.conftest import *
from tickets.models.ticket import Ticket
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_create_ticket_success(auth_client, ticket_category):
    client, _ = auth_client
    url = reverse('tickets-list')
    data = {
        'subject': 'Ошибка',
        'category': ticket_category.id,
        'description': 'Приложение не работает'
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Ticket.objects.count() == 1


@pytest.mark.django_db
def test_create_ticket_unauthenticated(api_client):
    url = reverse('tickets-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_ticket_too_many_attachments(auth_client, ticket_category, big_file_list):
    client, _ = auth_client
    url = reverse('tickets-list')
    files = [SimpleUploadedFile(f'file_{i}.txt', f.read()) for i, f in enumerate(big_file_list)]
    data = {
        'subject': 'Слишком много файлов',
        'category': ticket_category.id,
        'description': 'Ошибка при загрузке',
        'attachments': files
    }
    response = client.post(url, data, format='multipart')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'attachments' in response.data


@pytest.mark.django_db
def test_create_ticket_invalid_data(auth_client):
    client, _ = auth_client
    url = reverse('tickets-list')
    data = {
        'subject': '',
        'category': '',
        'description': ''
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'subject' in response.data