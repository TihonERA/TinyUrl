import json
from dataclasses import asdict

from aio_pika import DeliveryMode, Message
from aio_pika.abc import AbstractChannel

from src.dto.clicks import LinkClickedDTO


class ClicksProducer:
    def __init__(self, channel: AbstractChannel) -> None:
        self._channel = channel

    async def send(self, data: LinkClickedDTO) -> None:
        exchange = await self._channel.get_exchange(name="clicks.exchange")

        json_data = json.dumps(asdict(data))
        message_bytes = json_data.encode()

        message = Message(
            body=message_bytes,
            delivery_mode=DeliveryMode.PERSISTENT,
            content_type="application/json",
        )

        await exchange.publish(message, routing_key="links.clicks")
