import logging

from fastapi import APIRouter, Depends
from src.models.auth import Token
from fastapi.security import OAuth2PasswordRequestForm
from src.database import get_database
from src.database.operations.auth import (
    create_user_access_token,
)

from src.utils import config

router = APIRouter()


@router.post("/token", response_model=Token, status_code=201)
async def login_for_token(
    database=Depends(get_database),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    logging.debug("login_for_token()")
    return create_user_access_token(
        database,
        form_data.username,
        form_data.password,
        config.get_config(config.ENV_AUTH_ACCESS_TOKEN_EXPIRE_MINUTES),
    )
