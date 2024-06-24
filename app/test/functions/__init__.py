from src.models.user import UserIn, UserOut
from src.utils.config import DotEnvConfig
from test.data.user_json import new_user_json
from test.data.organisation_json import new_organisation_json
from src.database.operations.user import create_user, find_user
from src.database.operations.organisation import create_organisation
from src.database.operations.auth import (
    create_admin_access_token,
    create_user_access_token,
)
from src.database.operations import add_user_to_organisation
from src.models.organisation import (
    OrganisationOut,
    OrganisationIn,
)
from bson import ObjectId


config = DotEnvConfig()

user_data = new_user_json[0]


def get_admin_header():
    username = config.get_config(config.ENV_ADMIN_EMAIL)
    password = config.get_config(config.ENV_ADMIN_PASSWORD)
    token = create_admin_access_token(username, password)

    return {"Authorization": f"{token.token_type} {token.access_token}"}


def get_user_header(
    database, user: UserIn = UserIn(**user_data), create: bool = True
):
    if create:
        create_test_user(database, user)
    token = create_user_access_token(database, user.email, user.password)
    return {"Authorization": f"{token.token_type} {token.access_token}"}


def create_test_user(database, user: UserIn = UserIn(**user_data)) -> UserOut:
    return create_user(database, user)


def create_test_organisation(
    database,
    organisation: OrganisationIn = OrganisationIn(**new_organisation_json[0]),
) -> OrganisationOut:
    return create_organisation(database, organisation)


def create_test_user_with_organisation(
    database,
    is_admin: bool = True,
    user: UserIn = UserIn(**user_data),
    organisation: OrganisationIn = OrganisationIn(**new_organisation_json[0]),
) -> UserOut:
    test_user = create_test_user(database, user)
    test_organisation = create_test_organisation(database, organisation)
    add_user_to_organisation(
        database,
        ObjectId(test_user.id),
        ObjectId(test_organisation.id),
        is_admin,
    )

    return find_user(database, ObjectId(test_user.id))


__all__ = [
    "get_admin_header",
    "get_user_header",
    "create_test_user",
    "create_test_organisation",
    "create_test_user_with_organisation",
]
