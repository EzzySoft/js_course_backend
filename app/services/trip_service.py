from datetime import datetime
from typing import List

import requests
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from crud import trip_crud, trip_user_crud
from exceptions import UserNotAllowedError
from schemas.trip_scheme import RequestTripScheme, TripResponseScheme
from schemas.user_scheme import UserScheme
from services import auth_service
from services.auth_service import get_user_from_session_id


async def create(
        trip_request: RequestTripScheme, session_id: str | None, db: AsyncSession
) -> dict:
    user = await get_user_from_session_id(session_id=session_id, db=db)

    trip = await trip_user_crud.create(user, trip_request, db)

    return {"message": "Trip created successfully", "trip_id": trip.trip_id}


async def delete(trip_id: int, session_id: str | None, db: AsyncSession) -> dict:
    user = await get_user_from_session_id(session_id=session_id, db=db)
    trip_delete = await trip_crud.get(trip_id, db)

    await trip_user_crud.delete_trip(user, trip_delete, db)

    return {"message": "Trip deleted successfully"}


async def get(trip_id: int, db: AsyncSession) -> TripResponseScheme:
    trip = await trip_crud.get(trip_id, db)

    creator_id = await trip_user_crud.get_trip_creator_id(trip_id, db)
    creator = await auth_service.get_user(creator_id, db)

    response_trip = TripResponseScheme(**trip.__dict__, creator=creator)

    return response_trip


async def get_user_trips(
        session_id: str | None, db: AsyncSession
) -> List[TripResponseScheme]:
    user = await get_user_from_session_id(session_id=session_id, db=db)

    trips = await trip_user_crud.get_user_trips(user, db)

    response_trips = [
        TripResponseScheme(
            **trip.__dict__,
            creator=await auth_service.get_user(
                await trip_user_crud.get_trip_creator_id(trip.trip_id, db), db
            ),
        )
        for trip in trips
    ]

    return response_trips


async def get_all(db: AsyncSession) -> List[TripResponseScheme]:
    trips = await trip_crud.get_al_trips(db)

    response_trips = [
        TripResponseScheme(
            **trip.__dict__,
            creator=await auth_service.get_user(
                await trip_user_crud.get_trip_creator_id(trip.trip_id, db), db
            ),
        )
        for trip in trips
    ]

    return response_trips


async def check_user(trip_id: int, session_id: str | None, db: AsyncSession):
    user: UserScheme = await get_user_from_session_id(session_id=session_id, db=db)

    users = await trip_user_crud.get_trip_users(trip_id, db)
    creator_id = await trip_user_crud.get_trip_creator_id(trip_id, db)

    is_in_trip = user.user_id in users
    is_creator = user.user_id == creator_id

    return {"is_in_trip": is_in_trip, "is_creator": is_creator}
