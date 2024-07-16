from pydantic import BaseModel
from src.models.user import UserOut


class OrganisationMembershipBase(BaseModel):
    user: str


class OrganisationMembership(OrganisationMembershipBase):
    is_admin: bool = False


class NewOrganisationMembership(OrganisationMembership):
    organisation: str


class OrganisationMember(UserOut):
    is_admin: bool


class OrganisationBase(BaseModel):
    name: str
    devices: list[str] = list()


class OrganisationOut(OrganisationBase):
    id: str
    memberships: list[OrganisationMembership] = list()


class OrganisationWithMembers(OrganisationBase):
    id: str
    members: list[OrganisationMember] = list()


class OrganisationIn(OrganisationBase):
    pass
