from pydantic import BaseModel


# TODO: validation
class Parameter(BaseModel):
    name: str
    code: str
    unit: str  # unit_id
    description: str | None = None


class DeviceBase(BaseModel):
    name: str
    code: str
    organisation: str
    parameters: list[Parameter] = []


class DeviceIn(DeviceBase):
    pass


class DeviceOut(DeviceBase):
    id: str


class DeviceInDB(DeviceOut):
    pass
