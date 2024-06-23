from fastapi.testclient import TestClient
from src.main import app
from src.database import clean_database


def test_create_device_api():
    with TestClient(app):
        clean_database()

    assert False


def test_create_device_api_unauthorized():
    assert False


def test_create_device_api_duplicate():
    assert False


def test_get_device_api():
    assert False


def test_get_device_api_unauthorized():
    assert False


def test_update_device_api():
    assert False


def test_update_device_api_unauthorized():
    assert False


def test_update_device_api_duplicate():
    assert False


def test_delete_device_api():
    assert False


def test_delete_device_api_unauthorized():
    assert False
