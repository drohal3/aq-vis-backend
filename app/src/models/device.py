from pydantic import BaseModel

class NewDevice(BaseModel):
    deviceName: str
    organisation: str

class Device(NewDevice):
    id: str
