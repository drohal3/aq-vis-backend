from fastapi import HTTPException

class ItemNotFoundException(HTTPException):
    def __init__(self, identifier: str):
        super().__init__(status_code=404, detail=f"Item with identifier {identifier} not found")

