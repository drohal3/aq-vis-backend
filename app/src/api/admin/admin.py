from fastapi import APIRouter, Depends, HTTPException
from src.api.admin.organisations import router as organisations_router
from src.api.admin.users import router as users_router

routers = {
    "organisations": {
        "router": organisations_router,
        "prefix": "/organisations",
        "tags": ["admin organisations"],
    },
    "users": {
        "router": users_router,
        "prefix": "/users",
        "tags": ["admin users"],
    },
}

admin_router = APIRouter()

for router in routers.values():
    admin_router.include_router(
        router.get("router"),
        prefix=router.get("prefix"),
        tags=router.get("tags"),
    )

# TODO: authenticate admin, middleware?
