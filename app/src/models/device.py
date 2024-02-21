from pydantic import BaseModel

class NewDevice(BaseModel):
    name: str
    code: str
    organisation: str

class Device(NewDevice):
    id: str
