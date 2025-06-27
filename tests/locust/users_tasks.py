from locust import TaskSet, task
import logging
from tests.locust.utils.auth import AuthMixin


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("locust_test")


class UsersTasks(TaskSet, AuthMixin):
    def on_start(self):
        self.headers = {}
        self.user_data = self.register_user()
        if self.user_data:
            self.login_user(self.user_data)


    # def register_user(self):
    #     url = "/api/v1/users/register/"
    #     unique_id = uuid4().hex[:15]
    #     data = {
    #         "email": f"user_{unique_id}@test.com",
    #         "username": f"Test_{unique_id}",
    #         "password": "Abc_123d",
    #         "re_password": "Abc_123d"
    #     }

    #     with self.client.post(url, json=data, catch_response=True, name="users_register") as response:
    #         if response.status_code == 201:
    #             # logger.info(f"[OK] Registered user: {data['email']}")
    #             return response.json()
    #         else:
    #             logger.warning(f"[FAIL] {response.status_code} | URL: {url}")
    #             logger.warning(f"  Request: {json.dumps(data)}")
    #             logger.warning(f"  Response: {response.text}")
    #             response.failure(f"Unexpected status: {response.status_code}")


    # def login_user(self, user_data):
    #     url = "/api/v1/auth/login/"
    #     payload = {
    #         "username": user_data["username"],
    #         "password": "Abc_123d"
    #     }

    #     with self.client.post(url, json=payload, name="users_login", catch_response=True) as response:
    #         if response.status_code == 200 and "access" in response.json():
    #             token = response.json()["access"]
    #             self.headers = {"Authorization": f"Bearer {token}"}
    #             # logger.info(f"[OK] Logged in: {user_data['username']}")
    #             response.success()
    #         else:
    #             logger.warning(f"[FAIL] Login failed: {response.status_code}")
    #             logger.warning(f"  Response: {response.text}")
    #             response.failure("Login failed")

    @task
    def get_profile(self):
        if not self.headers:
            logger.warning("No auth headers, skipping get_profile")
            return

        url = "/api/v1/users/me/"
        with self.client.get(url, headers=self.headers, name="users_me", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                logger.warning(f"[FAIL] Profile fetch failed: {response.status_code}")
                response.failure("Profile fetch failed")
