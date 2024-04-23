from bson import ObjectId
from fastapi import APIRouter, HTTPException
from src.models.organisation import (
    NewOrganisation,
    Organisation,
    NewOrganisationMembership,
    OrganisationMembership,
)
from src.database.operations.organisation import (
    create_organisation as create_organisation_operation,
    add_membership as add_membership_operation,
    remove_membership as remove_membership_operation,
)
from src.database.operations.user import (
    add_organisation as add_organisation_operation,
    remove_organisation as remove_organisation_operation,
)
from src.database import get_database
import logging

router = APIRouter()


@router.post("/", response_model=Organisation, status_code=201)
async def create_organisation(form_data: NewOrganisation):
    database = get_database()
    created_organisation = create_organisation_operation(database, form_data)

    # need to rename _id to id since _id is reserved in Python
    logging.debug(f"Created organisation: {created_organisation}")

    return created_organisation


@router.put("/", response_model=Organisation)
async def update_organisation(form_data: Organisation):
    database = get_database()
    # TODO: authenticate
    organisation_id = form_data.id
    data = form_data.model_dump()
    del data["id"]
    database.organisations.update_one(
        {"_id": ObjectId(organisation_id)}, {"$set": data}, upsert=True
    )
    updated_organisation = database.organisations.find_one(
        {"_id": ObjectId(organisation_id)}
    )
    updated_organisation["id"] = str(updated_organisation["_id"])

    return updated_organisation


@router.delete("/{id}", status_code=204)
async def delete_organisation(id: str):
    database = get_database()
    # TODO: authenticate
    database.organisations.delete_one({"_id": ObjectId(id)})
    # TODO: delete organisation's devices


@router.get("/{id}", response_model=Organisation)
async def get_organisation(id: str):
    database = get_database()
    organisation = database.organisations.find_one({"_id": ObjectId(id)})

    logging.debug(organisation)

    if organisation is None:
        raise HTTPException(status_code=404, detail="Not Found!")

    # need to rename _id to id since _id is reserved in Python
    organisation["id"] = str(organisation["_id"])

    return organisation


@router.get("/", response_model=list[Organisation])
async def get_organisations():
    database = get_database()
    organisations = database.organisations.find()
    ret = []
    for organisation in organisations:
        organisation["id"] = str(organisation["_id"])
        ret.append(Organisation(**organisation))

    return ret


@router.post("/add_user")
async def add_user(form_data: NewOrganisationMembership):
    # TODO: auth
    database = get_database()
    data = form_data.model_dump()
    user_id = data["user"]
    organisation_id = data["organisation"]
    add_organisation_operation(
        database, ObjectId(user_id), ObjectId(organisation_id)
    )
    add_membership_operation(
        database, ObjectId(organisation_id), OrganisationMembership(**data)
    )


@router.post("/remove_user")
async def remove_user(form_data: NewOrganisationMembership):
    database = get_database()
    data = form_data.model_dump()
    user_id = data["user"]
    organisation_id = data["organisation"]
    remove_organisation_operation(
        database, ObjectId(user_id), ObjectId(organisation_id)
    )
    remove_membership_operation(
        database, ObjectId(organisation_id), ObjectId(user_id)
    )
