from pymongo.database import Database
from bson import ObjectId

from src.models.organisation import Organisation, NewOrganisation, OrganisationMembership


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

def add_membership(database: Database, organisation_id: ObjectId, membership: OrganisationMembership):
    membership_data = membership.model_dump()
    print(f"======> membership: {membership_data}")
    organisation = find_organisation(database, organisation_id)
    print(f"======> organisation: {organisation}")
    members = organisation["members"]
    members.append(membership_data)
    print(f"members: {members}")

    # TODO: if user already a member?
    database.organisations.update_one({"_id": ObjectId(organisation_id)}, {"$set": {'members': members}})

def remove_membership(database: Database, organisation_id: ObjectId, user_id: ObjectId):
    organisation = find_organisation(database, organisation_id)
    members = organisation["members"]
    members_new = []
    for member in members:
        if member["user"] != str(user_id):
            members_new.append(member)
    database.organisations.update_one({"_id": organisation_id}, {"$set": {'members': members_new}})
