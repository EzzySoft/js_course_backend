from fastapi import APIRouter

from .trips import router as trips_router
from .auth import router as auth_router
from config import settings


router = APIRouter(
    prefix=settings.api.v1.prefix
)
router.include_router(
    trips_router,
    prefix=settings.api.v1.trips
)

router.include_router(
    auth_router,
    prefix=settings.api.v1.auth
)
