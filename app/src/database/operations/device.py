from pymongo.database import Database
from bson import ObjectId
from src.models.device import DeviceIn, DeviceOut

def _transform_id(collection: list[dict]) -> list[dict]:
    ret = []
    for item in collection:
        item["id"] = str(item["_id"])
        del item["_id"]
        ret.append(item)
    return ret

def find_device_by_id(database: Database, device_id: ObjectId) -> DeviceOut:
    device = database.devices.find_one({"_id": device_id})

    return DeviceOut(**_transform_id([device])[0])

def find_devices_by_organisation(database: Database, organisation: ObjectId) -> list[DeviceOut]:
    devices = database.devices.find({"organisation": str(organisation)})


def create_device(database: Database, device_data: DeviceIn) -> DeviceOut:
    device_id = database.devices.insert_one(device_data.dict()).inserted_id
    return find_device_by_id(database, device_id)


def delete_device(database: Database, device_id: ObjectId) -> None:
    database.devices.delete_one({"_id": device_id})
