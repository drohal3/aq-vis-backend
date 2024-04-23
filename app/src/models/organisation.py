from pydantic import BaseModel

class OrganisationMembership(BaseModel):
    user: str
    is_admin: bool = False

class NewOrganisationMembership(OrganisationMembership):
    organisation: str

class OrganisationBase(BaseModel):
    name: str
    devices: list[str] = list
    members: list[OrganisationMembership] = list


class Organisation(OrganisationBase):
    id: str


class NewOrganisation(OrganisationBase):
    pass
