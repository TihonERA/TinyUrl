from typing import Protocol

from src.dto.clicks import LinkClickedDTO


class IClicksProducer(Protocol):
    async def send(self, data: LinkClickedDTO) -> None: ...
