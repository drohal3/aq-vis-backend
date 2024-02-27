from pymongo import MongoClient
import os

from src.utils.config import (
    DotEnvConfig
)

config = DotEnvConfig()

environment = os.getenv("ENVIRONMENT")

database_name = config.get_database_name()
print(f"Database name: {database_name} aaa")
database_url = config.get_config("MONGODB_CONNECTION_URI")

database_client = MongoClient(database_url)
database = database_client[database_name]

__all__ = [
    "config",
    "DotEnvConfig",
    "database_client",
    "database"
]