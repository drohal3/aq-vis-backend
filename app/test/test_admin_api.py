from fastapi.testclient import TestClient
from src.main import app
from src.utils.config import DotEnvConfig

config = DotEnvConfig()


def test_admin_login_api():
    with TestClient(app) as client:
        username = config.get_config(config.ENV_ADMIN_EMAIL)
        password = config.get_config(config.ENV_ADMIN_PASSWORD)
        response = client.post(
            "/admin/token", data={"username": username, "password": password}
        )

        assert response.status_code == 201
        assert type(response.json()["access_token"]) == str


def test_admin_login_api_incorrect_credentials():
    with TestClient(app) as client:
        username = config.get_config(config.ENV_ADMIN_EMAIL)
        password = config.get_config(config.ENV_ADMIN_PASSWORD)
        response = client.post(
            "/admin/token",
            data={"username": username, "password": f"{password}incorrect"},
        )
        assert response.status_code == 401

        response = client.post(
            "/admin/token",
            data={"username": f"{username}incorrect", "password": password},
        )
        assert response.status_code == 401
