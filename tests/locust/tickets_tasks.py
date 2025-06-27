from locust import TaskSet, task
from uuid import uuid4
from tests.locust.utils.auth import AuthMixin
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("locust_test")


class TicketsTasks(TaskSet, AuthMixin):
    def on_start(self):
        self.headers = {}
        self.user_data = self.register_user()
        if self.user_data:
            self.login_user(self.user_data)


    @task
    def list_tickets(self):
        with self.client.get("/api/v1/tickets/", headers=self.headers, name="tickets_list", catch_response=True) as response:
            if response.status_code == 200 and self.user_data:
                logger.info(f"Fetched tickets list for user: {self.user_data['username']}")
                response.success()
            else:
                logger.warning(f"[FAIL] Failed to fetch tickets list: {response.status_code}")
                response.failure(f"Unexpected status: {response.status_code}")


    @task
    def create_ticket(self):
        url = "/api/v1/tickets/"
        unique_id = uuid4().hex[:15]
        data = {
            "subject": f"Test Ticket {unique_id}",
            "category": None,
            "description": f"This is a test ticket {unique_id}",
            "attachments": []
        }

        with self.client.post(url, json=data, headers=self.headers, catch_response=True, name="ticket_create") as response:
            if response.status_code == 201:
                logger.info(f"Created ticket: {data['subject']}")
                response.success()
            else:
                logger.warning(f"[FAIL] Ticket creation failed: {response.status_code}")
                logger.warning(f"  Request: {data}")
                logger.warning(f"  Response: {response.text}")
                response.failure(f"Unexpected status: {response.status_code}")


    @task
    def get_ticket_details(self):
        ticket_id = self.get_existing_ticket_id()
        if not ticket_id:
            logger.warning("No ticket available for fetching details.")
            return

        url = f"/api/v1/tickets/{ticket_id}/"
        with self.client.get(url, headers=self.headers, catch_response=True, name="ticket_detail") as response:
            if response.status_code == 200:
                logger.info(f"Fetched ticket details for ticket ID: {ticket_id}")
                response.success()
            else:
                logger.warning(f"[FAIL] Failed to fetch ticket details: {response.status_code}")
                response.failure(f"Unexpected status: {response.status_code}")


    @task
    def list_ticket_comments(self):
        ticket_id = self.get_existing_ticket_id()
        if not ticket_id:
            logger.warning("No ticket available to fetch comments.")
            return

        url = f"/api/v1/tickets/{ticket_id}/comments/"
        with self.client.get(url, headers=self.headers, catch_response=True, name="ticket_comments_list") as response:
            if response.status_code == 200:
                logger.info(f"Fetched comments for ticket ID: {ticket_id}")
                response.success()
            else:
                logger.warning(f"[FAIL] Failed to fetch comments: {response.status_code}")
                response.failure(f"Unexpected status: {response.status_code}")


    @task
    def create_ticket_comment(self):
        ticket_id = self.get_existing_ticket_id()
        if not ticket_id:
            logger.warning("No ticket available to comment on.")
            return

        unique_id = uuid4().hex[:6]
        data = {
            "message": f"This is a comment {unique_id}",
            "is_internal": False
        }

        url = f"/api/v1/tickets/{ticket_id}/comments/"
        with self.client.post(url, json=data, headers=self.headers, catch_response=True, name="ticket_comment_create") as response:
            if response.status_code == 201:
                logger.info(f"Created comment for ticket ID: {ticket_id}")
                response.success()
            elif response.status_code == 403:
                logger.warning(f"[FAIL] Not allowed to create internal comment: {response.status_code}")
                response.failure("Forbidden")
            else:
                logger.warning(f"[FAIL] Failed to create comment: {response.status_code}")
                logger.warning(f"  Request: {data}")
                logger.warning(f"  Response: {response.text}")
                response.failure(f"Unexpected status: {response.status_code}")


    def get_existing_ticket_id(self):
        url = "/api/v1/tickets/"
        with self.client.get(url, headers=self.headers, catch_response=True, name="ticket_get_id") as response:
            if response.status_code == 200:
                tickets = response.json()
                if tickets:
                    return tickets[0]['id']
            return None
