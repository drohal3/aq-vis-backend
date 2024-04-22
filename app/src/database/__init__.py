from src.database.database import Database

mongo_db = Database()

def get_database():
    return mongo_db.get_database()

def get_client():
    mongo_db.get_client()

def clean_database():
    # TODO: only if test
    mongo_db.clean_database()


__all__ = ["mongo_db", "get_database", "get_client", "clean_database"]
