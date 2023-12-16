# Authentication tutorial: https://github.com/techwithtim/Fast-API-Tutorial/blob/main/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utils.config import DotEnvConfig
from src.api.measurements import router as measurements_router
from src.api.user import router as user_router
from src.api.auth import router as auth_router


# from pymongo import MongoClient
# from fastapi.security import OAuth2PasswordBearer
# from typing import Annotated
#
#

config = DotEnvConfig()

SECRET_KEY = config.get_config(DotEnvConfig.ENV_AUTH_SECRET_KEY)
ALGORITHM = config.get_config(DotEnvConfig.ENV_AUTH_ALGORITHM)
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get_config(DotEnvConfig.ENV_AUTH_ACCESS_TOKEN_EXPIRE_MINUTES))

app = FastAPI()
app.include_router(measurements_router, prefix="/measurements", tags=["measurements"])
app.include_router(user_router, prefix="/users", tags=["user"])
app.include_router(auth_router, tags=["authentication"])


# Allow all origins in development, TODO: adjust accordingly for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# def startup_db_client():
#     app.mongodb_client = MongoClient(config["MONGODB_CONNECTION_URI"])
#     app.database = app.mongodb_client[config["DB_NAME"]]
#     print("Connected to the MongoDB database!")
#
# @app.on_event("shutdown")
# def shutdown_db_client():
#     app.mongodb_client.close()
#

