from fastapi.testclient import TestClient
from src.main import app
from src.database.operations.user import create_user, find_user, delete_user
from src.database import get_database, clean_database
from src.models.user import NewUser
from bson import ObjectId
from test.data.user_json import new_user_json


def test_create_user():
    with TestClient(app):
        clean_database()
        database = get_database()
        new_user = create_user(database, NewUser(**new_user_json[0]))
        new_user_id = new_user["id"]

        user = find_user(database, ObjectId(new_user_id))

        assert user["id"] == new_user_id


def test_delete_user():
    with TestClient(app):
        clean_database()
        database = get_database()
        new_user = create_user(database, NewUser(**new_user_json[0]))
        new_user_id = new_user["id"]

        delete_user(database, ObjectId(new_user_id))

        user = find_user(database, ObjectId(new_user_id))

        assert user is None

# TODO: def test_update_user():
