import logging

from fastapi import APIRouter, Depends
from src.models.auth import Token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from src.database import get_database
from src.database.operations.auth import (
    get_auth_user,
    create_login_access_token,
)
from src.utils import config

router = APIRouter()


@router.post("/token", response_model=Token, status_code=201)
async def login_for_token(
    database=Depends(get_database),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    # TODO: use _id instead of username!
    logging.debug("login_for_token()")
    user = get_auth_user(
        database, email=form_data.username, password=form_data.password
    )
    print(user)

    access_token_expires = timedelta(
        minutes=int(
            config.get_config(config.ENV_AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    )

    access_token = create_login_access_token(
        database, email=user["email"], expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "Bearer"}
