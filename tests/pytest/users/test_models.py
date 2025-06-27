import pytest
from users.models import User


@pytest.mark.django_db
def test_create_common_user(password):
    user = User.objects.create_user(username='test', email='a@b.com', password=password)
    assert user.role == User.Role.USER
    assert user.check_password(password)


@pytest.mark.django_db
def test_create_support_user(password):
    user = User.objects.create_user(
        username='test2', email='c@d.com', password=password, role=User.Role.SUPPORT
    )
    assert user.role == User.Role.SUPPORT
    assert user.check_password(password)

@pytest.mark.django_db
def test_create_admin_user(password):
   
    user = User.objects.create_superuser(
        username='test3', email='e@f.com', password=password, role=User.Role.ADMIN
    )
    assert user.role == User.Role.ADMIN
    assert user.is_superuser is True
    assert user.check_password(password)

def test_is_support():
    user = User(username='temp', role=User.Role.SUPPORT)
    assert user.is_support() is True

    user.role = User.Role.USER
    assert user.is_support() is False
