from bson import ObjectId
from fastapi import APIRouter, HTTPException
from src.models.organisation import NewOrganisation, Organisation
from src.database.operations.organisation import create_organisation as create_organisation_operation
from src.utils import mongo_db
import logging

router = APIRouter()

# TODO: only admins should be allowed to call this API - move to admin area!


@router.post("/", response_model=Organisation)
async def create_organisation(form_data: NewOrganisation):
    database = mongo_db.get_database()
    created_organisation = create_organisation_operation(database, form_data)

    # need to rename _id to id since _id is reserved in Python
    logging.debug(f"Created organisation: {created_organisation}")

    return created_organisation


@router.put("/", response_model=Organisation)
async def update_organisation(form_data: Organisation):
    database = mongo_db.get_database()
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


@router.delete("/{id}")
async def delete_organisation(id: str):
    database = mongo_db.get_database()
    # TODO: authenticate
    database.organisations.delete_one({"_id": ObjectId(id)})
    # TODO: delete organisation's devices


@router.get("/{id}", response_model=Organisation)
async def get_organisation(id: str):
    database = mongo_db.get_database()
    organisation = database.organisations.find_one({"_id": ObjectId(id)})

    logging.debug(organisation)

    if organisation is None:
        raise HTTPException(status_code=404, detail="Not Found!")

    # need to rename _id to id since _id is reserved in Python
    organisation["id"] = str(organisation["_id"])

    return organisation


@router.get("/", response_model=list[Organisation])
async def get_organisations():
    database = mongo_db.get_database()
    organisations = database.organisations.find()
    ret = []
    for organisation in organisations:
        organisation["id"] = str(organisation["_id"])
        ret.append(Organisation(**organisation))

    return ret
