from fastapi.testclient import TestClient
from src.main import app
from src.database import get_database, clean_database
from bson import ObjectId
from src.models.organisation import NewOrganisation, OrganisationMembership
from src.database.operations import organisation_operations
from test.data.organisation_json import new_organisation_json
from src.exceptions import DuplicateException, NotFoundException
import pytest

new_organisation_json_data = new_organisation_json[0]


def test_create_organisation_find_organisation():
    with TestClient(app):
        clean_database()
        database = get_database()
        new_organisation = organisation_operations.create_organisation(
            database, NewOrganisation(**new_organisation_json_data)
        )
        new_organisation_id = new_organisation.id
        organisation = organisation_operations.find_organisation(
            database, ObjectId(new_organisation_id)
        )
        assert new_organisation_id == organisation.id


def test_delete_organisation():
    with TestClient(app):
        clean_database()
        database = get_database()
        new_organisation = organisation_operations.create_organisation(
            database, NewOrganisation(**new_organisation_json_data)
        )
        new_organisation_id = new_organisation.id
        organisation_operations.delete_organisation(
            database, ObjectId(new_organisation_id)
        )
        organisation = organisation_operations.find_organisation(
            database, ObjectId(new_organisation_id)
        )
        assert organisation is None


def test_add_membership():
    with TestClient(app):
        clean_database()
        database = get_database()
        new_organisation = organisation_operations.create_organisation(
            database, NewOrganisation(**new_organisation_json_data)
        )
        new_organisation_id = new_organisation.id

        some_id = "000000000000000000000000"

        organisation_operations.add_membership(
            database,
            ObjectId(new_organisation_id),
            OrganisationMembership(**{"user": some_id, "is_admin": False}),
        )

        organisation = organisation_operations.find_organisation(
            database, ObjectId(new_organisation_id)
        )

        assert organisation.members[0].user == some_id
        assert len(organisation.members) == 1


def test_add_duplicate_membership():
    with TestClient(app):
        clean_database()
        database = get_database()
        new_organisation = organisation_operations.create_organisation(
            database, NewOrganisation(**new_organisation_json_data)
        )
        new_organisation_id = new_organisation.id

        # new_user = create_user(database, UserIn(**new_user_json[0]))
        # new_user_id = new_user.id
        some_id = "000000000000000000000000"

        organisation_operations.add_membership(
            database,
            ObjectId(new_organisation_id),
            OrganisationMembership(**{"user": some_id, "is_admin": False}),
        )

        with pytest.raises(DuplicateException):
            organisation_operations.add_membership(
                database,
                ObjectId(new_organisation_id),
                OrganisationMembership(**{"user": some_id, "is_admin": False}),
            )

        organisation = organisation_operations.find_organisation(
            database, ObjectId(new_organisation.id)
        )
        assert len(organisation.members) == 1


def test_add_membership_organisation_not_exist():
    with TestClient(app):
        clean_database()
        database = get_database()
        some_id = "000000000000000000000000"

        with pytest.raises(NotFoundException):
            organisation_operations.add_membership(
                database,
                ObjectId(some_id),
                OrganisationMembership(**{"user": some_id, "is_admin": False}),
            )


def test_remove_membership():
    with TestClient(app):
        clean_database()
        database = get_database()
        new_organisation = organisation_operations.create_organisation(
            database, NewOrganisation(**new_organisation_json_data)
        )

        some_id_1 = "000000000000000000000000"
        some_id_2 = "000000000000000000000001"
        organisation_operations.add_membership(
            database,
            ObjectId(new_organisation.id),
            OrganisationMembership(**{"user": some_id_1, "is_admin": False}),
        )
        organisation_operations.add_membership(
            database,
            ObjectId(new_organisation.id),
            OrganisationMembership(**{"user": some_id_2, "is_admin": False}),
        )
        organisation_operations.remove_membership(
            database, ObjectId(new_organisation.id), ObjectId(some_id_1)
        )

        organisation = organisation_operations.find_organisation(
            database, ObjectId(new_organisation.id)
        )

        assert (
            organisation.members[0].user == some_id_2
        )  # only second id present
        assert len(organisation.members) == 1

def test_remove_membership_not_exist():
    with TestClient(app):
        clean_database()
        database = get_database()
        some_id = "000000000000000000000000"
        with pytest.raises(NotFoundException):
            organisation_operations.remove_membership(
                database,
                ObjectId(some_id),
                ObjectId(some_id)
            )
