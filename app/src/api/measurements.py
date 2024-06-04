from fastapi import APIRouter, Depends
import boto3
from boto3.dynamodb.conditions import Key
from src.utils.config import DotEnvConfig
from src.dependencies.authentication import get_current_active_user
from src.models.user import UserOut

TABLE = "cpc_measurements_test"

router = APIRouter()
config = DotEnvConfig()


@router.get("")
def read_items(
    date_time_from: str,
    date_time_to: str,
    device_id: int,
    parameters: str,
    current_user: UserOut = Depends(get_current_active_user),
):
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=config.get_config(config.ENV_AWS_ACCESS_KEY_ID),
        aws_secret_access_key=config.get_config(
            config.ENV_AWS_SECRET_ACCESS_KEY
        ),
        region_name=config.get_config(config.ENV_AWS_REGION_NAME),
    )

    table = dynamodb.Table(TABLE)
    # DATE_FROM = '2023-11-23 12:30:00'
    # DATE_TO = '2023-11-23 13:30:00'
    response = table.query(
        KeyConditionExpression=Key("device_id").eq(device_id)
        & Key("sample_date_time").between(date_time_from, date_time_to),
    )

    filtered = []

    for item in response["Items"]:
        wanted_keys = parameters.split(",")
        bigdict = item["sample_data"]
        data = dict((k, bigdict[k]) for k in wanted_keys if k in bigdict)
        filtered.append({
            "sample_date_time": item["sample_date_time"],
            "device_id": item["device_id"],
            **data
        })
    return filtered


@router.get("/devices")
def get_devices(current_user: UserOut = Depends(get_current_active_user)):
    return [{"name": "cpc1", "id": 0}]
