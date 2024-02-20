from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies.authentication import (
    get_password_hash,
    get_current_active_user,
)
from src.models.organisation import OrganisationInDB
from src.models.user import User, NewUser
from src.utils import database

import logging

router = APIRouter()

@router.get("/{organisation_id}", response_model=OrganisationInDB)
async def get_organisation(organisation_id: str, current_user: User = Depends(get_current_active_user)):
    if not current_user.organisation == str(organisation_id):
        raise HTTPException(401, detail="Unauthorized!")

    organisation = database.organisations.find_one({"_id": ObjectId(ObjectId(organisation_id))})
    organisation["id"] = str(organisation["_id"])
    del organisation["_id"]

    return organisation