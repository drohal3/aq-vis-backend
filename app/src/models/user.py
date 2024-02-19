from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool = Field(default=True, description="Disabled user")
    organisation: str | None = Field(
        default=None, description="Organisation the user belongs to"
    )

class User(UserBase):
    id: str

class UnsecureUser(User):
    hashed_password: str

class NewUser(UserBase):
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "string",
                    "email": "example@test.com",
                    "full_name": "Example User",
                    "disabled": False,
                    "password": "string"
                }
            ]
        }
    }


