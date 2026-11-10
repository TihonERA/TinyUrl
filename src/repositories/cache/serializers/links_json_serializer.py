import json
from dataclasses import asdict
from datetime import datetime

from src.dto.links import LinksDTO


class LinksJsonSerializer:
    @staticmethod
    def to_json(link: LinksDTO) -> str:
        link_as_dict = asdict(link)

        link_as_dict["created_at"] = link.created_at.isoformat()

        if link.expires_at is not None:
            link_as_dict["expires_at"] = link.expires_at.isoformat()

        return json.dumps(link_as_dict)

    @staticmethod
    def from_json(link_json: str | bytes) -> LinksDTO:
        link_as_dict = json.loads(link_json)

        link_as_dict["created_at"] = datetime.fromisoformat(link_as_dict["created_at"])

        if link_as_dict.get("expires_at"):
            link_as_dict["expires_at"] = datetime.fromisoformat(
                link_as_dict["expires_at"]
            )

        return LinksDTO(**link_as_dict)
