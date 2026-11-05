import asyncio
from logging import getLogger

import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from aio_pika.exceptions import ChannelClosed

from src.core.config import get_settings

logger = getLogger(__name__)


def place_holder(msg: AbstractIncomingMessage) -> None:
    logger.info(f"Got message {msg.body.decode()}")


async def main() -> None:
    stop_event = asyncio.Event()

    connection = await aio_pika.connect_robust(str(get_settings().RABBITMQ_URL))

    async with connection:
        logger.info("Opened TCP connection")
        channel = await connection.channel()

        queue_name = "links.clicks"

        try:
            queue = await channel.declare_queue(name=queue_name, durable=True)
        except ChannelClosed:
            logger.error(f"Error queue with name {queue_name} was not found")
            return

        logger.info(f"Created/got queue with name: {queue_name}")

        await queue.consume(place_holder)

        await stop_event.wait()


if __name__ == "__main__":
    asyncio.run(main())
