from fastapi.testclient import TestClient
from src.main import app
from src.database.operations.user import create_user
from src.models.user import UserIn
from src.database import get_database, clean_database
from test.data.user_json import new_user_json


def setup_function():
    pass


def test_me():
    with TestClient(app) as client:
        clean_database()
        database = get_database()
        create_user(database, UserIn(**new_user_json[0]))
        token_response = client.post(
            "/token",
            data={
                "username": new_user_json[0]["email"],
                "password": new_user_json[0]["password"],
            },
        )
        token = token_response.json()["access_token"]
        token_type = token_response.json()["token_type"]

        response = client.get(
            "/users/me", headers={"Authorization": f"{token_type} {token}"}
        )

        assert response.status_code == 200
        response_json = response.json()
        assert response_json["email"] == new_user_json[0]["email"]


def test_me_unauthorized():
    with TestClient(app) as client:
        response = client.get("/users/me")
        assert response.status_code == 401
