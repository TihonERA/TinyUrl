from aio_pika import DeliveryMode, Message
from aio_pika.abc import AbstractChannel
from aio_pika.pool import Pool

from src.dto.clicks import LinkClickedDTO
from src.producers.clicks_serializer import ClicksSerializer


class ClicksProducer:
    def __init__(self, channel: Pool[AbstractChannel]) -> None:
        self._channel = channel

    async def send(self, data: LinkClickedDTO) -> None:
        async with self._channel.acquire() as channel:
            exchange = await channel.get_exchange(name="clicks.exchange")

            message_bytes = ClicksSerializer.to_bytes(data)

            message = Message(
                body=message_bytes,
                delivery_mode=DeliveryMode.PERSISTENT,
                content_type="application/json",
            )

            await exchange.publish(message, routing_key="links.clicks")
