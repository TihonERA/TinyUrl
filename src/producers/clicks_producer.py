import json
from dataclasses import asdict

from aio_pika import DeliveryMode, ExchangeType, Message
from aio_pika.abc import AbstractChannel

from src.dto.clicks import LinkClickedDTO


class ClicksProducer:
    def __init__(self, channel: AbstractChannel) -> None:
        self.channel = channel

    async def send(self, data: LinkClickedDTO) -> None:
        exchange = await self.channel.declare_exchange(
            name="clicks.exchange", durable=True, type=ExchangeType.TOPIC
        )

        queue = await self.channel.declare_queue(name="links.clicks", durable=True)

        await queue.bind(exchange)

        json_data = json.dumps(asdict(data))
        message_bytes = json_data.encode()

        message = Message(
            body=message_bytes,
            delivery_mode=DeliveryMode.PERSISTENT,
            content_type="application/json",
        )

        await exchange.publish(message, routing_key="links.clicks")
