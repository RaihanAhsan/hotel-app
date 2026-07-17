from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    ref = Column(String(50), unique=True, index=True, nullable=False)
    guest = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    room = Column(String(100), nullable=False)
    room_id = Column(String(50), nullable=False)
    checkin = Column(String(20), nullable=False)
    checkout = Column(String(20), nullable=False)
    guests = Column(Integer, nullable=False)
    nights = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
    special = Column(Text, nullable=True)
    card_last4 = Column(String(4), nullable=False)
    status = Column(String(50), default="Confirmed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Room(Base):
    __tablename__ = "rooms"
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    features = Column(Text, nullable=False)  # JSON string