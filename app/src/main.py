# Authentication tutorial:
# https://github.com/techwithtim/Fast-API-Tutorial/blob/main/main.py
# FastAPI tutorial:
# https://www.youtube.com/watch?v=XnYYwcOfcn8&list=PLqAmigZvYxIL9dnYeZEhMoHcoP4zop8-p
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utils import config, DotEnvConfig
from src.database import mongo_db
from src.api import (
    measurements_router,
    user_router,
    auth_router,
    devices_router,
    organisations_router,
    units_router,
)
from src.api.admin.admin import admin_router

import logging

# load variables from .env to the environment

# from fastapi.security import OAuth2PasswordBearer
# from typing import Annotated
#
#

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    # filename="basic.log",
)

logging.debug("This is a debug message.")
logging.info("This is an info message.")
logging.warning("This is a warning message.")
logging.error("This is an error message.")
logging.critical("This is a critical message.")

SECRET_KEY = config.get_config(DotEnvConfig.ENV_AUTH_SECRET_KEY)
ALGORITHM = config.get_config(DotEnvConfig.ENV_AUTH_ALGORITHM)
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    config.get_config(DotEnvConfig.ENV_AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
)

routers = {
    "measurements": {
        "router": measurements_router,
        "prefix": "/measurements",
        "tags": ["measurements"],
    },
    "users": {"router": user_router, "prefix": "/users", "tags": ["users"]},
    "auth": {"router": auth_router, "prefix": "", "tags": ["authentication"]},
    "devices": {
        "router": devices_router,
        "prefix": "/devices",
        "tags": ["devices"],
    },
    "organisations": {
        "router": organisations_router,
        "prefix": "/organisations",
        "tags": ["organisations"],
    },
    "units": {"router": units_router, "prefix": "/units", "tags": ["units"]},
    "admin": {"router": admin_router, "prefix": "/admin", "tags": []},
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    database_name = config.get_database_name()
    database_url = config.get_connection_url()

    print(f"Database URL: {database_url}")
    print(f"Database Name: {database_name}")

    mongo_db.create_database(database_name, database_url)

    database = mongo_db.get_database()
    database_client = mongo_db.get_client()

    app.mongodb_client = database_client
    app.database = database
    for rout in routers.values():
        r = rout.get("router", False)
        if not r:
            continue
        r.database = app.database
    logging.info(f"Connected to the MongoDB database {database.name}!")
    yield
    app.mongodb_client.close()
    logging.info("Connected to the MongoDB database closed!")


app = FastAPI(lifespan=lifespan)

# Allow all origins in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers.values():
    app.include_router(
        router.get("router"),
        prefix=router.get("prefix"),
        tags=router.get("tags"),
    )


@app.get("/")
async def example():
    return {"message": "Hello"}
