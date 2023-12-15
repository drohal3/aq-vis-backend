from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.utils.config import DotEnvConfig
from src.models.auth import Token, TokenData
from src.models.user import (User, UserInDB, NewUser)



config = DotEnvConfig()

SECRET_KEY = config.get_config(DotEnvConfig.ENV_AUTH_SECRET_KEY)
ALGORITHM = config.get_config(DotEnvConfig.ENV_AUTH_ALGORITHM)
ACCESS_TOKEN_EXPIRE_MINUTES = config.get_config(DotEnvConfig.ENV_AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

db = {
    "dom": {
        "username": "test",
        "full_name": "test test",
        "email": "email@test.com",
        "hashed_password": "",
        "disabled": False
    }
}

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
        print(f"username {username} not found")
        return False
    if not verify_password(password, user.hashed_password):
        print("password incorrect")
        return False

    return user



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
