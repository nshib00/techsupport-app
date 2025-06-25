import pytest
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def users_notifications_url():
    def make_url(user):
        token = str(AccessToken.for_user(user))
        return f"/ws/users/notifications/?token={token}"
    return make_url


@pytest.fixture
def support_notifications_url():
    def make_url(user):
        token = str(AccessToken.for_user(user))
        return f"/ws/support/notifications/?token={token}"
    return make_url


@pytest.fixture
def users_notifications_url_with_token():
    def make_url(token: str):
        return f"/ws/users/notifications/?token={token}"
    return make_url