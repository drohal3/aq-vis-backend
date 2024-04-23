from fastapi import APIRouter, Depends
from pymongo.database import Database

from src.database.operations.auth import get_current_active_user
from src.database import get_database

from src.models.user import User
from fastapi.security import OAuth2PasswordBearer


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/me", response_model=User)
async def read_user_me(
    database: Database = Depends(get_database),
    token: str = Depends(oauth2_scheme),
):
    return get_current_active_user(database, token)


# @router.get("/me/items", response_model=User)
# async def read_own_items(
#       current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": 1, "owner": current_user}]

# @router.get("/")
