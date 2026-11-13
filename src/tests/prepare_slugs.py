import time
from logging import getLogger

from httpx import Client

logger = getLogger(__name__)


def main() -> None:
    SLUGS = []
    SLUGS_FILE_PATH = "src/tests/slugs.txt"

    with Client(base_url="http://localhost:8000") as client:
        for _ in range(10):
            body = {"original_url": "https://google.com/", "is_active": True}
            response = client.post("/links", json=body)

            try:
                slug = response.json()["slug"]

                SLUGS.append(slug)
                time.sleep(0.5)
            except KeyError:
                logger.warning("Hit the rate limit!")

    with open(SLUGS_FILE_PATH, "w", encoding="utf-8") as file:
        for slug in SLUGS:
            file.write(f"{slug}\n")


if __name__ == "__main__":
    main()
