from fastapi.testclient import TestClient
from src.main import app
from src.database import clean_database, get_database
from src.models.organisation import OrganisationIn
from src.models.user import UserIn
from test.data.device_json import new_device_json
from test.data.user_json import new_user_json
from test.data.organisation_json import new_organisation_json
from test.functions import get_user_header, create_test_user_with_organisation


def test_create_device_api():
    with TestClient(app) as client:
        clean_database()
        database = get_database()
        user_in = UserIn(**new_user_json[0])
        test_user = create_test_user_with_organisation(database, True, user_in)
        device_data = new_device_json[0].copy()
        device_data["organisation"] = test_user.organisation
        response = client.post(
            "/devices",
            json=device_data,
            headers=get_user_header(database, user_in, False),
        )
        assert response.status_code == 201


def test_create_device_api_unauthorized():
    with TestClient(app) as client:
        clean_database()
        database = get_database()

        user_0 = create_test_user_with_organisation(
            database,
            True,
            UserIn(**new_user_json[0]),
            OrganisationIn(**new_organisation_json[0]),
        )
        create_test_user_with_organisation(
            database,
            True,
            UserIn(**new_user_json[1]),
            OrganisationIn(**new_organisation_json[1]),
        )
        device_data = new_device_json[0].copy()
        device_data["organisation"] = user_0.organisation
        response = client.post(
            "/devices",
            json=device_data,
        )
        assert response.status_code == 401
        create_test_user_with_organisation(
            database, True, UserIn(**new_user_json[1])
        )
        response = client.post(
            "/devices",
            json=device_data,
            headers=get_user_header(database, UserIn(**new_user_json[1])),
        )
        assert response.status_code == 401


# def test_create_device_api_duplicate():
#     with TestClient(app) as client:
#         clean_database()
#         database = get_database()
#         user_in = UserIn(**new_user_json[0])
#         test_user = create_test_user_with_organisation(
#         database, True, user_in)
#         device_data = new_device_json[0].copy()
#         device_data["organisation"] = test_user.organisation
#         response = client.post(
#             "/devices",
#             json=device_data,
#             headers=get_user_header(database, user_in, False),
#         )
#         assert response.status_code == 201
#         response = client.post(
#             "/devices",
#             json=device_data,
#             headers=get_user_header(database, user_in, False),
#         )
#         assert response.status_code == 409
# # NOTE: even if there are duplicate device_codes, they have unique ids


def test_get_device_api():
    with TestClient(app) as client:
        clean_database()
        database = get_database()
        user_in = UserIn(**new_user_json[0])
        test_user = create_test_user_with_organisation(database, True, user_in)
        device_data = new_device_json[0].copy()
        device_data["organisation"] = test_user.organisation
        response = client.post(
            "/devices",
            json=device_data,
            headers=get_user_header(database, user_in, False),
        )

        new_device_id = response.json()["id"]
        response = client.get(
            f"/devices/{new_device_id}",
            headers=get_user_header(database, user_in, False),
        )

        assert response.status_code == 200


def test_get_device_api_unauthorized():
    with TestClient(app) as client:
        clean_database()
        database = get_database()
        user_in_0 = UserIn(**new_user_json[0])
        user_in_1 = UserIn(**new_user_json[1])
        test_user = create_test_user_with_organisation(
            database, True, user_in_0
        )
        create_test_user_with_organisation(database, True, user_in_1)
        device_data = new_device_json[0].copy()
        device_data["organisation"] = test_user.organisation
        response = client.post(
            "/devices",
            json=device_data,
            headers=get_user_header(database, user_in_0, False),
        )

        new_device_id = response.json()["id"]
        response = client.get(
            f"/devices/{new_device_id}",
            headers=get_user_header(database, user_in_1, False),
        )

        assert response.status_code == 401


#
def test_update_device_api():
    with TestClient(app) as client:
        clean_database()
        database = get_database()
        user_in = UserIn(**new_user_json[0])
        test_user = create_test_user_with_organisation(database, True, user_in)
        device_data = new_device_json[0].copy()
        device_data["organisation"] = test_user.organisation
        response = client.post(
            "/devices",
            json=device_data,
            headers=get_user_header(database, user_in, False),
        )

        new_device_id = response.json()["id"]

        device_data_1 = new_device_json[1].copy()
        device_data_1["organisation"] = test_user.organisation

        client.put(
            f"/devices/{new_device_id}",
            json=device_data_1,
            headers=get_user_header(database, user_in),
        )

        response = client.get(
            f"/devices/{new_device_id}",
            headers=get_user_header(database, user_in, False),
        )

        assert response.status_code == 200
        assert response.json()["name"] == device_data_1["name"]
        assert response.json()["code"] == device_data_1["code"]
        assert response.json()["organisation"] == device_data_1["organisation"]
        assert response.json()["id"] == new_device_id


def test_update_device_api_unauthorized():
    with TestClient(app) as client:
        clean_database()
        database = get_database()
        user_in = UserIn(**new_user_json[0])
        user_in_1 = UserIn(**new_user_json[1])
        test_user = create_test_user_with_organisation(database, True, user_in)
        device_data = new_device_json[0].copy()
        device_data["organisation"] = test_user.organisation
        response = client.post(
            "/devices",
            json=device_data,
            headers=get_user_header(database, user_in, False),
        )

        new_device_id = response.json()["id"]

        device_data_1 = new_device_json[1].copy()
        device_data_1["organisation"] = test_user.organisation

        put_response = client.put(
            f"/devices/{new_device_id}",
            json=device_data_1,
            headers=get_user_header(database, user_in_1, True),
        )

        assert put_response.status_code == 401

        response = client.get(
            f"/devices/{new_device_id}",
            headers=get_user_header(database, user_in, False),
        )

        assert response.json()["name"] == device_data["name"]
        assert response.json()["code"] == device_data["code"]
        assert response.json()["organisation"] == device_data["organisation"]
        assert response.json()["id"] == new_device_id


# def test_update_device_api_duplicate():
#     assert False
# # Note: even if code is duplicated, id is the same.
# # Duplicate device_code is allowed for time being


def test_delete_device_api():
    with TestClient(app) as client:
        clean_database()
        database = get_database()
        user_in = UserIn(**new_user_json[0])
        test_user = create_test_user_with_organisation(database, True, user_in)
        device_data = new_device_json[0].copy()
        device_data["organisation"] = test_user.organisation
        new_device_response = client.post(
            "/devices",
            json=device_data,
            headers=get_user_header(database, user_in, False),
        )
        response = client.delete(
            f"/devices/{new_device_response.json().get('id')}",
            headers=get_user_header(database, user_in, False),
        )

        assert response.status_code == 204

        response = client.get(
            f"/devices/{new_device_response.json().get('id')}",
            headers=get_user_header(database, user_in, False),
        )

        assert response.status_code == 404


def test_delete_device_api_unauthorized():
    with TestClient(app) as client:
        clean_database()
        database = get_database()
        user_in = UserIn(**new_user_json[0])
        user_in_1 = UserIn(**new_user_json[1])
        test_user = create_test_user_with_organisation(database, True, user_in)
        device_data = new_device_json[0].copy()
        device_data["organisation"] = test_user.organisation
        new_device_response = client.post(
            "/devices",
            json=device_data,
            headers=get_user_header(database, user_in, False),
        )
        response = client.delete(
            f"/devices/{new_device_response.json().get('id')}",
            headers=get_user_header(database, user_in_1, True),
        )

        assert response.status_code == 401

        response = client.get(
            f"/devices/{new_device_response.json().get('id')}",
            headers=get_user_header(database, user_in, False),
        )

        assert response.status_code == 200
