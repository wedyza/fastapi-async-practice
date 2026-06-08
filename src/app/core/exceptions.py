class CustomExceptionBase(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)

class NotFoundException(CustomExceptionBase):
    ...

class AlreadyExistsException(CustomExceptionBase):
    ...

class WrongCredentialsException(CustomExceptionBase):
    ...


class CustomSystemExceptionBase(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)

class UncategorizedException(CustomSystemExceptionBase):
    ...