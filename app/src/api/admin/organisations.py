from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from src.models.organisation import NewOrganisation, OrganisationInDB
from src.utils import database
import logging

router = APIRouter()

# TODO: only admins should be allowed to call this API - move to admin area!

@router.post("/", response_model=OrganisationInDB)
async def create_organisation(form_data: NewOrganisation):
    data = form_data.model_dump()
    logging.info(f"Creating organisation: {data}")
    organisation_id = database.organisations.insert_one(data).inserted_id
    created_organisation = database.organisations.find_one({"_id": ObjectId(organisation_id)})

    # need to rename _id to id since _id is reserved in Python
    created_organisation["id"] = str(created_organisation["_id"])
    logging.debug(f"Created organisation: {created_organisation}")

    return created_organisation

@router.put("/", response_model=OrganisationInDB)
async def update_organisation(form_data: OrganisationInDB):
    # TODO: authenticate
    organisation_id = form_data.id
    data = form_data.model_dump()
    del data['id']
    database.organisations.update_one({"_id": ObjectId(organisation_id)}, {"$set": data}, upsert=True)
    updated_organisation = database.organisations.find_one({"_id": ObjectId(organisation_id)})
    updated_organisation["id"] = str(updated_organisation["_id"])

    return updated_organisation

@router.delete("/{id}")
async def delete_organisation(id: str):
    # TODO: authenticate
    database.organisations.delete_one({"_id": ObjectId(id)})
    # TODO: delete organisation's devices


@router.get("/{id}", response_model=OrganisationInDB)
async def get_organisation(id: str):
    organisation = database.organisations.find_one({"_id": ObjectId(id)})

    logging.debug(organisation)

    if organisation is None:
        raise HTTPException(status_code=404, detail="Not Found!")

    # need to rename _id to id since _id is reserved in Python
    organisation["id"] = str(organisation["_id"])

    return organisation

@router.get("/", response_model=list[OrganisationInDB])
async def get_organisations():
    organisations = database.organisations.find()
    ret = []
    for organisation in organisations:
        organisation["id"] = str(organisation["_id"])
        ret.append(OrganisationInDB(**organisation))

    return ret

