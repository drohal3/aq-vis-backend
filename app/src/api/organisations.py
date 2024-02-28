from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from src.dependencies.authentication import (
    get_current_active_user,
)
from src.models.organisation import OrganisationInDB
from src.models.user import User
from src.utils import mongo_db


router = APIRouter()


@router.get("/{organisation_id}", response_model=OrganisationInDB)
async def get_organisation(
    organisation_id: str, current_user: User = Depends(get_current_active_user)
):
    database = mongo_db.get_database()
    if not current_user.organisation == str(organisation_id):
        raise HTTPException(401, detail="Unauthorized!")

    organisation = database.organisations.find_one(
        {"_id": ObjectId(organisation_id)}
    )
    organisation["id"] = str(organisation["_id"])
    del organisation["_id"]

    devices = []

    for device in organisation["devices"]:
        devices.append(str(device))
    organisation["devices"] = devices

    return organisation
