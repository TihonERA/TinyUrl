import asyncio
import logging
import signal

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from src.consumers.clicks_consumer_factory import create_clicks_consumer
from src.core.cache import redis_client
from src.core.config import get_settings
from src.core.database import async_engine

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
    loop = asyncio.get_running_loop()

    connection = await aio_pika.connect_robust(str(get_settings().RABBITMQ_URL))

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, stop_event.set)

    try:
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

            consumer_tag = await queue.consume(on_message)

            await stop_event.wait()

            logger.info("Stop signal received. Starting Graceful shutdown.")

            await queue.cancel(consumer_tag)
    finally:
        logger.info("Closing broker connections...")
        await connection.close()

        logger.info("Closing Redis connection...")
        await redis_client.aclose()

        logger.info("Clossing Database connection...")
        await async_engine.dispose()

        logger.info("Shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
