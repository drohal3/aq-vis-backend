from bson import ObjectId
from fastapi import APIRouter, HTTPException

from src.models.user import UserOut, UserIn, UserBase
from src.database import get_database
from src.database.operations import user_operations

# TODO: =====> =====> =====> Authentication! <===== <===== <=====

router = APIRouter()


@router.post("/", response_model=UserOut)
async def create_user(form_data: UserIn):
    # TODO: database to DI (Depends)
    database = get_database()

    email = form_data.email

    if user_operations.find_unsecure_user_by_email(database, email):
        raise HTTPException(
            status_code=409,
            detail="User with this email address already exists.",
        )

    return user_operations.create_user(database, form_data)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: str, form_data: UserBase):
    database = get_database()

    user_to_update = user_operations.find_unsecure_user(database, ObjectId(user_id))

    if user_to_update is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    updated_user_data = user_to_update.copy(
        update=form_data.dict(exclude_unset=True)
    )

    user_operations.update_user(database, ObjectId(user_id), updated_user_data)

    return user_operations.find_user(database, ObjectId(user_id))


@router.delete("/{id}")
async def delete_user():
    # database = get_database()
    pass
