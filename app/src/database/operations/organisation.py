from pymongo.database import Database
from bson import ObjectId
from src.exceptions import NotFoundException, DuplicateException
from src.database.operations import user_operations
from src.models.organisation import (
    OrganisationOut,
    OrganisationWithMembers,
    OrganisationIn,
    OrganisationMembership,
    OrganisationMember,
)


def find_organisation(
    database: Database, organisation_id: ObjectId
) -> OrganisationOut | None:
    organisation = database.organisations.find_one({"_id": organisation_id})
    if organisation is None:
        return organisation
    organisation["id"] = str(organisation["_id"])

    devices = []

    for device in organisation.get("devices", []):
        devices.append(str(device))
    organisation["devices"] = devices

    return OrganisationOut(**organisation)


def _load_members_to_organisation(
    database: Database, organisation: OrganisationOut
) -> OrganisationWithMembers:
    members = []
    for membership in organisation.memberships:
        user = user_operations.find_user(
            database, ObjectId(membership.user)
        ).model_dump()
        user["is_admin"] = membership.is_admin
        member = OrganisationMember(**user)
        members.append(member)
    # del organisation["memberships"]

    organisation = organisation.model_dump()
    organisation["members"] = members

    return OrganisationWithMembers(**organisation)


def find_organisation_with_members(
    database: Database, organisation_id: ObjectId
) -> OrganisationWithMembers:
    organisation_out = find_organisation(database, organisation_id)

    return _load_members_to_organisation(database, organisation_out)


def create_organisation(
    database: Database, organisation_data: OrganisationIn
) -> OrganisationOut | None:
    data = organisation_data.model_dump()
    organisation_id = database.organisations.insert_one(data).inserted_id
    return find_organisation(database, organisation_id)


def delete_organisation(database: Database, organisation_id: ObjectId):
    database.organisations.delete_one({"_id": organisation_id})


def add_membership(
    database: Database,
    organisation_id: ObjectId,
    membership: OrganisationMembership,
):
    membership_data = membership.model_dump()
    organisation = find_organisation(database, organisation_id)

    if not organisation:
        raise NotFoundException(f"Organisation {organisation_id} not found")

    organisation = organisation.model_dump()
    memberships = organisation["memberships"]

    for member in memberships:
        if member["user"] == membership_data["user"]:
            raise DuplicateException()

    memberships.append(membership_data)
    database.organisations.update_one(
        {"_id": ObjectId(organisation_id)},
        {"$set": {"memberships": memberships}},
    )


def remove_membership(
    database: Database, organisation_id: ObjectId, user_id: ObjectId
):
    organisation = find_organisation(database, organisation_id)
    if not organisation:
        raise NotFoundException(f"Organisation {organisation_id} not found")
    organisation = organisation.model_dump()
    memberships = organisation["memberships"]
    memberships_new = []
    for member in memberships:
        if member["user"] != str(user_id):
            memberships_new.append(member)
    database.organisations.update_one(
        {"_id": organisation_id}, {"$set": {"memberships": memberships_new}}
    )


def add_device(
    database: Database, organisation_id: ObjectId, device_id: ObjectId
):
    organisation = database.organisations.find_one(
        {"_id": ObjectId(organisation_id)}
    )

    if not organisation:
        raise NotFoundException()

    devices = organisation.get("devices", [])

    if device_id in devices:
        raise DuplicateException()

    database.organisations.update_one(
        {"_id": ObjectId(organisation_id)}, {"$set": {"devices": devices}}
    )


def remove_device(
    database: Database, organisation_id: ObjectId, device_id: ObjectId
):
    organisation = database.organisations.find_one(
        {"_id": ObjectId(organisation_id)}
    )

    devices = organisation.get("devices", [])
    new_devices = []
    for device in devices:
        if not device == str(device_id):
            new_devices.append(device)

    database.organisations.update_one(
        {"_id": ObjectId(organisation_id)}, {"$set": {"devices": new_devices}}
    )
