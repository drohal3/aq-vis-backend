from pydantic import BaseModel

class ParameterUnit(BaseModel):
    code: str
    name: str
    abbreviation: str

class Parameter(BaseModel):
    code: str
    name: str

class Device(BaseModel):
    deviceId: str
    deviceName: str
    organisation: str

