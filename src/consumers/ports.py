from typing import Protocol

from aio_pika.abc import AbstractIncomingMessage


class IClicksConsumer(Protocol):
    async def create(self, msg: AbstractIncomingMessage) -> None: ...
