from pydantic import BaseModel


class OrganisationMembershipBase(BaseModel):
    user: str


class OrganisationMembership(OrganisationMembershipBase):
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
