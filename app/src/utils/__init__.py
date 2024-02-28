import os

from src.utils.config import (
    DotEnvConfig
)

from src.utils.database import Database

config = DotEnvConfig()

environment = os.getenv("ENVIRONMENT")

mongo_db = Database()

__all__ = [
    "config",
    "DotEnvConfig",
    "mongo_db"
]