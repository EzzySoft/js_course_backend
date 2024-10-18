from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.base import Base


class Trip(Base):
    __tablename__ = "trip"
    trip_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pickup = Column(String, nullable=False)
    dropoff = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)

    users = relationship("User", secondary="trip_user", back_populates="trips")
