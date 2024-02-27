from pymongo import MongoClient

from src.utils.config import (
    DotEnvConfig
)

config = DotEnvConfig()

environment = config.get_config("ENVIRONMENT")

database_name = config.get_config("DB_NAME_TEST") \
    if environment == "test" \
    else config.get_config("DB_NAME")
database_url = config.get_config("MONGODB_CONNECTION_URI")

database_client = MongoClient(database_url)
database = database_client[database_name]

__all__ = [
    "config",
    "DotEnvConfig",
    "database_client",
    "database"
]