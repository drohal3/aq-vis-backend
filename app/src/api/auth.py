import logging

from fastapi import APIRouter, Depends, HTTPException, status
from src.models.auth import Token
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies.authentication import (
    create_access_token,
    authenticate_user,
)
from datetime import timedelta
from src.utils.config import DotEnvConfig
from src.utils import mongo_db

router = APIRouter()
config = DotEnvConfig()


@router.post("/token", response_model=Token)
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # TODO: use _id instead of username!
    logging.debug("login_for_token()")
    db = mongo_db.get_database()
    user = authenticate_user(db, form_data.username, form_data.password)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=int(
            config.get_config(config.ENV_AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "Bearer"}
