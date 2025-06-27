import json
from uuid import uuid4
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("locust_test")


class AuthMixin:
    def register_user(self):
        url = "/api/v1/users/register/"
        unique_id = uuid4().hex[:15]
        data = {
            "email": f"user_{unique_id}@test.com",
            "username": f"Test_{unique_id}",
            "password": "Abc_123d",
            "re_password": "Abc_123d"
        }

        with self.client.post(url, json=data, catch_response=True, name="users_register") as response: # type: ignore
            if response.status_code == 201:
                return response.json()
            else:
                logger.warning(f"[FAIL] {response.status_code} | URL: {url}")
                logger.warning(f"  Request: {json.dumps(data)}")
                logger.warning(f"  Response: {response.text}")
                response.failure(f"Unexpected status: {response.status_code}")
                return None

    def login_user(self, user_data):
        url = "/api/v1/auth/login/"
        payload = {
            "username": user_data["username"],
            "password": "Abc_123d"
        }

        with self.client.post(url, json=payload, name="users_login", catch_response=True) as response: # type: ignore
            if response.status_code == 200 and "access" in response.json():
                token = response.json()["access"]
                self.headers = {"Authorization": f"Bearer {token}"}
                response.success()
                return True
            else:
                logger.warning(f"[FAIL] Login failed: {response.status_code}")
                logger.warning(f"  Response: {response.text}")
                response.failure("Login failed")
                return False

