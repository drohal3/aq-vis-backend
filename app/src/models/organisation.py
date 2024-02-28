from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId


class Organisation(BaseModel):
    name: str
    devices: list[str] = list


class OrganisationInDB(Organisation):
    id: str


class NewOrganisation(Organisation):
    pass
