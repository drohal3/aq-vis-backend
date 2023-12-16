import os

from dotenv import dotenv_values

class DotEnvConfig:
    ENV_AUTH_SECRET_KEY = "SECRET_KEY"
    ENV_AUTH_ALGORITHM = "ALGORITHM"
    ENV_AUTH_ACCESS_TOKEN_EXPIRE_MINUTES = "ACCESS_TOKEN_EXPIRE_MINUTES"

    ENV_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
    ENV_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
    ENV_AWS_REGION_NAME = "AWS_REGION_NAME"

    def __init__(self):
        self.config = {
            **dotenv_values(".env")
        }

        print(f"dotenv: {self.config}")

    def get_config(self, key):
        return self.config[key]

