from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool or None = None

class UserInDB(User):
    hashed_password: str

class NewUser(User):
    password: str

