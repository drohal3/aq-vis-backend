from fastapi.testclient import TestClient
from src.database import get_database, clean_database
from src.main import app
from src.database.operations.user import create_user
from src.database.operations.auth import (
    create_login_access_token,
    get_current_user,
    get_auth_user,
)
from test.data.user_json import new_user_json
from src.models.user import NewUser

new_user_data = new_user_json[0]


def test_access_token():
    with TestClient(app):
        clean_database()
        database = get_database()

        create_user(database=database, data=NewUser(**new_user_data))

        user = get_auth_user(
            database=database,
            email=new_user_data["email"],
            password=new_user_data["password"],
        )

        assert user["email"] == new_user_data["email"]

        access_token = create_login_access_token(
            database=database, email=new_user_data["email"]
        )

        current_user = get_current_user(database=database, token=access_token)

        assert current_user["email"] == new_user_data["email"]
