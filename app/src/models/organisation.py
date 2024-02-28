from pydantic import BaseModel


class Organisation(BaseModel):
    name: str
    devices: list[str] = list


class OrganisationInDB(Organisation):
    id: str


class NewOrganisation(Organisation):
    pass
