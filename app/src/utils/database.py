from pymongo import MongoClient


class Database:
    database = None
    client = None

    def create_database(self, database_name, database_url):
        self.client = MongoClient(database_url)
        self.database = self.client[database_name]

    def get_database(self):
        return self.database

    def get_client(self):
        return self.client
