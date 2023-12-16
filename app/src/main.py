# Authentication tutorial: https://github.com/techwithtim/Fast-API-Tutorial/blob/main/main.py

from fastapi import Depends, FastAPI,HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.models.user import User, NewUser
from src.models.auth import Token
from datetime import timedelta

from src.utils.config import DotEnvConfig
from src.dependencies.authentication import (
    get_password_hash,
    create_access_token,
    db,
    authenticate_user,
    get_current_active_user
)

from src.api.measurements import router as measurements_router

from fastapi.middleware.cors import CORSMiddleware

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

# Allow all origins in development, TODO: adjust accordingly for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# TODO: use routers instead defining routs directly in main.py
@app.post("/user/create", response_model=User)
def create_user(form_data: NewUser):
    password = form_data.password
    hashed_password = get_password_hash(password)

    new_user_data = form_data.model_dump()
    new_user_data.pop("password")
    new_user_data["hashed_password"] = hashed_password

    db[form_data.username] = new_user_data  # TODO: save in DB

    return new_user_data

@app.post("/token", response_model=Token)
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print("-----> Login for token")
    user = authenticate_user(db, form_data.username, form_data.password)
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "Bearer"}

@app.get("/users/me/", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items", response_model=User)
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]

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

