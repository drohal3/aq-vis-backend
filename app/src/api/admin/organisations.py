from bson import ObjectId
from fastapi import APIRouter, HTTPException
from src.models.organisation import (
    NewOrganisation,
    Organisation,
    NewOrganisationMembership,
    OrganisationMembership,
)
from src.database.operations import (
    organisation_operations,
    user_operations,
    remove_user_from_organisation_operation,
    device_operations,
)
from src.database import get_database
from src.exceptions import NotFoundException, DuplicateException
import logging

router = APIRouter()


@router.post("/", response_model=Organisation, status_code=201)
async def create_organisation(form_data: NewOrganisation):
    database = get_database()
    created_organisation = organisation_operations.create_organisation(
        database, form_data
    )

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


@router.delete("/{organisation_id}", status_code=204)
async def delete_organisation(organisation_id: str):
    database = get_database()
    organisation = organisation_operations.find_organisation(
        database, ObjectId(organisation_id)
    )
    if not organisation:
        raise HTTPException(
            status_code=404,
            detail=f"Organisation {organisation_id} not found!",
        )
    for device in organisation.devices:
        device_operations.delete_device(database, ObjectId(device))
    organisation_operations.delete_organisation(
        database, ObjectId(organisation_id)
    )


@router.get("/{organisation_id}", response_model=Organisation)
async def get_organisation(organisation_id: str):
    database = get_database()
    organisation = database.organisations.find_one(
        {"_id": ObjectId(organisation_id)}
    )

    logging.debug(organisation)

    if organisation is None:
        raise HTTPException(
            status_code=404,
            detail=f"Organisation with id {organisation_id} not found!",
        )

    # need to rename _id to id since _id is reserved in Python
    organisation["id"] = str(organisation["_id"])

    return organisation


@router.get("/", response_model=list[Organisation])
async def get_organisations():
    database = get_database()
    organisations = database.organisations.find()
    ret = []
    for organisation in organisations:
        logging.debug(f"=====> organisation: {organisation}")
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
    user_operations.add_organisation(
        database, ObjectId(user_id), ObjectId(organisation_id)
    )

    user = user_operations.find_user(database, ObjectId(user_id))

    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found!"
        )

    try:
        # TODO: add operation from operations __init__
        organisation_operations.add_membership(
            database, ObjectId(organisation_id), OrganisationMembership(**data)
        )
    except NotFoundException:
        raise HTTPException(
            status_code=404,
            detail=f"Organisation with id {organisation_id} not found",
        )
    except DuplicateException:
        raise HTTPException(
            status_code=409,
            detail=f"User with id {user_id} "
            f"is already member of organisation with id {organisation_id}",
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected Error!")


@router.post("/remove_user")
async def remove_user(form_data: NewOrganisationMembership):
    database = get_database()
    data = form_data.model_dump()
    user_id = data["user"]
    organisation_id = data["organisation"]
    try:
        remove_user_from_organisation_operation(
            database, ObjectId(user_id), ObjectId(organisation_id)
        )
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
