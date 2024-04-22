from fastapi.testclient import TestClient
from src.utils import mongo_db
from src.main import app
from src.database.operations.user import create_user
from src.database.operations.auth import create_login_access_token, get_current_user
from test.data.user_json import new_user_json
from src.models.user import NewUser

new_user_data = new_user_json[0]
def test_access_token():
    with TestClient(app):
        mongo_db.clean_database()
        database = mongo_db.get_database()

        create_user(database, NewUser(**new_user_data))

        access_token = create_login_access_token(database, new_user_data["email"])

        current_user = get_current_user(database, access_token)

        assert current_user["email"] == new_user_data["email"]
