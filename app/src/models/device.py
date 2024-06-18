from pydantic import BaseModel, Field


# TODO: validation
class Parameter(BaseModel):
    name: str
    code: str
    unit: str  # unit_id
    description: str | None = Field(
        default=None, title="Description of the parameter"
    )


class DeviceBase(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        description="The length must be at least 3 characters",
    )
    code: str = Field(
        ...,
        title="The code is used to identify the device"
        " in external systems (i.e. IoT data)",
    )
    organisation: str = Field(
        ..., title="Reference to the Organisation the device belongs to"
    )
    parameters: list[Parameter] = Field(
        default=[], title="List of parameters the device is able to measure"
    )


class DeviceIn(DeviceBase):
    pass


class DeviceOut(DeviceBase):
    id: str


class DeviceInDB(DeviceOut):
    pass
