from fastapi.testclient import TestClient
from src.main import app
from src.database import clean_database
from test.data.user_json import new_user_json


def test_create_user_get_user_api():
    with TestClient(app) as client:
        clean_database()
        response = client.post("admin/users", json=new_user_json[0])
        assert response.status_code == 201

        user_id = response.json()["id"]
        response = client.get(f"admin/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["id"] == user_id


def test_create_duplicate_user_api():
    with TestClient(app) as client:
        clean_database()
        client.post("admin/users", json=new_user_json[0])
        response = client.post("admin/users", json=new_user_json[0])
        assert response.status_code == 409


def test_delete_user_api():
    with TestClient(app) as client:
        clean_database()
        response = client.post("admin/users", json=new_user_json[0])

        assert response.status_code == 201

        user_id = response.json()["id"]

        response = client.delete(f"admin/users/{user_id}")
        assert response.status_code == 204

        response = client.get(f"admin/users/{user_id}")
        assert response.status_code == 404
