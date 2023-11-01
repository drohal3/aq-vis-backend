from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient

config = dotenv_values(".env")

app = FastAPI()
# TODO: https://dev.to/imkarthikeyan/how-to-build-a-todo-api-using-fastapi-and-mongodb-1en8

@app.get("/test")
async def root():
    return {"message": "Hello World aaa!"}

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGODB_CONNECTION_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


# TODO: https://github.com/testdrivenio/fastapi-jwt/blob/main/main.py ???