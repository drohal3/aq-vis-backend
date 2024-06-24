from fastapi.testclient import TestClient
from src.main import app
from src.database import clean_database, get_database
from src.database.operations.device import create_device
from src.models.device import DeviceIn
from src.models.organisation import OrganisationIn
from src.models.user import UserIn

from test.functions import create_test_user_with_organisation, get_user_header
from test.data.organisation_json import new_organisation_json
from test.data.user_json import new_user_json
from test.data.device_json import new_device_json


def test_get_organisation_api():
    with TestClient(app) as client:
        clean_database()
        database = get_database()
        user_in = UserIn(**new_user_json[0])
        organisation_in = OrganisationIn(**new_organisation_json[0])

        user = create_test_user_with_organisation(
            database, True, user_in, organisation_in
        )
        organisation_id = user.organisation
        response = client.get(
            f"/organisations/{organisation_id}",
            headers=get_user_header(database, user_in, False),
        )

        assert response.status_code == 200
        assert response.json()["id"] == organisation_id


def test_get_organisation_api_unauthorized():
    with TestClient(app) as client:
        clean_database()
        database = get_database()
        user_in = UserIn(**new_user_json[0])
        user_in_1 = UserIn(**new_user_json[1])
        organisation_in = OrganisationIn(**new_organisation_json[0])
        organisation_in_1 = OrganisationIn(**new_organisation_json[1])

        user = create_test_user_with_organisation(
            database, True, user_in, organisation_in
        )
        create_test_user_with_organisation(
            database, True, user_in_1, organisation_in_1
        )
        organisation_id = user.organisation
        response = client.get(
            f"/organisations/{organisation_id}",
            headers=get_user_header(database, user_in_1, False),
        )

        assert response.status_code == 401


def test_get_devices_api():
    with TestClient(app) as client:
        clean_database()
        database = get_database()
        user_in = UserIn(**new_user_json[0])
        organisation_in = OrganisationIn(**new_organisation_json[0])

        user = create_test_user_with_organisation(
            database, True, user_in, organisation_in
        )
        organisation_id = user.organisation
        device_in_data = new_device_json[0].copy()
        device_in_data["organisation"] = organisation_id
        device_in = DeviceIn(**device_in_data)

        new_device = create_device(database, device_in)

        response = client.get(
            f"/organisations/{organisation_id}/devices",
            headers=get_user_header(database, user_in, False),
        )
        assert response.status_code == 200

        assert response.json()[0]["id"] == new_device.id


def test_get_devices_api_unauthorized():
    with TestClient(app) as client:
        clean_database()
        database = get_database()
        user_in = UserIn(**new_user_json[0])
        user_in_1 = UserIn(**new_user_json[1])
        organisation_in = OrganisationIn(**new_organisation_json[0])
        organisation_in_1 = OrganisationIn(**new_organisation_json[1])
        user = create_test_user_with_organisation(
            database, True, user_in, organisation_in
        )
        create_test_user_with_organisation(
            database, True, user_in_1, organisation_in_1
        )
        organisation_id = user.organisation

        response = client.get(
            f"/organisations/{organisation_id}/devices",
            headers=get_user_header(database, user_in_1, False),
        )
        assert response.status_code == 401
