from fastapi.testclient import TestClient
from src.main import app
from src.database.operations.user import create_user, find_user, delete_user
from src.utils import mongo_db
from src.models.user import NewUser
from bson import ObjectId

new_user_json = {
            "disabled": False,
            "email": "example@test.com",
            "full_name": "Example User",
            "password": "string",
            "username": "string"
        }

def test_create_user():
    with TestClient(app):
        mongo_db.clean_database()
        database = mongo_db.get_database()
        new_user = create_user(database, NewUser(**new_user_json))
        new_user_id = new_user["id"]

        user = find_user(database, ObjectId(new_user_id))

        assert user["id"] == new_user_id


def test_delete_user():
    with TestClient(app):
        mongo_db.clean_database()
        database = mongo_db.get_database()
        new_user = create_user(database, NewUser(**new_user_json))
        new_user_id = new_user["id"]

        delete_user(database, ObjectId(new_user_id))

        user = find_user(database, ObjectId(new_user_id))

        assert user is None

# TODO: def test_update_user():
