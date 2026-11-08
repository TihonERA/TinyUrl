from src.dto.links import LinksDTO
from src.models.links import Links


class LinksMapper:
    @staticmethod
    def to_dto(link: Links) -> LinksDTO:
        return LinksDTO(
            id=link.id,
            slug=link.slug,
            original_url=link.original_url,
            is_active=link.is_active,
            created_at=link.created_at,
            expires_at=link.expires_at,
        )
