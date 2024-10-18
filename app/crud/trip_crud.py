from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import TripNotFoundError
from models.trip_model import Trip
from schemas.trip_scheme import RequestTripScheme
from schemas.trip_scheme import TripScheme


async def create(trip_create: RequestTripScheme, db: AsyncSession) -> TripScheme:
    new_trip = Trip(
        pickup=trip_create.pickup,
        dropoff=trip_create.dropoff,
        start_time=trip_create.start_time,
        end_time=trip_create.end_time,
    )

    db.add(new_trip)
    await db.commit()
    await db.refresh(new_trip)

    trip = TripScheme(
        pickup=new_trip.pickup,
        dropoff=new_trip.dropoff,
        start_time=new_trip.start_time,
        end_time=new_trip.end_time,
        trip_id=new_trip.trip_id,
    )

    return trip


async def get(trip_id: int, db: AsyncSession) -> TripScheme:
    trip = (
        (await db.execute(select(Trip).filter(Trip.trip_id == trip_id)))
        .scalars()
        .first()
    )

    if trip is None:
        raise TripNotFoundError

    trip_scheme = TripScheme(
        pickup=trip.pickup,
        dropoff=trip.dropoff,
        start_time=trip.start_time,
        end_time=trip.end_time,
        trip_id=trip.trip_id,
    )
    return trip_scheme


async def get_al_trips(db: AsyncSession) -> TripScheme:
    trips = (
        (await db.execute(select(Trip)))
        .scalars()
    )
    trips_schemes = [TripScheme(**trip.__dict__) for trip in trips]

    return trips_schemes


async def delete(trip_delete: TripScheme, db: AsyncSession) -> None:
    query = select(Trip).filter(Trip.trip_id == trip_delete.trip_id)

    result = await db.execute(query)
    trip = result.scalars().first()

    if not trip:
        raise TripNotFoundError

    await db.delete(trip)
    await db.commit()
