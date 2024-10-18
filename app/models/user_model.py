from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import relationship

from models.base import Base


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    telegram = Column(String, nullable=False)
    password_hash = Column(LargeBinary)

    trips = relationship("Trip", secondary="trip_user", back_populates="users")
