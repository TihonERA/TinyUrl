import asyncio
import logging

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from src.core.config import get_settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)


async def place_holder(msg: AbstractIncomingMessage) -> None:
    logger.info(f"Got message {msg.body.decode()}")


async def main() -> None:
    stop_event = asyncio.Event()

    connection = await aio_pika.connect_robust(str(get_settings().RABBITMQ_URL))

    async with connection:
        logger.info("Opened TCP connection")
        channel = await connection.channel()

        queue_name = "links.clicks"

        queue = await channel.declare_queue(name=queue_name, durable=True)

        logger.info(f"Created/got queue with name: {queue_name}")

        await queue.consume(place_holder)

        await stop_event.wait()


if __name__ == "__main__":
    asyncio.run(main())
