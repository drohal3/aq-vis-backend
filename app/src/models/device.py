from pydantic import BaseModel


# TODO: validation
class Parameter(BaseModel):
    name: str
    code: str
    unit: str  # unit_id
    description: str | None = None


class NewDevice(BaseModel):
    name: str
    code: str
    organisation: str
    parameters: list[Parameter] = []


class Device(NewDevice):
    id: str
