from src.database import get_database, clean_database
from fastapi.testclient import TestClient
from src.main import app
from src.database.operations import device_operations
from src.models.device import DeviceIn
from test.data.device_json import new_device_json
from bson import ObjectId


def test_create_device_find_device():
    with TestClient(app):
        clean_database()
        database = get_database()
        new_device = device_operations.create_device(
            database, DeviceIn(**new_device_json[0])
        )

        assert new_device.name == new_device_json[0]["name"]
        assert new_device.organisation == new_device_json[0]["organisation"]

        found_device = device_operations.find_device_by_id(
            database, ObjectId(new_device.id)
        )
        assert found_device.name == new_device.name


def test_update_device():
    with TestClient(app):
        clean_database()
        database = get_database()
        new_device = device_operations.create_device(
            database, DeviceIn(**new_device_json[0])
        )

        update_data = new_device_json[0].copy()
        update_data["organisation"] = "0000000000000001"

        updated_device = device_operations.update_device(
            database, ObjectId(new_device.id), DeviceIn(**update_data)
        )

        assert updated_device.organisation == update_data["organisation"]

        found_device = device_operations.find_device_by_id(
            database, ObjectId(new_device.id)
        )

        assert found_device.organisation == update_data["organisation"]


def test_delete_device():
    with TestClient(app):
        clean_database()
        database = get_database()
        new_device = device_operations.create_device(
            database, DeviceIn(**new_device_json[0])
        )

        device_operations.delete_device(database, ObjectId(new_device.id))

        found_device = device_operations.find_device_by_id(
            database, ObjectId(new_device.id)
        )

        assert found_device is None
