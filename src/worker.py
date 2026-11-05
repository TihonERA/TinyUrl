import asyncio
from logging import getLogger

import aio_pika
from aio_pika.exceptions import ChannelClosed

from src.core.config import get_settings

logger = getLogger(__name__)


async def main() -> None:
    stop_event = asyncio.Event()

    connection = await aio_pika.connect_robust(str(get_settings().RABBITMQ_HOST))
    channel = connection.channel()

    async with connection:
        channel = await connection.channel()

        queue_name = "links.clicks"

        try:
            queue = await channel.declare_queue(queue_name, passive=True)
        except ChannelClosed:
            logger.error(f"Error queue with name {queue_name} was not found")
            return

        await queue.consume(lambda msg: print(f"Got message: {msg}"))

        await stop_event.wait()


if __name__ == "__main__":
    asyncio.run(main())
