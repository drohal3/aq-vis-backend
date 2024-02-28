from fastapi import APIRouter, Depends
import boto3
from boto3.dynamodb.conditions import Key
from src.utils.config import DotEnvConfig
from src.dependencies.authentication import get_current_active_user
from src.models.user import User

TABLE = "cpc_measurements_test"

router = APIRouter()
config = DotEnvConfig()


@router.get("")
def read_items(
    date_time_from: str,
    date_time_to: str,
    device_id: int,
    current_user: User = Depends(get_current_active_user),
):
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=config.get_config(config.ENV_AWS_ACCESS_KEY_ID),
        aws_secret_access_key=config.get_config(
            config.ENV_AWS_SECRET_ACCESS_KEY
        ),
        region_name=config.get_config(config.ENV_AWS_REGION_NAME),
    )

    print(f">>>> >>>> date_time_from: {date_time_from}")

    table = dynamodb.Table(TABLE)
    # DATE_FROM = '2023-11-23 12:30:00'
    # DATE_TO = '2023-11-23 13:30:00'
    response = table.query(
        KeyConditionExpression=Key("device_id").eq(device_id)
        & Key("sample_date_time").between(date_time_from, date_time_to)
    )
    print(response)
    return response["Items"]


@router.get("/devices")
def get_devices(current_user: User = Depends(get_current_active_user)):
    return [{"name": "cpc1", "id": 0}]
