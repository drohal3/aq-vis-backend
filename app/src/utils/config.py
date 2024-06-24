from dotenv import load_dotenv
import os


class DotEnvConfig:
    ENV_AUTH_SECRET_KEY = "SECRET_KEY"
    ENV_AUTH_ALGORITHM = "ALGORITHM"
    ENV_AUTH_ACCESS_TOKEN_EXPIRE_MINUTES = "ACCESS_TOKEN_EXPIRE_MINUTES"

    ENV_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
    ENV_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
    ENV_AWS_REGION_NAME = "AWS_REGION_NAME"

    ENV_DB_NAME = "DB_NAME"
    ENV_DB_NAME_TEST = "DB_NAME_TEST"

    ENV_DB_CONNECTION_URL = "MONGODB_CONNECTION_URI"
    ENV_DB_CONNECTION_URL_TEST = "MONGODB_CONNECTION_URI_TEST"

    PYTEST_CURRENT_TEST = "PYTEST_CURRENT_TEST"

    ENV_ADMIN_EMAIL = "ADMIN_EMAIL"
    ENV_ADMIN_PASSWORD = "ADMIN_PASSWORD"

    def __init__(self):
        load_dotenv(".env")

    def get_config(self, key):
        return os.getenv(key)

    def get_database_name(self):
        return (
            self.get_config(self.ENV_DB_NAME)
            if not self.get_config(self.PYTEST_CURRENT_TEST)
            else self.get_config(self.ENV_DB_NAME_TEST)
        )

    def get_connection_url(self):
        return (
            self.get_config(self.ENV_DB_CONNECTION_URL)
            if not self.get_config(self.PYTEST_CURRENT_TEST)
            else self.get_config(self.ENV_DB_CONNECTION_URL_TEST)
        )
