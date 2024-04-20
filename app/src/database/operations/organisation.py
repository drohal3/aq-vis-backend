from pymongo.database import Database
from bson import ObjectId

from src.models.organisation import Organisation, NewOrganisation


def find_organisation(database: Database, organisation_id: ObjectId) -> Organisation | None:
    organisation = database.organisations.find_one({"_id": organisation_id})
    if organisation is None:
        return organisation
    organisation["id"] = str(organisation["_id"])

    devices = []

    for device in organisation["devices"]:
        devices.append(str(device))
    organisation["devices"] = devices

    return organisation

def create_organisation(database: Database, organisation_data: NewOrganisation) -> Organisation | None:
    data = organisation_data.model_dump()
    organisation_id = database.organisations.insert_one(data).inserted_id
    return find_organisation(database, organisation_id)

def delete_organisation(database: Database, organisation_id: ObjectId):
    database.organisations.delete_one({"_id": organisation_id})
