from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.utils import config, DotEnvConfig, mongo_db
from src.models.auth import TokenData
from src.models.user import UnsecureUser

import logging


SECRET_KEY = config.get_config(DotEnvConfig.ENV_AUTH_SECRET_KEY)
ALGORITHM = config.get_config(DotEnvConfig.ENV_AUTH_ALGORITHM)
ACCESS_TOKEN_EXPIRE_MINUTES = config.get_config(
    DotEnvConfig.ENV_AUTH_ACCESS_TOKEN_EXPIRE_MINUTES
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    # TODO: move to database/operations
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token():
    pass


def get_user(db, username: str) -> UnsecureUser or None:
    logging.debug(f"get_user() - username: {username}")
    user = db.users.find_one({"username": username})
    if user is None:
        return None
    logging.debug(f"get_user() - user: {user}")

    user["id"] = str(user["_id"])
    return UnsecureUser(**user)


def authenticate_user(db, username: str, password: str):
    # TODO: move to database/operations
    user = get_user(db, username)
    if not user:
        logging.debug(f"authenticate_user() - username {username} not found")
        return False
    if not verify_password(password, user.hashed_password):
        print("authenticate_user() - password incorrect")
        return False

    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # print(f"token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        # print(payload)
        # print(f"username: {username}")
        if username is None:
            # print("No username")
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(mongo_db.get_database(), username=token_data.username)
    # TODO: for database, dependency injection as in cases above or not?
    if user is None:
        # print("no user")
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: UnsecureUser = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user
