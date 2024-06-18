from pydantic import BaseModel, Field


class UserBase(BaseModel):
    # username: str = Field(
    #     ...,
    #     min_length=5,
    #     max_length=15,
    #     description="Username must be between 5 and 15 characters long"
    # )
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
    password: str = Field(
        ...,
        min_length=7,
        max_length=128,
        description="Password must be between 7 and 128 characters long"
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "string",
                    "email": "example@test.com",
                    "full_name": "Example User",
                    "disabled": False,
                    "password": "string123",
                }
            ]
        }
    }
