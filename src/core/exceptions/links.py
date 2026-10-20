from src.core.exceptions.base import DomainError


class SlugNotUniqueError(DomainError):
    pass


class SlugCreationError(DomainError):
    pass


class LinkNotFound(DomainError):
    pass
