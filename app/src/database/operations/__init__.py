from src.database.operations import user as user_operations
from src.database.operations import (
    organisation as organisation_operations,
    device as device_operations,
)
from pymongo.database import Database
from src.models.organisation import (
    NewOrganisationMembership,
    OrganisationMembership,
)
from bson import ObjectId
from src.exceptions import NotFoundException


# START organisation - user
def add_user_to_organisation(
    database: Database,
    user_id: ObjectId,
    organisation_id: ObjectId,
    is_admin: bool = False,
):
    membership = NewOrganisationMembership(
        **{
            "user": str(user_id),
            "organisation": str(organisation_id),
            "is_admin": is_admin,
        }
    )
    # TODO: use it!
    user_id = membership.user
    organisation_id = membership.organisation
    new_membership_data = membership.model_dump()
    user = user_operations.find_user(database, ObjectId(user_id))

    if user is None:
        raise NotFoundException(f"User {user_id} not found!")

    user_operations.add_organisation(
        database, ObjectId(user_id), ObjectId(organisation_id)
    )
    organisation_operations.add_membership(
        database,
        ObjectId(organisation_id),
        OrganisationMembership(**new_membership_data),
    )


def remove_user_from_organisation_operation(
    database: Database, user_id: ObjectId, organisation_id: ObjectId
):
    user_operations.remove_organisation(database, user_id, organisation_id)
    organisation_operations.remove_membership(
        database, organisation_id, user_id
    )


# END organisation - user


__all__ = [
    "add_user_to_organisation",
    "remove_user_from_organisation_operation",
    "organisation_operations",
    "device_operations",
    "user_operations",
]
