import os

from src.utils.config import DotEnvConfig

from src.database.database import Database

config = DotEnvConfig()

__all__ = ["config", "DotEnvConfig"]
