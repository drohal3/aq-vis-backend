from fastapi import APIRouter
from src.models.unit import Unit

router = APIRouter()

units = [
    {"id": "id_conc", "name": "concentration", "symbol": "#/cm3"},
    {"id": "id_temp", "name": "temperature", "symbol": "°C"},
    {"id": "id_percent", "name": "percent", "symbol": "%"},
    {"id": "id_conc_mig", "name": "micrograms per m³", "symbol": "μg/m³"},
    {"id": "id_ppb", "name": "parts per billion", "symbol": "ppb"},
    {"id": "id_ppm", "name": "parts per million", "symbol": "ppm"},
]


@router.get("", response_model=list[Unit])
async def get_all():
    return units
