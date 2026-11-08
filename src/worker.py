import asyncio
import logging

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from src.consumers.clicks_consumer_factory import create_clicks_consumer
from src.core.config import get_settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)


async def on_message(msg: AbstractIncomingMessage) -> None:
    async with msg.process(requeue=False):
        clicks_consumer = create_clicks_consumer()

        await clicks_consumer.create(msg)


async def main() -> None:
    stop_event = asyncio.Event()

    connection = await aio_pika.connect_robust(str(get_settings().RABBITMQ_URL))

    async with connection:
        logger.info("Opened TCP connection")
        channel = await connection.channel()

        await channel.set_qos(prefetch_count=10)

        queue_name = "links.clicks"

        queue = await channel.declare_queue(
            name="links.clicks",
            durable=True,
            arguments={
                "x-dead-letter-exchange": "clicks.dlx",
                "x-dead-letter-routing-key": "links.clicks.dead_letter",
            },
        )

        logger.info(f"Created/got queue with name: {queue_name}")

        await queue.consume(on_message)

        await stop_event.wait()


if __name__ == "__main__":
    asyncio.run(main())
