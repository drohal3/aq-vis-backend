from fastapi.testclient import TestClient
from src.main import app

from src.utils import mongo_db
from bson import ObjectId

from src.models.organisation import NewOrganisation
from src.database.operations.organisation import create_organisation, find_organisation, delete_organisation


new_organisation_json = {
    "name": "Test Organisation",
    "devices": []
}
def test_create_organisation():
    with TestClient(app):
        mongo_db.clean_database()
        database = mongo_db.get_database()
        new_organisation = create_organisation(database, NewOrganisation(**new_organisation_json))
        new_organisation_id = new_organisation["id"]
        organisation = find_organisation(database, ObjectId(new_organisation_id))
        assert new_organisation_id == organisation["id"]

def test_delete_organisation():
    with TestClient(app):
        mongo_db.clean_database()
        database = mongo_db.get_database()
        new_organisation = create_organisation(database, NewOrganisation(**new_organisation_json))
        new_organisation_id = new_organisation["id"]
        delete_organisation(database, ObjectId(new_organisation_id))
        organisation = find_organisation(database, ObjectId(new_organisation_id))
        assert organisation is None
