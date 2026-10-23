from src.core.exceptions.base import ApplicationError, DomainError


class SlugNotUniqueError(ApplicationError):
    pass


class SlugCreationError(DomainError):
    def __init__(self) -> None:
        super().__init__("Couldn't generate unique slug")


class LinkNotFound(DomainError):
    def __init__(self) -> None:
        super().__init__("Link not found")


class LinkExpiredError(DomainError):
    def __init__(self) -> None:
        super().__init__("Link is expired")
