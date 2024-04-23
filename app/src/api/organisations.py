from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database

from src.database.operations.auth import get_current_active_user
from src.models.organisation import Organisation
from src.models.user import User
from src.database import get_database
from src.database.operations.organisation import find_organisation


router = APIRouter()


@router.get("/{organisation_id}", response_model=Organisation)
async def get_organisation(
    organisation_id: str,
    database: Database = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    if not current_user["organisation"] == str(organisation_id):
        raise HTTPException(401, detail="Unauthorized!")

    organisation = find_organisation(database, ObjectId(organisation_id))

    return organisation
