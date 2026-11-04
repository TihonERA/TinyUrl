import json
from dataclasses import asdict

from src.dto.clicks import LinkClickedDTO


class ClicksSerializer:
    @staticmethod
    def to_bytes(data: LinkClickedDTO) -> bytes:
        data_as_dict = asdict(data)

        data_as_dict["clicked_at"] = data.clicked_at.isoformat()

        return json.dumps(data_as_dict).encode()
