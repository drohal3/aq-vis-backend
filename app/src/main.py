# Authentication tutorial: https://github.com/techwithtim/Fast-API-Tutorial/blob/main/main.py
# FastAPI tutorial: https://www.youtube.com/watch?v=XnYYwcOfcn8&list=PLqAmigZvYxIL9dnYeZEhMoHcoP4zop8-p

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utils import config, DotEnvConfig, database_client, database
from src.api.measurements import router as measurements_router
from src.api.user import router as user_router
from src.api.auth import router as auth_router
from src.api.organisations import router as organisations_router

import logging

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
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get_config(DotEnvConfig.ENV_AUTH_ACCESS_TOKEN_EXPIRE_MINUTES))

routers = {
    "measurements": {
        "router": measurements_router,
        "prefix": "/measurements",
        "tags": ["measurements"]
    },
    "users": {
        "router": user_router,
        "prefix": "/users",
        "tags": ["users"]
    },
    "auth": {
        "router": auth_router,
        "prefix": "",
        "tags": ["authentication"]
    },
    "organisations": {
        "router": organisations_router,
        "prefix": "/organisations",
        "tags": ["organisations"]
    }
}

app = FastAPI()
for router in routers.values():
    app.include_router(router.get('router'), prefix=router.get('prefix'), tags=router.get('tags'))


# Allow all origins in development, TODO: adjust accordingly for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = database_client
    app.database = database
    for rout in routers.values():
        r = rout.get("router", False)
        if not r:
            continue
        r.database = app.database
    logging.info(f"Connected to the MongoDB database {database.name}!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    logging.info("Connected to the MongoDB database closed!")


