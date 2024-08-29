from backend.api.routers import (
    detect,
    healthcheck,
)
from fastapi import APIRouter

router = APIRouter()

router.include_router(detect.router, tags=["detect"])
router.include_router(healthcheck.router, tags=["healthcheck"])
