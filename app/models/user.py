from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)