from sqlalchemy import Column, Integer, ForeignKey
from models.base import Base


class TripUser(Base):
    __tablename__ = "trip_user"
    trip_user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trip.trip_id"), nullable=False)
