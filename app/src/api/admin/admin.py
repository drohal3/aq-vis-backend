from fastapi import HTTPException

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from src.api.admin.organisations import router as organisations_router
from src.api.admin.users import router as users_router
from src.utils import config
from src.models.auth import Token
from src.database.operations.auth import create_access_token
import logging

routers = {
    "organisations": {
        "router": organisations_router,
        "prefix": "/organisations",
        "tags": ["admin organisations"],
    },
    "users": {
        "router": users_router,
        "prefix": "/users",
        "tags": ["admin users"],
    },
}

admin_router = APIRouter()

for router in routers.values():
    admin_router.include_router(
        router.get("router"),
        prefix=router.get("prefix"),
        tags=router.get("tags"),
    )

# TODO: authenticate admin, middleware?
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@admin_router.post("/token", response_model=Token, status_code=201)
async def login_for_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    logging.info(f"login_for_token - form_data: {form_data}")
    email = form_data.username
    password = form_data.password

    if not (
        email == config.get_config(config.ENV_ADMIN_EMAIL)
        and password == config.get_config(config.ENV_ADMIN_PASSWORD)
    ):
        raise HTTPException(
            status_code=401, detail="Incorrect email or password"
        )

    access_token_expires = timedelta(
        minutes=int(
            config.get_config(config.ENV_AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    )

    data = {"sub": email}

    access_token = create_access_token(
        data, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "Bearer"}
