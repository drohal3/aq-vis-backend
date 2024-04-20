from fastapi.testclient import TestClient
from src.main import app
from src.utils import mongo_db

def setup_function():
    pass

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