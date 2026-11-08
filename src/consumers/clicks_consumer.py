from aio_pika.abc import AbstractIncomingMessage

from src.serializers.clicks_serializer import ClicksSerializer
from src.services.ports import IClicksService


class ClicksConsumer:
    def __init__(self, clicks_service: IClicksService) -> None:
        self.clicks_service = clicks_service

    async def create(self, msg: AbstractIncomingMessage) -> None:
        data = ClicksSerializer.to_dto(msg.body)

        await self.clicks_service.create(data)
