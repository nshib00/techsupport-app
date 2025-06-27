from locust import HttpUser, between
from tests.locust.tickets_tasks import TicketsTasks
from tests.locust.users_tasks import UsersTasks


class LocustTestUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [UsersTasks, TicketsTasks]
    host = "http://127.0.0.1:8090"