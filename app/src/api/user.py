from fastapi import APIRouter, Depends
from src.dependencies.authentication import (
    get_password_hash,
    get_current_active_user,
)
from src.models.user import User, NewUser

import logging

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(form_data: NewUser):
    database = router.database
    password = form_data.password
    hashed_password = get_password_hash(password)

    new_user_data = form_data.model_dump()
    new_user_data.pop("password")
    new_user_data["hashed_password"] = hashed_password
    user_id = database.users.insert_one(new_user_data).inserted_id
    logging.debug(f"create_user() - user_id: {user_id}")
    user = database.users.find_one({"_id": user_id})

    logging.info(f"create_user() - created user: {user}")

    user["id"] = str(user["_id"])

    return user

@router.get("/me", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# @router.get("/me/items", response_model=User)
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": 1, "owner": current_user}]

# @router.get("/")