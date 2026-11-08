import json
from dataclasses import asdict
from datetime import datetime

from src.dto.clicks import LinkClickedDTO


class ClicksSerializer:
    @staticmethod
    def to_bytes(data: LinkClickedDTO) -> bytes:
        data_as_dict = asdict(data)

        data_as_dict["clicked_at"] = data.clicked_at.isoformat()

        return json.dumps(data_as_dict).encode()

    @staticmethod
    def to_dto(data: bytes) -> LinkClickedDTO:
        data_as_string = data.decode()
        data_as_dict = json.loads(data_as_string)

        data_as_dict["clicked_at"] = datetime.fromisoformat(data_as_dict["clicked_at"])

        return LinkClickedDTO(**data_as_dict)
