from pydantic import BaseModel

class NewDevice(BaseModel):
    deviceName: str
    deviceCode: str
    organisation: str

class Device(NewDevice):
    id: str
