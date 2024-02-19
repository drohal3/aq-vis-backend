from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

class Organisation(BaseModel):
    name: str

class OrganisationInDB(Organisation):
    id: str

class NewOrganisation(Organisation):
    pass
