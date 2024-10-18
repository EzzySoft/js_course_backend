from pydantic import BaseModel

from .user_scheme import UserGetScheme


class RequestTripScheme(BaseModel):
    pickup: str
    dropoff: str
    start_time: str
    end_time: str


class TripScheme(BaseModel):
    pickup: str
    dropoff: str
    start_time: str
    end_time: str
    trip_id: int


class TripResponseScheme(TripScheme):
    creator: UserGetScheme
