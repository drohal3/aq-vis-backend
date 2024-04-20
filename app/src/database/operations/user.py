from pymongo.database import Database
from bson import ObjectId

import logging

from src.dependencies.authentication import (
    get_password_hash,
)
from src.models.user import User, NewUser

def find_user(database: Database, user_id: ObjectId) -> User | None:
    user = database.users.find_one({"_id": user_id})
    if user is None:
        return user
    user["id"] = str(user["_id"])

    return user

def create_user(database: Database, data: NewUser) -> User:
    password = data.password
    hashed_password = get_password_hash(password)

    new_user_data = data.model_dump()
    new_user_data.pop("password")
    new_user_data["hashed_password"] = hashed_password
    user_id = database.users.insert_one(new_user_data).inserted_id
    logging.debug(f"create_user() - user_id: {user_id}")
    user = find_user(database, user_id)

    logging.info(f"create_user() - created user: {user}")

    return user

def delete_user(database: Database, user_id: ObjectId):
    database.users.delete_one({"_id": user_id})

