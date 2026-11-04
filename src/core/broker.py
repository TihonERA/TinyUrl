from typing import Final

from aio_pika import ExchangeType, connect_robust
from aio_pika.abc import AbstractChannel, AbstractRobustConnection
from aio_pika.pool import Pool

from src.core.config import get_settings


class MessageBroker:
    NOT_INITIALIZED_ERROR_MESSAGE: Final = "Connection pool is not initialized"

    def __init__(self, amqp_url: str) -> None:
        self._url = amqp_url
        self.connection_pool: Pool[AbstractRobustConnection] | None = None
        self.channel_pool: Pool[AbstractChannel] | None = None

    async def _get_connection(self) -> AbstractRobustConnection:
        return await connect_robust(self._url)

    async def _get_channel(self) -> AbstractChannel:
        if self.connection_pool is None:
            raise RuntimeError(self.NOT_INITIALIZED_ERROR_MESSAGE)
        async with self.connection_pool.acquire() as connection:
            return await connection.channel()

    async def initialize(self) -> None:
        self.connection_pool = Pool(self._get_connection, max_size=2)
        self.channel_pool = Pool(self._get_channel, max_size=10)

    async def initialize_clicks_topology(self) -> None:
        if self.channel_pool is None:
            raise RuntimeError(self.NOT_INITIALIZED_ERROR_MESSAGE)

        async with self.channel_pool.acquire() as channel:
            exchange = await channel.declare_exchange(
                name="clicks.exchange", durable=True, type=ExchangeType.TOPIC
            )

            queue = await channel.declare_queue(name="links.clicks", durable=True)

            await queue.bind(exchange, routing_key="links.clicks")

    async def close(self) -> None:
        if self.channel_pool is not None:
            await self.channel_pool.close()
        if self.connection_pool is not None:
            await self.connection_pool.close()


broker = MessageBroker(str(get_settings().RABBITMQ_URL))
