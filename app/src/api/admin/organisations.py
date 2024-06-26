from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends
from src.models.organisation import (
    OrganisationIn,
    OrganisationOut,
    NewOrganisationMembership,
)
from src.database.operations import (
    organisation_operations,
    remove_user_from_organisation_operation,
    device_operations,
)
from src.database import get_database
from src.database.operations.auth import get_current_admin
from src.database.operations import add_user_to_organisation

from src.exceptions import NotFoundException, DuplicateException
import logging

router = APIRouter()


@router.post("", response_model=OrganisationOut, status_code=201)
async def create_organisation(
    form_data: OrganisationIn,
    current_admin: str = Depends(get_current_admin),
):
    logging.debug(f"creating organisation by admin: {current_admin}")
    database = get_database()
    created_organisation = organisation_operations.create_organisation(
        database, form_data
    )

    # need to rename _id to id since _id is reserved in Python
    logging.debug(f"Created organisation: {created_organisation}")

    return created_organisation


@router.put("", response_model=OrganisationOut)
async def update_organisation(
    form_data: OrganisationOut,
    current_admin: str = Depends(get_current_admin),
):
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
async def delete_organisation(
    organisation_id: str,
    current_admin: str = Depends(get_current_admin),
):
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


@router.get("/{organisation_id}", response_model=OrganisationOut)
async def get_organisation(
    organisation_id: str,
    current_admin: str = Depends(get_current_admin),
):
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


@router.get("", response_model=list[OrganisationOut])
async def get_organisations(
    current_admin: str = Depends(get_current_admin),
):
    database = get_database()
    organisations = database.organisations.find()
    ret = []
    for organisation in organisations:
        logging.debug(f"=====> organisation: {organisation}")
        organisation["id"] = str(organisation["_id"])
        ret.append(OrganisationOut(**organisation))

    return ret


@router.post("/add_user")
async def add_user(
    form_data: NewOrganisationMembership,
    current_admin: str = Depends(get_current_admin),
):
    # TODO: use add_user_to_organisation function!!!
    database = get_database()
    data = form_data.model_dump()
    user_id = data["user"]
    organisation_id = data["organisation"]
    is_admin = data["is_admin"]

    try:
        add_user_to_organisation(database, user_id, organisation_id, is_admin)
    except NotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
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
async def remove_user(
    form_data: NewOrganisationMembership,
    current_admin: str = Depends(get_current_admin),
):
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


# TODO: add device to organisation, remove device from organisation
