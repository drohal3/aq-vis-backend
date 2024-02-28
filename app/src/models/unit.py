from pydantic import BaseModel


class Unit(BaseModel):
    id: str
    name: str
    symbol: str
