from pydantic import BaseModel

class OrganisationBase(BaseModel):
    name: str
    devices: list[str] = list


class Organisation(OrganisationBase):
    id: str


class NewOrganisation(OrganisationBase):
    pass

