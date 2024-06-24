from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database

from src.database.operations.auth import get_current_active_user
from src.models.device import DeviceOut
from src.models.organisation import OrganisationOut
from src.models.user import UserOut
from src.database import get_database
from src.database.operations import organisation_operations, device_operations


router = APIRouter()


@router.get("/{organisation_id}", response_model=OrganisationOut)
async def get_organisation(
    organisation_id: str,
    database: Database = Depends(get_database),
    current_user: UserOut = Depends(get_current_active_user),
):
    if not current_user["organisation"] == str(organisation_id):
        raise HTTPException(401, detail="Unauthorized!")

    organisation = organisation_operations.find_organisation(
        database, ObjectId(organisation_id)
    )

    if not organisation:
        raise HTTPException(
            404, detail=f"Organisation with id {organisation_id} not found!"
        )

    return organisation


@router.get("/{organisation_id}/devices", response_model=list[DeviceOut])
async def get_devices(
    organisation_id: str,
    current_user: UserOut = Depends(get_current_active_user),
):
    database = get_database()
    organisation = organisation_operations.find_organisation(
        database, ObjectId(organisation_id)
    )
    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation not found!")
    if not current_user.organisation == str(organisation["_id"]):
        raise HTTPException(status_code=401, detail="Unauthorized!")

    devices = device_operations.find_devices_by_organisation(
        database, ObjectId(organisation_id)
    )

    return devices
