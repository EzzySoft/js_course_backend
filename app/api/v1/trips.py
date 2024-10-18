from fastapi import APIRouter, Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from models import database_helper
from schemas.trip_scheme import RequestTripScheme
from services import trip_service
from services.response_service import ResponseService

router = APIRouter(tags=["Trips"])


@router.post("/")
async def create(trip: RequestTripScheme, session_id: str | None = Cookie(default=None),
                 db: AsyncSession = Depends(database_helper.session_getter)):
    return await ResponseService.response(
        trip_service.create(trip, session_id, db)
    )

@router.get("/")
async def get_all(                 db: AsyncSession = Depends(database_helper.session_getter)):
    return await ResponseService.response(
        trip_service.get_all(db)
    )


@router.get("/{trip_id}")
async def get(trip_id: int, db: AsyncSession = Depends(database_helper.session_getter)):
    return await ResponseService.response(
        trip_service.get(trip_id=trip_id, db=db)
    )


@router.delete("/{trip_id}")
async def delete(trip_id: int, session_id: str | None = Cookie(default=None),
                 db: AsyncSession = Depends(database_helper.session_getter)):
    return await ResponseService.response(
        trip_service.delete(trip_id, session_id, db)
    )


@router.get("/get_user_trips/")
async def get_user_trips(session_id: str | None = Cookie(default=None),
                         db: AsyncSession = Depends(database_helper.session_getter)):
    return await ResponseService.response(
        trip_service.get_user_trips(session_id, db)
    )
