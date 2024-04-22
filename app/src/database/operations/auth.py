import logging

from passlib.context import CryptContext
from src.database.operations.user import find_unsecure_user_by_email
from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.utils import config, DotEnvConfig
from fastapi import HTTPException, status
from src.models.auth import TokenDataE


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = config.get_config(DotEnvConfig.ENV_AUTH_SECRET_KEY)
ALGORITHM = config.get_config(DotEnvConfig.ENV_AUTH_ALGORITHM)
ACCESS_TOKEN_EXPIRE_MINUTES = config.get_config(
    DotEnvConfig.ENV_AUTH_ACCESS_TOKEN_EXPIRE_MINUTES
)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def _create_access_token(data: dict, expires_delta: timedelta or None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def create_login_access_token(database, email, expires_delta: timedelta or None = None):
    # TODO: token can be stored in database so it can be invalidated
    data = {"sub": email}

    return _create_access_token(data, expires_delta)

def get_auth_user(database, email: str, password: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    user = find_unsecure_user_by_email(database, email)

    if not user:
        raise credentials_exception

    if not verify_password(password, user["hashed_password"]):
        raise credentials_exception

    return user

def get_current_user(database, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("XXXXXxxxxXXXX <========")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            # print("No username")
            raise credentials_exception
        token_tada = TokenDataE(email=email)
    except JWTError:
        raise credentials_exception
    user = find_unsecure_user_by_email(database, token_tada.email)
    if user is None:
        # print("no user")
        raise credentials_exception

    return user

def get_current_active_user(database, token: str):
    current_user = get_current_user(database, token)
    logging.info(f"current_user haaaaaa: {current_user}")
    if current_user["disabled"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
