# Authentication tutorial: https://github.com/techwithtim/Fast-API-Tutorial/blob/main/main.py

from fastapi import Depends, FastAPI,HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import User, UserInDB, NewUser
from models.auth import Token, TokenData
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from utils.config import DotEnvConfig

# from pymongo import MongoClient
# from fastapi.security import OAuth2PasswordBearer
# from typing import Annotated
#
#

config = DotEnvConfig()

SECRET_KEY = config.get_config(DotEnvConfig.ENV_AUTH_SECRET_KEY)
ALGORITHM = config.get_config(DotEnvConfig.ENV_AUTH_ALGORITHM)
ACCESS_TOKEN_EXPIRE_MINUTES = config.get_config(DotEnvConfig.ENV_AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)

db = {
    "dom": {
        "username": "test",
        "full_name": "test test",
        "email": "email@test.com",
        "hashed_password": "",
        "disabled": False
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    print(f"username: {username}")
    print(db)
    if username in db.keys():
        print("username found in db")
        user_data = db[username]
        print(f"user found {user_data}")

        return UserInDB(**user_data)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            print("No username")
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        print("no user")
        raise credentials_exception

    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


# TODO: use routers instead defining routs directly in main.py
@app.post("/create_user", response_model=User)
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
    user = authenticate_user(db, form_data.username, form_data.password)
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

