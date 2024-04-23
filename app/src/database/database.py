from pymongo import MongoClient


# TODO: cleanup, refactor, move to appropriate folder
class Database:
    database = None
    client = None

    def create_database(self, database_name, database_url):
        self.client = MongoClient(database_url)
        self.database = self.client[database_name]
        print(type(self.database))

    def get_database(self):
        return self.database

    def get_client(self):
        return self.client

    # TODO: clean!
    def clean_database(self):
        self.database.users.drop()
        self.database.organisations.drop()
