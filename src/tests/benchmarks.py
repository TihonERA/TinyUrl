import random
import time

import httpx
from locust import FastHttpUser, between, events, task

SLUGS = []


@events.test_start.add_listener
def create_slugs(environment, **kwargs) -> None:
    base_url = "http://localhost:8000"

    with httpx.Client(base_url=base_url) as client:
        for _ in range(20):
            body = {"original_url": "https://google.com/", "is_active": True}
            response = client.post("/links", json=body)

            slug = response.json()["slug"]

            SLUGS.append(slug)
            time.sleep(0.1)


class User(FastHttpUser):
    wait_time = between(0.01, 0.05)

    @task
    def redirect(self) -> None:
        slug = random.choice(SLUGS)

        with self.client.get(
            f"/{slug}", allow_redirects=False, name="/[slug]", catch_response=True
        ) as response:
            if response.status_code != 302:
                response.failure(f"Expected 302, got {response.status_code}")
                return
            response.success()
