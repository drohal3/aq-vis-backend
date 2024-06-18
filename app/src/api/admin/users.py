from bson import ObjectId
from fastapi import APIRouter, HTTPException

from src.models.user import UserOut, UserIn
from src.database import get_database
from src.database.operations.user import create_user as create_user_operation, find_unsecure_user_by_email as find_unsecure_user_by_email_operation

router = APIRouter()


@router.post("/", response_model=UserOut)
async def create_user(form_data: UserIn):
    # TODO: database to DI (Depends)
    database = get_database()

    email = form_data.email

    if find_unsecure_user_by_email_operation(database, email):
        raise HTTPException(status_code=401, detail="User with this email address already exists.")

    return create_user_operation(database, form_data)


@router.put("/", response_model=UserOut)
async def update_user(form_data: UserOut):
    database = get_database()
    data = form_data.model_dump()
    user_id = data["id"]

    del data["id"]

    database.users.update_one({"_id": ObjectId(user_id)}, {"$set": data})
    updated_user = database.users.find_one({"_id": ObjectId(user_id)})
    updated_user["id"] = str(updated_user["_id"])

    return updated_user


@router.delete("/{id}")
async def delete_user():
    # database = get_database()
    pass
