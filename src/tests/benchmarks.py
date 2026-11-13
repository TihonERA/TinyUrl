import random
from pathlib import Path

from locust import FastHttpUser, between, task

SLUGS = []
SLUGS_FILE = Path("src/tests/slugs.txt")

if SLUGS_FILE.exists():
    with open(SLUGS_FILE) as f:
        SLUGS = [line.strip() for line in f if line.strip()]


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
