from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from src.dependencies.authentication import get_current_active_user
from src.models.device import Device, NewDevice
from src.models.user import User
from src.utils import database

import logging

router = APIRouter()


@router.post("/", response_model=Device)
async def create_device(form_data: NewDevice, current_user: User = Depends(get_current_active_user)):
    organisation_id = form_data.organisation
    organisation = database.organisations.find_one({"_id": ObjectId(organisation_id)})
    logging.debug(f"Organisation: {organisation}")
    logging.debug(f"current_user: {current_user}")
    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation Not Found!")

    if not current_user.organisation == str(organisation["_id"]):
        raise HTTPException(status_code=401, detail="Unauthorized!")

    device_id = database.devices.insert_one(form_data.model_dump()).inserted_id

    saved_device = database.devices.find_one({"_id": device_id})

    saved_device["id"] = saved_device["_id"]
    del saved_device["_id"]

    return saved_device

@router.get("/", response_model=list[Device])
async def get_devices(organisation: str, current_user: User = Depends(get_current_active_user)):
    pass
