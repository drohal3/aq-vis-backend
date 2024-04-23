from fastapi.testclient import TestClient
from src.main import app

from src.database import get_database, clean_database
from bson import ObjectId

from src.models.organisation import NewOrganisation
from src.database.operations.organisation import (
    create_organisation,
    find_organisation,
    delete_organisation,
)
from test.data.organisation_json import new_organisation_json

new_organisation_json_data = new_organisation_json[0]


def test_create_organisation():
    with TestClient(app):
        clean_database()
        database = get_database()
        new_organisation = create_organisation(
            database, NewOrganisation(**new_organisation_json_data)
        )
        new_organisation_id = new_organisation["id"]
        organisation = find_organisation(
            database, ObjectId(new_organisation_id)
        )
        assert new_organisation_id == organisation["id"]


def test_delete_organisation():
    with TestClient(app):
        clean_database()
        database = get_database()
        new_organisation = create_organisation(
            database, NewOrganisation(**new_organisation_json_data)
        )
        new_organisation_id = new_organisation["id"]
        delete_organisation(database, ObjectId(new_organisation_id))
        organisation = find_organisation(
            database, ObjectId(new_organisation_id)
        )
        assert organisation is None
