# from fastapi import HTTPException


class NotFoundException(Exception):
    def __init__(self, detail: str = "Not found!"):
        super().__init__(detail)


class DuplicateException(Exception):
    def __init__(self, detail: str = "Duplicate!"):
        super().__init__(detail)


# class ItemNotFoundHTTPException(HTTPException):
#     def __init__(self, identifier: str):
#         super().__init__(
#             status_code=404,
#             detail=f"Item with identifier {identifier} not found",
#         )

__all__ = ["NotFoundException", "DuplicateException"]
