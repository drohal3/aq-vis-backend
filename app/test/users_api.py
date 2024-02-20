from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def example_test():
    assert True
