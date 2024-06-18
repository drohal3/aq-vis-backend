from bson import ObjectId
from fastapi import APIRouter, HTTPException

from src.models.user import UserOut, UserIn, UserBase
from src.database import get_database
from src.database.operations.user import (
    create_user as create_user_operation,
    find_user as find_user_operation,
    find_unsecure_user_by_email as find_unsecure_user_by_email_operation,
    find_unsecure_user as find_unsecure_user_operation,
    update_user as update_user_operation,
)

# TODO: =====> =====> =====> Authentication! <===== <===== <=====

router = APIRouter()


@router.post("/", response_model=UserOut)
async def create_user(form_data: UserIn):
    # TODO: database to DI (Depends)
    database = get_database()

    email = form_data.email

    if find_unsecure_user_by_email_operation(database, email):
        raise HTTPException(
            status_code=401,
            detail="User with this email address already exists.",
        )

    return create_user_operation(database, form_data)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: str, form_data: UserBase):
    database = get_database()

    user_to_update = find_unsecure_user_operation(database, ObjectId(user_id))

    if user_to_update is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    updated_user_data = user_to_update.copy(
        update=form_data.dict(exclude_unset=True)
    )

    update_user_operation(database, ObjectId(user_id), updated_user_data)

    return find_user_operation(database, ObjectId(user_id))


@router.delete("/{id}")
async def delete_user():
    # database = get_database()
    pass
