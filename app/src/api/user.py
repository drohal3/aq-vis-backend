from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies.authentication import (
    get_password_hash,
    get_current_active_user,
)
from src.models.user import User, NewUser

import logging

router = APIRouter()


@router.get("/me", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# @router.get("/me/items", response_model=User)
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": 1, "owner": current_user}]

# @router.get("/")
