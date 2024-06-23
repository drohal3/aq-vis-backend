from src.utils.config import DotEnvConfig

config = DotEnvConfig()


def get_admin_header(client):
    username = config.get_config(config.ENV_ADMIN_EMAIL)
    password = config.get_config(config.ENV_ADMIN_PASSWORD)
    token_response = client.post(
        "/admin/token",
        data={
            "username": username,
            "password": password,
        },
    )
    token = token_response.json()["access_token"]
    token_type = token_response.json()["token_type"]

    return {"Authorization": f"{token_type} {token}"}


__all__ = ["get_admin_header"]
