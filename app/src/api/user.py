from fastapi import APIRouter, Depends
from src.dependencies.authentication import (
    get_password_hash,
    get_current_active_user,
    db,
)
from src.models.user import User, NewUser

router = APIRouter()

@router.post("/create", response_model=User)
def create_user(form_data: NewUser):
    password = form_data.password
    hashed_password = get_password_hash(password)

    new_user_data = form_data.model_dump()
    new_user_data.pop("password")
    new_user_data["hashed_password"] = hashed_password

    db[form_data.username] = new_user_data  # TODO: save in DB

    return new_user_data

@router.get("/me", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# @router.get("/me/items", response_model=User)
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": 1, "owner": current_user}]
