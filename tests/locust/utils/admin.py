def create_admin_user():
    import django
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techsupport.settings.dev")
    django.setup()

    from users.models import User

    admin_email = "admin@test.com"
    admin_password = "Admin_123"

    admin, created = User.objects.get_or_create(
        email=admin_email,
        role=User.Role.ADMIN,
        defaults={
            "username": "admin_user",
            "is_staff": True,
            "is_superuser": True,
        }
    )
    if created:
        admin.set_password(admin_password)
        admin.save()

    return admin_email, admin_password
    

def get_admin_token(client, email, password):
    response = client.post(
        "/api/v1/auth/login/",
        json={"username": email, "password": password}
    )

    if response.status_code == 200:
        return response.json()["access"]
    else:
        raise Exception(f"Admin login failed: {response.status_code} - {response.text}")