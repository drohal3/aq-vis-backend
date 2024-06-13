from pymongo.database import Database
from bson import ObjectId
from src.models.device import DeviceIn, DeviceOut


def _transform_id(item):
    item["id"] = str(item["_id"])
    del item["_id"]

    return item


def find_device_by_id(database: Database, device_id: ObjectId) -> DeviceOut:
    device = database.devices.find_one({"_id": device_id})

    return DeviceOut(**_transform_id(device))


def find_devices_by_organisation(
    database: Database, organisation: ObjectId
) -> list[DeviceOut]:
    devices = database.devices.find({"organisation": str(organisation)})

    ret = []
    for device in devices:
        ret.append(DeviceOut(**_transform_id(device)))

    return ret


def create_device(database: Database, device_data: DeviceIn) -> DeviceOut:
    device_id = database.devices.insert_one(device_data.dict()).inserted_id
    return find_device_by_id(database, device_id)


def update_device(
    database: Database, device_id: ObjectId, device_data: DeviceIn
) -> DeviceOut:
    database.devices.update_one(
        {"_id": device_id}, {"$set": device_data.model_dump()}
    )
    return find_device_by_id(database, device_id)


def delete_device(database: Database, device_id: ObjectId) -> None:
    database.devices.delete_one({"_id": device_id})
