from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from src.dependencies.authentication import get_current_active_user
from src.exceptions import DuplicateException
from src.models.device import DeviceOut, DeviceIn
from src.models.user import UserOut
from src.database import get_database
from src.database.operations import organisation_operations, device_operations

import logging

router = APIRouter()


@router.post("", response_model=DeviceOut, status_code=201)
async def create_device(
    form_data: DeviceIn,
    current_user: UserOut = Depends(get_current_active_user),
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

    if not form_data.organisation == current_user.organisation:
        raise HTTPException(status_code=401, detail="Unauthorized!")

    device = device_operations.create_device(database, form_data)
    device_id = device.id

    try:
        organisation_operations.add_device(
            database, ObjectId(organisation_id), ObjectId(device_id)
        )
    except DuplicateException:
        raise HTTPException(
            status_code=409,
            detail=f"Device {device_id} "
            f"already belongs to organisation {organisation_id}",
        )

    return device


@router.put("/{device_id}", response_model=DeviceOut)
async def update_device(
    device_id: str,
    form_data: DeviceIn,
    current_user: UserOut = Depends(get_current_active_user),
):
    database = get_database()
    device = device_operations.find_device_by_id(database, ObjectId(device_id))
    if not device:
        raise HTTPException(
            status_code=404, detail=f"Device {device_id} not found"
        )
    if device.organisation != current_user.organisation:
        raise HTTPException(status_code=401, detail="Unauthorized!")
    device = device_operations.update_device(
        database, ObjectId(device_id), form_data
    )
    return device


@router.get("", response_model=list[DeviceOut])
async def get_devices(
    organisation_id: str,
    current_user: UserOut = Depends(get_current_active_user),
):
    message = "use /organisations/{organisation_id}/devices endpoint instead!"
    return {"error": message}


@router.get("/{device_id}", response_model=DeviceOut, status_code=200)
async def get_device(
    device_id: str, current_user: UserOut = Depends(get_current_active_user)
):
    database = get_database()
    device = device_operations.find_device_by_id(database, ObjectId(device_id))

    if not device:
        raise HTTPException(
            status_code=404, detail=f"Device {device_id} not found"
        )

    if device.organisation != current_user.organisation:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return device


@router.delete("/{id}", status_code=204)
async def delete_device(
    id: str, current_user: UserOut = Depends(get_current_active_user)
):
    database = get_database()
    logging.debug(f"Deleting device {id}")
    device = device_operations.find_device_by_id(database, ObjectId(id))

    if not device:
        raise HTTPException(status_code=404, detail="Device not found!")
    organisation_id = device.organisation
    if not current_user.organisation == organisation_id:
        raise HTTPException(status_code=401, detail="Unauthorized!")
    organisation_operations.remove_device(
        database, ObjectId(organisation_id), ObjectId(id)
    )

    device_operations.delete_device(database, ObjectId(id))
