from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool = Field(default=True, description="Disabled user")
    organisation: str | None = Field(
        default=None, description="Organisation the user belongs to"
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "string",
                    "email": "example@test.com",
                    "full_name": "Example User",
                    "disabled": False,
                }
            ]
        }
    }


class UserOut(UserBase):
    id: str


class UserInDB(UserOut):
    hashed_password: str


class UserIn(UserBase):
    password: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "string",
                    "email": "example@test.com",
                    "full_name": "Example User",
                    "disabled": False,
                    "password": "string",
                }
            ]
        }
    }
