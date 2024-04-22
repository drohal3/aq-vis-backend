from fastapi.testclient import TestClient
from src.main import app
from src.database.operations.user import create_user
from src.models.user import NewUser
from src.utils import mongo_db
from test.data.user_json import new_user_json

def setup_function():
    pass

def test_me():
    with TestClient(app) as client:
        mongo_db.clean_database()
        database = mongo_db.get_database()
        create_user(database, NewUser(**new_user_json[0]))
        token_response = client.post("/token", data={"username": "string", "password": "string"})
        token = token_response.json()["access_token"]
        token_type = token_response.json()["token_type"]

        response = client.get("/users/me", headers={"Authorization": f"{token_type} {token}"})

        assert response.status_code == 200
        response_json = response.json()

        assert response_json["username"] == new_user_json[0]["username"]

def test_me_unauthorized():
    with TestClient(app) as client:
        response = client.get("/users/me")
        assert response.status_code == 401

def test_create_user_api():
    with TestClient(app) as client:
        mongo_db.clean_database()
        json = {
          "disabled": False,
          "email": "example@test.com",
          "full_name": "Example User",
          "password": "string",
          "username": "string"
        }

        response = client.post("admin/users", json=json)

        assert response.status_code == 200
