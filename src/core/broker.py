from aio_pika import connect_robust
from aio_pika.abc import AbstractChannel, AbstractRobustConnection
from aio_pika.pool import Pool


class MessageBroker:
    def __init__(self, amqp_url: str) -> None:
        self._url = amqp_url
        self.connection_pool: Pool[AbstractRobustConnection] | None = None
        self.channel_pool: Pool[AbstractChannel] | None = None

    async def _get_connection(self) -> AbstractRobustConnection:
        return await connect_robust(self._url)

    async def _get_channel(self) -> AbstractChannel:
        if self.connection_pool is None:
            raise RuntimeError("Connection pool is not initialized")
        async with self.connection_pool.acquire() as connection:
            return await connection.channel()

    async def initialize(self) -> None:
        self.connection_pool = Pool(self._get_connection, max_size=2)
        self.channel_pool = Pool(self._get_channel, max_size=10)

    async def close(self) -> None:
        if self.channel_pool is not None:
            await self.channel_pool.close()
        if self.connection_pool is not None:
            await self.connection_pool.close()
