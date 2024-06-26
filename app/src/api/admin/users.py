from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends
from src.database.operations.auth import get_current_admin

from src.models.user import UserOut, UserIn, UserBase
from src.database import get_database
from src.database.operations import user_operations

# TODO: =====> =====> =====> Authentication! <===== <===== <=====

router = APIRouter()


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: str, current_admin: str = Depends(get_current_admin)
):
    database = get_database()
    user = user_operations.find_user(database, ObjectId(user_id))

    if not user:
        raise HTTPException(
            status_code=404, detail=f"User {user_id} not found!"
        )

    return user


@router.post("/", response_model=UserOut, status_code=201)
async def create_user(
    form_data: UserIn, current_admin: str = Depends(get_current_admin)
):
    database = get_database()

    email = form_data.email

    if user_operations.find_unsecure_user_by_email(database, email):
        raise HTTPException(
            status_code=409,
            detail="User with this email address already exists.",
        )

    return user_operations.create_user(database, form_data)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: str,
    form_data: UserBase,
    current_admin: str = Depends(get_current_admin),
):
    database = get_database()

    user_to_update = user_operations.find_unsecure_user(
        database, ObjectId(user_id)
    )

    if user_to_update is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    updated_user_data = user_to_update.copy(
        update=form_data.model_dump(exclude_unset=True)
    )

    user_operations.update_user(database, ObjectId(user_id), updated_user_data)

    return user_operations.find_user(database, ObjectId(user_id))


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: str, current_admin: str = Depends(get_current_admin)
):
    database = get_database()
    user_operations.delete_user(database, ObjectId(user_id))
