from django.urls import reverse
import pytest
from rest_framework import status
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


@pytest.mark.django_db
def test_me_view(auth_client, create_user):
    client, _ = auth_client
    url = reverse('user-me')
    
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == create_user.email


@pytest.mark.django_db
def test_login_view(api_client, user_data, create_user_factory):
    data = user_data()
    create_user_factory(
        username=data['username'],
        email=data['email'],
        password=data['password'],
    )
    
    url = reverse('login')
    response = api_client.post(url, {
        'username': data['username'],
        'password': data['password'],
    }, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_refresh_view(auth_client, create_user):
    client, refresh_token = auth_client

    url = reverse('refresh-jwt')
    response = client.post(url, {'refresh': str(refresh_token)}, format='json')
    
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_logout_view(auth_client):
    client, refresh_token = auth_client
    url = reverse('logout')
    response = client.post(url, {'refresh': str(refresh_token)}, format='json')
    
    assert response.status_code == status.HTTP_205_RESET_CONTENT


@pytest.mark.django_db
def test_verify_view(auth_client, create_user):
    client, refresh_token = auth_client
    url = reverse("verify-jwt")

    # тест с невалидным токеном
    response = client.post(url, {'token': "invalid_token"}, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # тест с валидным токеном
    response = client.post(url, {'token': str(refresh_token)}, format='json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_register_view(api_client):
    url = reverse('user-register')
    data = {
        'username': 'new_user',
        'email': 'newuser@example.com',
        'password': 'NewPass123',
        're_password': 'NewPass123'
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data
    assert response.data['email'] == data['email']


@pytest.mark.django_db
def test_reset_password_view(auth_client, create_user):
    client, _ = auth_client

    url = reverse('reset-password')
    data = {'email': create_user.email}
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_reset_password_confirm_view(auth_client, create_user):
    client, _ = auth_client

    # генерация uid и token через утилиты django
    uid = urlsafe_base64_encode(force_bytes(create_user.pk))
    token = default_token_generator.make_token(create_user)

    url = reverse('reset-password-confirm')
    data = {
        'uid': uid,
        'token': token, # не refresh token
        'new_password': 'NewPassword123'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT