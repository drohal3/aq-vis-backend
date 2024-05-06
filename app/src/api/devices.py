from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from src.dependencies.authentication import get_current_active_user
from src.models.deviceindb import DeviceOut, DeviceIn
from src.models.user import UserOut
from src.database import get_database

import logging

router = APIRouter()


@router.post("", response_model=DeviceOut)
async def create_device(
    form_data: DeviceIn, current_user: UserOut = Depends(get_current_active_user)
):
    database = get_database()
    organisation_id = form_data.organisation
    organisation = database.organisations.find_one(
        {"_id": ObjectId(organisation_id)}
    )
    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation Not Found!")

    if not current_user.organisation == str(organisation["_id"]):
        raise HTTPException(status_code=401, detail="Unauthorized!")

    device_id = database.devices.insert_one(form_data.model_dump()).inserted_id

    devices = organisation.get("devices", [])
    devices.append(device_id)

    database.organisations.update_one(
        {"_id": ObjectId(organisation_id)}, {"$set": {"devices": devices}}
    )
    saved_device = database.devices.find_one({"_id": device_id})

    saved_device["id"] = str(saved_device["_id"])
    del saved_device["_id"]

    return saved_device


@router.get("", response_model=list[DeviceOut])
async def get_devices(
    organisation: str, current_user: UserOut = Depends(get_current_active_user)
):
    database = get_database()
    organisation = database.organisations.find_one(
        {"_id": ObjectId(organisation)}
    )
    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation not found!")
    if not current_user.organisation == str(organisation["_id"]):
        raise HTTPException(status_code=401, detail="Unauthorized!")

    devices = database.devices.find({"_id": {"$in": organisation["devices"]}})

    ret = []

    for device in devices:
        device["id"] = str(device["_id"])
        del device["_id"]
        ret.append(device)
        logging.debug(device)

    return ret


@router.delete("/{id}")
async def delete_device(
    id: str, current_user: UserOut = Depends(get_current_active_user)
):
    database = get_database()
    logging.debug(f"Deleting device {id}")
    device = database.devices.find_one({"_id": ObjectId(id)})
    if not device:
        raise HTTPException(status_code=404, detail="Device not found!")
    organisation_id = str(device["organisation"])
    if not current_user.organisation == organisation_id:
        raise HTTPException(status_code=401, detail="Unauthorized!")
    organisation = database.organisations.find_one(
        {"_id": ObjectId(organisation_id)}
    )
    devices_in_organisation = organisation["devices"]
    filtered_devices_in_organisation = []
    for device in devices_in_organisation:
        if str(device) != id:
            filtered_devices_in_organisation.append(device)
    logging.debug(
        f"Deleting device from organisation {devices_in_organisation}"
    )
    logging.debug(f"Filtered: {filtered_devices_in_organisation}")
    (
        database.organisations.update_one(
            {"_id": ObjectId(organisation_id)},
            {"$set": {"devices": filtered_devices_in_organisation}},
        )
    )
    database.devices.delete_one({"_id": ObjectId(id)})
