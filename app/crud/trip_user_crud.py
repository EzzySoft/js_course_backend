from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud import trip_crud
from exceptions import TripNotFoundError, UserTripNotFoundError
from models.trip_model import Trip
from models.trip_user_model import TripUser
from schemas.trip_scheme import TripScheme, RequestTripScheme
from schemas.user_scheme import UserScheme


async def create(
    user: UserScheme, trip_create: RequestTripScheme, db: AsyncSession
) -> TripScheme:
    try:
        trip = await trip_crud.create(trip_create, db)

        link = TripUser(user_id=user.user_id, trip_id=trip.trip_id)
        db.add(link)
        await db.commit()
        await db.refresh(link)

        return trip
    except Exception as e:
        await db.rollback()
        raise e


async def get(trip_id: int, db: AsyncSession) -> TripScheme:
    query = select(Trip).join(TripUser).filter(Trip.trip_id == trip_id)

    result = await db.execute(query)
    trip_object = result.scalars().first()

    if trip_object is None:
        raise TripNotFoundError

    trip_dict = trip_object.__dict__

    trip = TripScheme(**trip_dict)

    return trip


async def get_trip_creator_id(trip_id: int, db: AsyncSession) -> int:
    query = select(TripUser).filter(TripUser.trip_id == trip_id)

    result = await db.execute(query)

    trip_object = result.scalars().first()

    if trip_object is None:
        raise TripNotFoundError

    return trip_object.user_id


async def get_trip_users(trip_id: int, db: AsyncSession) -> list[int]:
    query = select(TripUser).filter(TripUser.trip_id == trip_id)

    result = await db.execute(query)
    trip_objects = result.scalars().all()

    return [trip_object.user_id for trip_object in trip_objects]


async def delete_trip(
    user: UserScheme, trip_delete: TripScheme, db: AsyncSession
) -> bool:
    try:

        query = (
            select(TripUser)
            .filter(TripUser.user_id == user.user_id)
            .filter(TripUser.trip_id == trip_delete.trip_id)
        )

        result = await db.execute(query)
        trip_user = result.scalars().all()

        if not trip_user:
            await db.rollback()
            raise UserTripNotFoundError(user.user_id, trip_delete.trip_id)

        for trip in trip_user:
            await db.delete(trip)
        await trip_crud.delete(trip_delete, db)

        await db.commit()
        return True

    except Exception as e:
        await db.rollback()
        raise e


async def get_user_trips(user: UserScheme, db: AsyncSession) -> List[TripScheme]:
    query = select(Trip).join(TripUser).filter(TripUser.user_id == user.user_id)

    result = await db.execute(query)
    trips_objects = result.scalars().all()

    ids = [trip.trip_id for trip in trips_objects]

    return [await trip_crud.get(trip_id, db) for trip_id in ids]
