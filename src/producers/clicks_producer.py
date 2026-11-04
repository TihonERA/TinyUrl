import logging

from aio_pika import DeliveryMode, Message
from aio_pika.abc import AbstractChannel
from aio_pika.exceptions import AMQPError
from aio_pika.pool import Pool

from src.dto.clicks import LinkClickedDTO
from src.producers.clicks_serializer import ClicksSerializer

logger = logging.getLogger(__name__)


class ClicksProducer:
    def __init__(self, channel_pool: Pool[AbstractChannel]) -> None:
        self._channel_pool = channel_pool

    async def send(self, data: LinkClickedDTO) -> None:
        try:
            async with self._channel_pool.acquire() as channel:
                exchange = await channel.get_exchange(
                    name="clicks.exchange", ensure=False
                )

                message_bytes = ClicksSerializer.to_bytes(data)

                message = Message(
                    body=message_bytes,
                    delivery_mode=DeliveryMode.PERSISTENT,
                    content_type="application/json",
                )

                await exchange.publish(message, routing_key="links.clicks")
        except (AMQPError, TimeoutError) as e:
            logger.error(
                "Couldn't send message to RabbitMQ, link_id: %d. ERROR: %s",
                data.link_id,
                e,
                exc_info=True,
            )
