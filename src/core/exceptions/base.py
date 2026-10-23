class DomainError(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class ApplicationError(Exception):
    pass
