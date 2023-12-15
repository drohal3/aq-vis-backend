from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import User, UserInDB, NewUser

@app.post("/create_user", response_model=User)
def create_user(form_data: NewUser):
    password = form_data.password
    hashed_password = get_password_hash(password)

    new_user_data = form_data.model_dump()
    new_user_data.pop("password")
    new_user_data["hashed_password"] = hashed_password

    db[form_data.username] = new_user_data  # TODO: save in DB

    return new_user_data