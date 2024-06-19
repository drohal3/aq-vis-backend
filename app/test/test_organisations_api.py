from fastapi.testclient import TestClient
from src.main import app
from src.database import clean_database

from test.data.organisation_json import new_organisation_json
from test.data.user_json import new_user_json

new_organisation_data = new_organisation_json[0]
new_user_data = new_user_json[0]


def test_create_organisation():
    with TestClient(app) as client:
        clean_database()
        response = client.post(
            "/admin/organisations", json=new_organisation_data
        )
        assert response.status_code == 201

def test_get_organisation():
    with TestClient(app) as client:
        clean_database()
        new_organisation = client.post(
            "/admin/organisations", json=new_organisation_data
        )

        new_organisation_id = new_organisation.json()["id"]

        response = client.get(f"/admin/organisations/{new_organisation_id}")
        assert response.status_code == 200
        assert response.json()["id"] == new_organisation_id

def test_get_organisation_not_exist():
    with TestClient(app) as client:
        clean_database()
        new_organisation_id = "000000000000000000000000"
        response = client.get(f"/admin/organisations/{new_organisation_id}")
        assert response.status_code == 404

def test_delete_organisation():
    with TestClient(app) as client:
        clean_database()
        response = client.post(
            "/admin/organisations", json=new_organisation_data
        )
        organisation_id = response.json()["id"]

        response = client.delete(f"/admin/organisations/{organisation_id}")
        assert response.status_code == 204


def test_add_and_remove_member():
    with TestClient(app) as client:
        clean_database()
        organisation_response = client.post(
            "/admin/organisations", json=new_organisation_data
        )
        organisation_id = organisation_response.json()["id"]
        user_response = client.post("admin/users", json=new_user_data)
        user_id = user_response.json()["id"]

        member_json = {"organisation": organisation_id, "user": user_id}
        response = client.post(
            "/admin/organisations/add_user", json=member_json
        )
        assert response.status_code == 200

        response = client.post(
            "/admin/organisations/remove_user", json=member_json
        )
        assert response.status_code == 200
