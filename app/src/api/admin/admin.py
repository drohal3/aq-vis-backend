from fastapi import APIRouter, Depends, HTTPException
from src.api.admin.organisations import router as organisations_router

routers = {
    "organisations": {
        "router": organisations_router,
        "prefix": "/organisations",
        "tags": ["admin organisations"]
    }
}

admin_router = APIRouter()

for router in routers.values():
    admin_router.include_router(router.get('router'), prefix=router.get('prefix'), tags=router.get('tags'))

# TODO: authenticate admin, middleware?
